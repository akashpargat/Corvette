"""duPont REGISTRY - exotic-car classifieds (Next.js)."""
from __future__ import annotations

import re

from ..extract import abs_url, next_data, walk
from ..models import Listing, parse_mileage, parse_price, parse_year
from .base import Ctx, dedupe, listings_from_jsonld, listings_from_vin_cards

NAME = "dupont"
LABEL = "duPont REGISTRY"
KIND = "marketplace"
HOST = "https://www.dupontregistry.com"
URL = HOST + "/autos/results/mclaren/artura/all?sort=price_asc&page={page}"


def fetch(client, ctx: Ctx):
    out = []
    for page in (1, 2, 3):
        res = client.get(URL.format(page=page))
        ctx.pages += 1
        if not res.ok:
            ctx.diagnose(res, LABEL)
            break
        got = []
        nd = next_data(res.text)
        if nd:
            ctx.sample('dupont-nextdata-keys', list((nd.get("props", {}).get("pageProps", {}) or {}).keys()))
            for r in walk(nd, lambda d: ("artura" in str(d.get("model", "")).lower() or "artura" in str(d.get("title", "")).lower()) and ("price" in d or "askingPrice" in d)):
                ctx.sample('dupont', r)
                got.append(_row(r))
        got += listings_from_jsonld(res.text, NAME, LABEL, res.url)
        if not got:
            got = _links(res.text, res.url)
        if not got:
            if page == 1:
                ctx.diagnose(res, LABEL)
            break
        out += got
        if len(got) < 20:
            break
    return dedupe(out)


def _row(r: dict) -> Listing:
    dealer = r.get("dealer") or r.get("seller") or {}
    if not isinstance(dealer, dict):
        dealer = {"name": str(dealer)}
    loc = ", ".join(x for x in [r.get("city") or dealer.get("city"), r.get("state") or dealer.get("state")] if x)
    href = r.get("url") or r.get("slug") or r.get("link") or ""
    return Listing(source=NAME, source_name=LABEL, url=abs_url(HOST, href) if href else HOST, title=r.get("title") or f"{r.get('year','')} McLaren Artura",
                   vin=r.get("vin"), year=r.get("year"), price=parse_price(r.get("price") or r.get("askingPrice")),
                   mileage=parse_mileage(r.get("mileage") or r.get("odometer")), dealer=dealer.get("name"), location=loc or None,
                   image=(r.get("image") or r.get("photo") or (r.get("images") or [None])[0]) if isinstance(r.get("images", []), list) else None,
                   color=r.get("exteriorColor") or r.get("color"), condition="new" if str(r.get("condition", "")).lower() == "new" else "used").finalize()


def _links(html: str, base: str) -> list[Listing]:
    out = []
    for m in re.finditer(r'href="([^"]*/autos/listing/[^"]*artura[^"]*)"', html, re.I):
        chunk = html[max(0, m.start() - 3000): m.end() + 3000]
        text = re.sub(r"<[^>]+>", " ", chunk)
        title_m = re.search(r"(20\d\d\s+McLaren\s+Artura[^<]{0,30})", text)
        out.append(Listing(source=NAME, source_name=LABEL, url=abs_url(base, m.group(1)), title=title_m.group(1).strip() if title_m else "McLaren Artura",
                           year=parse_year(title_m.group(1) if title_m else ""), price=parse_price(text), mileage=parse_mileage(text)).finalize())
    return out
