"""Cars & Bids - live auctions (Cloudflare-protected; best effort)."""
from __future__ import annotations

import re

from ..extract import abs_url, html_to_text, find_jsonld
from ..models import Listing, parse_mileage, parse_price, parse_year, is_target, current_target
from .base import Ctx, dedupe, listings_from_jsonld, parse_any

NAME = "carsandbids"
LABEL = "Cars & Bids"
KIND = "auction"
HOST = "https://carsandbids.com"
URL_T = HOST + "/search/{make_slug}/{model_slug}"


def fetch(client, ctx: Ctx):
    URL = ctx.url(URL_T)
    t = current_target()
    res = client.get(URL)
    ctx.pages += 1
    if not res.ok:
        ctx.diagnose(res, LABEL)
        return []
    out = parse_any(res.text, NAME, LABEL, res.url, listing_type="auction")
    pre = re.search(r'<script id="preloaded-data"[^>]*>(.*?)</script>', res.text, re.S)
    if pre:
        import json
        try:
            data = json.loads(pre.group(1))
            ctx.sample("carsandbids-preloaded", data)
            from ..extract import walk
            for a in walk(data, lambda d: is_target(str(d.get("title", ""))) and ("id" in d or "slug" in d)):
                ctx.sample("carsandbids-auction", a)
                url = a.get("url") or (f"/auctions/{a.get('id')}/{a.get('slug')}" if a.get("slug") else None)
                out.append(Listing(source=NAME, source_name=LABEL, url=abs_url(HOST, url) if url else URL, title=a["title"],
                                   year=parse_year(a["title"]), price=parse_price(a.get("current_bid") or a.get("currentBid") or a.get("price") or a.get("bid")),
                                   mileage=parse_mileage(str(a.get("mileage") or a.get("sub_title") or a.get("subtitle") or "")),
                                   listing_type="auction", condition="used", image=a.get("main_photo") or a.get("thumbnail"),
                                   auction_end=str(a.get("auction_end") or a.get("ends_at") or "") or None,
                                   location=a.get("location") if isinstance(a.get("location"), str) else None,
                                   extra={"auction_status": a.get("status")}).finalize())
        except ValueError:
            pass
    if not out:
        from ..browser import browser_get
        b = browser_get(URL, scroll=3)
        if not b.error and b.html:
            out += parse_any(b.html, NAME, LABEL, URL, listing_type="auction")
            res.text = b.html
    for m in re.finditer(r'href="(/auctions/[A-Za-z0-9]+/[^"]*%s[^"]*)"' % t["model_slug"], res.text, re.I):
        text = html_to_text(res.text[max(0, m.start() - 1500): m.start() + 2500])
        title_m = re.search(r"(20\d\d\s+%s\s+%s[^\n]{0,40})" % (t["make"], t["alias_re"]), text, re.I)
        l = Listing(source=NAME, source_name=LABEL, url=abs_url(HOST, m.group(1)), title=title_m.group(1).strip() if title_m else t["label"],
                    year=parse_year(text), price=parse_price(text), mileage=parse_mileage(text), listing_type="auction", condition="used",
                    extra={"description": text[:300]})
        out.append(l.finalize())
    if not out:
        ctx.diagnose(res, LABEL)
    return dedupe(out)
