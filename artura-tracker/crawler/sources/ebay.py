"""eBay Motors - search results cards."""
from __future__ import annotations

import re
from bs4 import BeautifulSoup

from ..models import Listing, parse_mileage, parse_price, parse_year
from .base import Ctx, dedupe

NAME = "ebay"
LABEL = "eBay Motors"
KIND = "marketplace"
URL = "https://www.ebay.com/sch/i.html?_nkw=mclaren+artura&_sacat=6001&_sop=15&_ipg=120&LH_PrefLoc=1"


def fetch(client, ctx: Ctx):
    res = client.get(URL)
    ctx.pages += 1
    if not res.ok:
        ctx.diagnose(res, LABEL)
        return []
    soup = BeautifulSoup(res.text, "lxml")
    out = []
    for item in soup.select("li.s-item, li.s-card, div.s-item__wrapper, [data-viewport] li"):
        a = item.select_one("a.s-item__link, a.s-card__link, a[href*='/itm/']")
        if not a:
            continue
        text = item.get_text("\n", strip=True)
        title = (item.select_one(".s-item__title, .s-card__title") or a).get_text(" ", strip=True)
        if "artura" not in title.lower() or re.search(r"\b(wheel|rim|part|model|toy|diecast|1:18|1/18|badge|brochure|key)\b", title, re.I):
            continue
        price_el = item.select_one(".s-item__price, .s-card__price")
        l = Listing(source=NAME, source_name=LABEL, url=a["href"].split("?")[0], title=title, year=parse_year(title),
                    price=parse_price(price_el.get_text() if price_el else text), mileage=parse_mileage(text),
                    listing_type="auction" if re.search(r"\bbids?\b", text, re.I) else "private",
                    condition="used", image=(item.select_one("img") or {}).get("src") if item.select_one("img") else None,
                    extra={"description": text[:400]})
        loc = re.search(r"(?:Located in|from)\s+([A-Z][A-Za-z .]+,\s*[A-Z][a-z ]+|[A-Z][A-Za-z .]+,\s*[A-Z]{2})", text)
        if loc:
            l.location = loc.group(1)
        out.append(l.finalize())
    if not out:
        ctx.diagnose(res, LABEL)
    return dedupe(out)
