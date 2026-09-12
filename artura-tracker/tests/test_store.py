import json
import os

from crawler.models import Listing
from crawler.store import merge


def _l(vin, price, source="cars_com", **kw):
    return Listing(source=source, source_name=source, url=f"https://{source}/{vin}", title="2023 McLaren Artura",
                   vin=vin, price=price, mileage=5000, location="Dallas, TX", **kw).finalize()


def _report(ok=("cars_com",)):
    return {"started_at": "t", "seconds": 1, "sources": [{"source": s, "status": "ok", "count": 1} for s in ok]}


def test_merge_new_then_drop_then_removed(tmp_path):
    d = str(tmp_path)
    p = merge(d, [_l("SBM16AEA5PW000001", 180000), _l("SBM16AEA5PW000002", 170000)], _report())
    assert p["summary"]["active"] == 2 and set(p["changes"]["new"]) == {"SBM16AEA5PW000001", "SBM16AEA5PW000002"}
    assert p["summary"]["cheapest_clean_price"] == 170000
    # same VIN from two sites, one cheaper -> price is the min, both offers kept
    p = merge(d, [_l("SBM16AEA5PW000001", 175000), _l("SBM16AEA5PW000001", 172000, source="carfax")], _report(("cars_com", "carfax")))
    car = next(r for r in p["listings"] if r["key"] == "SBM16AEA5PW000001")
    assert car["price"] == 172000 and len(car["offers"]) == 2 and car["last_price_change"]["delta"] == -8000
    assert "SBM16AEA5PW000001" in p["changes"]["price_drop"]
    # 000002 missing once: still active
    car2 = next(r for r in p["listings"] if r["key"] == "SBM16AEA5PW000002")
    assert car2["status"] == "active" and car2["missing_runs"] == 1
    # missing twice -> removed
    p = merge(d, [_l("SBM16AEA5PW000001", 172000)], _report())
    car2 = next(r for r in p["listings"] if r["key"] == "SBM16AEA5PW000002")
    assert car2["status"] == "removed"
    # files exist
    for n in ("listings.json", "history.json", "runs.json", "market.json"):
        assert os.path.exists(os.path.join(d, n))
    hist = json.load(open(os.path.join(d, "history.json")))
    assert [h["p"] for h in hist["SBM16AEA5PW000001"]] == [180000, 172000, 172000] or hist["SBM16AEA5PW000001"][-1]["p"] == 172000


def test_source_failure_does_not_remove_cars(tmp_path):
    d = str(tmp_path)
    merge(d, [_l("SBM16AEA5PW000009", 165000)], _report())
    # cars_com failed today; car not seen -> must not count as missing
    p = merge(d, [], {"started_at": "t", "seconds": 1, "sources": [{"source": "cars_com", "status": "blocked", "count": 0}]})
    car = next(r for r in p["listings"] if r["key"] == "SBM16AEA5PW000009")
    assert car["status"] == "active" and car.get("missing_runs", 0) == 0
