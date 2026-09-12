"""Cars & Bids - live auctions (Cloudflare-protected; best effort)."""
from __future__ import annotations

import re

from ..extract import abs_url, html_to_text, find_jsonld
from ..models import Listing, parse_mileage, parse_price, parse_year
from .base import Ctx, dedupe, listings_from_jsonld

NAME = "carsandbids"
LABEL = "Cars & Bids"
KIND = "auction"
HOST = "https://carsandbids.com"
URL = HOST + "/search/mclaren/artura"


def fetch(client, ctx: Ctx):
    res = client.get(URL)
    ctx.pages += 1
    if not res.ok:
        ctx.diagnose(res, LABEL)
        return []
    out = listings_from_jsonld(res.text, NAME, LABEL, res.url, listing_type="auction")
    for m in re.finditer(r'href="(/auctions/[A-Za-z0-9]+/[^"]*artura[^"]*)"', res.text, re.I):
        text = html_to_text(res.text[max(0, m.start() - 1500): m.start() + 2500])
        title_m = re.search(r"(20\d\d\s+McLaren\s+Artura[^\n]{0,40})", text)
        l = Listing(source=NAME, source_name=LABEL, url=abs_url(HOST, m.group(1)), title=title_m.group(1).strip() if title_m else "McLaren Artura",
                    year=parse_year(text), price=parse_price(text), mileage=parse_mileage(text), listing_type="auction", condition="used",
                    extra={"description": text[:300]})
        out.append(l.finalize())
    if not out:
        ctx.diagnose(res, LABEL)
    return dedupe(out)
