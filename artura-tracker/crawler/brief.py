"""Morning brief: cheapest clean-title Artura, top 10, changes, source health.

    python -m crawler.brief            # print the brief
    python -m crawler.brief --send     # also email it (SMTP_USER / SMTP_PASS env, Gmail app password works)
"""
from __future__ import annotations

import argparse
import json
import os
import smtplib
import sys
from datetime import datetime, timezone
from email.message import EmailMessage

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
DASHBOARD = "https://claude.ai/code/artifact/f23488b2-3815-4a16-acf0-7abfe702ce80"
SHORT = {"mclaren_preowned": "McLaren CPO", "dealer_sites": "dealer site", "cars_com": "Cars.com", "autotrader": "Autotrader",
         "kbb": "KBB", "cargurus": "CarGurus", "carfax": "CARFAX", "truecar": "TrueCar", "edmunds": "Edmunds", "autolist": "Autolist",
         "dupont": "duPont", "classic_com": "Classic.com", "bringatrailer": "BaT", "carsandbids": "Cars & Bids", "ebay": "eBay",
         "hemmings": "Hemmings", "fb_marketplace": "FB Marketplace", "craigslist": "Craigslist", "iseecars": "iSeeCars",
         "usedcars_com": "UsedCars.com", "carsforsale": "Carsforsale", "carsdirect": "CarsDirect", "classiccars_com": "ClassicCars",
         "jamesedition": "JamesEdition", "exoticcartrader": "Exotic Car Trader", "pcarmarket": "PCARMARKET", "collectingcars": "Collecting Cars",
         "mclarenlife": "McLaren Life", "autotempest": "AutoTempest", "autotrader_ca": "AutoTrader.ca", "kijiji": "Kijiji", "cargurus_ca": "CarGurus.ca",
         "pcarmarket_x": "x"}


def _money(n):
    return f"${n:,}" if n else "n/a"


def _car(l: dict) -> str:
    where = f" · {l['location']}" if l.get("location") else (f" · {l['state']}" if l.get("state") else "")
    seller = l.get("dealer") or ("private seller" if l.get("listing_type") == "private" else "seller n/a")
    miles = f"{l['mileage']:,} mi" if l.get("mileage") is not None else "miles n/a"
    flag = " 🇨🇦" if l.get("country") == "CA" else ""
    local = f" (CA${l['price_local']:,})" if l.get("price_local") else ""
    return f"{l.get('year') or '?'} Artura {l.get('trim') or ''}{local} · {miles} · {seller}{where}{flag}"


def _target_label(tk: str) -> str:
    from . import config
    return config.TARGETS.get(tk, {}).get("label", tk)


def _car(l: dict) -> str:  # noqa: F811 - model-aware version
    where = f" · {l['location']}" if l.get("location") else (f" · {l['state']}" if l.get("state") else "")
    seller = l.get("dealer") or ("private seller" if l.get("listing_type") == "private" else "seller n/a")
    miles = f"{l['mileage']:,} mi" if l.get("mileage") is not None else "miles n/a"
    flag = " 🇨🇦" if l.get("country") == "CA" else ""
    local = f" (CA${l['price_local']:,})" if l.get("price_local") else ""
    from . import config
    model = config.TARGETS.get(l.get("target", "artura"), {}).get("model", "Artura")
    return f"{l.get('year') or '?'} {model} {l.get('trim') or ''}{local} · {miles} · {seller}{where}{flag}"


def build(data_dir: str = DATA, top_n: int = 10) -> tuple[str, str]:
    from . import config
    d = json.load(open(os.path.join(data_dir, "listings.json")))
    runs = json.load(open(os.path.join(data_dir, "runs.json")))
    market = json.load(open(os.path.join(data_dir, "market.json")))
    today = d["summary"]["date"]
    by = {l["key"]: l for l in d["listings"]}
    c = d.get("changes", {})
    targets = [k for k in config.DEFAULT_TARGETS if any(l.get("target", "artura") == k for l in d["listings"])] or ["artura"]
    lines = []
    for tk in targets:
        label = _target_label(tk)
        pool = sorted([l for l in d["listings"] if l.get("target", "artura") == tk and l["status"] == "active" and l.get("rankable", l.get("candidate"))
                       and l.get("title_status") != "branded" and l.get("price")], key=lambda l: l["price"])
        top = pool[:top_n]
        yrs = config.TARGETS[tk]["years"]
        lines += ["=" * 8 + f" {label.upper()} ({yrs[0]}-{yrs[1]}) " + "=" * 8]
        if config.TARGETS[tk].get("exclude_trims"):
            lines.append("Excluded from ranking: " + ", ".join(sorted(config.TARGETS[tk]["exclude_trims"])))
        if top:
            h = top[0]
            prev = None
            if len(market) > 1:
                pm = market[-2]
                prev = (pm.get("targets") or {}).get(tk, {}).get("cheapest") if pm.get("targets") else (pm.get("cheapest") if tk == "artura" else None)
            delta = "" if prev is None else (" (unchanged from yesterday)" if prev == h["price"] else f" (yesterday's low was {_money(prev)})")
            lines.append(f"Cheapest clean-title {config.TARGETS[tk]['model']} today: {_money(h['price'])} — {_car(h)}{delta}")
        else:
            lines.append(f"No clean-title {label} candidates in today's data.")
        lines += ["", f"TOP {top_n} CHEAPEST {config.TARGETS[tk]['model'].upper()}"]
        for i, l in enumerate(top, 1):
            tags = []
            if l.get("first_seen") == today:
                tags.append("NEW")
            pc = l.get("last_price_change") or {}
            if pc.get("date") == today and pc.get("delta", 0) < 0:
                tags.append(f"▼ {_money(-pc['delta'])}")
            title = "verified clean" if l.get("title_status") == "clean" else "unverified"
            tag = f" [{' · '.join(tags)}]" if tags else ""
            srcs = ", ".join(SHORT.get(s, s) for s in l.get("sources", []))
            lines.append(f"{i}. {_money(l['price'])} — {_car(l)} · title {title}{tag} · on {srcs}")
            lines.append(f"   {l['url']}")
        def _keep(k):
            r = by.get(k)
            return bool(r) and r.get("target", "artura") == tk and r.get("rankable", r.get("candidate")) and r.get("title_status") != "branded"
        def _list(keys, fmt):
            rows = sorted([by[k] for k in keys if _keep(k)], key=lambda r: r.get("price") or 0)
            return [fmt(r) for r in rows[:15]] or ["   none"]
        lines += ["", f"CHANGES ({config.TARGETS[tk]['model']}, {config.TARGETS[tk]['years'][0]}-{config.TARGETS[tk]['years'][1]} candidates only)"]
        new_k = [k for k in c.get("new", []) if _keep(k)]
        drop_k = [k for k in c.get("price_drop", []) if _keep(k)]
        gone_k = [k for k in c.get("removed", []) if _keep(k) or (by.get(k, {}).get("target", "artura") == tk)]
        lines.append(f"New today ({len(new_k)}):")
        lines += _list(new_k, lambda r: f"   {_money(r.get('price'))} — {_car(r)}")
        lines.append(f"Price drops ({len(drop_k)}):")
        lines += _list(drop_k, lambda r: f"   {_money(r['last_price_change']['from'])} -> {_money(r['price'])} — {_car(r)}")
        lines.append(f"Sold or removed ({len(gone_k)}):")
        lines += _list(gone_k, lambda r: f"   {_money(r.get('price'))} — {_car(r)}")
        lines.append("")
    run = runs[-1]
    ok = [s for s in run["sources"] if s["status"] == "ok"]
    empty = [s for s in run["sources"] if s["status"] == "empty"]
    blocked = [s for s in run["sources"] if s["status"] in ("blocked", "failed")]
    lines += ["SOURCES", f"{len(ok)} ok · {len(empty)} empty · {len(blocked)} blocked source runs — {d['summary']['active']} unique cars tracked",
              "ok: " + ", ".join(f"{s.get('label', s['source'])}{'/' + s['target'] if s.get('target') not in (None, 'all') else ''} ({s['count']})" for s in ok),
              "blocked: " + ", ".join(sorted({s.get("label", s["source"]) for s in blocked}))]
    fb = next((s for s in run["sources"] if s["source"] == "fb_marketplace"), None)
    if fb and fb["status"] != "ok" and not (fb.get("extra") or {}).get("had_cookies"):
        lines.append("Facebook Marketplace is login-walled; add the FB_COOKIES_JSON repository secret to unlock it.")
    lines += ["", "Unverified = no source flagged salvage/rebuilt/flood/lemon, but no history report confirmed it. Pull a CARFAX and get a PPI before wiring money.",
              f"Dashboard: {DASHBOARD}"]
    names = " + ".join(config.TARGETS[t]["model"] for t in targets)
    subject = f"Supercar Hunt — top 10 cheapest clean-title {names} ({datetime.now(timezone.utc).strftime('%b %-d')})"
    return subject, "\n".join(lines)


def send(subject: str, body: str, to: str) -> str:
    user, pw = os.environ.get("SMTP_USER", ""), os.environ.get("SMTP_PASS", "")
    host, port = os.environ.get("SMTP_HOST", "smtp.gmail.com"), int(os.environ.get("SMTP_PORT", "587"))
    if not (user and pw):
        return "skipped: SMTP_USER/SMTP_PASS not set"
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = user, to, subject
    msg.set_content(body)
    with smtplib.SMTP(host, port, timeout=30) as s:
        s.starttls()
        s.login(user, pw)
        s.send_message(msg)
    return f"sent to {to}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true")
    ap.add_argument("--to", default=os.environ.get("BRIEF_TO", "akashpargat@yahoo.com"))
    ap.add_argument("--data", default=DATA)
    a = ap.parse_args()
    subject, body = build(a.data)
    print(subject); print(); print(body)
    if a.send:
        print("\n[email]", send(subject, body, a.to), file=sys.stderr)
