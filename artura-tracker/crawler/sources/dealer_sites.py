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
from ..models import set_target, current_target
from ..http_client import Client
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards, parse_any

NAME = "dealer_sites"
MULTI_TARGET = True
LABEL = "McLaren dealer websites"
KIND = "dealer"

LOCATOR_URLS = [
    "https://cars.mclaren.com/us_en/retailers",
    "https://www.mclaren.com/cars/us_en/retailers",
    "https://retailers.mclaren.com/en",
]
INVENTORY_PATHS = [
    "/inventory/?model={model_ascii}", "/inventory/?q={model_slug}", "/used-inventory/index.htm?model={model_ascii}",
    "/new-inventory/index.htm?model={model_ascii}", "/inventory/used/?model={model_ascii}", "/inventory/new/?model={model_ascii}",
    "/searchused.aspx?Model={model_ascii}", "/vehicles/?model={model_ascii}", "/pre-owned/?model={model_ascii}",
    "/inventory", "/used-inventory/", "/new-inventory/",
]


ALL_TARGETS = [config.TARGETS[k] for k in config.DEFAULT_TARGETS]
CA_NAMES = {name for t in ALL_TARGETS for name, _ in t["dealers_ca"]}
ALIAS_ANY = re.compile("|".join(t["alias_re"] for t in ALL_TARGETS), re.I)
SLUG_ANY = "|".join(t["model_slug"] for t in ALL_TARGETS)


def target_for(text: str):
    """Which target does this URL / page belong to? (first alias that matches)"""
    for t in ALL_TARGETS:
        if re.search(t["alias_re"], text or "", re.I):
            return t
    return None


def discover_dealers(client: Client, ctx: Ctx) -> list[tuple[str, str]]:
    dealers = {}
    for t in ALL_TARGETS:
        for name, url in t["dealers"] + t["dealers_ca"]:
            dealers.setdefault(url.rstrip("/"), name)
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
    extra = []
    rob = client.get(base + "/robots.txt", retries=0)
    if rob.ok:
        extra = [l.split(":", 1)[1].strip() for l in rob.text.splitlines() if l.lower().startswith("sitemap:")]
    for sm in extra[:6]:
        res = client.get(sm, retries=0)
        if res.ok and "<loc>" in res.text:
            locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", res.text)
            subs = [l for l in locs if l.endswith(".xml")]
            for s2 in subs[:10]:
                r2 = client.get(s2, retries=0)
                if r2.ok:
                    locs += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r2.text)
            urls += [l for l in locs if ALIAS_ANY.search(l) and not l.endswith(".xml")]
    if urls:
        return list(dict.fromkeys(urls))
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
        urls += [l for l in locs if ALIAS_ANY.search(l) and not l.endswith(".xml")]
        if urls:
            break
    return list(dict.fromkeys(urls))


def _crawl_dealer(name: str, base: str, log) -> tuple[str, list, str]:
    client = Client(log, delay=0.6, browser_budget=3)
    ctx = Ctx(log)
    found = []
    home = client.get(base, retries=0)
    if not home.ok:
        err = (home.error or str(home.status))
        short = "dns" if "resolve" in err else "ssl" if "SSL" in err else "timeout" if "timed out" in err.lower() else err[:40]
        return name, [], f"unreachable ({short})"
    base = re.match(r"https?://[^/]+", home.url).group(0)
    pages = _sitemap_urls(client, base)
    status = f"sitemap:{len(pages)}"
    if not pages:
        # fall back to inventory search pages, once per target
        tried = set()
        for t in ALL_TARGETS:
            for p in INVENTORY_PATHS:
                p = p.format(**t)
                if p in tried:
                    continue
                tried.add(p)
                res = client.get(base + p, retries=0)
                if res.ok and ALIAS_ANY.search(res.text):
                    set_target(target_for(res.text) or t)
                    found += parse_any(res.text, NAME, name, res.url, dealer=name)
                    for href in re.findall(r'href=["\']([^"\']*(?:%s)[^"\']*)["\']' % SLUG_ANY, res.text, re.I):
                        pages.append(abs_url(res.url, href))
                    if found or pages:
                        status = f"inventory-page:{p}"
                        break
            if found or pages:
                break
    if not pages:
        # last resort: follow the site's own inventory navigation links
        nav = [abs_url(base, h) for h in re.findall(r'href=["\']([^"\'#]+)["\']', home.text)
               if re.search(r"inventory|vehicles|pre-?owned|used|showroom|" + SLUG_ANY, h, re.I) and not re.search(r"\.(jpg|png|pdf|css|js)$|specials|service|parts|finance|about|contact|privacy", h, re.I)]
        nav = [n for n in dict.fromkeys(nav) if n.startswith(base)][:8]
        for n in nav:
            res = client.get(n, retries=0)
            if res.ok and ALIAS_ANY.search(res.text):
                for t in ALL_TARGETS:
                    if re.search(t["alias_re"], res.text, re.I):
                        set_target(t)
                        found += parse_any(res.text, NAME, name, res.url, dealer=name)
                for href in re.findall(r'href=["\']([^"\']*(?:%s)[^"\']*)["\']' % SLUG_ANY, res.text, re.I):
                    pages.append(abs_url(res.url, href))
        if found or pages:
            status = f"nav-links:{len(nav)}"
    pages = [p for p in dict.fromkeys(pages) if p.startswith("http") and not re.search(r"\.(jpg|png|pdf|xml|css|js)(\?|$)", p, re.I)]
    sampled = False
    for p in pages[:config.MAX_DETAIL_PAGES_PER_SOURCE * 2]:
        res = client.get(p, retries=0)
        if not res.ok:
            continue
        t = target_for(p) or target_for(res.text[:20000])
        if not t:
            continue
        set_target(t)
        got = parse_any(res.text, NAME, name, res.url, dealer=name)
        for g in got:
            g.target = t["key"]
        if got and not sampled and not any(g.price for g in got):
            sampled = True
            ctx2 = Ctx(log)
            log.info("  %s: page without price %s", name, res.url)
            ctx2.diagnose(res, name)
        for l in got:
            if not l.url or l.url == base:
                l.url = res.url
            l.dealer = l.dealer or name
        found += got
    found = dedupe(found)
    for l in found:
        l.extra["dealer_site"] = base
        if name in CA_NAMES:
            l.country, l.currency = "CA", "CAD"
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
