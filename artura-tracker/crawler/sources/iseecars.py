"""iSeeCars - aggregator with price analysis."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "iseecars", "iSeeCars", "aggregator"
URLS = ["https://www.iseecars.com/used-cars/used-mclaren-artura-for-sale"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/used-cars/|/listing/|/vehicle/")
