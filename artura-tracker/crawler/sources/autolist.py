"""Autolist - public JSON search API (aggregates many dealer feeds)."""
from __future__ import annotations

from .. import config
from ..extract import walk
from ..models import Listing, parse_mileage, parse_price, is_target, current_target
from .base import Ctx, dedupe

NAME = "autolist"
LABEL = "Autolist"
KIND = "marketplace"
API = "https://www.autolist.com/search?make={make}&model={model_ascii}&radius=Any&zip={zip}&page={page}&sort_filter=price:asc&limit=100"


def fetch(client, ctx: Ctx):
    out = []
    for page in (1, 2):
        res, data = client.get_json(ctx.url(API, zip=config.SEARCH_ZIP, page=page),
                                    headers={"Accept": "application/json", "Referer": ctx.url("https://www.autolist.com/{make_slug}-{model_slug}")})
        if not data:
            ctx.diagnose(res, LABEL)
            break
        rows = data.get("records") if isinstance(data, dict) else None
        if rows is None:
            rows = list(walk(data, lambda d: "vin" in d and "price" in d))
        if rows:
            ctx.sample('autolist', rows[0])
        for r in rows:
            if not is_target(str(r.get("model", "")) + " " + str(r.get("title") or r.get("display_name") or "")):
                continue
            l = Listing(source=NAME, source_name=LABEL, url="https://www.autolist.com" + (r.get("vdp_url") or r.get("url") or ""),
                        title=r.get("display_name") or r.get("title") or f"{r.get('year','')} {current_target()['label']}", vin=r.get("vin"),
                        year=r.get("year"), price=parse_price(r.get("price") or r.get("price_unformatted")),
                        mileage=parse_mileage(r.get("mileage") or r.get("mileage_unformatted")),
                        dealer=r.get("dealer_name"), location=", ".join(x for x in [r.get("city"), r.get("state")] if x) or None,
                        image=r.get("primary_photo_url"), condition="cpo" if r.get("certified") else ("new" if r.get("condition") == "new" else "used"),
                        color=r.get("exterior_color"), extra={"badges": " ".join(str(x) for x in (r.get("badges") or []))})
            out.append(l.finalize())
        if len(rows) < 100:
            break
    return dedupe(out)
