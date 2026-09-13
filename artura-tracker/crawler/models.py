"""Listing model and the normalisation helpers every source shares."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field, asdict
from typing import Optional

from . import config

VIN_RE = re.compile(r"\b(SBM[A-HJ-NPR-Z0-9]{14})\b")
PRICE_RE = re.compile(r"\$\s?([0-9]{2,3}(?:,[0-9]{3})+|[0-9]{5,7})(?!\s*/\s*mo)")
MILES_RE = re.compile(r"([0-9]{1,3}(?:,[0-9]{3})+|[0-9]{1,6})\s*(?:k\s*)?(?:mi\b|miles\b)", re.I)
MILES_K_RE = re.compile(r"\b([0-9]{1,3}(?:\.[0-9])?)\s*[kK]\s*(?:mi\b|miles\b)")
YEAR_RE = re.compile(r"\b(20(?:1[5-9]|2[0-9]))\b")

BRANDED_WORDS = [
    "salvage", "rebuilt", "reconstructed", "branded title", "lemon", "flood",
    "buyback", "manufacturer buy back", "junk title", "parts only", "bill of sale",
    "theft recovery", "total loss", "export only", "non-repairable", "certificate of destruction",
    "wrecked", "damaged", "repairable",
]
CLEAN_WORDS = ["clean title", "clean carfax", "no accidents", "clean history", "one owner", "1-owner", "1 owner"]

TRIMS = [
    ("Spider", re.compile(r"\bspider\b", re.I)),
    ("GT4", re.compile(r"\bgt4\b", re.I)),
    ("Performance", re.compile(r"\bperformance\b", re.I)),
    ("TechLux", re.compile(r"\btech\s?lux\b", re.I)),
    ("Vision", re.compile(r"\bvision\b", re.I)),
]

US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
    "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND",
    "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC",
}
STATE_NAMES = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA", "colorado": "CO",
    "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA",
    "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI", "minnesota": "MN",
    "mississippi": "MS", "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY", "north carolina": "NC",
    "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
    "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN", "texas": "TX",
    "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY",
}


@dataclass
class Listing:
    source: str                 # machine key, e.g. "cars_com"
    source_name: str            # human label, e.g. "Cars.com"
    url: str
    title: str = ""
    vin: Optional[str] = None
    year: Optional[int] = None
    trim: Optional[str] = None
    price: Optional[int] = None
    mileage: Optional[int] = None
    condition: str = "unknown"          # new | used | cpo | unknown
    title_status: str = "unknown"       # clean | branded | unknown
    title_notes: list = field(default_factory=list)
    dealer: Optional[str] = None
    location: Optional[str] = None
    state: Optional[str] = None
    color: Optional[str] = None
    listing_type: str = "dealer"        # dealer | private | auction
    auction_end: Optional[str] = None
    image: Optional[str] = None
    extra: dict = field(default_factory=dict)

    def finalize(self) -> "Listing":
        """Fill derived fields from whatever text we have."""
        blob = " ".join(str(x) for x in [self.title, self.extra.get("description", ""), self.extra.get("badges", "")])
        if not self.vin:
            m = VIN_RE.search(blob) or VIN_RE.search(self.url)
            if m:
                self.vin = m.group(1)
        if self.vin:
            self.vin = self.vin.upper()
        if not self.year:
            self.year = year_from_vin(self.vin) or parse_year(self.title) or parse_year(blob)
        elif self.vin and year_from_vin(self.vin) and self.year != year_from_vin(self.vin):
            self.year = year_from_vin(self.vin)
        if self.price is not None:
            self.price = _sane(self.price)
        if not self.trim:
            self.trim = detect_trim(blob) or "Coupe"
        if self.title_status == "unknown":
            st, notes = detect_title_status(blob)
            self.title_status = st
            self.title_notes = sorted(set(self.title_notes + notes))
        if not self.location:
            m = re.search(r"(?:Location:|located in|in)\s*([A-Z][A-Za-z.' ]{2,30},\s*[A-Z]{2})\b", blob)
            if m:
                self.location = m.group(1).strip()
        if self.location and (re.fullmatch(r"[\d .]+", self.location) or "kwh" in self.location.lower()):
            self.location = None
        if self.location and not self.state:
            self.state = extract_state(self.location)
        if self.title:
            self.title = re.sub(r"\s+", " ", self.title).strip()[:140]
        return self

    @property
    def key(self) -> str:
        if self.vin:
            return self.vin
        h = hashlib.sha1(f"{self.source}|{self.url}".encode()).hexdigest()[:12]
        return f"{self.source}:{h}"

    def is_candidate(self) -> bool:
        """A plausible, real, road-going Artura with a believable price."""
        if is_junk(self.title) or self.trim == "GT4":
            return False
        if self.price is None or not (config.PRICE_FLOOR <= self.price <= config.PRICE_CEILING):
            return False
        if self.year and not (config.YEAR_MIN <= self.year <= config.YEAR_MAX):
            return False
        return True

    def to_dict(self) -> dict:
        d = asdict(self)
        d["key"] = self.key
        d["candidate"] = self.is_candidate()
        return d


def parse_price(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    if isinstance(text, (int, float)):
        v = int(text)
        return _sane(v)
    m = PRICE_RE.search(str(text))
    if not m:
        digits = re.sub(r"[^0-9]", "", str(text).split(".")[0])
        return _sane(int(digits)) if 4 < len(digits) < 10 else None
    return _sane(int(m.group(1).replace(",", "")))


def _sane(v: int) -> Optional[int]:
    """Prices arrive as 179995, '17999500' (cents) or 0/1 placeholders."""
    if v <= 0:
        return None
    if v >= 1_500_000 and 20_000 <= v // 100 <= 600_000:
        return v // 100
    return v


VIN_YEAR = {"L": 2020, "M": 2021, "N": 2022, "P": 2023, "R": 2024, "S": 2025, "T": 2026, "V": 2027}


def year_from_vin(vin: Optional[str]) -> Optional[int]:
    if vin and len(vin) == 17:
        return VIN_YEAR.get(vin[9].upper())
    return None


def parse_mileage(text: Optional[str]) -> Optional[int]:
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return int(text)
    s = str(text)
    m = MILES_K_RE.search(s)
    if m:
        return int(float(m.group(1)) * 1000)
    m = MILES_RE.search(s)
    if m:
        return int(m.group(1).replace(",", ""))
    digits = re.sub(r"[^0-9]", "", s)
    return int(digits) if 0 < len(digits) <= 6 else None


def parse_year(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    m = YEAR_RE.search(str(text))
    return int(m.group(1)) if m else None


def detect_trim(text: str) -> Optional[str]:
    for name, rx in TRIMS:
        if rx.search(text or ""):
            return name
    return None


def detect_title_status(text: str) -> tuple[str, list]:
    t = (text or "").lower()
    notes = [w for w in BRANDED_WORDS if w in t]
    if notes:
        return "branded", notes
    if any(w in t for w in CLEAN_WORDS):
        return "clean", []
    return "unknown", []


def extract_state(location: str) -> Optional[str]:
    if not location:
        return None
    m = re.search(r",\s*([A-Z]{2})\b", location)
    if m and m.group(1) in US_STATES:
        return m.group(1)
    m = re.search(r"\b([A-Z]{2})\s*\d{5}\b", location)
    if m and m.group(1) in US_STATES:
        return m.group(1)
    low = location.lower()
    for name, code in STATE_NAMES.items():
        if re.search(rf"\b{name}\b", low):
            return code
    return None


JUNK_RE = re.compile(r"ride[- ]along|charity|experience|hot lap|track day|wheel set|wheels?\b|rims?\b|parts?\b|badge|brochure|key fob|model car|diecast|1:18|1/18|1:43|poster|jacket|seat\b|exhaust|spoiler|carbon fiber (?:kit|piece)|GT4 Trophy", re.I)


def is_artura(text: str) -> bool:
    return bool(re.search(r"artura", text or "", re.I))


def is_junk(text: str) -> bool:
    """Accessories, experiences and race cars that mention 'Artura' but are not a road car listing."""
    return bool(JUNK_RE.search(text or ""))
