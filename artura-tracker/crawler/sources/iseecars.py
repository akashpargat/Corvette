"""iSeeCars - aggregator with price analysis (client-rendered search)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "iseecars", "iSeeCars", "aggregator"
URLS = ["https://www.iseecars.com/cars-for-sale#Make={make}&Model={model_ascii}&Location=&Radius=all&sort=price&order=asc",
        "https://www.iseecars.com/used-cars/used-{make_slug}-for-sale"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/used-cars/|/vehicle|/listing|/car/", use_browser=True, scroll=4)
