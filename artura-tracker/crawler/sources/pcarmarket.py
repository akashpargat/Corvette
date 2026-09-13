"""PCARMARKET - enthusiast auctions (Porsche-centric, sells McLarens too)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "pcarmarket", "PCARMARKET", "auction"
URLS = ["https://www.pcarmarket.com/search/?q=artura", "https://www.pcarmarket.com/auction/all/?q=artura"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/auction/", listing_type="auction")
