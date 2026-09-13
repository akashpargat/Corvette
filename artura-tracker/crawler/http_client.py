"""A small polite HTTP client with retries, UA rotation and diagnostics."""
from __future__ import annotations

import random
import re
import time
from dataclasses import dataclass, field
from typing import Optional

import requests

from . import config

try:  # requests only decodes brotli when the library is present
    import brotli  # noqa: F401
    _HAS_BROTLI = True
except Exception:  # pragma: no cover
    _HAS_BROTLI = False


@dataclass
class FetchResult:
    url: str
    status: int
    text: str
    elapsed: float
    error: Optional[str] = None
    headers: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.error is None and 200 <= self.status < 300

    def blocked_reason(self) -> Optional[str]:
        """Best-effort detection of bot walls so the run report can say *why*."""
        t = self.text[:20000].lower()
        if self.status in (403, 429, 503):
            if "just a moment" in t or "cf-chl" in t or "cloudflare" in t:
                return "cloudflare challenge"
            if "access denied" in t or "akamai" in t or "reference #" in t:
                return "akamai access denied"
            if "datadome" in t:
                return "datadome"
            if "perimeterx" in t or "px-captcha" in t or "_pxhc" in t:
                return "perimeterx captcha"
            return f"http {self.status}"
        if "captcha" in t and len(self.text) < 20000:
            return "captcha page"
        if "<title>just a moment" in t:
            return "cloudflare challenge"
        return None


class Client:
    def __init__(self, log, delay: float = config.POLITE_DELAY_SECONDS, browser_fallback: bool = True,
                 browser_budget: int = 12):
        self.log = log
        self.delay = delay
        self.browser_fallback = browser_fallback
        self.browser_budget = browser_budget
        self.browser_hits = 0
        self.session = requests.Session()
        self.session.headers.update(self._headers())
        if config.PROXY_URL:
            self.session.proxies = {"http": config.PROXY_URL, "https": config.PROXY_URL}
        self._last = 0.0
        self.requests_made = 0

    @staticmethod
    def _headers(extra: Optional[dict] = None) -> dict:
        h = {
            "User-Agent": random.choice(config.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br" if _HAS_BROTLI else "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        if extra:
            h.update(extra)
        return h

    def _throttle(self):
        wait = self.delay - (time.time() - self._last)
        if wait > 0:
            time.sleep(wait + random.random() * 0.4)
        self._last = time.time()

    def get(self, url: str, *, headers: Optional[dict] = None, retries: int = 2,
            params: Optional[dict] = None, allow_redirects: bool = True) -> FetchResult:
        last_err = None
        for attempt in range(retries + 1):
            self._throttle()
            t0 = time.time()
            try:
                r = self.session.get(url, headers=self._headers(headers), params=params,
                                     timeout=config.REQUEST_TIMEOUT, allow_redirects=allow_redirects)
                self.requests_made += 1
                res = FetchResult(url=r.url, status=r.status_code, text=r.text,
                                  elapsed=time.time() - t0, headers=dict(r.headers))
                self.log.debug("GET %s -> %s (%d bytes, %.1fs)", url, r.status_code, len(r.text), res.elapsed)
                if r.status_code in (429, 503) and attempt < retries:
                    time.sleep(2.5 * (attempt + 1))
                    continue
                if self.browser_fallback and self.browser_hits < self.browser_budget and (res.blocked_reason() or r.status_code in (403, 406, 429, 503)):
                    return self._via_browser(url, res, headers)
                return res
            except requests.RequestException as e:  # network errors
                last_err = f"{type(e).__name__}: {e}"
                self.log.debug("GET %s failed: %s", url, last_err)
                time.sleep(1.5 * (attempt + 1))
        return FetchResult(url=url, status=0, text="", elapsed=0.0, error=last_err or "unknown error")

    def _via_browser(self, url: str, res: "FetchResult", headers: Optional[dict]) -> "FetchResult":
        from .browser import browser_get
        self.browser_hits += 1
        t0 = time.time()
        b = browser_get(url, referer=(headers or {}).get("Referer"))
        if (b.error or b.status != 200 or len(b.html) < 500) and self.browser_hits <= 2:
            time.sleep(8)
            b = browser_get(url, referer=(headers or {}).get("Referer"), wait_ms=6000, challenge_wait_s=30)
        self.log.info("  browser fallback %s -> %s (%d bytes%s)", url[:90], b.status, len(b.html), f", {b.error}" if b.error else "")
        if b.error or b.status != 200 or len(b.html) < 500:
            res.headers["x-browser-fallback"] = b.error or f"status {b.status}"
            return res
        return FetchResult(url=b.url, status=200, text=b.html, elapsed=time.time() - t0,
                           headers={"x-browser-fallback": "ok"})

    def get_json(self, url: str, **kw):
        res = self.get(url, **kw)
        if not res.ok:
            return res, None
        try:
            import json
            return res, json.loads(res.text)
        except ValueError:
            return res, None


def visible_text(html: str, limit: int = 600) -> str:
    """Strip tags for a short diagnostic snippet in logs."""
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:limit]


def page_title(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip()[:120] if m else ""


def sentinel_keys(html: str) -> list[str]:
    """Which well-known data blobs are present. Helps debug a zero-result source."""
    keys = ["__NEXT_DATA__", "__BONNET_DATA__", "__PRELOADED_STATE__", "ld+json",
            "digitalData", "window.__INITIAL_STATE__", "auctionsCompletedInitialData",
            "captcha", "Access Denied", "Just a moment", "px-captcha", "datadome",
            "marketplace_search", "login"]
    return [k for k in keys if k in html]
