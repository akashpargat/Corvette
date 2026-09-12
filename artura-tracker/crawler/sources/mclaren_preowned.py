"""McLaren Qualified (official certified pre-owned) - preowned.mclaren.com."""
from __future__ import annotations

import re

from ..extract import abs_url, html_to_text, find_jsonld, vehicles_from_jsonld
from ..models import Listing, parse_mileage, parse_price, parse_year
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards

NAME = "mclaren_preowned"
LABEL = "McLaren Qualified (official CPO)"
KIND = "dealer"
BASE = "https://preowned.mclaren.com"
SEARCH = BASE + "/amn/us/en/mclaren/artura"


def fetch(client, ctx: Ctx):
    out = []
    detail_urls = []
    for page in range(1, 6):
        url = SEARCH if page == 1 else f"{SEARCH}?page={page}"
        res = client.get(url)
        ctx.pages += 1
        if not res.ok:
            ctx.diagnose(res, LABEL)
            break
        links = set(re.findall(r'href="([^"]*/amn/us/en/vehicles/[^"#?]+)"', res.text))
        links |= set(re.findall(r"href='([^']*/amn/us/en/vehicles/[^'#?]+)'", res.text))
        new = [abs_url(BASE, l) for l in links if abs_url(BASE, l) not in detail_urls]
        if not new:
            if page == 1:
                ctx.diagnose(res, LABEL)
            break
        detail_urls.extend(new)
        if len(new) < 10:
            break
    ctx.note(f"{LABEL}: {len(detail_urls)} vehicle pages found")
    for url in detail_urls[:80]:
        res = client.get(url)
        ctx.pages += 1
        if not res.ok:
            continue
        found = listings_from_jsonld(res.text, NAME, LABEL, url, dealer="McLaren Qualified")
        if not found:
            found = listings_from_vin_cards(res.text, NAME, LABEL, url)
        if not found:
            found = [_from_text(url, res.text)]
        for l in found:
            l.url = url
            l.condition = "cpo"
            l.listing_type = "dealer"
            _enrich(l, res.text)
            out.append(l)
    return dedupe(out)


def _from_text(url: str, html: str) -> Listing:
    text = html_to_text(html)
    title_m = re.search(r"(20\d\d\s+McLaren\s+Artura[^\n]{0,30})", text)
    title = title_m.group(1).strip() if title_m else "McLaren Artura"
    prices = [parse_price(p) for p in re.findall(r"\$\s?[0-9]{3},[0-9]{3}", text)]
    prices = [p for p in prices if p and 60000 < p < 400000]
    return Listing(source=NAME, source_name=LABEL, url=url, title=title, year=parse_year(title),
                   price=min(prices) if prices else None, mileage=parse_mileage(text), condition="cpo",
                   dealer="McLaren Qualified").finalize()


def _enrich(l: Listing, html: str):
    text = html_to_text(html)
    m = re.search(r"(?:Retailer|Dealer|Location)\s*[:\-]?\s*(McLaren\s+[A-Z][A-Za-z .]+)", text)
    if m:
        l.dealer = m.group(1).strip()
    m = re.search(r"McLaren\s+(Atlanta|Austin|Beverly Hills|Boston|Charlotte|Chicago|Dallas|Denver|Greenwich|Houston|Long Island|Miami|Coral Gables|Newport Beach|Orlando|Palm Beach|West Palm Beach|Philadelphia|Rancho Mirage|San Diego|San Francisco|Scottsdale|Seattle|St\.? Louis|Tampa|Washington|North Jersey|Las Vegas|Nashville|Detroit|Manhattan|Sterling|Florida)", text)
    if m and not l.location:
        l.location = m.group(1)
        l.dealer = l.dealer or f"McLaren {m.group(1)}"
    if not l.mileage:
        l.mileage = parse_mileage(text)
    m = re.search(r"(?:Exterior|Colou?r)\s*[:\-]?\s*([A-Z][A-Za-z ]{2,30})", text)
    if m and not l.color:
        l.color = m.group(1).strip()
    if "clean" in text.lower() and "title" in text.lower():
        l.title_status = "clean"
    l.finalize()
