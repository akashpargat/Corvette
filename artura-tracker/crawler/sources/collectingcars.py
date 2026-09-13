"""Collecting Cars - online auctions (US and Canada lots)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "collectingcars", "Collecting Cars", "auction"
URLS = ["https://collectingcars.com/buying?query={model_slug}", "https://collectingcars.com/buying/search?q={query_enc}",
        "https://collectingcars.com/for-sale?query={query_enc}"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/for-sale/|/buying/[^?]|/lot/", listing_type="auction", use_browser=True, scroll=4)
