"""TrueCar - server-rendered cards; fall back to embedded JSON and VIN cards."""
from __future__ import annotations

import re
from bs4 import BeautifulSoup

from ..extract import abs_url, next_data, walk
from ..models import Listing, parse_mileage, parse_price, parse_year, is_target, vin_matches, current_target
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards, parse_any

NAME = "truecar"
LABEL = "TrueCar"
KIND = "marketplace"
HOST = "https://www.truecar.com"
URL = HOST + "/used-cars-for-sale/listings/{make_slug}/{model_slug}/?searchRadius=5000&sort[]=price_asc&page={page}"


def fetch(client, ctx: Ctx):
    out = []
    for page in (1, 2):
        res = client.get(ctx.url(URL, page=page))
        ctx.pages += 1
        if not res.ok:
            ctx.diagnose(res, LABEL)
            break
        got = _cards(res.text, res.url)
        nd = next_data(res.text)
        if nd:
            for v in walk(nd, lambda d: isinstance(d.get("vin"), str) and vin_matches(d["vin"])):
                ctx.sample("truecar-vehicle", v)
                got.append(_from_json(v))
        got = [g for g in got if g.vin or g.price]
        got += listings_from_jsonld(res.text, NAME, LABEL, res.url)
        if not got:
            got = listings_from_vin_cards(res.text, NAME, LABEL, res.url)
        if not got:
            if page == 1:
                ctx.diagnose(res, LABEL)
            break
        out += got
    return dedupe(out)


def _cards(html: str, base: str) -> list[Listing]:
    soup = BeautifulSoup(html, "lxml")
    out = []
    for a in soup.select("a[data-test='vehicleCardLink'], a[href*='/used-cars-for-sale/listing/']"):
        text = a.get_text("\n", strip=True)
        if not is_target(text):
            continue
        title_m = re.search(r"(20\d\d\s+%s\s+%s[^\n]*)" % (current_target()["make"], current_target()["alias_re"]), text, re.I)
        l = Listing(source=NAME, source_name=LABEL, url=abs_url(base, a.get("href", "")), title=title_m.group(1) if title_m else text[:80],
                    price=parse_price(text), mileage=parse_mileage(text), year=parse_year(text),
                    extra={"description": text[:400]})
        loc = re.search(r"\n([A-Z][A-Za-z .]+,\s*[A-Z]{2})\b", text)
        if loc:
            l.location = loc.group(1)
        from ..models import VIN_RE
        vin = VIN_RE.search(a.get("href", ""))
        if vin:
            l.vin = vin.group(1)
        out.append(l.finalize())
    return out


def _from_json(v: dict) -> Listing:
    veh = v.get("vehicle") or v
    dealer = v.get("dealership") or v.get("dealer") or {}
    loc = dealer.get("location") or {}
    pricing = v.get("pricing") or {}
    price = None
    for k in ("listPrice", "list_price", "price", "salePrice", "sale_price", "totalPrice", "displayPrice"):
        price = price or parse_price(pricing.get(k)) or parse_price(v.get(k))
    if not price:
        import re as _re, json as _json
        m = _re.search(r'"(?:list_?[pP]rice|sale_?[pP]rice|price)"\s*:\s*"?([0-9]{5,7})', _json.dumps(v))
        price = parse_price(m.group(1)) if m else None
    return Listing(source=NAME, source_name=LABEL, url=abs_url(HOST, v.get("vdpUrl") or v.get("url") or f"/used-cars-for-sale/listing/{v['vin']}/"),
                   title=f"{veh.get('year','')} {current_target()['label']} {veh.get('trim','') or ''}".strip(), vin=v["vin"],
                   year=veh.get("year"), price=price,
                   mileage=parse_mileage(veh.get("mileage") or v.get("mileage")), dealer=dealer.get("name"),
                   location=", ".join(x for x in [loc.get("city") or v.get("city"), loc.get("state") or v.get("state")] if x) or None,
                   condition="cpo" if v.get("certified") else "used", color=veh.get("exteriorColor")).finalize()
