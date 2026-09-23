"""Persistence + day-over-day diffing.

data/listings.json  - every listing ever seen (active + removed), merged by VIN
data/history.json   - {key: [{d: 'YYYY-MM-DD', p: price, s: source}, ...]}
data/runs.json      - last 90 run reports (per-source status)
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Optional

from .models import Listing

REMOVED_AFTER_MISSING_RUNS = 3  # a car has to be missing from every source three runs in a row before we call it gone


def _load(path: str, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except ValueError:
            return default


def _save(path: str, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, sort_keys=False)
    os.replace(tmp, path)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def merge(data_dir: str, fresh: list[Listing], run_report: dict) -> dict:
    """Merge today's crawl into the persisted state. Returns the dashboard payload."""
    lpath, hpath, rpath = (os.path.join(data_dir, n) for n in ("listings.json", "history.json", "runs.json"))
    prev = _load(lpath, {"listings": []})
    history = _load(hpath, {})
    runs = _load(rpath, [])
    prev["listings"] = fold_vin_rows(prev.get("listings", []), history)
    by_key = {r["key"]: r for r in prev["listings"]}
    d = today()
    ts = now_iso()
    sources_ok = {s["source"] for s in run_report["sources"] if s["status"] == "ok"} | {"seed"}
    # a seed/no-VIN record superseded by a VIN-keyed record for the same URL
    url_index = {}
    for r in prev.get("listings", []):
        for o in r.get("offers", []) or [{"url": r.get("url")}]:
            if o.get("url"):
                url_index.setdefault(o["url"].split("?")[0].rstrip("/"), r["key"])
    for l in fresh:
        old_key = url_index.get((l.url or "").split("?")[0].rstrip("/"))
        if old_key and old_key != l.key and old_key in by_key and not by_key[old_key].get("vin"):
            del by_key[old_key]

    # 1. group fresh listings by key (a VIN can appear on 5 sites). A VIN-less card
    #    (AutoTempest, Craigslist) joins a VIN group when it links to the same page.
    norm = lambda u: (u or "").split("?")[0].split("#")[0].rstrip("/").lower()
    url_to_key = {}
    for l in fresh:
        if l.vin:
            url_to_key.setdefault(norm(l.url), l.key)
    for r in prev.get("listings", []):
        if r.get("vin"):
            for o in r.get("offers", []) or [{"url": r.get("url")}]:
                url_to_key.setdefault(norm(o.get("url")), r["key"])
    groups: dict[str, list[Listing]] = {}
    fp_index: list[tuple] = []   # (key, mileage, price, year, country) of VIN groups
    for l in fresh:
        if l.vin:
            groups.setdefault(l.key, []).append(l)
            if l.mileage and l.price:
                fp_index.append((l.key, l.mileage, l.price, l.year, l.country))
    for r in prev.get("listings", []):
        if r.get("mileage") and r.get("price") and r.get("status") == "active":
            fp_index.append((r["key"], r["mileage"], r["price"], r.get("year"), r.get("country", "US")))
    prev_by_url = {}
    for r in prev.get("listings", []):
        for o in r.get("offers", []) or [{"url": r.get("url")}]:
            if o.get("url"):
                prev_by_url.setdefault(norm(o["url"]), r)
    for l in fresh:
        if l.vin:
            continue
        old = prev_by_url.get(norm(l.url))
        if old:   # a thin card today (no miles/price/year) still fingerprints with what we knew yesterday
            for f in ("mileage", "price", "year"):
                if not getattr(l, f) and old.get(f):
                    setattr(l, f, old[f])
        k = url_to_key.get(norm(l.url)) or fingerprint_match(l, [x for x in fp_index if not old or x[0] != old["key"]])
        if not k:
            k = l.key
            if l.mileage and l.price:
                fp_index.append((k, l.mileage, l.price, l.year, l.country))
        groups.setdefault(k, []).append(l)

    changes = {"new": [], "price_drop": [], "price_up": [], "removed": [], "returned": []}
    seen_today = set()
    for key, group in groups.items():
        offers = []
        for l in group:
            offers.append({"source": l.source, "source_name": l.source_name, "url": l.url, "price": l.price,
                           "dealer": l.dealer, "listing_type": l.listing_type, "condition": l.condition, "seen": d})
        best = _best(group)
        rec = best.to_dict()
        rec["key"] = key   # the group's key (a VIN yesterday's URL join found), never the best card's URL hash
        rec["offers"] = offers
        old = by_key.get(key)
        reliable = [o["price"] for o in offers if o["price"] and o["source"] not in UNRELIABLE_ALONE]
        priced = reliable or [o["price"] for o in offers if o["price"]]   # aggregator cards only when nothing better
        if len(priced) >= 2:
            hi = max(priced)
            priced = [p for p in priced if p >= hi * 0.6] or priced   # a card that scraped a neighbour's price
        rec["price"] = min(priced) if priced else None
        rec["price_confirmed"] = bool(reliable)
        # sources whose crawl did not run OK today are not evidence the car left them
        carried = {s for s in (old or {}).get("sources", []) if s not in sources_ok and s not in UNRELIABLE_ALONE}
        if not reliable and priced and old and old.get("price"):
            if carried:
                # its real source(s) failed today and only aggregator cards priced it: keep the confirmed price
                rec["price"] = old["price"]
                rec["price_confirmed"] = bool(old.get("price_confirmed", True))
            else:
                # only aggregator cards priced it today: an AutoTempest card regularly absorbs the
                # neighbouring card's price, so take the card closest to yesterday's price and
                # keep yesterday's price when none is within 15% of it
                near = min(priced, key=lambda p: abs(p - old["price"]))
                rec["price"] = near if abs(near - old["price"]) <= old["price"] * 0.15 else old["price"]
        rec.setdefault("country", "US")
        rec.setdefault("currency", "USD")
        if not rec.get("target"):
            rec["target"] = "artura"
        rec["price_high"] = max(priced) if priced else None
        rec["sources"] = sorted({o["source"] for o in offers} | carried)
        # keep the best-known static facts from history if today's scrape is thinner
        if old:
            for f in ("vin", "year", "trim", "mileage", "dealer", "location", "state", "color", "image", "title"):
                if not rec.get(f) and old.get(f):
                    rec[f] = old[f]
            if rec.get("title_status") == "unknown" and old.get("title_status") != "unknown":
                rec["title_status"] = old["title_status"]
                rec["title_notes"] = old.get("title_notes", [])
            rec["first_seen"] = old.get("first_seen", d)
            rec["missing_runs"] = 0
            if old.get("status") == "removed":
                changes["returned"].append(key)
            oldp = old.get("price")
            if oldp and rec["price"] and rec["price"] != oldp:
                rec["last_price_change"] = {"date": d, "from": oldp, "to": rec["price"], "delta": rec["price"] - oldp}
                (changes["price_drop"] if rec["price"] < oldp else changes["price_up"]).append(key)
            else:
                rec["last_price_change"] = old.get("last_price_change")
        else:
            rec["first_seen"] = d
            rec["missing_runs"] = 0
            rec["last_price_change"] = None
            changes["new"].append(key)
        rec["last_seen"] = d
        rec["last_seen_at"] = ts
        rec["status"] = "active"
        rec["candidate"] = _candidate(rec)
        rec["rankable"] = _rankable(rec)
        # price history (one point per day, lowest price of the day)
        hist = history.setdefault(key, [])
        if rec["price"]:
            if hist and hist[-1]["d"] == d:
                hist[-1]["p"] = min(hist[-1]["p"], rec["price"])
            elif not hist or hist[-1]["p"] != rec["price"]:
                hist.append({"d": d, "p": rec["price"]})
            elif hist[-1]["p"] == rec["price"] and (len(hist) < 2 or hist[-2]["p"] != rec["price"]):
                # extend a flat line with a fresh timestamp
                hist.append({"d": d, "p": rec["price"]})
            else:
                hist[-1]["d"] = d
        rec["price_history"] = hist[-60:]
        by_key[key] = rec
        seen_today.add(key)

    # 2. anything not seen today -> count a miss; remove after N misses,
    #    but only if the sources that used to carry it actually ran OK today.
    for key, rec in by_key.items():
        if key in seen_today:
            continue
        if rec.get("status") == "removed":
            continue
        carried_by = set(rec.get("sources", [rec.get("source")]))
        if carried_by and not (carried_by & sources_ok):
            continue  # its sources failed today; not evidence the car sold
        rec["missing_runs"] = rec.get("missing_runs", 0) + 1
        if rec["missing_runs"] >= REMOVED_AFTER_MISSING_RUNS:
            rec["status"] = "removed"
            rec["removed_on"] = d
            changes["removed"].append(key)
        rec["price_history"] = history.get(key, [])[-60:]
        rec.setdefault("country", "US")
        if not rec.get("target"):
            rec["target"] = "artura"
        rec["candidate"] = _candidate(rec)
        rec["rankable"] = _rankable(rec)

    listings = list(by_key.values())
    from .scoring import score_all
    model = score_all(listings)

    active = [r for r in listings if r["status"] == "active"]
    clean = [r for r in active if r.get("rankable") and r.get("title_status") != "branded"]
    cheapest = min(clean, key=lambda r: r["price"]) if clean else None
    per_target = {}
    for tk in sorted({r.get("target", "artura") for r in listings}):
        ta = [r for r in active if r.get("target") == tk]
        tc = [r for r in clean if r.get("target") == tk]
        low = min(tc, key=lambda r: r["price"]) if tc else None
        per_target[tk] = {"active": len(ta), "clean_candidates": len(tc), "cheapest_clean_key": low["key"] if low else None,
                          "cheapest_clean_price": low["price"] if low else None,
                          "new_today": sum(1 for k in changes["new"] if by_key.get(k, {}).get("target") == tk),
                          "price_drops_today": sum(1 for k in changes["price_drop"] if by_key.get(k, {}).get("target") == tk),
                          "market_model": model.get("per_target", {}).get(tk)}
    from . import config as _cfg
    summary = {
        "targets": per_target,
        "target_labels": {k: {"model": t["model"], "label": f"{t['label']} {t['years'][0]}–{t['years'][1]}"} for k, t in _cfg.TARGETS.items()},
        "generated_at": ts, "date": d, "active": len(active), "clean_candidates": len(clean),
        "new_today": len(changes["new"]), "price_drops_today": len(changes["price_drop"]),
        "removed_today": len(changes["removed"]), "cheapest_clean_key": cheapest["key"] if cheapest else None,
        "cheapest_clean_price": cheapest["price"] if cheapest else None,
        "median_clean_price": model.get("median"), "market_model": model,
        "sources_ok": sorted(sources_ok), "sources_failed": sorted(s["source"] for s in run_report["sources"] if s["status"] != "ok"),
    }
    run_report["summary"] = {k: summary[k] for k in ("active", "clean_candidates", "new_today", "price_drops_today", "removed_today", "cheapest_clean_price")}
    runs = (runs + [run_report])[-90:]
    # daily market series for the dashboard chart (overall + per target)
    series = _load(os.path.join(data_dir, "market.json"), [])
    lows = sorted(r["price"] for r in clean)
    point = {"d": d, "cheapest": lows[0] if lows else None, "p10": lows[max(0, len(lows) // 10 - 1)] if lows else None,
             "median": model.get("median"), "active": len(active), "clean": len(clean), "targets": {}}
    for tk, ts in per_target.items():
        tl = sorted(r["price"] for r in clean if r.get("target") == tk)
        point["targets"][tk] = {"cheapest": tl[0] if tl else None, "median": tl[len(tl) // 2] if tl else None,
                                "active": ts["active"], "clean": ts["clean_candidates"]}
    if series and series[-1]["d"] == d:
        series[-1] = point
    else:
        series.append(point)
    series = series[-365:]

    payload = {"summary": summary, "changes": changes, "listings": sorted(listings, key=lambda r: (r["status"] != "active", r.get("price") or 10**9))}
    _save(lpath, payload)
    _save(hpath, history)
    _save(rpath, runs)
    _save(os.path.join(data_dir, "market.json"), series)
    return payload


def record_sales(data_dir: str, sales: list[Listing], keep: int = 600) -> list[dict]:
    """Ended auctions (listing_type == "sold") are comps, not cars for sale: keep them in
    data/sales.json keyed by URL, newest ending first."""
    path = os.path.join(data_dir, "sales.json")
    rows = {r["url"]: r for r in _load(path, [])}
    d = today()
    for l in sales:
        if not l.url or l.listing_type != "sold":
            continue
        rec = rows.get(l.url) or {"url": l.url, "first_seen": d}
        rec.update({"target": l.target, "source": l.source, "source_name": l.source_name, "title": l.title, "year": l.year,
                    "trim": l.trim, "mileage": l.mileage if l.mileage is not None else rec.get("mileage"),
                    "price": l.price, "sold": bool(l.extra.get("sold")), "ended": l.extra.get("ended") or rec.get("ended"),
                    "location": l.location or rec.get("location"), "image": l.image or rec.get("image"), "last_seen": d})
        rows[l.url] = rec
    out = sorted(rows.values(), key=lambda r: (r.get("ended") or "", r.get("first_seen") or ""), reverse=True)[:keep]
    _save(path, out)
    return out


def fold_vin_rows(listings: list[dict], history: dict) -> list[dict]:
    """A row keyed by a URL hash that later learned its VIN belongs under the VIN key.

    Folds it into the VIN row (offers, sources, earliest first_seen, lowest reliable
    price, price history) or re-keys it when no VIN row exists yet, so the same car is
    never two rows."""
    out: dict[str, dict] = {}
    order: list[str] = []
    for r in listings:
        key = r.get("vin") or r["key"]
        cur = out.get(key)
        if cur is None:
            if key != r["key"]:
                _move_history(history, r["key"], key)
                r["key"] = key
            out[key] = r
            order.append(key)
            continue
        old_key = r["key"]
        seen = {(o.get("source"), _norm_url(o.get("url"))) for o in cur.get("offers", [])}
        for o in r.get("offers", []):
            if (o.get("source"), _norm_url(o.get("url"))) not in seen:
                cur.setdefault("offers", []).append(o)
                seen.add((o.get("source"), _norm_url(o.get("url"))))
        cur["sources"] = sorted({o["source"] for o in cur.get("offers", [])} | set(cur.get("sources", [])) | set(r.get("sources", [])))
        for f in ("year", "trim", "mileage", "dealer", "location", "state", "color", "image", "title", "target"):
            if not cur.get(f) and r.get(f):
                cur[f] = r[f]
        if cur.get("title_status") in (None, "unknown") and r.get("title_status") not in (None, "unknown"):
            cur["title_status"], cur["title_notes"] = r["title_status"], r.get("title_notes", [])
        cur["first_seen"] = min(x for x in (cur.get("first_seen"), r.get("first_seen")) if x) if (cur.get("first_seen") or r.get("first_seen")) else None
        if r.get("status") == "active" and cur.get("status") != "active":
            cur.update({"status": "active", "missing_runs": r.get("missing_runs", 0), "last_seen": r.get("last_seen"), "last_seen_at": r.get("last_seen_at")})
            cur.pop("removed_on", None)
        elif r.get("status") == cur.get("status") == "active":
            cur["missing_runs"] = min(cur.get("missing_runs", 0), r.get("missing_runs", 0))
            cur["last_seen"] = max(x for x in (cur.get("last_seen"), r.get("last_seen")) if x)
        reliable = [o["price"] for o in cur["offers"] if o.get("price") and o.get("source") not in UNRELIABLE_ALONE and o.get("seen") == cur.get("last_seen")]
        if reliable:
            hi = max(reliable)
            reliable = [p for p in reliable if p >= hi * 0.6] or reliable
            cur["price"] = min(reliable)
            cur["price_high"] = max(reliable)
        _move_history(history, old_key, key)
        cur["price_history"] = history.get(key, [])[-60:]
    return [out[k] for k in order]


def _norm_url(u):
    return (u or "").split("?")[0].split("#")[0].rstrip("/").lower()


def _move_history(history: dict, old_key: str, key: str):
    if old_key == key or old_key not in history:
        return
    pts = {(p["d"], p["p"]): p for p in history.get(key, []) + history.pop(old_key)}
    merged = sorted(pts.values(), key=lambda p: p["d"])
    out = []
    for p in merged:   # one point per day: keep the lowest price of that day
        if out and out[-1]["d"] == p["d"]:
            out[-1]["p"] = min(out[-1]["p"], p["p"])
        else:
            out.append(p)
    history[key] = out


def fingerprint_match(l: Listing, index) -> Optional[str]:
    """Same odometer reading and (nearly) the same asking price is the same car."""
    if not (l.mileage and l.price):
        return None
    best, best_diff = None, None
    for key, miles, price, year, country in index:
        if country != l.country:
            continue
        if year and l.year and year != l.year:
            continue
        if abs(miles - l.mileage) > max(10, miles * 0.005):
            continue
        diff = abs(price - l.price) / max(price, 1)
        if diff <= 0.02 and (best_diff is None or diff < best_diff):
            best, best_diff = key, diff
    return best


def _best(group: list[Listing]) -> Listing:
    def score(l: Listing):
        return sum(1 for f in (l.vin, l.price, l.mileage, l.year, l.dealer, l.location, l.image, l.color) if f) + (2 if l.source in ("carfax", "cargurus", "mclaren_preowned") else 0)
    return max(group, key=score)


RACE_TRIMS = {"GT4", "GT3", "Super Trofeo"}   # track-only cars are never "the cheapest road car"
UNRELIABLE_ALONE = {"autotempest", "iseecars"}   # aggregator cards: fine as corroboration, not as the only price


def _rankable(rec: dict) -> bool:
    if not rec.get("candidate") or rec.get("listing_type") == "auction":
        return False
    if rec.get("mileage") is None:
        return False          # a car with no odometer reading cannot be called "the cheapest"
    srcs = set(rec.get("sources") or [rec.get("source")])
    if srcs and srcs <= UNRELIABLE_ALONE:
        return False
    return True


def _candidate(rec: dict) -> bool:
    from . import config
    t = config.TARGETS.get(rec.get("target") or "artura") or config.TARGETS["artura"]
    p = rec.get("price")
    if not p or not (t.get("price_floor", config.PRICE_FLOOR) <= p <= t.get("price_ceiling", config.PRICE_CEILING)):
        return False
    y = rec.get("year")
    if not y or not (t["years"][0] <= y <= t["years"][1]):
        return False
    if rec.get("trim") in t.get("exclude_trims", set()) or rec.get("trim") in RACE_TRIMS:
        return False
    from .models import is_junk
    if is_junk(rec.get("title", ""), t):
        return False
    import re as _re
    if t.get("exclude_re") and _re.search(t["exclude_re"], f"{rec.get('title','')} {rec.get('url','')}", _re.I) and not _re.search(t["alias_re"], rec.get("title", "") or "", _re.I):
        return False
    if rec.get("extra", {}).get("reference_only"):
        return False
    return True
