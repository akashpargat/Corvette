"""Canadian exotic dealers that are not McLaren franchises (Grand Touring Automobiles, Pfaff, Ferrari Quebec, Weissach)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "clutch_canada", "Canadian exotic dealers", "dealer"
URLS = ["https://www.grandtouringautos.com/inventory/?q=artura", "https://www.pfaffautoworks.com/inventory/?q=artura",
        "https://www.weissach.com/inventory/?q=artura", "https://www.ferrariquebec.com/inventory/?q=artura"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"artura", country="CA", currency="CAD")
