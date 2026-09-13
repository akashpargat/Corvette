"""Central configuration for the Artura crawler.

Everything the user is likely to tune lives here: the target car, the
price sanity floor, dealer domains, Facebook Marketplace hubs.
"""
from __future__ import annotations

import os
import re

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
# Targets: every car we hunt, loaded from artura-tracker/targets.json.
# Add a car = add one JSON entry (or run: python -m crawler.targets add "Ferrari" "296 GTB").
# ---------------------------------------------------------------------------
DEALER_NETWORKS = {
    "mclaren": {"us": DEALER_SITES, "ca": DEALER_SITES_CA},
    "lamborghini": {"us": LAMBORGHINI_DEALERS, "ca": LAMBORGHINI_DEALERS_CA},
}
TARGETS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "targets.json")


def _slug(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load_targets(path: str = TARGETS_FILE) -> dict:
    import json
    raw = json.load(open(path, encoding="utf-8"))
    targets = {}
    for key, t in raw.items():
        if t.get("enabled", True) is False:
            continue
        make, model = t["make"], t["model"]
        import unicodedata
        model_ascii = t.get("model_ascii") or unicodedata.normalize("NFKD", model).encode("ascii", "ignore").decode()
        net = DEALER_NETWORKS.get(t.get("dealer_network", "").lower(), {"us": [], "ca": []})
        entry = {
            "key": key, "make": make, "model": model, "model_ascii": model_ascii, "label": f"{make} {model}",
            "make_slug": _slug(make), "model_slug": _slug(model_ascii),
            "alias_re": t.get("alias_re") or re.escape(model_ascii.lower()).replace("\\ ", r"\s*"),
            "vin_prefixes": tuple(t.get("vin_prefixes") or ()), "years": tuple(t.get("years") or (YEAR_MIN, YEAR_MAX)),
            "price_floor": t.get("price_floor", PRICE_FLOOR), "price_ceiling": t.get("price_ceiling", PRICE_CEILING),
            "trims": [(n, rx) for n, rx in t.get("trims", [])], "default_trim": t.get("default_trim", "Coupe"),
            "junk_re": t.get("junk_re") or "", "exclude_re": t.get("exclude_re") or "", "exclude_trims": set(t.get("exclude_trims") or []), "cargurus_entity": t.get("cargurus_entity") or "",
            "carfax_path": t.get("carfax_path") or f"Used-{make}-{model_ascii.replace(' ', '-')}",
            "carfax_make": t.get("carfax_make") or make, "carfax_model": t.get("carfax_model") or model_ascii,
            "query": f"{make} {model_ascii}".lower(), "dealers": net["us"], "dealers_ca": net["ca"],
        }
        entry["query_plus"] = entry["query"].replace(" ", "+")
        entry["query_enc"] = entry["query"].replace(" ", "%20")
        entry["model_lower"] = model_ascii.lower()
        targets[key] = entry
    return targets


TARGETS = load_targets()
DEFAULT_TARGETS = list(TARGETS.keys())
