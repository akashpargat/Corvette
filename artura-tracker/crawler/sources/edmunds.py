"""Edmunds - inventory gateway JSON, then HTML fallback."""
from __future__ import annotations

from .. import config
from ..extract import walk
from ..models import Listing, parse_mileage, parse_price
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards, parse_any

NAME = "edmunds"
LABEL = "Edmunds"
KIND = "marketplace"
HOST = "https://www.edmunds.com"
API = HOST + "/gateway/api/purchasefunnel/v1/srp/inventory?make=mclaren&model=artura&radius=6000&zip={zip}&pagesize=100&pagenum={page}&sortby=price:asc&inventorytype=used,cpo,new"
PAGE = HOST + "/used-mclaren-artura/"


def fetch(client, ctx: Ctx):
    out = []
    for page in (1, 2):
        res, data = client.get_json(API.format(zip=config.SEARCH_ZIP, page=page),
                                    headers={"Accept": "application/json", "Referer": PAGE, "x-client-action-name": "srp"})
        if not data:
            if page == 1:
                ctx.note(f"{LABEL}: inventory API unavailable ({res.blocked_reason() or res.status}); trying HTML")
            break
        rows = list(walk(data, lambda d: isinstance(d.get("vin"), str) and d["vin"].startswith("SBM")))
        ctx.sample('edmunds', rows[0] if rows else data)
        for r in rows:
            out.append(_row(r))
        if len(rows) < 100:
            break
    if not out:
        res = client.get(PAGE)
        ctx.pages += 1
        if res.ok:
            out += parse_any(res.text, NAME, LABEL, res.url)
        if not out:
            ctx.diagnose(res, LABEL)
    return dedupe(out)


def _row(r: dict) -> Listing:
    vi = r.get("vehicleInfo") or {}
    sv = vi.get("styleInfo") or {}
    pv = r.get("prices") or {}
    d = r.get("dealerInfo") or {}
    hist = r.get("historyInfo") or {}
    loc = ", ".join(x for x in [d.get("address", {}).get("city") if isinstance(d.get("address"), dict) else None,
                                d.get("address", {}).get("stateCode") if isinstance(d.get("address"), dict) else None] if x)
    l = Listing(source=NAME, source_name=LABEL, url=HOST + (r.get("vdpLink") or f"/inventory/{r['vin']}.html"),
                title=f"{sv.get('year','')} McLaren Artura {sv.get('trim','') or ''}".strip(), vin=r["vin"],
                year=sv.get("year"), price=parse_price(pv.get("displayPrice") or pv.get("baseMsrp")),
                mileage=parse_mileage((vi.get("mileage") if isinstance(vi.get("mileage"), (int, str)) else None)),
                dealer=d.get("name"), location=loc or None, condition=str(r.get("type", "used")).lower(),
                color=(vi.get("vehicleColors") or {}).get("exterior", {}).get("name") if isinstance(vi.get("vehicleColors"), dict) else None,
                extra={"accidents": hist.get("accidentText"), "owners": hist.get("ownerText"), "salvage": hist.get("salvageHistory")})
    if hist.get("salvageHistory") or hist.get("lemonHistory") or hist.get("frameDamage"):
        l.title_status = "branded"
        l.title_notes.append("edmunds history flag")
    elif hist.get("accidentText") and "no accident" in str(hist.get("accidentText")).lower():
        l.title_status = "clean"
    return l.finalize()
