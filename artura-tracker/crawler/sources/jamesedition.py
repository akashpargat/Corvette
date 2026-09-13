"""JamesEdition - luxury marketplace, strong exotic-dealer coverage."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "jamesedition", "JamesEdition", "marketplace"
URLS = ["https://www.jamesedition.com/cars/mclaren/artura?country=United%20States", "https://www.jamesedition.com/cars/mclaren/artura?country=Canada"]

def fetch(client, ctx: Ctx):
    us = crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS[:1], href_re=r"/cars/mclaren/artura/")
    ca = crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS[1:], href_re=r"/cars/mclaren/artura/", country="CA", currency="CAD")
    return us + [l for l in ca if l.key not in {u.key for u in us}]
