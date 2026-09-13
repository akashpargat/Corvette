"""Generic extractors: JSON-LD, embedded JSON blobs, VIN-anchored text cards."""
from __future__ import annotations

import json
import re
from typing import Iterable, Optional

from .models import VIN_RE, parse_mileage, parse_price, parse_year

LDJSON_RE = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)


def find_jsonld(html: str) -> list:
    out = []
    for m in LDJSON_RE.finditer(html):
        raw = m.group(1).strip()
        try:
            obj = json.loads(raw)
        except ValueError:
            # Some sites put several objects or trailing commas in one tag.
            try:
                obj = json.loads(re.sub(r",\s*([}\]])", r"\1", raw))
            except ValueError:
                continue
        if isinstance(obj, list):
            out.extend(o for o in obj if isinstance(o, dict))
        elif isinstance(obj, dict):
            if "@graph" in obj and isinstance(obj["@graph"], list):
                out.extend(o for o in obj["@graph"] if isinstance(o, dict))
            out.append(obj)
    return out


def _types(obj: dict) -> set:
    t = obj.get("@type", [])
    if isinstance(t, str):
        t = [t]
    return {str(x).lower() for x in t}


def vehicles_from_jsonld(objs: Iterable[dict]) -> list[dict]:
    """Return simplified vehicle dicts from schema.org Vehicle/Car/Product objects."""
    found = []
    stack = list(objs)
    while stack:
        o = stack.pop()
        if not isinstance(o, dict):
            continue
        ts = _types(o)
        # nested ItemList -> itemListElement -> item
        for k in ("itemListElement", "mainEntity", "offers", "item", "about", "itemOffered"):
            v = o.get(k)
            if isinstance(v, list):
                stack.extend(x for x in v if isinstance(x, dict))
            elif isinstance(v, dict):
                stack.append(v)
        if not (ts & {"vehicle", "car", "product", "motorizedbicycle", "automobile"}):
            continue
        name = o.get("name") or ""
        desc = o.get("description") or ""
        offers = o.get("offers") or {}
        if isinstance(offers, list):
            offers = offers[0] if offers else {}
        price = offers.get("price") if isinstance(offers, dict) else None
        if price is None and "price" in o:
            price = o.get("price")
        mileage = None
        mo = o.get("mileageFromOdometer")
        if isinstance(mo, dict):
            mileage = parse_mileage(mo.get("value"))
        elif mo:
            mileage = parse_mileage(mo)
        vin = o.get("vehicleIdentificationNumber") or o.get("vin") or o.get("sku") or ""
        vm = VIN_RE.search(str(vin)) or VIN_RE.search(json.dumps(o)[:4000])
        year = o.get("vehicleModelDate") or o.get("modelDate") or o.get("productionDate") or parse_year(name)
        color = o.get("color")
        url = offers.get("url") if isinstance(offers, dict) else None
        url = url or o.get("url") or o.get("@id")
        image = o.get("image")
        if isinstance(image, list):
            image = image[0] if image else None
        if isinstance(image, dict):
            image = image.get("url") or image.get("contentUrl")
        seller = offers.get("seller") if isinstance(offers, dict) else None
        if isinstance(seller, dict):
            seller = seller.get("name")
        model = o.get("model") or ""
        if isinstance(model, dict):
            model = model.get("name", "")
        pp = parse_price(price) if price is not None else None
        if pp is not None and pp < 40000:
            pp = None  # a monthly payment or placeholder, never an Artura
        found.append({
            "name": name, "description": desc, "price": pp,
            "mileage": mileage, "vin": vm.group(1) if vm else None,
            "year": int(str(year)[:4]) if year and str(year)[:4].isdigit() else None,
            "color": color if isinstance(color, str) else None, "url": url, "image": image,
            "seller": seller, "model": str(model), "condition": str(o.get("itemCondition") or (offers.get("itemCondition") if isinstance(offers, dict) else "") or ""),
        })
    return found


def find_script_json(html: str, marker: str) -> Optional[object]:
    """Locate `marker` in the page and parse the JSON object/array that follows it."""
    i = html.find(marker)
    if i < 0:
        return None
    j = i + len(marker)
    # skip to first { or [
    while j < len(html) and html[j] not in "{[":
        if html[j] == ";" or html[j] == "<":
            return None
        j += 1
    if j >= len(html):
        return None
    return parse_json_prefix(html, j)


def parse_json_prefix(text: str, start: int) -> Optional[object]:
    """Parse the JSON value starting at text[start] by bracket matching."""
    depth = 0
    in_str = False
    esc = False
    for k in range(start, len(text)):
        c = text[k]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
            if depth == 0:
                chunk = text[start:k + 1]
                try:
                    return json.loads(chunk)
                except ValueError:
                    try:
                        return json.loads(chunk.encode().decode("unicode_escape"))
                    except Exception:
                        return None
    return None


def next_data(html: str) -> Optional[dict]:
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def walk(obj, pred, _depth=0):
    """Yield every dict in a nested structure that satisfies pred(dict)."""
    if _depth > 40:
        return
    if isinstance(obj, dict):
        if pred(obj):
            yield obj
        for v in obj.values():
            yield from walk(v, pred, _depth + 1)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v, pred, _depth + 1)


def find_vins(text: str) -> list[str]:
    seen, out = set(), []
    for m in VIN_RE.finditer(text or ""):
        v = m.group(1)
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def html_to_text(html: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", " ", html, flags=re.S | re.I)
    t = re.sub(r"<(br|/p|/div|/li|/h[1-6]|/tr|/td|/th)[^>]*>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&nbsp;|&#160;", " ", t)
    t = re.sub(r"&amp;", "&", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t


def abs_url(base: str, href: str) -> str:
    from urllib.parse import urljoin
    return urljoin(base, href)


def enclosing_object(text: str, pos: int, max_back: int = 6000) -> Optional[int]:
    """Index of the '{' that opens the JSON object containing text[pos]. Heuristic."""
    depth = 0
    i = pos
    stop = max(0, pos - max_back)
    while i > stop:
        c = text[i]
        if c == "}":
            depth += 1
        elif c == "{":
            if depth == 0:
                return i
            depth -= 1
        i -= 1
    return None


def vin_dicts_from_html(html: str, limit: int = 400) -> list[dict]:
    """Every JSON object in the page that carries a McLaren VIN, from any script blob.

    Works for Dealer.com (DDC.dataLayer), DealerOn (dlron-srp-model), DealerInspire,
    CARFAX/CarGurus preloaded state, Cars & Bids preloaded-data and most Next.js pages.
    """
    out = []
    seen = set()
    for m in VIN_RE.finditer(html):
        if len(out) >= limit:
            break
        start = enclosing_object(html, m.start())
        if start is None:
            continue
        obj = parse_json_prefix(html, start)
        if not isinstance(obj, dict):
            # RSC / double-escaped payloads: try unescaping the chunk
            chunk = html[start: min(len(html), start + 8000)].replace('\\"', '"').replace("\\\\", "\\")
            obj = parse_json_prefix(chunk, 0)
        if not isinstance(obj, dict):
            continue
        key = json.dumps(obj, sort_keys=True, default=str)[:400]
        if key in seen:
            continue
        seen.add(key)
        out.append(obj)
    return out


def _first_key(d: dict, pattern: str, want=None):
    rx = re.compile(pattern, re.I)
    for k, v in d.items():
        if rx.search(k) and v not in (None, "", [], {}):
            if want == "num":
                n = parse_price(v) if isinstance(v, (int, float, str)) else None
                if n:
                    return n
            elif want == "str":
                if isinstance(v, (str, int, float)):
                    return str(v)
            else:
                return v
    return None


def vehicle_from_vin_dict(o: dict) -> dict:
    """Map an arbitrary dealer/marketplace JSON object to our vehicle fields."""
    flat = dict(o)
    for k, v in list(o.items()):            # one level of nesting is common (pricing: {...}, dealer: {...})
        if isinstance(v, dict):
            for k2, v2 in v.items():
                flat.setdefault(f"{k}.{k2}", v2)
    vin = None
    for k, v in flat.items():
        if isinstance(v, str) and VIN_RE.fullmatch(v.strip()) and re.search(r"vin|identifier|id$", k, re.I):
            vin = v.strip()
            break
    if not vin:
        vm = VIN_RE.search(json.dumps(o, default=str))
        vin = vm.group(1) if vm else None
    price = None
    for pat in (r"^(internet|selling|sale|asking|final|our|dealer|retail|list|listing|current|display|vehicle)?_?price(amount|value)?$",
                r"price", r"^msrp$"):
        cand = []
        for k, v in flat.items():
            if re.search(pat, k, re.I) and not re.search(r"monthly|payment|lease|finance|per_?month|apr|rate|history|drop|change|delta|was|old|prev|original|msrp_?diff|diff", k, re.I):
                n = parse_price(v) if isinstance(v, (int, float, str)) else None
                if n and 40000 <= n <= 600000:
                    cand.append(n)
        if cand:
            price = min(cand)
            break
    mileage = None
    for k, v in flat.items():
        if re.search(r"odometer|mileage|^miles$|mileageFromOdometer|\.value$", k, re.I) and not re.search(r"unit|string|label|formatted|type", k, re.I):
            n = parse_mileage(v) if isinstance(v, (int, float, str)) else None
            if n is not None and 0 <= n < 100000 and not re.search(r"price", k, re.I):
                mileage = n
                break
    year = _first_key(flat, r"^(model)?year$|modelDate|vehicleModelDate", "str")
    year = int(str(year)[:4]) if year and str(year)[:4].isdigit() else None
    trim = _first_key(flat, r"^trim(name)?$|^vehicleTrim$|^series$", "str")
    color = _first_key(flat, r"exterior_?colou?r(name|simple)?$|^colou?r$|^normalizedExteriorColor$", "str")
    dealer = _first_key(flat, r"dealer(ship)?_?name|seller_?name|^dealer\.name$|serviceProviderName|ownerName|^retailer(name)?$", "str")
    city = _first_key(flat, r"(^|[._])(city|dealer_?city|seller_?city|city_?name)$", "str")
    state = _first_key(flat, r"(^|[._])(state|state_?code|region|dealer_?state|seller_?region|province)$", "str")
    if city and (len(str(city)) > 40 or re.search(r"\d", str(city))):
        city = None
    if state and not (re.fullmatch(r"[A-Za-z]{2}", str(state)) or re.fullmatch(r"[A-Za-z .]{4,20}", str(state))):
        state = None
    url = _first_key(flat, r"^(vdp_?url|vdpBaseUrl|url|link|href|detail_?url|listing_?url|canonical_?url|vdpLink|vdp)$", "str")
    image = _first_key(flat, r"image|photo|thumbnail|picture", "str")
    if image and not str(image).startswith("http"):
        image = None
    cond = (_first_key(flat, r"^(type|condition|stock_?type|inventory_?type|vehicle_?type|status|listingType)$", "str") or "").lower()
    condition = "cpo" if "cert" in cond or flat.get("certified") or flat.get("isCertified") else "new" if cond == "new" or cond.startswith("new") else "used" if "used" in cond or "pre" in cond else "unknown"
    branded = any(v for k, v in flat.items() if re.search(r"salvage|branded|lemon|flood|rebuilt|frameDamage|totalLoss", k, re.I) and v is True)
    clean = any(v for k, v in flat.items() if re.search(r"noAccidents?|accidentFree|isCleanTitle|clean_?title", k, re.I) and v is True)
    acc = _first_key(flat, r"^accident(s|Count|History|Text)?$|^has_?accidents?$|accident.*(text|summary|status|count|label)$")
    acc_s = str(acc) if acc is not None else ""
    if acc in (0, "0", False) or re.search(r"no (reported )?accidents?|none reported|accident.?free|no damage", acc_s, re.I):
        clean = clean or not branded
    elif re.search(r"salvage|rebuilt|total loss|lemon|flood", acc_s, re.I):
        branded = True
    title = _first_key(flat, r"^(title|listing_?title|name|heading|display_?name|vehicle_?title)$", "str") or ""
    return {"vin": vin, "price": price, "mileage": mileage, "year": year, "trim": trim, "color": color, "dealer": dealer,
            "city": city, "state": state, "url": url, "image": image, "condition": condition,
            "branded": branded, "clean": clean, "title": title, "accidents": acc,
            "owners": _first_key(flat, r"owner(s|Count|History|Text)?$")}
