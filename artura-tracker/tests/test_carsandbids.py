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
  <div class="price">Bid to $95,500</div><a href="/auctions/3gj8Wgj1/2016-mclaren-artura-coupe">2016 McLaren Artura Coupe</a>
  <span>Ended Sep 12, 2026</span><span>21,400 Miles</span></li>
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
    assert (a.title, a.year, a.price, a.mileage, a.listing_type, a.location) == ("2018 McLaren Artura Spider", 2018, 109000, 8300, "sold", "Fort Lauderdale, FL")
    assert a.extra["sold"] is True and a.extra["ended"] == "2026-09-18"
    assert (b.price, b.listing_type, b.extra["sold"], b.extra["ended"], b.mileage) == (95500, "sold", False, "2026-09-12", 21400)
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
    assert len(rows) == 2 and rows[0]["price"] == 109000 and rows[0]["sold"] is True and rows[1]["sold"] is False
    assert os.path.exists(os.path.join(str(tmp_path), "sales.json")) and json.load(open(os.path.join(str(tmp_path), "sales.json")))[0]["url"].endswith("artura-spider")
