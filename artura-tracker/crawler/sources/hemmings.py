"""Hemmings classifieds (dealer + private)."""
from __future__ import annotations

import re

from ..extract import abs_url, html_to_text, next_data, walk
from ..models import Listing, parse_mileage, parse_price, parse_year
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards, parse_any

NAME = "hemmings"
LABEL = "Hemmings"
KIND = "marketplace"
HOST = "https://www.hemmings.com"
URL = HOST + "/classifieds/cars-for-sale/mclaren/artura"


def fetch(client, ctx: Ctx):
    res = client.get(URL)
    ctx.pages += 1
    if not res.ok:
        ctx.diagnose(res, LABEL)
        return []
    out = listings_from_jsonld(res.text, NAME, LABEL, res.url)
    nd = next_data(res.text)
    if nd:
        for r in walk(nd, lambda d: "artura" in str(d.get("model", d.get("title", ""))).lower() and ("price" in d or "askingPrice" in d)):
            out.append(Listing(source=NAME, source_name=LABEL, url=abs_url(HOST, r.get("url") or r.get("slug") or ""), title=r.get("title") or f"{r.get('year','')} McLaren Artura",
                               vin=r.get("vin"), year=r.get("year"), price=parse_price(r.get("price") or r.get("askingPrice")),
                               mileage=parse_mileage(r.get("mileage") or r.get("odometer")), location=r.get("location") or None,
                               listing_type="auction" if r.get("isAuction") else "dealer").finalize())
    for m in re.finditer(r'href="([^"]*/listing/[^"]*artura[^"]*)"', res.text, re.I):
        text = html_to_text(res.text[m.start(): m.start() + 3000])
        title_m = re.search(r"(20\d\d\s+McLaren\s+Artura[^\n]{0,40})", text)
        out.append(Listing(source=NAME, source_name=LABEL, url=abs_url(HOST, m.group(1)), title=title_m.group(1).strip() if title_m else "McLaren Artura",
                           year=parse_year(text), price=parse_price(text), mileage=parse_mileage(text)).finalize())
    if not out:
        out = listings_from_vin_cards(res.text, NAME, LABEL, res.url)
    if not out:
        ctx.diagnose(res, LABEL)
    return dedupe(out)
