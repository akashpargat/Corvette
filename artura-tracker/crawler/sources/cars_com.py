"""Cars.com search results (server-rendered cards + embedded digitalData)."""
from __future__ import annotations

import re
from bs4 import BeautifulSoup

from ..extract import abs_url, find_script_json, walk
from ..models import Listing, parse_mileage, parse_price, parse_year
from .base import Ctx, dedupe, listings_from_jsonld

NAME = "cars_com"
LABEL = "Cars.com"
KIND = "marketplace"
URL = ("https://www.cars.com/shopping/results/?stock_type=all&makes[]=mclaren&models[]=mclaren-artura"
       "&maximum_distance=all&zip={zip}&page_size=100&sort=list_price&page={page}")


def fetch(client, ctx: Ctx):
    from .. import config
    out = []
    for page in (1, 2, 3):
        res = client.get(URL.format(zip=config.SEARCH_ZIP, page=page))
        ctx.pages += 1
        if not res.ok:
            ctx.diagnose(res, LABEL)
            break
        got = _parse_cards(res.text, res.url)
        got += listings_from_jsonld(res.text, NAME, LABEL, res.url)
        # digitalData carries VINs for every card on the page
        dd = find_script_json(res.text, "CARS.digitalData")
        if dd:
            vins = {}
            for v in walk(dd, lambda d: "vin" in d and isinstance(d.get("vin"), str)):
                vins[str(v.get("listingId") or v.get("listing_id") or "")] = v["vin"]
            for l in got:
                lid = l.extra.get("listing_id", "")
                if not l.vin and lid in vins:
                    l.vin = vins[lid]
                    l.finalize()
        if not got:
            if page == 1:
                ctx.diagnose(res, LABEL)
            break
        out += got
        if len(got) < 90:
            break
    return dedupe(out)


def _parse_cards(html: str, base: str) -> list[Listing]:
    soup = BeautifulSoup(html, "lxml")
    out = []
    cards = soup.select("div.vehicle-card, [data-listing-id]")
    for c in cards:
        title_el = c.select_one("h2.title, .title")
        title = title_el.get_text(" ", strip=True) if title_el else ""
        if "artura" not in title.lower():
            continue
        a = c.select_one("a.vehicle-card-link, a[href*='/vehicledetail/']")
        href = a["href"] if a and a.has_attr("href") else ""
        price_el = c.select_one(".primary-price")
        mileage_el = c.select_one(".mileage")
        dealer_el = c.select_one(".dealer-name, .seller-name")
        loc_el = c.select_one(".miles-from, .vehicle-dealer-location, .dealer-location")
        img = c.select_one("img")
        stock = c.select_one(".stock-type")
        badges = " ".join(b.get_text(" ", strip=True) for b in c.select(".vehicle-badging, .sds-badge, .badge"))
        lid = c.get("data-listing-id") or ""
        l = Listing(source=NAME, source_name=LABEL, url=abs_url(base, href) if href else base, title=title,
                    year=parse_year(title), price=parse_price(price_el.get_text() if price_el else None),
                    mileage=parse_mileage(mileage_el.get_text() if mileage_el else None),
                    dealer=dealer_el.get_text(" ", strip=True) if dealer_el else None,
                    location=_clean_loc(loc_el.get_text(" ", strip=True) if loc_el else None),
                    image=(img.get("data-src") or img.get("src")) if img else None,
                    condition=_cond(stock.get_text(strip=True) if stock else ""),
                    extra={"listing_id": lid, "badges": badges})
        vin_m = re.search(r"(SBM[A-HJ-NPR-Z0-9]{14})", str(c))
        if vin_m:
            l.vin = vin_m.group(1)
        out.append(l.finalize())
    return out


def _clean_loc(s):
    if not s:
        return None
    s = re.sub(r"\(.*?\)", "", s)
    return s.strip(" ·-") or None


def _cond(s: str) -> str:
    s = s.lower()
    if "certified" in s:
        return "cpo"
    if "new" in s:
        return "new"
    if "used" in s:
        return "used"
    return "unknown"
