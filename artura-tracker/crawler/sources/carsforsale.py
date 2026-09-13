"""Carsforsale.com - aggregator."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "carsforsale", "Carsforsale.com", "aggregator"
URLS = ["https://www.carsforsale.com/search?make={make}&model={model_ascii}"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/vehicle/|/listing/|for-sale")
