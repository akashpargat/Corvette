from crawler.extract import find_jsonld, vehicles_from_jsonld, find_script_json, parse_json_prefix
from crawler.sources.base import listings_from_jsonld, listings_from_vin_cards

HTML = '''<html><head>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Car","name":"2023 McLaren Artura Performance",
"vehicleIdentificationNumber":"SBM16AEA5PW000777","mileageFromOdometer":{"@type":"QuantitativeValue","value":"4,120","unitCode":"SMI"},
"vehicleModelDate":"2023","color":"Vega Blue","offers":{"@type":"Offer","price":"179995","priceCurrency":"USD","url":"https://dealer.example/vdp/777","itemCondition":"https://schema.org/UsedCondition"}}</script>
<script>window.__BONNET_DATA__={"inventory":{"1":{"vin":"SBM16AEA5PW000888","model":"Artura","year":2024,"pricingDetail":{"salePrice":199000}}}};</script>
</head><body><div class="card">2024 McLaren Artura Spider $205,900 1,200 mi. VIN: SBM16AEA5PW000999 <a href="/used/999">view</a></div></body></html>'''


def test_jsonld_vehicle():
    v = vehicles_from_jsonld(find_jsonld(HTML))
    assert v and v[0]["vin"] == "SBM16AEA5PW000777" and v[0]["price"] == 179995 and v[0]["mileage"] == 4120
    ls = listings_from_jsonld(HTML, "t", "T", "https://dealer.example/")
    assert ls[0].url == "https://dealer.example/vdp/777" and ls[0].condition == "used" and ls[0].trim == "Performance"


def test_script_json_and_vin_cards():
    data = find_script_json(HTML, "window.__BONNET_DATA__")
    assert data["inventory"]["1"]["vin"] == "SBM16AEA5PW000888"
    cards = listings_from_vin_cards(HTML, "t", "T", "https://dealer.example/")
    vins = {c.vin for c in cards}
    assert "SBM16AEA5PW000999" in vins
    c = next(x for x in cards if x.vin == "SBM16AEA5PW000999")
    assert c.price == 205900 and c.mileage == 1200 and c.trim == "Spider" and c.url.endswith("/used/999")
