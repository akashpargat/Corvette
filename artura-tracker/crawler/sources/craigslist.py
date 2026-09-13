"""Craigslist - every US and Canadian site (private sellers + small dealers)."""
from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor

from ..http_client import Client
from ..models import Listing, parse_mileage, parse_price, parse_year
from .base import Ctx, dedupe, cards_from_links

NAME = "craigslist"
LABEL = "Craigslist (US + Canada)"
KIND = "marketplace"
SITES_PAGE = "https://www.craigslist.org/about/sites"
FALLBACK = ["newyork", "losangeles", "chicago", "houston", "dallas", "sfbay", "miami", "atlanta", "phoenix", "seattle", "boston",
            "washingtondc", "denver", "sandiego", "orangecounty", "lasvegas", "austin", "philadelphia", "detroit", "minneapolis",
            "tampa", "orlando", "sacramento", "portland", "charlotte", "nashville", "stlouis", "saltlakecity", "raleigh",
            "toronto", "vancouver", "montreal", "calgary", "edmonton", "ottawa"]


def _sites(client: Client, ctx: Ctx):
    res = client.get(SITES_PAGE, retries=0)
    if not res.ok:
        return [(s, "US" if s not in ("toronto", "vancouver", "montreal", "calgary", "edmonton", "ottawa") else "CA") for s in FALLBACK]
    out = []
    # the page has <h1>US</h1> ... <h1>Canada</h1> ... sections
    us = res.text.find(">US<")
    ca = res.text.find(">Canada<")
    eu = res.text.find(">Europe<") if ">Europe<" in res.text else len(res.text)
    for (a, b, country) in ((us, ca, "US"), (ca, eu, "CA")):
        if a < 0:
            continue
        for sub in re.findall(r'href="https?://([a-z0-9]+)\.craigslist\.org', res.text[a:b]):
            out.append((sub, country))
    return list(dict.fromkeys(out)) or [(s, "US") for s in FALLBACK]


def _one(sub_country, log):
    sub, country = sub_country
    client = Client(log, delay=0.2, browser_fallback=False)
    url = f"https://{sub}.craigslist.org/search/cta?query=mclaren+artura&min_price=40000"
    res = client.get(url, retries=0)
    if not res.ok or "artura" not in res.text.lower():
        return [], res.status
    got = cards_from_links(res.text, res.url, r"/(cto|ctd)/d/|/cars-trucks/|\.html$", NAME, LABEL, "private", country,
                           "CAD" if country == "CA" else "USD")
    for l in got:
        l.extra["craigslist_site"] = sub
        if re.search(r"/ctd/", l.url):
            l.listing_type = "dealer"
    return got, res.status


def fetch(client, ctx: Ctx):
    sites = _sites(client, ctx)
    ctx.note(f"{LABEL}: {len(sites)} sites")
    out, blocked = [], 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for got, status in ex.map(lambda s: _one(s, ctx.log), sites):
            if status in (403, 429, 0):
                blocked += 1
            out += got
    ctx.pages += len(sites)
    if blocked > len(sites) * 0.8:
        ctx.note(f"{LABEL}: {blocked}/{len(sites)} sites returned 403/429 (http 403)")
    return dedupe(out)
