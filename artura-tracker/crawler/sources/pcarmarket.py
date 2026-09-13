"""PCARMARKET - enthusiast auctions (Porsche-centric, sells McLarens too). Client-rendered search."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "pcarmarket", "PCARMARKET", "auction"
URLS = ["https://www.pcarmarket.com/search?q={model_slug}", "https://www.pcarmarket.com/auction/results/?q={model_slug}"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/auction/", listing_type="auction", use_browser=True, wait_for="a[href*='/auction/']", scroll=4)
