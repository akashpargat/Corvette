"""usedcars.com - aggregator."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "usedcars_com", "UsedCars.com", "aggregator"
URLS = ["https://www.usedcars.com/buy/make-mclaren/model-artura"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/buy/|/listing|/vehicle")
