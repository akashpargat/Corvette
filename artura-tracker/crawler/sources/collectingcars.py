"""Collecting Cars - online auctions (US and Canada lots)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "collectingcars", "Collecting Cars", "auction"
URLS = ["https://collectingcars.com/buying?query=artura", "https://collectingcars.com/buying/search?q=mclaren%20artura",
        "https://collectingcars.com/for-sale?query=mclaren%20artura"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/for-sale/|/buying/[^?]|/lot/", listing_type="auction", use_browser=True, scroll=4)
