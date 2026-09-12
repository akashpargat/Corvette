"""One-off seed so the dashboard has real cars on day zero.

These nine cars were pulled from McLaren's official Qualified pre-owned
search on 2026-09-12 (prices and mileage as shown that day). The daily
crawler replaces them with VIN-keyed records on its first successful run.
"""
from crawler.models import Listing
from crawler.store import merge

SEED = [
    ("2023 McLaren Artura", 160699, 8755, "Paris Blue", "McLaren Greenwich", "Greenwich, CT", "https://preowned.mclaren.com/amn/us/en/vehicles/mclaren-artura-qualified-cnf6dn8"),
    ("2023 McLaren Artura", 174991, 10811, "White", "McLaren Scottsdale", "Scottsdale, AZ", "https://preowned.mclaren.com/amn/us/en/vehicles/mclaren-artura-qualified-jvf6xr7"),
    ("2023 McLaren Artura", 175490, 8325, "Onyx Black", "McLaren Dallas", "Dallas, TX", "https://preowned.mclaren.com/amn/us/en/vehicles/mclaren-artura-qualified-nhfutht"),
    ("2023 McLaren Artura", 184991, 5927, "Teal", "McLaren Scottsdale", "Scottsdale, AZ", "https://preowned.mclaren.com/amn/us/en/vehicles/mclaren-artura-qualified-fefz93d"),
    ("2023 McLaren Artura", 189999, 2650, "Silica White", "McLaren Newport Beach", "Newport Beach, CA", "https://preowned.mclaren.com/amn/us/en/vehicles/mclaren-artura-qualified-fefl8pm"),
    ("2023 McLaren Artura", 192384, 9274, "Vega Blue", "McLaren Florida", "Florida", "https://preowned.mclaren.com/amn/us/en/vehicles/mclaren-artura-qualified-hzfpj6w"),
    ("2023 McLaren Artura", 194990, 2769, "McLaren Orange", "McLaren Palm Beach", "West Palm Beach, FL", "https://preowned.mclaren.com/amn/us/en/vehicles/mclaren-artura-qualified-kcfz5m7"),
    ("2023 McLaren Artura", 199995, 1243, "Ice Silver", "McLaren Miami", "Coral Gables, FL", "https://preowned.mclaren.com/amn/us/en/vehicles/mclaren-artura-qualified-nhf2llr"),
]

if __name__ == "__main__":
    ls = [Listing(source="seed", source_name="Seed (McLaren Qualified, 2026-09-12)", url=u, title=t, price=p, mileage=m, color=c,
                  dealer=d, location=loc, condition="cpo", title_status="unknown").finalize() for t, p, m, c, d, loc, u in SEED]
    rep = {"started_at": "2026-09-12T23:30:00+00:00", "seconds": 0, "raw_listings": len(ls), "zip": "10001",
           "sources": [{"source": "seed", "label": "Seed (web search, day zero)", "kind": "seed", "status": "ok", "count": len(ls), "seconds": 0, "pages": 0, "notes": ["Hand-seeded from McLaren Qualified search results; replaced by the first crawl."], "error": None}]}
    pay = merge("data", ls, rep)
    print(pay["summary"])
