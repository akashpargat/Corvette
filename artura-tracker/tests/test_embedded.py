from crawler.extract import vin_dicts_from_html, vehicle_from_vin_dict
from crawler.sources.base import parse_any

DDC = '''<html><script type="application/ld+json">{"@type":["Product","Car"],"name":"Certified Pre-Owned 2025 McLaren Artura Performance","offers":{"@type":"Offer","price":"1489","url":"https://d.example/certified/x.htm"}}</script>
<script>window.DDC = window.DDC || {}; DDC.dataLayer = {"page":{"pageType":"vdp"},"vehicles":[{"vin":"SBM16BEA4SW003068","year":2025,"make":"McLaren","model":"Artura","trim":"Performance","internetPrice":244900,"msrp":289000,"odometer":1200,"exteriorColor":"Onyx Black","status":"certified","link":"/certified/McLaren/2025-McLaren-Artura-938e.htm","payment":{"monthly":1489}}]};</script></html>'''
DLRON = '''<script id='dlron-srp-model' type="application/json">{"Vehicles":[{"Vin":"SBM16BEA1TW004129","Year":2026,"Make":"McLaren","Model":"Artura","Trim":"Base","Price":259585,"Mileage":12,"ExteriorColor":"Ember","VdpUrl":"/new-Pinellas+Park-2026-McLaren-Artura-+-SBM16BEA1TW004129","MonthlyPayment":3300}]}</script>'''
CFX = '''<script>window.__PRELOADED_STATE__={"listings":[{"vin":"SBM16AEA0PW000718","year":2023,"listPrice":156635,"mileage":14948,"noAccidents":true,"oneOwner":false,"dealer":{"name":"Da Vinci Automotive","city":"Bronx","state":"NY"},"vdpUrl":"https://www.carfax.com/vehicle/SBM16AEA0PW000718","salvageTitle":false}]};</script>'''


def test_ddc_datalayer_beats_monthly_payment_jsonld():
    ls = parse_any(DDC, "t", "T", "https://d.example/", dealer="McLaren Denver")
    assert len(ls) == 1
    l = ls[0]
    assert l.vin == "SBM16BEA4SW003068" and l.price == 244900 and l.mileage == 1200 and l.year == 2025
    assert l.trim == "Performance" and l.condition == "cpo" and l.color == "Onyx Black"
    assert l.url.endswith("938e.htm")


def test_dealeron_srp_model():
    ls = parse_any(DLRON, "t", "T", "https://www.mclarentampabay.com/")
    assert ls[0].price == 259585 and ls[0].mileage == 12 and ls[0].year == 2026 and ls[0].condition in ("new", "unknown")
    assert ls[0].url.startswith("https://www.mclarentampabay.com/new-")


def test_carfax_preloaded_state_title_flags():
    ls = parse_any(CFX, "carfax", "CARFAX", "https://www.carfax.com/Used-Mclaren-Artura_w10502")
    l = ls[0]
    assert l.price == 156635 and l.title_status == "clean" and l.dealer == "Da Vinci Automotive" and l.state == "NY"


def test_location_keys_do_not_match_battery_capacity():
    html = '<script>var x={"vin":"SBM16AEA2PW001840","price":164795,"batteryCapacity":"7.4 kWh","sellerRegion":"IL","sellerCity":"Naperville","accidentHistory":{"text":"No accidents or damage reported to CARFAX"}};</script>'
    l = parse_any(html, "t", "T", "https://x/artura")[0]
    assert l.location == "Naperville, IL" and l.state == "IL" and l.title_status == "clean"


def test_location_from_description():
    from crawler.models import Listing
    l = Listing(source="t", source_name="T", url="u", title="Used 2023 McLaren Artura", extra={"description": "Location: Indianapolis, IN. This 2023 McLaren Artura is listed for $174550"}).finalize()
    assert l.location == "Indianapolis, IN" and l.state == "IN"


def test_cards_from_links_and_cad_conversion():
    from crawler.sources.base import cards_from_links
    html = '''<ul><li><a href="/a/mclaren/artura/toronto/on/5_12345"><h2>2023 McLaren Artura Performance</h2></a>
    <span>CA$239,900</span><span>8,200 km</span><span>Toronto, ON</span></li>
    <li><a href="/a/mclaren/720s/x/1"><h2>2020 McLaren 720S</h2></a><span>CA$300,000</span></li></ul>'''
    ls = cards_from_links(html, "https://www.autotrader.ca/", r"/a/mclaren/artura/", "t", "T", country="CA", currency="CAD")
    assert len(ls) == 1
    l = ls[0]
    assert l.price_local == 239900 and l.price == round(239900 * 0.73) and l.mileage == round(8200 * 0.621371)
    assert l.year == 2023 and l.trim == "Performance" and l.url.startswith("https://www.autotrader.ca/a/")


def test_canada_search_returning_a_us_card_stays_usd():
    from crawler.sources.base import cards_from_links
    html = '''<div><a href="/cars/lamborghini/huracan/2017-lamborghini-huracan-rwd-for-sale-1"><h2>2017 Lamborghini Huracan RWD</h2></a>
    <span>$179,990</span><span>West hollywood, CA, United States</span></div>'''
    from crawler.models import set_target
    set_target("huracan")
    try:
        l = cards_from_links(html, "https://www.jamesedition.com/", r"/cars/lamborghini/huracan/", "t", "T", country="CA", currency="CAD")[0]
    finally:
        set_target("artura")
    assert l.country == "US" and l.currency == "USD" and l.price == 179990 and l.price_local is None
