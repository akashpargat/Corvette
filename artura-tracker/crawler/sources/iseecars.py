"""iSeeCars - aggregator with price analysis (client-rendered search)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "iseecars", "iSeeCars", "aggregator"
URLS = ["https://www.iseecars.com/cars-for-sale#Make=McLaren&Model=Artura&Location=&Radius=all&sort=price&order=asc",
        "https://www.iseecars.com/used-cars/used-mclaren-for-sale"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/used-cars/|/vehicle|/listing|/car/", use_browser=True, scroll=4)
