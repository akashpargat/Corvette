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
    from ..browser import browser_get
    from ..http_client import FetchResult
    out = []
    for page in (1, 2, 3):
        url = URL.format(zip=config.SEARCH_ZIP, page=page)
        b = browser_get(url, wait_for="a[href*='/vehicledetail/']", network_idle=True, scroll=4, wait_ms=4000)
        ctx.pages += 1
        res = FetchResult(url=b.url or url, status=b.status, text=b.html, elapsed=0.0, error=b.error)
        if not res.ok:
            ctx.diagnose(res, LABEL)
            break
        got = _parse_cards(res.text, res.url)
        if not got:
            got = _parse_rendered(res.text, res.url)
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


def _parse_rendered(html: str, base: str) -> list[Listing]:
    """Selector-free parse: every VDP link, then the smallest ancestor that shows a price."""
    soup = BeautifulSoup(html, "lxml")
    out, seen = [], set()
    for a in soup.select("a[href*='/vehicledetail/']"):
        href = a.get("href", "").split("?")[0]
        if not href or href in seen:
            continue
        node, text = a, a.get_text("\n", strip=True)
        for _ in range(6):
            if "$" in text and re.search(r"artura", text, re.I):
                break
            node = node.parent
            if node is None:
                break
            text = node.get_text("\n", strip=True)
        if "$" not in text or not re.search(r"artura", text, re.I):
            continue
        seen.add(href)
        lines = [t for t in text.split("\n") if t.strip()]
        title = next((t for t in lines if re.search(r"20\d\d.*artura", t, re.I)), "McLaren Artura")
        price_line = next((t for t in lines if re.search(r"\$\s?\d{2,3},\d{3}", t)), "")
        mile_line = next((t for t in lines if re.search(r"\bmi\b|miles", t, re.I)), "")
        dealer = next((t for t in lines if re.search(r"McLaren|Motors|Auto|Cars|Imports|Group|Dealer|Porsche|Ferrari|Lamborghini|Mercedes|BMW|Audi|Lexus|Bentley|Maserati|Aston", t) and "$" not in t and not re.search(r"artura", t, re.I)), None)
        loc = next((t for t in lines if re.search(r"^[A-Z][A-Za-z .]+,\s*[A-Z]{2}(\s*\(|$)", t)), None)
        img = node.select_one("img") if hasattr(node, "select_one") else None
        l = Listing(source=NAME, source_name=LABEL, url=abs_url(base, href), title=title[:120], year=parse_year(title),
                    price=parse_price(price_line), mileage=parse_mileage(mile_line) if mile_line else None, dealer=dealer,
                    location=_clean_loc(loc), image=(img.get("data-src") or img.get("src")) if img else None,
                    condition=_cond(title), extra={"badges": " ".join(t for t in lines if re.search(r"deal|price drop|new listing", t, re.I))[:200]})
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
