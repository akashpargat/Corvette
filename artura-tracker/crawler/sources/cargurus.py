"""CarGurus - JSON search endpoint first, HTML page second."""
from __future__ import annotations

import re

from .. import config
from ..extract import find_script_json, walk, abs_url
from ..models import Listing, parse_mileage, parse_price
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards, parse_any

NAME = "cargurus"
LABEL = "CarGurus"
KIND = "marketplace"
HOST = "https://www.cargurus.com"
ENTITY = "d3238"  # McLaren Artura
API = (HOST + "/Cars/searchResults.action?zip={zip}&distance=50000&entitySelectingHelper.selectedEntity={entity}"
       "&sortDir=ASC&sortType=PRICE&maxResults=100&offset={offset}&filtersModified=true&showNegotiable=true&inventorySearchWidgetType=AUTO")
PAGE = HOST + "/Cars/l-Used-McLaren-Artura-" + ENTITY


def fetch(client, ctx: Ctx):
    out = []
    for offset in (0, 100):
        res, data = client.get_json(API.format(zip=config.SEARCH_ZIP, entity=ENTITY, offset=offset),
                                    headers={"Accept": "application/json, text/plain, */*", "Referer": PAGE,
                                             "X-Requested-With": "XMLHttpRequest"})
        if data:
            got = _parse_api(data, ctx)
            out += got
            if len(got) < 100:
                break
        else:
            if offset == 0:
                ctx.note(f"{LABEL}: JSON endpoint unavailable ({res.blocked_reason() or res.status}); trying HTML")
            break
    if not out:
        res = client.get(PAGE)
        ctx.pages += 1
        if res.ok:
            data = find_script_json(res.text, "window.__PRELOADED_STATE__") or find_script_json(res.text, '"listings":')
            out += _parse_api(data, ctx) if data else []
            out += parse_any(res.text, NAME, LABEL, res.url)
        if not out:
            ctx.diagnose(res, LABEL)
    return dedupe(out)


def _parse_api(data, ctx=None) -> list[Listing]:
    out = []
    if ctx is not None:
        ctx.sample('cargurus', data if not isinstance(data, list) else data[:1])
    rows = data if isinstance(data, list) else list(walk(data, lambda d: "listingTitle" in d or ("vin" in d and "price" in d)))
    for r in rows:
        if not isinstance(r, dict):
            continue
        title = r.get("listingTitle") or r.get("title") or ""
        if "artura" not in title.lower() and "artura" not in str(r.get("modelName", "")).lower():
            continue
        lid = r.get("id") or r.get("listingId")
        loc = r.get("sellerCity") or r.get("dealerCity") or ""
        st = r.get("sellerRegion") or r.get("dealerState") or ""
        l = Listing(source=NAME, source_name=LABEL, url=f"{HOST}/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action#listing={lid}" if lid else PAGE,
                    title=title, vin=r.get("vin"), year=r.get("carYear") or r.get("year"),
                    price=parse_price(r.get("price") or r.get("priceString")), mileage=parse_mileage(r.get("mileage") or r.get("mileageString")),
                    dealer=r.get("serviceProviderName") or r.get("sellerName") or r.get("dealerName"),
                    location=", ".join(x for x in [loc, st] if x) or None, state=st or None,
                    image=(r.get("originalPictureData") or {}).get("url") if isinstance(r.get("originalPictureData"), dict) else r.get("mainPictureUrl"),
                    condition="cpo" if r.get("isCertified") else ("new" if r.get("isNew") else "used"),
                    listing_type="private" if r.get("isPrivateSeller") or r.get("sellerType") == "PRIVATE" else "dealer",
                    color=r.get("exteriorColorName") or r.get("normalizedExteriorColor"),
                    extra={"deal_rating": r.get("dealRating") or r.get("dealRatingKey"), "days_on_market": r.get("daysOnMarket"),
                           "accidents": r.get("hasAccidents"), "owners": r.get("ownerCount"),
                           "badges": " ".join(str(x) for x in (r.get("vehicleHistoryBadges") or []))})
        if r.get("hasAccidents") is False and r.get("isSalvage") is False:
            l.title_status = "clean"
        if r.get("isSalvage") or r.get("salvageHistory") or r.get("frameDamage"):
            l.title_status = "branded"
            l.title_notes.append("cargurus salvage/frame flag")
        out.append(l.finalize())
    return out
