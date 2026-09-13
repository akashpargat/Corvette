"""usedcars.com - aggregator."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "usedcars_com", "UsedCars.com", "aggregator"
URLS = ["https://www.usedcars.com/buy/make-{make_slug}/model-{model_slug}"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/buy/|/listing|/vehicle")
