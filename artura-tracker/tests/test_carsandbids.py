import json
import os

from crawler.models import set_target
from crawler.sources.carsandbids import parse_cards
from crawler.store import record_sales

PAGE = """<html><body><ul class="auctions-list">
<li class="auction-item"><a href="/auctions/rjY7lpQx/2018-mclaren-artura-spider?ss_id=abc"><img src="a.jpg"></a>
  <div class="badge">FEATURED</div><div class="price">Sold for $109,000</div>
  <a href="/auctions/rjY7lpQx/2018-mclaren-artura-spider">2018 McLaren Artura Spider</a>
  <p>671-hp Hybrid V6, Technology Pack, Vega Blue</p>
  <span>Ended 9/18/26</span><span>~8,300 Miles</span><span>Fort Lauderdale, FL</span><button>Watch</button></li>
<li class="auction-item"><a href="/auctions/3gj8Wgj1/2016-mclaren-artura-coupe"><img src="b.jpg"></a>
  <div class="price">Sold After for $95,500</div><a href="/auctions/3gj8Wgj1/2016-mclaren-artura-coupe">2016 McLaren Artura Coupe</a>
  <span>Ended Sep 12, 2026</span><span>21k Miles, 570-hp V8, RWD</span></li>
<li class="auction-item"><a href="/auctions/9zzLive1/2019-mclaren-artura-spider"><img src="c.jpg"></a>
  <div class="price">Bid: $85,000</div><span>Ends in 2 days</span><span>14 bids</span>
  <a href="/auctions/9zzLive1/2019-mclaren-artura-spider">2019 McLaren Artura Spider</a><span>5,900 Miles</span></li>
</ul></body></html>"""

from crawler import config
T = config.TARGETS["artura"]


def test_cards_are_read_one_per_auction_with_status():
    set_target("artura")
    ls = parse_cards(PAGE, "https://carsandbids.com", T)
    assert [l.url for l in ls] == ["https://carsandbids.com/auctions/rjY7lpQx/2018-mclaren-artura-spider",
                                   "https://carsandbids.com/auctions/3gj8Wgj1/2016-mclaren-artura-coupe",
                                   "https://carsandbids.com/auctions/9zzLive1/2019-mclaren-artura-spider"]
    a, b, c = ls
    assert (a.title, a.year, a.price, a.mileage, a.listing_type, a.location) == ("2018 McLaren Artura Spider", 2018, 109000, 8300, "sold", None)
    assert a.extra["sold"] is True and a.extra["ended"] == "2026-09-18"
    assert (b.price, b.listing_type, b.extra["sold"], b.extra["ended"], b.mileage) == (95500, "sold", True, "2026-09-12", 21000)
    assert (c.title, c.price, c.listing_type, c.mileage) == ("2019 McLaren Artura Spider", 85000, "auction", 5900)
    assert "Ends in 2 days" in (c.auction_end or "")


def test_record_sales_keeps_newest_first_and_dedupes(tmp_path):
    set_target("artura")
    ls = parse_cards(PAGE, "https://carsandbids.com", T)
    for l in ls:
        l.target = "artura"
    rows = record_sales(str(tmp_path), ls)
    assert [r["ended"] for r in rows] == ["2026-09-18", "2026-09-12"]
    rows = record_sales(str(tmp_path), ls)
    assert len(rows) == 2 and rows[0]["price"] == 109000 and rows[0]["sold"] is True and rows[1]["sold"] is True
    assert os.path.exists(os.path.join(str(tmp_path), "sales.json")) and json.load(open(os.path.join(str(tmp_path), "sales.json")))[0]["url"].endswith("artura-spider")


def test_first_gen_huracan_never_gets_an_evo_trim_from_its_description():
    from crawler.models import Listing
    set_target("huracan")
    l = Listing(source="ebay", source_name="eBay", url="https://www.ebay.com/itm/1", title="2017 Lamborghini Huracan LP 580-2",
                price=171430, year=2017, extra={"description": "V10 Power, RWD, Bianco Monocerus"}).finalize()
    assert l.trim == "LP 580-2" and l.is_candidate()
    l = Listing(source="ebay", source_name="eBay", url="https://www.ebay.com/itm/2", title="2017 Lamborghini Huracan",
                price=164900, year=2017, extra={"description": "602-hp V10, RWD, Rear-Wheel Drive"}).finalize()
    assert l.trim == "LP 580-2"
    l = Listing(source="ebay", source_name="eBay", url="https://www.ebay.com/itm/3", title="2021 Lamborghini Huracan EVO RWD Coupe",
                price=263000, year=2021).finalize()
    assert l.trim == "EVO RWD" and not l.is_candidate()
    l = Listing(source="cars_com", source_name="Cars.com", url="https://www.cars.com/v/4", title="Used 2019 Lamborghini Huracan Super Trofeo EVO",
                price=219888, year=2019).finalize()
    assert l.trim == "Super Trofeo" and not l.is_candidate()
    set_target("artura")
