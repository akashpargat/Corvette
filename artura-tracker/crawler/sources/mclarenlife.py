"""McLaren Life forum classifieds - owner-to-owner sales."""
from __future__ import annotations
import re
from ..extract import abs_url
from .base import Ctx, crawl_simple, dedupe
NAME, LABEL, KIND = "mclarenlife", "McLaren Life classifieds", "marketplace"
TARGET_MAKES = ("McLaren",)
HOST = "https://www.mclarenlife.com"
URLS = [HOST + "/forums/", HOST + "/search/?q=artura+for+sale&o=date"]

def fetch(client, ctx: Ctx):
    res = client.get(URLS[0])
    ctx.pages += 1
    forums = []
    if res.ok:
        forums = [abs_url(HOST, h) for h in dict.fromkeys(re.findall(r'href="(/forums/[^"]*(?:for-sale|classified|marketplace)[^"]*)"', res.text, re.I))][:4]
    if not forums:
        forums = [HOST + "/forums/mclaren-for-sale.32/"]
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=forums, href_re=r"/threads/.*" + ctx.target["model_slug"], listing_type="private")
