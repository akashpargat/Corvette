"""Kijiji Autos + Kijiji classifieds (Canada, CAD)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "kijiji", "Kijiji / Kijiji Autos (Canada)", "marketplace"
URLS = ["https://www.kijijiautos.ca/cars/mclaren/artura/", "https://www.kijiji.ca/b-cars-trucks/canada/mclaren-artura/k0c174l0"]

def fetch(client, ctx: Ctx):
    a = crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS[:1], href_re=r"/vip/|/cars/mclaren/artura/", country="CA", currency="CAD", use_browser=True, wait_for="a[href*='/vip/']")
    b = crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS[1:], href_re=r"/v-cars-trucks/", listing_type="private", country="CA", currency="CAD")
    return a + [l for l in b if l.key not in {x.key for x in a}]
