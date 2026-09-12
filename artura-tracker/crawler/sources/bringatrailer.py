"""Bring a Trailer - live auctions (and recent results as price references)."""
from __future__ import annotations

import re

from ..extract import find_script_json, walk, html_to_text
from ..models import Listing, parse_mileage, parse_price, parse_year
from .base import Ctx, dedupe

NAME = "bringatrailer"
LABEL = "Bring a Trailer"
KIND = "auction"
URL = "https://bringatrailer.com/mclaren/artura/"


def fetch(client, ctx: Ctx):
    res = client.get(URL)
    ctx.pages += 1
    if not res.ok:
        ctx.diagnose(res, LABEL)
        return []
    out = []
    live = find_script_json(res.text, "auctionsCurrentInitialData") or find_script_json(res.text, "var auctionsCurrentInitialData")
    done = find_script_json(res.text, "auctionsCompletedInitialData") or find_script_json(res.text, "var auctionsCompletedInitialData")
    for blob, status in ((live, "live"), (done, "sold")):
        if not blob:
            continue
        for a in walk(blob, lambda d: "title" in d and ("url" in d or "titlesub" in d)):
            title = str(a.get("title", ""))
            if "artura" not in title.lower():
                continue
            amount = a.get("current_bid") or a.get("sold_price") or a.get("amount") or parse_price(str(a.get("current_bid_formatted") or a.get("sold_text") or ""))
            l = Listing(source=NAME, source_name=LABEL, url=a.get("url") or URL, title=title, year=parse_year(title),
                        price=parse_price(amount), mileage=parse_mileage(a.get("titlesub") or a.get("excerpt") or ""),
                        listing_type="auction", condition="used", image=a.get("thumbnail_url") or a.get("images", {}).get("small", {}).get("url") if isinstance(a.get("images"), dict) else a.get("thumbnail_url"),
                        auction_end=str(a.get("timestamp_end") or a.get("end_date") or "") or None,
                        extra={"auction_status": status, "sold_text": a.get("sold_text"), "description": a.get("excerpt", "")})
            if status == "sold":
                l.extra["reference_only"] = True
            out.append(l.finalize())
    if not out:
        # live listing cards in HTML
        for m in re.finditer(r'<a[^>]+href="(https://bringatrailer\.com/listing/[^"]*artura[^"]*)"[^>]*>', res.text, re.I):
            text = html_to_text(res.text[m.start(): m.start() + 3000])
            title_m = re.search(r"(20\d\d\s+McLaren\s+Artura[^\n]{0,40})", text)
            out.append(Listing(source=NAME, source_name=LABEL, url=m.group(1), title=title_m.group(1) if title_m else "McLaren Artura",
                               year=parse_year(text), price=parse_price(text), listing_type="auction", condition="used").finalize())
    if not out:
        ctx.diagnose(res, LABEL)
    return dedupe(out)
