"""CarsDirect - aggregator."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "carsdirect", "CarsDirect", "aggregator"
URLS = ["https://www.carsdirect.com/used_cars/search?make={make_slug}&model={model_slug}"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/used_cars/|/listing|/vehicle")
