"""CLASSIC.COM - market aggregator listing dealers + auctions for sale."""
from __future__ import annotations

import re

from ..extract import abs_url, html_to_text
from ..models import Listing, parse_mileage, parse_price, parse_year, is_target, current_target
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards, parse_any

NAME = "classic_com"
LABEL = "CLASSIC.COM"
KIND = "aggregator"
HOST = "https://www.classic.com"
URL = HOST + "/m/{make_slug}/{model_slug}/?status=for-sale&sort=price-asc&page={page}"


def fetch(client, ctx: Ctx):
    out = []
    for page in (1, 2):
        res = client.get(ctx.url(URL, page=page))
        ctx.pages += 1
        if not res.ok:
            ctx.diagnose(res, LABEL)
            break
        got = parse_any(res.text, NAME, LABEL, res.url)
        got += _cards(res.text, res.url)
        if not got:
            if page == 1:
                ctx.diagnose(res, LABEL)
            break
        out += got
        if len(got) < 20:
            break
    return dedupe(out)


def _cards(html: str, base: str) -> list[Listing]:
    out = []
    for m in re.finditer(r'<a[^>]+href="(/veh/[^"]+)"[^>]*>', html):
        href = m.group(1)
        chunk = html[m.start(): m.start() + 5000]
        text = html_to_text(chunk)
        if not is_target(text):
            continue
        t = current_target()
        title_m = re.search(r"(20\d\d\s+%s\s+%s[^\n]{0,40})" % (t["make"], t["alias_re"]), text, re.I)
        l = Listing(source=NAME, source_name=LABEL, url=abs_url(base, href), title=title_m.group(1).strip() if title_m else t["label"],
                    year=parse_year(title_m.group(1) if title_m else text), price=parse_price(text), mileage=parse_mileage(text),
                    listing_type="auction" if re.search(r"auction|bid", text, re.I) else "dealer", extra={"description": text[:300]})
        loc = re.search(r"\n\s*([A-Z][A-Za-z .]+,\s*[A-Z]{2})\b", text)
        if loc:
            l.location = loc.group(1)
        out.append(l.finalize())
    return out
