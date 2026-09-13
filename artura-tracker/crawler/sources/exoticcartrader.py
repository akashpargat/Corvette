"""Exotic Car Trader - consignment marketplace for exotics."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "exoticcartrader", "Exotic Car Trader", "marketplace"
URLS = ["https://www.exoticcartrader.com/inventory?make=McLaren&model=Artura", "https://www.exoticcartrader.com/mclaren/artura"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/vehicle/|/inventory/|/listing/", listing_type="private")
