"""JamesEdition - luxury marketplace, strong exotic-dealer coverage."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "jamesedition", "JamesEdition", "marketplace"
URLS = ["https://www.jamesedition.com/cars/{make_slug}/{model_slug}?country=United%20States", "https://www.jamesedition.com/cars/{make_slug}/{model_slug}?country=Canada"]

def fetch(client, ctx: Ctx):
    # JamesEdition ignores the country filter often enough that we trust each card's own location instead.
    out = crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/cars/{make_slug}/{model_slug}/".format(**ctx.target))
    for l in out:
        text = f"{l.location or ''} {(l.extra or {}).get('description', '')}"
        if "canada" in text.lower() and not l.price_local:
            l.country, l.currency = "CA", "CAD"
            l.finalize()
    return out
