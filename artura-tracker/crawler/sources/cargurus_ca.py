"""CarGurus Canada (CAD)."""
from .base import Ctx, crawl_simple
NAME, LABEL, KIND = "cargurus_ca", "CarGurus.ca", "marketplace"
URLS = ["https://www.cargurus.ca/Cars/l-Used-{make}-{model_ascii}-{cargurus_entity}"]

def fetch(client, ctx: Ctx):
    if not ctx.target["cargurus_entity"]:
        ctx.note(f"{LABEL}: no cargurus_entity in targets.json for {ctx.target['label']}")
        return []
    return crawl_simple(client, ctx, name=NAME, label=LABEL, urls=[ctx.url(u) for u in URLS], href_re=r"/Cars/inventorylisting/|/details/", country="CA", currency="CAD", use_browser=True)
