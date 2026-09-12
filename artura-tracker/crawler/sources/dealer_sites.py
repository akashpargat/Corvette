"""Every official US McLaren retailer's own website.

Strategy (robust against 30 different dealer platforms):
  1. Discover retailer sites from the McLaren retailer locator; merge with config list.
  2. For each site, read sitemap(s) and collect URLs mentioning "artura".
  3. Also try the common inventory search paths as a fallback.
  4. Fetch each candidate page and extract Vehicle JSON-LD, else VIN-anchored cards.
"""
from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor

from .. import config
from ..extract import abs_url, find_vins
from ..http_client import Client
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards

NAME = "dealer_sites"
LABEL = "McLaren dealer websites"
KIND = "dealer"

LOCATOR_URLS = [
    "https://cars.mclaren.com/us_en/retailers",
    "https://www.mclaren.com/cars/us_en/retailers",
    "https://retailers.mclaren.com/en",
]
INVENTORY_PATHS = [
    "/inventory/?model=Artura", "/inventory/?q=artura", "/used-inventory/index.htm?model=Artura",
    "/new-inventory/index.htm?model=Artura", "/inventory/used/?model=Artura", "/inventory/new/?model=Artura",
    "/searchused.aspx?Model=Artura", "/searchnew.aspx?Model=Artura", "/vehicles/?model=Artura",
    "/cars-for-sale/mclaren/artura/", "/pre-owned/?model=Artura", "/inventory", "/used-inventory/", "/new-inventory/",
]


def discover_dealers(client: Client, ctx: Ctx) -> list[tuple[str, str]]:
    dealers = {url.rstrip("/"): name for name, url in config.DEALER_SITES}
    for u in LOCATOR_URLS:
        res = client.get(u)
        ctx.pages += 1
        if not res.ok:
            continue
        for href in re.findall(r'https?://(?:www\.)?[a-z0-9.-]*mclaren[a-z0-9.-]*\.(?:com|net)', res.text, re.I):
            h = href.lower().rstrip("/")
            if any(x in h for x in ("cars.mclaren.com", "www.mclaren.com", "retailers.mclaren.com", "preowned.mclaren.com",
                                    "mclaren.com/cars", "mclarenapplied", "mclarenstore", "mclarenracing", "mclarenautomotive")):
                continue
            if h not in dealers:
                dealers[h] = h.split("//")[1].split("/")[0].replace("www.", "")
        break
    return [(n, u) for u, n in dealers.items()]


def _sitemap_urls(client: Client, base: str) -> list[str]:
    urls = []
    for path in ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml", "/vehicle-sitemap.xml", "/inventory-sitemap.xml"):
        res = client.get(base + path, retries=0)
        if not res.ok or "<loc>" not in res.text:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", res.text)
        subs = [l for l in locs if l.endswith(".xml") and any(k in l.lower() for k in ("vehicle", "inventory", "vdp", "sitemap"))]
        for s in subs[:8]:
            r2 = client.get(s, retries=0)
            if r2.ok:
                locs += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r2.text)
        urls += [l for l in locs if "artura" in l.lower() and not l.endswith(".xml")]
        if urls:
            break
    return list(dict.fromkeys(urls))


def _crawl_dealer(name: str, base: str, log) -> tuple[str, list, str]:
    client = Client(log, delay=0.6)
    ctx = Ctx(log)
    found = []
    home = client.get(base, retries=1)
    if not home.ok:
        return name, [], f"unreachable ({home.error or home.status})"
    base = re.match(r"https?://[^/]+", home.url).group(0)
    pages = _sitemap_urls(client, base)
    status = f"sitemap:{len(pages)}"
    if not pages:
        # fall back to inventory search pages
        for p in INVENTORY_PATHS:
            res = client.get(base + p, retries=0)
            if res.ok and re.search(r"artura", res.text, re.I):
                found += listings_from_jsonld(res.text, NAME, name, res.url, dealer=name)
                found += listings_from_vin_cards(res.text, NAME, name, res.url, dealer=name)
                # collect VDP links from the search page
                for href in re.findall(r'href=["\']([^"\']*artura[^"\']*)["\']', res.text, re.I):
                    pages.append(abs_url(res.url, href))
                if found or pages:
                    status = f"inventory-page:{p}"
                    break
    pages = [p for p in dict.fromkeys(pages) if not re.search(r"\.(jpg|png|pdf|xml)$", p, re.I)]
    for p in pages[:config.MAX_DETAIL_PAGES_PER_SOURCE]:
        res = client.get(p, retries=0)
        if not res.ok:
            continue
        got = listings_from_jsonld(res.text, NAME, name, res.url, dealer=name)
        if not got:
            got = listings_from_vin_cards(res.text, NAME, name, res.url, dealer=name)
        for l in got:
            if not l.url or l.url == base:
                l.url = res.url
            l.dealer = l.dealer or name
        found += got
    found = dedupe(found)
    for l in found:
        l.extra["dealer_site"] = base
        if not l.location:
            l.location = name.replace("McLaren ", "")
        l.finalize()
    return name, found, f"{status}, {len(found)} listings"


def fetch(client: Client, ctx: Ctx):
    dealers = discover_dealers(client, ctx)
    ctx.note(f"{LABEL}: {len(dealers)} retailer sites to crawl")
    out = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for name, found, status in ex.map(lambda d: _crawl_dealer(d[0], d[1], ctx.log), dealers):
            ctx.log.info("  %-28s %s", name, status)
            ctx.notes.append(f"{name}: {status}")
            out += found
    return dedupe(out)
