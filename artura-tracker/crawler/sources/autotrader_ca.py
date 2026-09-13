"""AutoTrader.ca - Canada's largest marketplace (prices in CAD)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "autotrader_ca", "AutoTrader.ca", "marketplace"
URLS = ["https://www.autotrader.ca/cars/mclaren/artura/?rcp=100&rcs=0&srt=3&prx=-1&loc=Toronto%2C%20ON&hprc=True&wcp=True&sts=Used-New&inMarket=advancedSearch"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/a/mclaren/artura/", country="CA", currency="CAD")
