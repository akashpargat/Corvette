"""Central configuration for the Artura crawler.

Everything the user is likely to tune lives here: the target car, the
price sanity floor, dealer domains, Facebook Marketplace hubs.
"""
from __future__ import annotations

import os

MAKE = "McLaren"
MODEL = "Artura"
YEAR_MIN = 2020
YEAR_MAX = 2026

# Anything below this is almost certainly a salvage bid, a deposit, a
# wheel set, or a scam. It is kept in the raw feed but never counted as
# a candidate "cheapest car".
PRICE_FLOOR = 60_000
PRICE_CEILING = 400_000

# Search anchor. Radius is set to "nationwide" on every source that
# supports it; the zip only matters for sources that require one.
SEARCH_ZIP = os.environ.get("ARTURA_ZIP", "10001")

# Optional HTTP(S) proxy for sources that block datacenter IPs
# (format: http://user:pass@host:port). Empty = direct.
PROXY_URL = os.environ.get("SCRAPER_PROXY_URL", "").strip()

REQUEST_TIMEOUT = 30
POLITE_DELAY_SECONDS = 1.2
MAX_DETAIL_PAGES_PER_SOURCE = 60

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
]

# Official McLaren retailers in the United States. The dealer crawler also
# discovers retailers from the McLaren retailer locator at run time; this
# list is the fallback and the seed. Domains are best-effort and are
# verified on each run (a dead domain just reports as "unreachable").
DEALER_SITES = [
    ("McLaren Atlanta", "https://atlanta.mclaren.com"),
    ("McLaren Austin", "https://www.mclarenaustin.com"),
    ("McLaren Beverly Hills", "https://www.mclarenbeverlyhills.com"),
    ("McLaren Boston", "https://www.mclarenboston.com"),
    ("McLaren Charlotte", "https://www.mclarencharlotte.com"),
    ("McLaren Chicago", "https://www.mclarenchicago.com"),
    ("McLaren Dallas", "https://www.mclarendallas.com"),
    ("McLaren Denver", "https://www.mclarendenver.com"),
    ("McLaren Greenwich", "https://www.mclarengreenwich.com"),
    ("McLaren Houston", "https://www.mclarenhouston.com"),
    ("McLaren Long Island", "https://www.mclarenlongisland.com"),
    ("McLaren Miami", "https://www.mclarenmiami.com"),
    ("McLaren Newport Beach", "https://www.mclarennb.com"),
    ("McLaren Orlando", "https://www.mclarencf.com"),
    ("McLaren Palm Beach", "https://www.mclarenpalmbeach.com"),
    ("McLaren Philadelphia", "https://www.mclarenphl.com"),
    ("McLaren Rancho Mirage", "https://www.mclarenranchomirage.com"),
    ("McLaren San Diego", "https://www.mclarensandiego.com"),
    ("McLaren San Francisco", "https://www.mclarensanfrancisco.com"),
    ("McLaren Scottsdale", "https://www.mclarenscottsdale.com"),
    ("McLaren Seattle", "https://www.mclarenseattle.com"),
    ("McLaren St. Louis", "https://www.mclarenstlouis.com"),
    ("McLaren Tampa Bay", "https://www.mclarentampabay.com"),
    ("McLaren Washington DC", "https://www.mclarenwashingtondc.com"),
    ("McLaren North Jersey", "https://www.mclarennorthjersey.com"),
    ("McLaren Las Vegas", "https://www.mclarenlasvegas.com"),
    ("McLaren Nashville", "https://www.mclarennashville.com"),
    ("McLaren Detroit", "https://www.mclarendetroit.com"),
    ("McLaren Manhattan", "https://www.mclarenmanhattan.com"),
    ("McLaren Sterling", "https://www.mclarensterling.com"),
]

# Facebook Marketplace "hub" cities. FB searches a radius around each hub;
# these hubs blanket every metro where an Artura is plausibly listed.
FB_HUBS = [
    "nyc", "la", "chicago", "houston", "phoenix", "philadelphia", "sanantonio",
    "sandiego", "dallas", "sanjose", "austin", "jacksonville", "fortworth",
    "columbus", "charlotte", "sanfrancisco", "indianapolis", "seattle", "denver",
    "washington", "boston", "nashville", "detroit", "portland", "memphis",
    "lasvegas", "louisville", "baltimore", "milwaukee", "albuquerque", "tucson",
    "sacramento", "kansascity", "atlanta", "omaha", "raleigh", "miami",
    "minneapolis", "tulsa", "cleveland", "neworleans", "tampa", "orlando",
    "pittsburgh", "cincinnati", "stlouis", "saltlakecity", "honolulu",
    "richmond", "hartford", "buffalo", "oklahomacity", "birmingham",
    "sanjuan", "boise", "charleston", "westpalmbeach", "fortlauderdale",
    "scottsdale", "palmsprings", "newportbeach", "greenwich",
]
FB_MIN_PRICE = 40_000
