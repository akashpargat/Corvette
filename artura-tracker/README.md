# Artura Hunt

A daily, nationwide search for the cheapest **clean-title McLaren Artura (2020–2026) in the United States**, with a
dashboard that shows what is new, what dropped in price, and what sold.

```
artura-tracker/
├── crawler/            Python crawler (17 sources) → data/*.json
│   ├── sources/        one module per site; each returns normalised Listing objects
│   ├── models.py       Listing + price/mileage/VIN/title-status parsing
│   ├── extract.py      JSON-LD, embedded-JSON and VIN-anchored fallbacks
│   ├── store.py        merge by VIN, price history, new/drop/removed diffing
│   └── scoring.py      market model (price ~ miles + year) and deal ranking
├── dashboard/          static dashboard (no build step, no framework)
├── data/               listings.json · history.json · runs.json · market.json (committed daily)
├── build_site.py       inlines data into a single self-contained site/index.html
└── tests/              unit tests for parsing and diffing
.github/workflows/artura-daily.yml   runs every morning, commits data, publishes GitHub Pages
```

## Status after the first day (verified 2026-09-13, GitHub-hosted runner, no proxy)

| Source | Result | Notes |
|---|---|---|
| McLaren Qualified CPO | ok · 12 cars | official certified pre-owned |
| McLaren dealer sites | ok · ~90 cars from 12 sites | Boston, Chicago, Denver, Philadelphia, Tampa Bay, North Jersey, Long Island, Beverly Hills, Dallas, Houston, Rancho Mirage, Newport Beach. Scottsdale, Greenwich, San Francisco, Charlotte block datacenter IPs; several retailers have no own site |
| Autotrader / KBB | ok · ~158 cars each | needs the headed browser (Akamai) |
| CarGurus | ok · ~25 cars | HTML via browser |
| CARFAX | ok · ~24 cars | HTML via browser |
| duPont REGISTRY | ok · ~16 cars | rendered in browser |
| Bring a Trailer | ok · 14 live/sold | sold results kept as price references only |
| Cars & Bids | ok · 1 | |
| Cars.com | intermittent | Cloudflare challenge passes some runs, not others |
| TrueCar | blocked | PerimeterX press-and-hold; needs `SCRAPER_PROXY_URL` (residential) |
| Edmunds, Autolist, eBay, CLASSIC.COM | blocked | IP-range blocks; need `SCRAPER_PROXY_URL` |
| Hemmings | empty | no Artura listings found |
| Facebook Marketplace | login wall | add `FB_COOKIES_JSON` (see below) |

Every VIN is de-duplicated across sources, so the ~220 active rows are unique cars, most seen on 2-4 sites.

## One-time setup (5 minutes)

1. **GitHub Pages** – repo Settings → Pages → *Source: GitHub Actions*. The workflow's deploy job then publishes
   `https://akashpargat.github.io/Corvette/` on every run. Until then the dashboard is the Claude artifact the
   daily Routine republishes.
2. **Daily schedule** – GitHub only runs `schedule:` workflows from the default branch, so merge this branch into
   `master` to get the built-in 06:00 Central cron. Until it is merged, the Claude Routine "Artura Hunt daily
   crawl + brief" kicks the crawl every morning by touching `artura-tracker/TRIGGER`.
3. **Facebook Marketplace** – secret `FB_COOKIES_JSON` (instructions below).
4. **Blocked marketplaces** – optional secret `SCRAPER_PROXY_URL` with a residential proxy unlocks TrueCar,
   Edmunds, Autolist, eBay and CLASSIC.COM.

## Sources

| Kind | Source | How |
|---|---|---|
| Official | McLaren Qualified pre-owned (preowned.mclaren.com) | listing pages → JSON-LD / text |
| Dealers | Every US McLaren retailer website (30 seeded + discovered from the retailer locator) | sitemap → VDP pages → JSON-LD / VIN cards |
| Marketplaces | Cars.com, Autotrader, KBB, CarGurus, CARFAX, TrueCar, Edmunds, Autolist, duPont REGISTRY, Hemmings, eBay Motors | site JSON endpoints, embedded state, or rendered cards |
| Aggregator | CLASSIC.COM | rendered cards |
| Auctions | Bring a Trailer, Cars & Bids | embedded auction JSON |
| Private | Facebook Marketplace, 60+ metro hubs | headless Chromium (Playwright) |

Every source is isolated: one failing or blocked site never stops the run, and the dashboard's **Source health**
panel shows exactly which sources returned cars, which were empty, and which were blocked (with the reason).

### Facebook Marketplace

Facebook has no Marketplace API and puts a login wall in front of anonymous datacenter traffic. The crawler tries
anonymously and reports "login wall" honestly. To unlock it, export your own Facebook cookies once (a browser
extension such as *Cookie-Editor* → Export → JSON while logged in on facebook.com) and save them as the repository
secret **`FB_COOKIES_JSON`**. The crawler injects them into the headless browser; no password is ever stored.

### Blocked sources

Some sites (Autotrader/KBB, Edmunds, Cars & Bids) use bot walls that sometimes reject GitHub's IP ranges. Two levers:

* **`SCRAPER_PROXY_URL`** secret – any residential HTTP proxy (`http://user:pass@host:port`); both `requests` and
  Playwright will use it.
* **`ARTURA_ZIP`** repository variable – the search anchor zip (default 10001); radius is always nationwide.

## Running it

```bash
cd artura-tracker
pip install -r requirements.txt && python -m playwright install chromium
python -m crawler.main                       # all sources (~5–10 min)
python -m crawler.main --sources cars_com,carfax -v
python -m crawler.main --skip fb_marketplace
python build_site.py && open site/index.html
python -m pytest tests
```

GitHub Actions runs the same thing every day at 06:00 Central (`cron: 0 11 * * *`), commits `data/`, and publishes
`site/` to GitHub Pages. Trigger a run any time from the **Actions → Artura Tracker → Run workflow** button.

## How "cheapest clean" is decided

1. **Candidate**: price between $60k and $400k, model year 2020–2026, not a sold-auction reference.
2. **Title**: `branded` if any source or the listing text mentions salvage/rebuilt/flood/lemon/etc.;
   `clean` when CARFAX, CarGurus or Edmunds history flags say no accidents/no salvage or the seller states it;
   otherwise `unknown` (shown as *unverified*). Branded cars are hidden by default.
3. **Dedup by VIN** across all sources; the shown price is the lowest current asking price, all offers are kept.
4. **Deal %** is distance below a least-squares market model (price vs miles and year) fitted on that day's clean pool.
5. **Removed** only after a car is missing from two consecutive runs *and* its sources actually succeeded that day.

## Data shape (`data/listings.json`)

```json
{"summary": {"date": "2026-09-12", "active": 42, "cheapest_clean_price": 160699, "...": "..."},
 "changes":  {"new": ["VIN"], "price_drop": [], "price_up": [], "removed": [], "returned": []},
 "listings": [{"key": "SBM16AEA5PW00xxxx", "year": 2023, "trim": "Coupe", "price": 160699, "mileage": 8755,
               "title_status": "unknown", "dealer": "McLaren Greenwich", "location": "Greenwich, CT", "state": "CT",
               "sources": ["mclaren_preowned", "cars_com"], "offers": [{"source": "cars_com", "url": "...", "price": 160699}],
               "price_history": [{"d": "2026-09-12", "p": 160699}], "first_seen": "2026-09-12", "status": "active",
               "deal_pct": 6.2, "rank_cheapest_clean": 1}]}
```
