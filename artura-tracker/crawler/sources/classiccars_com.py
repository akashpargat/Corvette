"""ClassicCars.com + AutoHunter (same company)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "classiccars_com", "ClassicCars.com", "marketplace"
URLS = ["https://classiccars.com/listings/find/all-years/mclaren/artura", "https://www.autohunter.com/search?query=mclaren%20artura"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=URLS, href_re=r"/listings/view/|/auction/|/listing/")
