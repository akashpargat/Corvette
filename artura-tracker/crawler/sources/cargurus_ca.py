"""CarGurus Canada (CAD)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "cargurus_ca", "CarGurus.ca", "marketplace"
URLS = ["https://www.cargurus.ca/Cars/l-Used-McLaren-Artura-d3238"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/Cars/inventorylisting/|/details/", country="CA", currency="CAD", use_browser=True)
