"""AutoTrader.ca - Canada's largest marketplace (prices in CAD)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "autotrader_ca", "AutoTrader.ca", "marketplace"
URLS = ["https://www.autotrader.ca/cars/{make_slug}/{model_slug}/?rcp=100&rcs=0&srt=3&prx=-1&loc=Toronto%2C%20ON&hprc=True&wcp=True&sts=Used-New&inMarket=advancedSearch"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/a/{make_slug}/{model_slug}/".format(**ctx.target), country="CA", currency="CAD")
