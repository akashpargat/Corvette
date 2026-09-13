"""AutoTempest - meta-search over Cars.com, Autotrader, eBay, Craigslist, CarGurus, TrueCar."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "autotempest", "AutoTempest", "aggregator"
URLS = ["https://www.autotempest.com/results?make={make_slug}&model={model_slug}&zip=10001&radius=any&sort=price"]

def fetch(client, ctx: Ctx):
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"https?://(?!www\.autotempest)", use_browser=True, scroll=6, wait_for=".result-list, .listing, [class*=result]")
