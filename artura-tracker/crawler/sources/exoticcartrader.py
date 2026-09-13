"""Exotic Car Trader - consignment marketplace for exotics (inventory link discovered from the home page)."""
from __future__ import annotations
import re
from ..extract import abs_url
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "exoticcartrader", "Exotic Car Trader", "marketplace"
HOST = "https://www.exoticcartrader.com"

def fetch(client, ctx: Ctx):
    home = client.get(HOST)
    ctx.pages += 1
    urls = []
    if home.ok:
        for h in dict.fromkeys(re.findall(r'href="([^"]*(?:cars-for-sale|inventory|vehicles)[^"]*)"', home.text, re.I)):
            u = abs_url(HOST, h)
            if u.startswith(HOST):
                urls += [u, u + ("&" if "?" in u else "?") + "search=" + ctx.target["model_slug"], u + ("&" if "?" in u else "?") + "make=McLaren"]
            if len(urls) >= 6:
                break
    urls = urls or [HOST + "/cars-for-sale?search=" + ctx.target["model_slug"]]
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=urls[:6], href_re=r"/vehicle/|/inventory/|/listing/|/cars-for-sale/", listing_type="private")
