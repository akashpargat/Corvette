"""Real-browser fetch used as a fallback when a site bot-walls plain HTTP.

Cloudflare "Just a moment", Kasada/PerimeterX "enable JS", and CloudFront
rules frequently pass for a real Chromium even from a datacenter IP. Each
call spins up its own Playwright driver so it is safe from worker threads.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Optional

from . import config

CHALLENGE_RE = re.compile(r"just a moment|enable javascript and cookies|verifying you are human|checking your browser|access denied|attention required", re.I)


@dataclass
class BrowserResult:
    status: int
    url: str
    html: str
    error: Optional[str] = None


def browser_get(url: str, *, wait_ms: int = 3500, challenge_wait_s: int = 20, scroll: int = 0,
                referer: Optional[str] = None, wait_for: Optional[str] = None, network_idle: bool = False) -> BrowserResult:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:  # pragma: no cover
        return BrowserResult(0, url, "", f"playwright unavailable: {e}")
    try:
        with sync_playwright() as p:
            import os
            launch = {"headless": os.environ.get("HEADLESS", "1") != "0", "args": ["--disable-blink-features=AutomationControlled", "--no-sandbox",
                                                 "--disable-dev-shm-usage"]}
            if config.PROXY_URL:
                launch["proxy"] = {"server": config.PROXY_URL}
            browser = p.chromium.launch(**launch)
            ctx = browser.new_context(locale="en-US", timezone_id="America/Chicago",
                                      viewport={"width": 1366, "height": 900},
                                      extra_http_headers={"Referer": referer} if referer else {})
            ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
                                "window.chrome = window.chrome || { runtime: {} };")
            page = ctx.new_page()
            # strip the Headless marker from the UA without inventing a mismatched one
            real_ua = page.evaluate("navigator.userAgent")
            if "Headless" in real_ua:
                ctx.close()
                ctx = browser.new_context(locale="en-US", timezone_id="America/Chicago",
                                          viewport={"width": 1366, "height": 900},
                                          user_agent=real_ua.replace("HeadlessChrome", "Chrome"),
                                          extra_http_headers={"Referer": referer} if referer else {})
                ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
                                    "window.chrome = window.chrome || { runtime: {} };")
                page = ctx.new_page()
            status = 0
            try:
                resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
                status = resp.status if resp else 0
            except Exception as e:
                browser.close()
                return BrowserResult(0, url, "", f"goto failed: {str(e)[:160]}")
            page.wait_for_timeout(wait_ms)
            t0 = time.time()
            while time.time() - t0 < challenge_wait_s:
                title = (page.title() or "")
                body = page.content()
                if not CHALLENGE_RE.search(title) and not (len(body) < 30000 and CHALLENGE_RE.search(body[:5000])):
                    break
                page.wait_for_timeout(1500)
            if network_idle:
                try:
                    page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
            if wait_for:
                try:
                    page.wait_for_selector(wait_for, timeout=15000)
                except Exception:
                    pass
            for _ in range(scroll):
                page.mouse.wheel(0, 2200)
                page.wait_for_timeout(700)
            html = page.content()
            final = page.url
            # JSON endpoints render inside <pre>
            m = re.match(r"^\s*<html><head></head><body><pre[^>]*>(.*)</pre></body></html>\s*$", html, re.S)
            if m:
                import html as htmlmod
                html = htmlmod.unescape(m.group(1))
            browser.close()
            if CHALLENGE_RE.search(html[:5000]) and len(html) < 30000:
                return BrowserResult(status or 403, final, html, "challenge not passed")
            return BrowserResult(200 if status in (0, 403, 406, 429, 503) and len(html) > 2000 else status, final, html)
    except Exception as e:
        return BrowserResult(0, url, "", f"browser error: {str(e)[:160]}")
