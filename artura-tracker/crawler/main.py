"""Run every source, merge, score, and write the dashboard data files.

    python -m crawler.main                      # everything
    python -m crawler.main --sources cars_com,ebay
    python -m crawler.main --skip fb_marketplace
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import config
from .http_client import Client
from .sources import load_sources
from .sources.base import Ctx
from .store import merge, now_iso

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(os.path.dirname(HERE), "data")


def run_source(mod, log) -> tuple[dict, list]:
    ctx = Ctx(log)
    client = Client(log)
    t0 = time.time()
    report = {"source": mod.NAME, "label": mod.LABEL, "kind": mod.KIND, "status": "ok", "count": 0,
              "seconds": 0.0, "pages": 0, "notes": [], "error": None}
    listings = []
    try:
        listings = [l for l in mod.fetch(client, ctx) if l is not None]
        listings = [l for l in listings if "artura" in (l.title or "").lower() or (l.vin or "").startswith("SBM16")]
        report["count"] = len(listings)
        if not listings:
            report["status"] = "empty"
    except Exception as e:  # never let one source kill the run
        report["status"] = "failed"
        report["error"] = f"{type(e).__name__}: {e}"[:300]
        log.error("%s failed: %s\n%s", mod.LABEL, e, traceback.format_exc()[-1500:])
    report["seconds"] = round(time.time() - t0, 1)
    report["pages"] = ctx.pages + client.requests_made
    report["notes"] = ctx.notes[:40]
    if getattr(ctx, "extra", None):
        report["extra"] = ctx.extra
    if report["status"] != "ok":
        for n in ctx.notes:
            low = n.lower()
            if any(k in low for k in ("cloudflare", "akamai", "captcha", "datadome", "perimeterx", "http 403", "login wall")):
                report["status"] = "blocked"
                break
    log.info("== %-32s %-8s %3d listings  %5.1fs", mod.LABEL, report["status"], report["count"], report["seconds"])
    return report, listings


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default="", help="comma-separated subset of sources")
    ap.add_argument("--skip", default="", help="comma-separated sources to skip")
    ap.add_argument("--data", default=DEFAULT_DATA)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname).1s %(message)s", datefmt="%H:%M:%S", stream=sys.stdout)
    log = logging.getLogger("artura")
    only = [s.strip() for s in args.sources.split(",") if s.strip()]
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    mods = [m for m in load_sources(only or None) if m.NAME not in skip]
    log.info("Artura crawl starting: %d sources, zip=%s, proxy=%s", len(mods), config.SEARCH_ZIP, "yes" if config.PROXY_URL else "no")

    reports, fresh = [], []
    t0 = time.time()
    # Facebook runs a browser; keep it out of the thread pool.
    browser_mods = [m for m in mods if m.NAME == "fb_marketplace"]
    http_mods = [m for m in mods if m.NAME != "fb_marketplace"]
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_source, m, log): m for m in http_mods}
        for f in as_completed(futs):
            rep, ls = f.result()
            reports.append(rep)
            fresh += ls
    for m in browser_mods:
        rep, ls = run_source(m, log)
        reports.append(rep)
        fresh += ls
    order = {m.NAME: i for i, m in enumerate(mods)}
    reports.sort(key=lambda r: order.get(r["source"], 99))

    run_report = {"started_at": now_iso(), "seconds": round(time.time() - t0, 1), "sources": reports,
                  "raw_listings": len(fresh), "zip": config.SEARCH_ZIP}
    payload = merge(args.data, fresh, run_report)
    s = payload["summary"]
    log.info("Done in %.0fs: %d raw -> %d active listings, %d clean candidates, cheapest clean $%s, new %d, drops %d",
             run_report["seconds"], len(fresh), s["active"], s["clean_candidates"],
             f"{s['cheapest_clean_price']:,}" if s["cheapest_clean_price"] else "n/a", s["new_today"], s["price_drops_today"])
    ok = sum(1 for r in reports if r["status"] == "ok")
    log.info("Sources ok: %d/%d  (%s)", ok, len(reports), ", ".join(f"{r['source']}={r['status']}:{r['count']}" for r in reports))
    return 0


if __name__ == "__main__":
    sys.exit(main())
