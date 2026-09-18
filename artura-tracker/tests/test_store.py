import json
import os

from crawler.models import Listing
from crawler.store import merge


def _l(vin, price, source="cars_com", **kw):
    return Listing(source=source, source_name=source, url=f"https://{source}/{vin}", title="2023 McLaren Artura",
                   vin=vin, price=price, mileage=5000, year=2023, location="Dallas, TX", **kw).finalize()


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
    # missing three runs in a row -> removed
    merge(d, [_l("SBM16AEA5PW000001", 172000)], _report())
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


def test_brief_builds_from_merged_data(tmp_path):
    from crawler.brief import build
    d = str(tmp_path)
    merge(d, [_l("SBM16AEA5PW000001", 180000), _l("SBM16AEA5PW000002", 170000)], _report())
    subject, body = build(d)
    assert "Supercar Hunt" in subject and "TOP 10 CHEAPEST" in body
    assert "$170,000" in body and body.index("$170,000") < body.index("$180,000")
    assert "NEW" in body and "1 ok" in body


def test_vinless_card_joins_vin_group_by_url_and_outlier_price_ignored(tmp_path):
    d = str(tmp_path)
    vin = _l("SBM16AEA5PW000777", 315000, source="autotrader")
    vin.url = "https://www.autotrader.com/cars-for-sale/vehicle/1?x=1"
    card = Listing(source="autotempest", source_name="AutoTempest", url="https://www.autotrader.com/cars-for-sale/vehicle/1?aff=atempest",
                   title="2026 McLaren Artura", price=161498).finalize()
    p = merge(d, [vin, card], _report(("autotrader", "autotempest")))
    assert len([r for r in p["listings"] if r["status"] == "active"]) == 1
    car = p["listings"][0]
    assert car["key"] == "SBM16AEA5PW000777" and car["price"] == 315000 and len(car["offers"]) == 2


def test_vinless_card_joins_by_mileage_and_price_fingerprint(tmp_path):
    d = str(tmp_path)
    vin = _l("SBM16AEA0PW000718", 155985, source="carfax")
    vin.mileage = 14948
    card = Listing(source="cars_com", source_name="Cars.com", url="https://www.cars.com/vehicledetail/abc/",
                   title="2023 McLaren Artura", price=155985, mileage=14948, year=2023).finalize()
    other = Listing(source="cars_com", source_name="Cars.com", url="https://www.cars.com/vehicledetail/def/",
                    title="2023 McLaren Artura", price=189000, mileage=2100, year=2023).finalize()
    p = merge(d, [vin, card, other], _report(("carfax", "cars_com")))
    active = [r for r in p["listings"] if r["status"] == "active"]
    assert len(active) == 2
    joined = next(r for r in active if r["key"] == "SBM16AEA0PW000718")
    assert sorted(joined["sources"]) == ["carfax", "cars_com"]


def test_aggregator_offer_never_sets_price_when_a_real_source_exists(tmp_path):
    d = str(tmp_path)
    a = _l("SBM16AEA5PW000555", 249900, source="autotrader")
    b = Listing(source="autotempest", source_name="AutoTempest", url="https://www.autotrader.com/cars-for-sale/vehicle/x",
                title="2025 McLaren Artura Spider", price=155985, year=2025, mileage=5000).finalize()
    a.url = "https://www.autotrader.com/cars-for-sale/vehicle/x"
    p = merge(d, [a, b], _report(("autotrader", "autotempest")))
    car = next(r for r in p["listings"] if r["key"] == "SBM16AEA5PW000555")
    assert car["price"] == 249900 and len(car["offers"]) == 2


def test_url_keyed_row_that_learned_its_vin_folds_into_the_vin_row(tmp_path):
    d = str(tmp_path)
    vin = "SBM16AEAXPW001732"
    # yesterday's state: the same car twice, once under its VIN and once under a Cars.com URL hash that carries the VIN
    prev = {"listings": [
        {"key": vin, "vin": vin, "source": "autotrader", "url": "https://www.autotrader.com/cars-for-sale/vehicle/1", "price": 164158,
         "mileage": 12670, "year": 2023, "target": "artura", "country": "US", "status": "active", "first_seen": "2026-09-14", "last_seen": "2026-09-17",
         "sources": ["autotrader"], "offers": [{"source": "autotrader", "url": "https://www.autotrader.com/cars-for-sale/vehicle/1", "price": 164158, "seen": "2026-09-17"}],
         "title_status": "clean", "title_notes": ["CARFAX clean"]},
        {"key": "cars_com:c3e098108f0a", "vin": vin, "source": "cars_com", "url": "https://www.cars.com/vehicledetail/abc/", "price": 164383,
         "mileage": 12670, "year": 2023, "target": "artura", "country": "US", "status": "active", "first_seen": "2026-09-13", "last_seen": "2026-09-17",
         "sources": ["cars_com"], "offers": [{"source": "cars_com", "url": "https://www.cars.com/vehicledetail/abc/", "price": 164383, "seen": "2026-09-17"}],
         "title_status": "unknown"},
    ]}
    os.makedirs(d, exist_ok=True)
    json.dump(prev, open(os.path.join(d, "listings.json"), "w"))
    json.dump({vin: [{"d": "2026-09-14", "p": 164733}, {"d": "2026-09-17", "p": 164158}],
               "cars_com:c3e098108f0a": [{"d": "2026-09-13", "p": 165183}]}, open(os.path.join(d, "history.json"), "w"))
    fresh_vin = _l(vin, 164158, source="autotrader")
    fresh_vin.url = "https://www.autotrader.com/cars-for-sale/vehicle/1"
    card = Listing(source="cars_com", source_name="Cars.com", url="https://www.cars.com/vehicledetail/abc/", title="Used 2023 McLaren Artura",
                   price=164383, mileage=12670, year=2023).finalize()
    p = merge(d, [fresh_vin, card], _report(("autotrader", "cars_com")))
    active = [r for r in p["listings"] if r["status"] == "active"]
    assert [r["key"] for r in active] == [vin]
    car = active[0]
    assert car["price"] == 164158 and car["first_seen"] == "2026-09-13" and car["title_status"] == "clean"
    assert set(car["sources"]) == {"autotrader", "cars_com"}
    hist = json.load(open(os.path.join(d, "history.json")))
    assert "cars_com:c3e098108f0a" not in hist and hist[vin][0] == {"d": "2026-09-13", "p": 165183}
    assert car["key"] not in p["changes"]["new"]


def test_group_joined_by_yesterdays_url_keeps_the_vin_key(tmp_path):
    d = str(tmp_path)
    vin = "SBM16AEA3PW001443"
    a = _l(vin, 179900, source="autotrader")
    a.url = "https://www.autotrader.com/cars-for-sale/vehicle/2"
    card = Listing(source="cars_com", source_name="Cars.com", url="https://www.cars.com/vehicledetail/xyz/", title="Used 2023 McLaren Artura",
                   price=179985, mileage=5000, year=2023).finalize()
    merge(d, [a, card], _report(("autotrader", "cars_com")))
    # next day only the VIN-less Cars.com card shows up; it joins the VIN row by URL and must stay keyed by the VIN
    card2 = Listing(source="cars_com", source_name="Cars.com", url="https://www.cars.com/vehicledetail/xyz/", title="Used 2023 McLaren Artura",
                    price=179985, mileage=5000, year=2023).finalize()
    p = merge(d, [card2], _report(("autotrader", "cars_com")))
    active = [r for r in p["listings"] if r["status"] == "active"]
    assert [r["key"] for r in active] == [vin] and active[0]["vin"] == vin
    assert vin in p["changes"]["price_up"] and vin not in p["changes"]["new"]
    # and the day after, still one row
    p = merge(d, [card2], _report(("autotrader", "cars_com")))
    assert [r["key"] for r in p["listings"] if r["status"] == "active"] == [vin]
