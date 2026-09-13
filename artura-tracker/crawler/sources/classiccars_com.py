"""ClassicCars.com + AutoHunter (same company)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "classiccars_com", "ClassicCars.com", "marketplace"
URLS = ["https://classiccars.com/listings/find/all-years/{make_slug}/{model_slug}", "https://www.autohunter.com/search?q={query_plus}"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/listings/view/|/auction/|/listing/")
