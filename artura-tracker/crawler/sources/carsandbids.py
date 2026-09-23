"""Cars & Bids - live auctions and recently ended results (Cloudflare-protected; best effort).

The model search page lists live auctions ("Bid: $x · Ends in ...") and recently ended ones
("Sold for $x" / "Bid to $x" + "Ended m/d/yy"). Live auctions become auction listings;
ended ones become sale comps (listing_type="sold") that the store keeps in data/sales.json.
"""
from __future__ import annotations

import re
from datetime import date

from ..extract import abs_url
from ..models import Listing, parse_mileage, parse_price, parse_year, current_target, extract_state

NAME = "carsandbids"
LABEL = "Cars & Bids"
KIND = "auction"
HOST = "https://carsandbids.com"
URL_T = HOST + "/search/{make_slug}/{model_slug}"

AUCTION_RE = re.compile(r"/auctions/([A-Za-z0-9]+)/", re.I)
STATUS_RE = re.compile(r"Sold for|Bid to|\bBid:?\s*\$|Current Bid|Ends? in|Ending|Time Left|Ended\b|\d+\s+bids?\b", re.I)
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def _ended_date(text: str):
    m = re.search(r"Ended\s+(\d{1,2})/(\d{1,2})/(\d{2,4})", text, re.I)
    if m:
        mo, d, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y = y + 2000 if y < 100 else y
        return f"{y:04d}-{mo:02d}-{d:02d}"
    m = re.search(r"Ended\s+([A-Za-z]{3})[a-z]*\.?\s+(\d{1,2})(?:,?\s+(\d{4}))?", text, re.I)
    if m and m.group(1).lower() in MONTHS:
        y = int(m.group(3)) if m.group(3) else date.today().year
        return f"{y:04d}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}"
    return None


def parse_cards(html: str, base_url: str = HOST, target: dict | None = None) -> list[Listing]:
    """One Listing per auction card: the smallest ancestor of an /auctions/ link that shows an
    auction status and holds exactly one auction."""
    from bs4 import BeautifulSoup
    t = target or current_target()
    soup = BeautifulSoup(html, "lxml")
    out, seen = [], set()
    for a in soup.find_all("a", href=True):
        m = AUCTION_RE.search(a["href"])
        if not m:
            continue
        aid = m.group(1)
        if aid in seen:
            continue
        node, text = a, a.get_text("\n", strip=True)
        for _ in range(8):
            if STATUS_RE.search(text) and re.search(r"20\d\d", text):
                break
            node = node.parent
            if node is None:
                break
            text = node.get_text("\n", strip=True)
        if node is None or not STATUS_RE.search(text) or len(text) > 3000:
            continue
        ids = {AUCTION_RE.search(x["href"]).group(1) for x in node.find_all("a", href=True) if AUCTION_RE.search(x["href"])}
        if len(ids) != 1:
            continue                    # container holds several auctions; would mix prices
        seen.add(aid)
        lines = [re.sub(r"\s+", " ", x).strip() for x in text.split("\n") if x.strip()]
        lines = [x for x in lines if x.lower() not in ("watch", "featured", "reserve", "no reserve")]
        title = next((x for x in lines if re.match(r"^(19|20)\d\d\s", x) and re.search(t["alias_re"], x, re.I)), None) \
            or next((x for x in lines if re.search(t["alias_re"], x, re.I)), None)
        if not title:
            continue
        title = re.sub(r"\s*(Watch|Featured)$", "", title, flags=re.I)
        sold = re.search(r"Sold for\s*\$?\s*([\d,]+)", text, re.I)
        bid_to = re.search(r"Bid to\s*\$?\s*([\d,]+)", text, re.I)
        live = re.search(r"(?:Current\s*)?Bid:?\s*\$\s*([\d,]+)", text, re.I)
        ended = _ended_date(text)
        mile_m = re.search(r"~?\s*([\d,]{3,7})\s*(?:Miles|mi\b)", text, re.I)
        mileage = parse_mileage(mile_m.group(0)) if mile_m else None
        loc = next((x for x in lines if re.search(r"^[A-Z][A-Za-z .'-]+,\s*[A-Z]{2}$", x) and extract_state(x)), None)
        img = node.find("img")
        href = abs_url(base_url, a["href"].split("?")[0].split("#")[0])
        desc = " | ".join(lines)[:400]
        if sold or bid_to or (ended and not live):
            price = parse_price(sold.group(1)) if sold else (parse_price(bid_to.group(1)) if bid_to else None)
            out.append(Listing(source=NAME, source_name=LABEL, url=href, title=title, year=parse_year(title), price=price,
                               mileage=mileage, listing_type="sold", condition="used", location=loc,
                               image=(img.get("data-src") or img.get("src")) if img else None,
                               extra={"sold": bool(sold), "ended": ended, "description": desc}).finalize())
        else:
            out.append(Listing(source=NAME, source_name=LABEL, url=href, title=title, year=parse_year(title),
                               price=parse_price(live.group(1)) if live else None, mileage=mileage, listing_type="auction",
                               condition="used", location=loc, image=(img.get("data-src") or img.get("src")) if img else None,
                               auction_end=(re.search(r"(Ends?\s+in[^|]{0,40}|Time Left[^|]{0,30})", text, re.I) or [None, None])[1],
                               extra={"description": desc}).finalize())
    return out


def fetch(client, ctx):
    URL = ctx.url(URL_T)
    res = client.get(URL)
    ctx.pages += 1
    out = parse_cards(res.text, HOST) if res.ok else []
    if not out:
        from ..browser import browser_get
        b = browser_get(URL, scroll=4, network_idle=True, wait_ms=4000)
        ctx.pages += 1
        if not b.error and b.html:
            out = parse_cards(b.html, HOST)
            if not out:
                from ..http_client import FetchResult
                ctx.diagnose(FetchResult(url=URL, status=b.status, text=b.html, elapsed=0.0, error=None), LABEL)
        elif not res.ok:
            ctx.diagnose(res, LABEL)
    if out:
        ctx.sample("carsandbids-card", {"title": out[0].title, "type": out[0].listing_type, "price": out[0].price,
                                        "mileage": out[0].mileage, "extra": out[0].extra})
    live = sum(1 for l in out if l.listing_type == "auction")
    ctx.log.info("%s: %d live auctions, %d ended results", LABEL, live, len(out) - live)
    return out
