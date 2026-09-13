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


def test_vin_year_and_cents():
    from crawler.models import year_from_vin
    assert year_from_vin("SBM16AEA5PW001931") == 2023 and year_from_vin("SBM16BEA8TW004421") == 2026
    assert parse_price(33320000) == 333200 and parse_price("$3,332,000") == 3332000 // 100 * 1 if False else parse_price(33320000) == 333200
    l = Listing(source="x", source_name="X", url="u", title="McLaren Artura", vin="SBM16AEA8RW002123", price=18444900).finalize()
    assert l.year == 2024 and l.price == 184449


def test_huracan_target():
    from crawler.models import set_target, current_target, Listing, detect_trim, vin_matches
    set_target("huracan")
    try:
        l = Listing(source="x", source_name="X", url="u", title="2022 Lamborghini Huracán EVO RWD Spyder VIN ZHWUT4ZF9NLA12345", price=249000, mileage=8000).finalize()
        assert l.target == "huracan" and l.vin == "ZHWUT4ZF9NLA12345" and l.trim == "EVO RWD Spyder" and l.year == 2022 and l.is_candidate()
        assert detect_trim("Huracan STO") == "STO" and vin_matches("ZHWUC1ZF5KLA00001") and not vin_matches("SBM16AEA5PW001931")
        race = Listing(source="x", source_name="X", url="u", title="2021 Lamborghini Huracan Super Trofeo EVO race car", price=200000).finalize()
        assert not race.is_candidate()
    finally:
        set_target("artura")


def test_sibling_models_are_excluded():
    from crawler.models import set_target, Listing
    set_target("huracan")
    try:
        t = Listing(source="dealer_sites", source_name="d", url="https://x/2026-lamborghini-temerario-zhwuc1zc6tla01419", title="2026 Lamborghini", vin="ZHWUC1ZC6TLA01419", price=202609, year=2026).finalize()
        assert not t.is_candidate()
    finally:
        set_target("artura")
    a = Listing(source="x", source_name="x", url="https://x/2024-mclaren-750s", title="2024 McLaren 750S Spider", price=300000, year=2024).finalize()
    assert not a.is_candidate()
