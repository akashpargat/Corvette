"""Autotrader.com - listings come from the window.__BONNET_DATA__ blob."""
from __future__ import annotations

import re

from ..extract import find_script_json, walk, abs_url
from ..models import Listing, parse_mileage, parse_price, is_target, vin_matches, current_target
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards

NAME = "autotrader"
LABEL = "Autotrader"
KIND = "marketplace"
HOST = "https://www.autotrader.com"
URL = HOST + "/cars-for-sale/all-cars/{make_slug}/{model_slug}?searchRadius=0&sortBy=derivedpriceASC&numRecords=100&firstRecord={first}"


def fetch(client, ctx: Ctx, host: str = HOST, url_tpl: str = URL, name: str = NAME, label: str = LABEL):
    out = []
    for first in (0, 100, 200):
        res = client.get(ctx.url(url_tpl, first=first), headers={"Referer": host + "/"})
        ctx.pages += 1
        if not res.ok:
            ctx.diagnose(res, label)
            break
        got = parse_bonnet(res.text, host, name, label)
        if not got:
            got = listings_from_jsonld(res.text, name, label, res.url) or listings_from_vin_cards(res.text, name, label, res.url)
        if not got:
            if first == 0:
                ctx.diagnose(res, label)
            break
        out += got
        if len(got) < 90:
            break
    return dedupe(out)


def parse_bonnet(html: str, host: str, name: str, label: str) -> list[Listing]:
    data = find_script_json(html, "window.__BONNET_DATA__")
    if not data:
        data = find_script_json(html, "__BONNET_DATA__=")
    if not data:
        return []
    out = []
    for inv in walk(data, lambda d: isinstance(d.get("vin"), str) and vin_matches(d.get("vin", ""))):
        model = str(inv.get("model", ""))
        title = inv.get("title") or f"{inv.get('year','')} {current_target()['make']} {model} {inv.get('trim','')}".strip()
        if not is_target(title + " " + model):
            continue
        pricing = inv.get("pricingDetail") or {}
        price = pricing.get("salePrice") or pricing.get("derived") or pricing.get("msrp") or inv.get("price")
        spec = inv.get("specifications") or {}
        mileage = (spec.get("mileage") or {}).get("value") if isinstance(spec.get("mileage"), dict) else inv.get("mileage")
        owner = inv.get("owner") or {}
        if isinstance(owner, dict):
            dealer = owner.get("name")
            loc = owner.get("location") or {}
            addr = loc.get("address") if isinstance(loc, dict) else {}
            location = ", ".join(x for x in [addr.get("city"), addr.get("state")] if x) if isinstance(addr, dict) else None
        else:
            dealer, location = None, None
        images = inv.get("images") or {}
        img = None
        if isinstance(images, dict):
            srcs = images.get("sources") or []
            if srcs and isinstance(srcs[0], dict):
                img = srcs[0].get("src")
        listing_type = "private" if str(inv.get("listingType", "")).lower().startswith("priv") or inv.get("isPrivate") else "dealer"
        l = Listing(source=name, source_name=label, url=abs_url(host, inv.get("vdpBaseUrl") or f"/cars-for-sale/vehicle/{inv.get('id','')}"),
                    title=title, vin=inv["vin"], year=int(inv.get("year") or 0) or None, price=parse_price(price),
                    mileage=parse_mileage(mileage), dealer=dealer, location=location, image=img,
                    condition={"NEW": "new", "USED": "used", "CERTIFIED": "cpo"}.get(str(inv.get("type") or inv.get("listingType") or "").upper(), "unknown"),
                    listing_type=listing_type, color=(inv.get("exteriorColorSimple") or inv.get("exteriorColor")),
                    extra={"badges": " ".join(str(b) for b in (inv.get("badges") or []))})
        out.append(l.finalize())
    return out
