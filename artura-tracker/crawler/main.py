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
from .models import set_target, is_target, vin_matches

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA = os.path.join(os.path.dirname(HERE), "data")


def run_source(mod, log, target: dict) -> tuple[dict, list]:
    set_target(target)
    ctx = Ctx(log, target=target)
    client = Client(log)
    t0 = time.time()
    multi = getattr(mod, "MULTI_TARGET", False)
    report = {"source": mod.NAME, "label": mod.LABEL, "kind": mod.KIND, "status": "ok", "count": 0,
              "seconds": 0.0, "pages": 0, "notes": [], "error": None, "target": "all" if multi else target["key"]}
    listings = []
    try:
        listings = [l for l in mod.fetch(client, ctx) if l is not None]
        if not multi:
            listings = [l for l in listings if is_target(l.title or "", target) or vin_matches(l.vin, target)]
            for l in listings:
                l.target = target["key"]
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
    log.info("== %-32s %-9s %-8s %3d listings  %5.1fs", mod.LABEL, report["target"], report["status"], report["count"], report["seconds"])
    return report, listings


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default="", help="comma-separated subset of sources")
    ap.add_argument("--skip", default="", help="comma-separated sources to skip")
    ap.add_argument("--data", default=DEFAULT_DATA)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--targets", default=",".join(config.DEFAULT_TARGETS), help="comma-separated target keys (artura,huracan)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname).1s %(message)s", datefmt="%H:%M:%S", stream=sys.stdout)
    log = logging.getLogger("artura")
    only = [s.strip() for s in args.sources.split(",") if s.strip()]
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    mods = [m for m in load_sources(only or None) if m.NAME not in skip]
    targets = [config.TARGETS[k.strip()] for k in args.targets.split(",") if k.strip()]
    log.info("Crawl starting: %d sources x %s, zip=%s, proxy=%s", len(mods), [t["key"] for t in targets], config.SEARCH_ZIP, "yes" if config.PROXY_URL else "no")

    # (source, target) jobs: multi-target sources (dealer sites) run once; make-specific ones only for their make
    jobs = []
    for m in mods:
        makes = getattr(m, "TARGET_MAKES", None)
        if getattr(m, "MULTI_TARGET", False):
            jobs.append((m, targets[0]))
            continue
        for t in targets:
            if makes and t["make"] not in makes:
                continue
            jobs.append((m, t))
    reports, fresh = [], []
    t0 = time.time()
    # Facebook runs a browser; keep it out of the thread pool.
    browser_jobs = [j for j in jobs if j[0].NAME == "fb_marketplace"]
    http_jobs = [j for j in jobs if j[0].NAME != "fb_marketplace"]
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_source, m, log, t): (m, t) for m, t in http_jobs}
        for f in as_completed(futs):
            rep, ls = f.result()
            reports.append(rep)
            fresh += ls
    for m, t in browser_jobs:
        rep, ls = run_source(m, log, t)
        reports.append(rep)
        fresh += ls
    order = {m.NAME: i for i, m in enumerate(mods)}
    torder = {t["key"]: i for i, t in enumerate(targets)}
    reports.sort(key=lambda r: (order.get(r["source"], 99), torder.get(r["target"], -1)))

    run_report = {"started_at": now_iso(), "seconds": round(time.time() - t0, 1), "sources": reports,
                  "raw_listings": len(fresh), "zip": config.SEARCH_ZIP, "targets": [t["key"] for t in targets]}
    payload = merge(args.data, fresh, run_report)
    s = payload["summary"]
    log.info("Done in %.0fs: %d raw -> %d active listings, %d clean candidates, cheapest clean $%s, new %d, drops %d",
             run_report["seconds"], len(fresh), s["active"], s["clean_candidates"],
             f"{s['cheapest_clean_price']:,}" if s["cheapest_clean_price"] else "n/a", s["new_today"], s["price_drops_today"])
    ok = sum(1 for r in reports if r["status"] == "ok")
    log.info("Source runs ok: %d/%d  (%s)", ok, len(reports), ", ".join(f"{r['source']}[{r['target']}]={r['status']}:{r['count']}" for r in reports))
    return 0


if __name__ == "__main__":
    sys.exit(main())
