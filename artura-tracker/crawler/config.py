"""Central configuration for the Artura crawler.

Everything the user is likely to tune lives here: the target car, the
price sanity floor, dealer domains, Facebook Marketplace hubs.
"""
from __future__ import annotations

import os

YEAR_MIN = 2020
YEAR_MAX = 2026

# Anything below this is almost certainly a salvage bid, a deposit, a
# wheel set, or a scam. It is kept in the raw feed but never counted as
# a candidate "cheapest car".
PRICE_FLOOR = 60_000
PRICE_CEILING = 400_000

# Canadian listings are converted to USD for ranking; the CAD figure is kept as price_local.
CAD_TO_USD = float(os.environ.get("CAD_TO_USD", "0.73"))

# Search anchor. Radius is set to "nationwide" on every source that
# supports it; the zip only matters for sources that require one.
SEARCH_ZIP = os.environ.get("ARTURA_ZIP", "").strip() or "10001"

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
    ("McLaren Austin", "https://austin.mclaren.com"),
    ("McLaren Beverly Hills", "https://www.mclarenbeverlyhills.com"),
    ("McLaren Boston", "https://www.mclarenboston.com"),
    ("McLaren Charlotte", "https://www.charlottemclaren.com"),
    ("McLaren Chicago", "https://www.mclarenchicago.com"),
    ("McLaren Dallas", "https://www.mclarendallas.com"),
    ("McLaren Denver", "https://www.mclaren-denver.com"),
    ("McLaren Greenwich", "https://www.mclarengreenwich.com"),
    ("McLaren Houston", "https://www.mclarenhouston.com"),
    ("McLaren Long Island", "https://www.mclarenlongisland.com"),
    ("McLaren Miami", "https://miami.mclaren.com"),
    ("McLaren Newport Beach", "https://www.mclarennb.com"),
    ("McLaren Orlando", "https://www.mclarencf.com"),
    ("McLaren Palm Beach", "https://www.mclarenpalmbeach.com"),
    ("McLaren Philadelphia", "https://www.mclarenphl.com"),
    ("McLaren Rancho Mirage", "https://www.mclarenranchomirage.com"),
    ("McLaren San Diego", "https://sandiego.mclaren.com"),
    ("McLaren San Francisco", "https://www.mclarensanfrancisco.com"),
    ("McLaren Scottsdale", "https://www.mclarenscottsdale.com"),
    ("McLaren Seattle", "https://seattle.mclaren.com"),
    ("McLaren St. Louis", "https://stlouis.mclaren.com"),
    ("McLaren Tampa Bay", "https://www.mclarentampabay.com"),
    ("McLaren Washington DC", "https://washingtondc.mclaren.com"),
    ("McLaren Sterling", "https://sterling.mclaren.com"),
    ("McLaren North Jersey", "https://www.mclarennorthjersey.com"),
    ("McLaren Las Vegas", "https://lasvegas.mclaren.com"),
    ("McLaren Nashville", "https://nashville.mclaren.com"),
    ("McLaren Detroit", "https://detroit.mclaren.com"),
    ("McLaren Manhattan", "https://manhattan.mclaren.com"),
    ("McLaren Boston (retailer site)", "https://boston.mclaren.com"),
    ("McLaren Scottsdale (retailer site)", "https://scottsdale.mclaren.com"),
    ("McLaren North Jersey (retailer site)", "https://northjersey.mclaren.com"),
    ("McLaren Chicago (retailer site)", "https://chicago.mclaren.com"),
    ("McLaren Greenwich (retailer site)", "https://greenwich.mclaren.com"),
    ("McLaren Dallas (retailer site)", "https://dallas.mclaren.com"),
    ("McLaren Houston (retailer site)", "https://houston.mclaren.com"),
    ("McLaren Philadelphia (retailer site)", "https://philadelphia.mclaren.com"),
    ("McLaren Palm Beach (retailer site)", "https://palmbeach.mclaren.com"),
    ("McLaren Newport Beach (retailer site)", "https://newportbeach.mclaren.com"),
    ("McLaren Beverly Hills (retailer site)", "https://beverlyhills.mclaren.com"),
    ("McLaren San Francisco (retailer site)", "https://sanfrancisco.mclaren.com"),
    ("McLaren Long Island (retailer site)", "https://longisland.mclaren.com"),
    ("McLaren Orlando (retailer site)", "https://orlando.mclaren.com"),
    ("McLaren Tampa Bay (retailer site)", "https://tampabay.mclaren.com"),
    ("McLaren Denver (retailer site)", "https://denver.mclaren.com"),
    ("McLaren Charlotte (retailer site)", "https://charlotte.mclaren.com"),
    ("McLaren Rancho Mirage (retailer site)", "https://ranchomirage.mclaren.com"),
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
FB_HUBS_CA = ["toronto", "vancouver", "montreal", "calgary", "edmonton", "ottawa", "winnipeg", "quebec", "hamilton", "halifax", "victoria", "kelowna", "london"]
FB_MIN_PRICE = 40_000

DEALER_SITES_CA = [
    ("McLaren Toronto", "https://www.mclarentoronto.com"),
    ("McLaren Vancouver", "https://www.mclarenvancouver.com"),
    ("McLaren Montreal", "https://www.mclarenmontreal.com"),
    ("McLaren Calgary", "https://www.mclarencalgary.com"),
    ("McLaren Toronto (retailer site)", "https://toronto.mclaren.com"),
    ("McLaren Vancouver (retailer site)", "https://vancouver.mclaren.com"),
    ("McLaren Montreal (retailer site)", "https://montreal.mclaren.com"),
    ("Pfaff Reserve (Toronto)", "https://www.pfaffreserve.com"),
    ("Pfaff Autoworks (Toronto)", "https://www.pfaffautoworks.com"),
    ("Grand Touring Automobiles (Toronto)", "https://www.grandtouringautos.com"),
    ("Weissach (Vancouver)", "https://www.weissach.com"),
    ("Ferrari Quebec (Montreal)", "https://www.ferrariquebec.com"),
    ("Lamborghini Calgary", "https://www.lamborghinicalgary.com"),
]


LAMBORGHINI_DEALERS = [
    ("Lamborghini Beverly Hills", "https://www.lamborghinibeverlyhills.com"),
    ("Lamborghini Newport Beach", "https://www.lamborghininewportbeach.com"),
    ("Lamborghini Calabasas", "https://www.lamborghinicalabasas.com"),
    ("Lamborghini San Diego", "https://www.lamborghinisandiego.com"),
    ("Lamborghini San Francisco", "https://www.lamborghinisanfrancisco.com"),
    ("Lamborghini Los Gatos", "https://www.lamborghinilosgatos.com"),
    ("Lamborghini Houston", "https://www.lamborghinihouston.com"),
    ("Lamborghini Dallas", "https://www.lamborghinidallas.com"),
    ("Lamborghini Austin", "https://www.lamborghiniaustin.com"),
    ("Lamborghini Miami", "https://www.lamborghinimiami.com"),
    ("Lamborghini Palm Beach", "https://www.lamborghinipalmbeach.com"),
    ("Lamborghini Broward", "https://www.lamborghinibroward.com"),
    ("Lamborghini Orlando", "https://www.lamborghiniorlando.com"),
    ("Lamborghini Sarasota", "https://www.lamborghinisarasota.com"),
    ("Lamborghini Tampa Bay", "https://www.lamborghinitampabay.com"),
    ("Lamborghini Atlanta", "https://www.lamborghiniatlanta.com"),
    ("Lamborghini Charlotte", "https://www.lamborghinicharlotte.com"),
    ("Lamborghini Nashville", "https://www.lamborghininashville.com"),
    ("Lamborghini Chicago", "https://www.lamborghinichicago.com"),
    ("Lamborghini St. Louis", "https://www.lamborghinistlouis.com"),
    ("Lamborghini Denver", "https://www.lamborghinidenver.com"),
    ("Lamborghini Las Vegas", "https://www.lamborghinilasvegas.com"),
    ("Lamborghini Scottsdale", "https://www.lamborghiniscottsdale.com"),
    ("Lamborghini Bellevue", "https://www.lamborghinibellevue.com"),
    ("Lamborghini Boston", "https://www.lamborghiniboston.com"),
    ("Lamborghini Long Island", "https://www.lamborghinilongisland.com"),
    ("Lamborghini Paramus", "https://www.lamborghiniparamus.com"),
    ("Manhattan Motorcars (Lamborghini)", "https://www.manhattanmotorcars.com"),
    ("Lamborghini Palmyra NJ", "https://www.lamborghinipalmyranj.com"),
    ("Lamborghini Sterling", "https://www.lamborghinisterling.com"),
    ("Lamborghini Washington", "https://www.lamborghiniwashington.com"),
    ("Lamborghini Pittsburgh", "https://www.lamborghinipittsburgh.com"),
    ("Lamborghini Cleveland", "https://www.lamborghinicleveland.com"),
    ("Lamborghini Troy (Detroit)", "https://www.lamborghinitroy.com"),
    ("Lamborghini Kansas City", "https://www.lamborghinikansascity.com"),
    ("Lamborghini Minneapolis", "https://www.lamborghiniminneapolis.com"),
    ("Lamborghini Salt Lake City", "https://www.lamborghinisaltlakecity.com"),
    ("Lamborghini Portland", "https://www.lamborghiniportland.com"),
    ("Lamborghini Philadelphia", "https://www.lamborghiniphiladelphia.com"),
    ("Lamborghini Greenwich", "https://www.lamborghinigreenwich.com"),
    ("Lamborghini North Los Angeles", "https://www.lamborghininorthlosangeles.com"),
]
LAMBORGHINI_DEALERS_CA = [
    ("Lamborghini Uptown Toronto", "https://www.lamborghiniuptowntoronto.com"),
    ("Lamborghini Vancouver", "https://www.lamborghinivancouver.com"),
    ("Lamborghini Montreal", "https://www.lamborghinimontreal.com"),
    ("Lamborghini Calgary", "https://www.lamborghinicalgary.com"),
]

# ---------------------------------------------------------------------------
# Targets: every car we hunt. Each source builds its URLs from these fields.
# ---------------------------------------------------------------------------
TARGETS = {
    "artura": {
        "key": "artura", "make": "McLaren", "model": "Artura", "model_ascii": "Artura", "label": "McLaren Artura",
        "make_slug": "mclaren", "model_slug": "artura", "alias_re": r"artura",
        "vin_prefixes": ("SBM16",), "years": (2020, 2026), "price_floor": 60_000,
        "trims": [("Spider", r"\bspider\b"), ("GT4", r"\bgt4\b"), ("Performance", r"\bperformance\b"),
                  ("TechLux", r"\btech\s?lux\b"), ("Vision", r"\bvision\b")],
        "default_trim": "Coupe", "junk_re": r"GT4 Trophy",
        "cargurus_entity": "d3238", "carfax_path": "Used-Mclaren-Artura_w10502", "carfax_make": "Mclaren", "carfax_model": "Artura",
        "query": "mclaren artura", "dealers": DEALER_SITES, "dealers_ca": DEALER_SITES_CA,
    },
    "huracan": {
        "key": "huracan", "make": "Lamborghini", "model": "Huracán", "model_ascii": "Huracan", "label": "Lamborghini Huracán",
        "make_slug": "lamborghini", "model_slug": "huracan", "alias_re": r"hurac[aá]n",
        "vin_prefixes": ("ZHWU", "ZHWE", "ZHWH", "ZHWG", "ZHWR"), "years": (2020, 2026), "price_floor": 60_000,
        "trims": [("STO", r"\bsto\b"), ("Tecnica", r"\btecnica\b"), ("Sterrato", r"\bsterrato\b"),
                  ("Performante Spyder", r"performante\s+spyder"), ("Performante", r"\bperformante\b"),
                  ("EVO RWD Spyder", r"evo\s+rwd\s+spyder|rwd\s+spyder"), ("EVO Spyder", r"evo\s+spyder"),
                  ("EVO RWD", r"evo\s+rwd|\brwd\b"), ("EVO", r"\bevo\b"),
                  ("LP 610-4 Spyder", r"610-4\s+spyder"), ("LP 610-4", r"610-4|lp\s?610"), ("LP 580-2", r"580-2|lp\s?580"),
                  ("Spyder", r"\bspyder\b")],
        "default_trim": "Coupe", "junk_re": r"Super Trofeo|GT3",
        "cargurus_entity": "d2285", "carfax_path": "Used-Lamborghini-Huracan_w749", "carfax_make": "Lamborghini", "carfax_model": "Huracan",
        "query": "lamborghini huracan", "dealers": LAMBORGHINI_DEALERS, "dealers_ca": LAMBORGHINI_DEALERS_CA,
    },
}
DEFAULT_TARGETS = ["artura", "huracan"]
for _t in TARGETS.values():
    _t["query_plus"] = _t["query"].replace(" ", "+")
    _t["query_enc"] = _t["query"].replace(" ", "%20")
    _t["model_lower"] = _t["model_ascii"].lower()
