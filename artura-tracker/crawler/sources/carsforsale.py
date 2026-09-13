"""Carsforsale.com - aggregator."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "carsforsale", "Carsforsale.com", "aggregator"
URLS = ["https://www.carsforsale.com/mclaren-artura-for-sale-C1140964", "https://www.carsforsale.com/search?make=McLaren&model=Artura"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/vehicle/|/listing/|for-sale")
