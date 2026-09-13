"""Facebook Marketplace - every US region, via a real browser (Playwright).

Facebook has no Marketplace API and shows a login wall to anonymous
datacenter traffic most of the time. This source therefore:

  * runs a headless Chromium with a realistic profile;
  * injects a logged-in session if FB_COOKIES_JSON is set (export your own
    cookies once with a "Cookie-Editor" style extension: Marketplace ->
    Export -> JSON, and store it as a GitHub Actions secret);
  * searches every hub city in config.FB_HUBS with the query "mclaren artura";
  * parses both the rendered cards and the embedded GraphQL payloads;
  * reports "login_required" honestly when it is walled, instead of
    pretending the region had no cars.
"""
from __future__ import annotations

import json
import os
import re
import time
from urllib.parse import quote

from .. import config
from ..extract import parse_json_prefix
from ..models import Listing, parse_mileage, parse_price, parse_year
from .base import Ctx, dedupe

NAME = "fb_marketplace"
LABEL = "Facebook Marketplace"
KIND = "marketplace"
SEARCH = "https://www.facebook.com/marketplace/{hub}/search?query={q}&minPrice={minp}&exact=false"


def fetch(client, ctx: Ctx):
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:  # pragma: no cover
        ctx.note(f"{LABEL}: playwright not installed ({e})")
        return []
    cookies = _cookies_from_env()
    out = []
    walled = 0
    hubs = config.FB_HUBS
    with sync_playwright() as p:
        launch = {"headless": os.environ.get("HEADLESS", "1") != "0", "args": ["--disable-blink-features=AutomationControlled", "--no-sandbox"]}
        if config.PROXY_URL:
            launch["proxy"] = {"server": config.PROXY_URL}
        browser = p.chromium.launch(**launch)
        context = browser.new_context(
            user_agent=config.USER_AGENTS[0], locale="en-US", timezone_id="America/Chicago",
            viewport={"width": 1366, "height": 900}, device_scale_factor=1,
        )
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        if cookies:
            context.add_cookies(cookies)
            ctx.note(f"{LABEL}: using {len(cookies)} session cookies from FB_COOKIES_JSON")
        page = context.new_page()
        for i, hub in enumerate(hubs):
            url = SEARCH.format(hub=hub, q=quote("mclaren artura"), minp=config.FB_MIN_PRICE)
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(2500)
                _dismiss_login_dialog(page)
                for _ in range(3):
                    page.mouse.wheel(0, 2500)
                    page.wait_for_timeout(900)
                html = page.content()
                if _is_login_wall(page.url, html):
                    walled += 1
                    ctx.log.info("  fb %-16s login wall", hub)
                    if walled >= 4 and not out:
                        ctx.note(f"{LABEL}: login wall on {walled} hubs in a row; stopping. Add FB_COOKIES_JSON secret to unlock.")
                        break
                    continue
                got = _parse_cards(page, hub) + _parse_embedded(html, hub)
                ctx.log.info("  fb %-16s %d cards", hub, len(got))
                out += got
            except Exception as e:
                ctx.log.info("  fb %-16s error %s", hub, str(e)[:120])
            ctx.pages += 1
            time.sleep(1.0)
        browser.close()
    ctx.note(f"{LABEL}: {len(hubs)} hubs searched, {walled} login-walled, {len(out)} raw cards")
    ctx.extra = {"login_walled_hubs": walled, "hubs": len(hubs), "had_cookies": bool(cookies)}
    return dedupe([l for l in out if "artura" in l.title.lower()])


def _cookies_from_env():
    raw = os.environ.get("FB_COOKIES_JSON", "").strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except ValueError:
        return []
    out = []
    for c in data if isinstance(data, list) else data.get("cookies", []):
        if not isinstance(c, dict) or "name" not in c or "value" not in c:
            continue
        out.append({"name": c["name"], "value": c["value"], "domain": c.get("domain", ".facebook.com"),
                    "path": c.get("path", "/"), "secure": True, "httpOnly": bool(c.get("httpOnly", False)),
                    "sameSite": "None"})
    return out


def _dismiss_login_dialog(page):
    for sel in ("div[aria-label='Close']", "div[role='dialog'] div[aria-label='Close']", "[aria-label='Close'] "):
        try:
            el = page.query_selector(sel)
            if el:
                el.click(timeout=1500)
                page.wait_for_timeout(500)
                return
        except Exception:
            pass
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass


def _is_login_wall(url: str, html: str) -> bool:
    if "/login" in url or "login.php" in url:
        return True
    has_items = "/marketplace/item/" in html
    if has_items:
        return False
    return bool(re.search(r"(log in to continue|log into facebook|you must log in|create new account)", html, re.I))


def _parse_cards(page, hub: str) -> list[Listing]:
    out = []
    try:
        anchors = page.query_selector_all("a[href*='/marketplace/item/']")
    except Exception:
        return out
    seen = set()
    for a in anchors:
        try:
            href = a.get_attribute("href") or ""
            m = re.search(r"/marketplace/item/(\d+)", href)
            if not m or m.group(1) in seen:
                continue
            seen.add(m.group(1))
            text = a.inner_text()
        except Exception:
            continue
        lines = [t.strip() for t in text.split("\n") if t.strip()]
        if not lines:
            continue
        title = next((l for l in lines if "artura" in l.lower() or "mclaren" in l.lower()), lines[min(1, len(lines) - 1)])
        price_line = next((l for l in lines if "$" in l), "")
        loc_line = next((l for l in lines if re.search(r",\s*[A-Z]{2}$", l)), None)
        miles_line = next((l for l in lines if re.search(r"\bmi(les)?\b|\bK miles", l, re.I)), "")
        l = Listing(source=NAME, source_name=LABEL, url=f"https://www.facebook.com/marketplace/item/{m.group(1)}/", title=title,
                    year=parse_year(title), price=parse_price(price_line), mileage=parse_mileage(miles_line) if miles_line else None,
                    location=loc_line, listing_type="private", condition="used",
                    extra={"hub": hub, "description": " | ".join(lines)[:300]})
        try:
            img = a.query_selector("img")
            if img:
                l.image = img.get_attribute("src")
        except Exception:
            pass
        out.append(l.finalize())
    return out


def _parse_embedded(html: str, hub: str) -> list[Listing]:
    """GraphQL payloads embedded in the page carry exact prices and locations."""
    out = []
    for m in re.finditer(r'"listing":\s*\{', html):
        obj = parse_json_prefix(html, m.end() - 1)
        if not isinstance(obj, dict):
            continue
        title = obj.get("marketplace_listing_title") or obj.get("custom_title") or ""
        if "artura" not in title.lower():
            continue
        lid = obj.get("id")
        price = (obj.get("listing_price") or {}).get("amount") or (obj.get("listing_price") or {}).get("formatted_amount")
        loc = (((obj.get("location") or {}).get("reverse_geocode")) or {})
        loc_s = ", ".join(x for x in [loc.get("city"), loc.get("state")] if x)
        img = ((obj.get("primary_listing_photo") or {}).get("image") or {}).get("uri")
        vs = obj.get("custom_sub_titles_with_rendering_flags") or []
        subtitle = " ".join(str(v.get("subtitle", "")) for v in vs if isinstance(v, dict))
        out.append(Listing(source=NAME, source_name=LABEL, url=f"https://www.facebook.com/marketplace/item/{lid}/", title=title,
                           year=parse_year(title), price=parse_price(price), mileage=parse_mileage(subtitle),
                           location=loc_s or None, image=img, listing_type="private", condition="used",
                           extra={"hub": hub, "description": subtitle[:200]}).finalize())
    return out
