"""CARFAX - the helix search API returns JSON with title/accident history flags."""
from __future__ import annotations

from .. import config
from ..models import Listing, parse_mileage, parse_price
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards

NAME = "carfax"
LABEL = "CARFAX"
KIND = "marketplace"
API = ("https://helix.carfax.com/search/v2/vehicles?zip={zip}&radius=5000&make=Mclaren&model=Artura"
       "&sort=PRICE_ASC&rows={rows}&page={page}&tpQualityThreshold=0&urlInfo=Used-Mclaren-Artura_w10502")
PAGE = "https://www.carfax.com/Used-Mclaren-Artura_w10502"


def fetch(client, ctx: Ctx):
    out = []
    for page in (1, 2):
        res, data = client.get_json(API.format(zip=config.SEARCH_ZIP, rows=100, page=page),
                                    headers={"Accept": "application/json", "Origin": "https://www.carfax.com",
                                             "Referer": PAGE})
        if not data or not isinstance(data, dict):
            if page == 1:
                ctx.note(f"{LABEL}: helix API unavailable ({res.blocked_reason() or res.status}); trying HTML")
            break
        rows = data.get("listings") or []
        for r in rows:
            out.append(_row(r))
        if len(rows) < 100:
            break
    if not out:
        res = client.get(PAGE)
        ctx.pages += 1
        if res.ok:
            out += listings_from_jsonld(res.text, NAME, LABEL, res.url)
            out += listings_from_vin_cards(res.text, NAME, LABEL, res.url)
        if not out:
            ctx.diagnose(res, LABEL)
    return dedupe(out)


def _row(r: dict) -> Listing:
    dealer = r.get("dealer") or {}
    loc = ", ".join(x for x in [dealer.get("city"), dealer.get("state")] if x)
    title = f"{r.get('year','')} {r.get('make','')} {r.get('model','')} {r.get('trim','')}".strip()
    l = Listing(source=NAME, source_name=LABEL, url=r.get("vdpUrl") or PAGE, title=title, vin=r.get("vin"),
                year=r.get("year"), price=parse_price(r.get("listPrice") or r.get("currentPrice")), mileage=parse_mileage(r.get("mileage")),
                dealer=dealer.get("name"), location=loc or None, state=dealer.get("state"),
                image=(r.get("images") or {}).get("firstPhoto", {}).get("large") if isinstance(r.get("images"), dict) else None,
                condition="cpo" if r.get("certified") else ("new" if r.get("stockType") == "NEW" else "used"),
                color=r.get("exteriorColor"),
                extra={"accidents": r.get("accidentHistory", {}).get("text") if isinstance(r.get("accidentHistory"), dict) else None,
                       "owners": r.get("ownerHistory", {}).get("text") if isinstance(r.get("ownerHistory"), dict) else None,
                       "one_owner": r.get("oneOwner"), "no_accidents": r.get("noAccidents"),
                       "badges": " ".join(str(b) for b in (r.get("badges") or []))})
    if r.get("noAccidents") and not r.get("salvageTitle"):
        l.title_status = "clean"
    for k in ("salvageTitle", "rebuiltTitle", "floodDamage", "lemonHistory", "frameDamage", "hasBrandedTitle"):
        if r.get(k):
            l.title_status = "branded"
            l.title_notes.append(f"carfax {k}")
    return l.finalize()
