"""CarsDirect - aggregator."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "carsdirect", "CarsDirect", "aggregator"
URLS = ["https://www.carsdirect.com/used_cars/search?make=mclaren&model=artura", "https://www.carsdirect.com/used-cars/mclaren-artura"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/used_cars/|/listing|/vehicle")
