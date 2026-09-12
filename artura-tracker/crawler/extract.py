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
        found.append({
            "name": name, "description": desc, "price": parse_price(price) if price is not None else None,
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
