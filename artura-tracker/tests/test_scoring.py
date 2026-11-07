from crawler.scoring import score_all


def _row(price, **kw):
    r = {"target": "huracan", "year": 2017, "mileage": 30000, "price": price, "status": "active",
         "candidate": True, "rankable": True, "listing_type": "dealer"}
    r.update(kw)
    return r


def test_live_auction_bid_is_not_flagged_as_suspect_price():
    rows = [_row(240000 + i * 1000, mileage=20000 + i * 1000) for i in range(12)]
    bid = _row(100000, listing_type="auction", rankable=False)
    teaser = _row(98000)
    score_all(rows + [bid, teaser])
    assert teaser["price_suspect"] is True
    assert bid["price_suspect"] is False
