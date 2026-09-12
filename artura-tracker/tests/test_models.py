from crawler.models import Listing, parse_mileage, parse_price, parse_year, detect_title_status, extract_state, detect_trim


def test_price_parsing():
    assert parse_price("$189,995") == 189995
    assert parse_price("Price: $164,900 · Great Deal") == 164900
    assert parse_price("$1,499/mo est.") is None
    assert parse_price(175490) == 175490
    assert parse_price("Call for price") is None


def test_mileage_parsing():
    assert parse_mileage("8,755 mi.") == 8755
    assert parse_mileage("3K miles") == 3000
    assert parse_mileage("2.5k mi") == 2500
    assert parse_mileage(4908) == 4908


def test_year_trim_state():
    assert parse_year("Used 2023 McLaren Artura Performance") == 2023
    assert detect_trim("2024 McLaren Artura Spider TechLux") == "Spider"
    assert extract_state("Scottsdale, AZ") == "AZ"
    assert extract_state("Coral Gables, Florida 33134") == "FL"


def test_title_status():
    assert detect_title_status("Salvage title, rear damage")[0] == "branded"
    assert detect_title_status("One owner, clean CARFAX, no accidents")[0] == "clean"
    assert detect_title_status("2023 McLaren Artura")[0] == "unknown"


def test_listing_finalize_and_candidate():
    l = Listing(source="x", source_name="X", url="https://x/y", title="2023 McLaren Artura Performance VIN SBM16AEA5PW000123",
                price=172000, mileage=5000, location="Dallas, TX").finalize()
    assert l.vin == "SBM16AEA5PW000123"
    assert l.year == 2023 and l.trim == "Performance" and l.state == "TX"
    assert l.key == "SBM16AEA5PW000123"
    assert l.is_candidate()
    cheap = Listing(source="x", source_name="X", url="https://x/z", title="2023 McLaren Artura", price=2200).finalize()
    assert not cheap.is_candidate()
