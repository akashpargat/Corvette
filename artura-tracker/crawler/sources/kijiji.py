"""Kijiji classifieds (Canada, CAD). Kijiji Autos was folded into kijiji.ca."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "kijiji", "Kijiji (Canada)", "marketplace"
URLS = ["https://www.kijiji.ca/b-cars-trucks/canada/{make_slug}-{model_slug}/k0c174l0", "https://www.kijiji.ca/b-cars-vehicles/canada/{make_slug}-{model_slug}/k0c27l0"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/v-cars-trucks/|/v-cars-vehicles/", listing_type="private", country="CA", currency="CAD")
