"""Helpers shared by source modules."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from ..extract import find_jsonld, vehicles_from_jsonld, html_to_text, find_vins, abs_url
from ..http_client import Client, FetchResult, page_title, sentinel_keys, visible_text
from ..models import Listing, parse_mileage, parse_price, parse_year, is_artura, VIN_RE


@dataclass
class Ctx:
    """Per-run context handed to every source."""
    log: object
    notes: list = field(default_factory=list)
    pages: int = 0

    def note(self, msg: str):
        self.notes.append(msg)
        self.log.info(msg)

    def diagnose(self, res: FetchResult, label: str = ""):
        """Log why a page produced nothing, in a way readable from CI logs."""
        why = res.blocked_reason() or res.error or "no listings parsed"
        self.log.warning("%s%s: %s | status=%s bytes=%d title=%r keys=%s",
                         label, f" {res.url}" if res.url else "", why, res.status, len(res.text),
                         page_title(res.text), sentinel_keys(res.text))
        self.log.warning("  text: %s", visible_text(res.text, 400))
        if res.status == 200 and len(res.text) > 5000:
            scripts = re.findall(r"<script([^>]{0,160})>", res.text)
            ids = [re.sub(r"\s+", " ", a).strip()[:90] for a in scripts if ("id=" in a or "type=" in a)]
            self.log.warning("  scripts(%d): %s", len(scripts), " | ".join(dict.fromkeys(ids))[:1200])
            hits = [m.start() for m in re.finditer(r"[Aa]rtura", res.text)][:200]
            shown = 0
            for h in hits:
                ctx = res.text[max(0, h - 160): h + 220].replace("\n", " ")
                if "$" in ctx or "price" in ctx.lower() or "vin" in ctx.lower():
                    self.log.warning("  artura@%d: %s", h, ctx)
                    shown += 1
                if shown >= 4:
                    break
        self.notes.append(f"{label or res.url}: {why}")

    def sample(self, label: str, obj, limit: int = 1500):
        """Log a JSON sample once per label so the schema is visible in CI logs."""
        import json
        key = f"_sampled_{label}"
        if getattr(self, key, False):
            return
        setattr(self, key, True)
        try:
            self.log.info("  sample[%s]: %s", label, json.dumps(obj, default=str)[:limit])
        except Exception:
            pass


def listings_from_jsonld(html: str, source: str, source_name: str, base_url: str,
                         listing_type: str = "dealer", dealer: Optional[str] = None) -> list[Listing]:
    out = []
    for v in vehicles_from_jsonld(find_jsonld(html)):
        text = f"{v['name']} {v['model']} {v['description']}"
        if not is_artura(text) and not (v["vin"] or "").startswith("SBM16"):
            continue
        url = v["url"] or base_url
        if url and not url.startswith("http"):
            url = abs_url(base_url, url)
        cond = "unknown"
        c = v["condition"].lower()
        if "new" in c:
            cond = "new"
        elif "used" in c or "refurb" in c:
            cond = "used"
        lst = Listing(source=source, source_name=source_name, url=url or base_url, title=v["name"] or "McLaren Artura",
                      vin=v["vin"], year=v["year"], price=v["price"], mileage=v["mileage"], color=v["color"],
                      dealer=v["seller"] or dealer, image=v["image"], listing_type=listing_type, condition=cond,
                      extra={"description": (v["description"] or "")[:600]})
        out.append(lst.finalize())
    return out


def listings_from_vin_cards(html: str, source: str, source_name: str, base_url: str,
                            dealer: Optional[str] = None) -> list[Listing]:
    """Last-resort parser: find each VIN in the page and read price/mileage/year near it.

    Works on almost any server-rendered inventory page because dealer platforms
    print the VIN inside each card (data-vin, a spec table, or a "VIN:" line).
    """
    out = []
    seen = set()
    for m in VIN_RE.finditer(html):
        vin = m.group(1)
        if vin in seen:
            continue
        seen.add(vin)
        lo, hi = max(0, m.start() - 6000), min(len(html), m.end() + 6000)
        chunk = html[lo:hi]
        text = html_to_text(chunk)
        if not is_artura(text):
            continue
        title_m = re.search(r"(20(?:1[5-9]|2[0-9])\s+(?:New\s+|Used\s+|Certified\s+)?McLaren\s+Artura(?:\s+(?:Spider|Performance|TechLux|Vision|GT4|Coupe))*)", text, re.I)
        title = title_m.group(1).strip() if title_m else "McLaren Artura"
        prices = [parse_price(p) for p in re.findall(r"\$\s?[0-9]{2,3}(?:,[0-9]{3})+", text)]
        prices = [p for p in prices if p and 40000 <= p <= 500000]
        # nearest link to a VDP that contains the vin or 'artura'
        link_m = (re.search(r'href=["\']([^"\']*%s[^"\']*)["\']' % vin, chunk, re.I)
                  or re.search(r'href=["\']([^"\']*artura[^"\']*)["\']', chunk, re.I)
                  or re.search(r'href=["\']([^"\']*/(?:used|new|inventory|vehicle|vdp|certified|pre-owned)[^"\']*)["\']', chunk, re.I))
        url = abs_url(base_url, link_m.group(1)) if link_m else base_url
        lst = Listing(source=source, source_name=source_name, url=url, title=title, vin=vin,
                      year=parse_year(title), price=min(prices) if prices else None,
                      mileage=parse_mileage(text) if re.search(r"\bmi(les)?\b", text, re.I) else None,
                      dealer=dealer, extra={"description": text[:500]})
        out.append(lst.finalize())
    return out


def dedupe(listings: list[Listing]) -> list[Listing]:
    best: dict[str, Listing] = {}
    for l in listings:
        k = l.key
        cur = best.get(k)
        if cur is None:
            best[k] = l
            continue
        # merge: keep the record with more filled fields
        score = lambda x: sum(1 for f in (x.price, x.mileage, x.year, x.dealer, x.location, x.image) if f)
        if score(l) > score(cur):
            best[k] = l
    return list(best.values())
