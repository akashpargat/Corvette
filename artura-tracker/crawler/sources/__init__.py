"""Source registry. Each module exposes NAME, LABEL, KIND and fetch(client, ctx)."""
from __future__ import annotations

from importlib import import_module

SOURCE_MODULES = [
    "mclaren_preowned",
    "dealer_sites",
    "cars_com",
    "autotrader",
    "kbb",
    "cargurus",
    "carfax",
    "truecar",
    "edmunds",
    "autolist",
    "dupont",
    "classic_com",
    "bringatrailer",
    "carsandbids",
    "ebay",
    "hemmings",
    "craigslist",
    "iseecars",
    "usedcars_com",
    "carsforsale",
    "carsdirect",
    "classiccars_com",
    "jamesedition",
    "exoticcartrader",
    "pcarmarket",
    "collectingcars",
    "mclarenlife",
    "autotempest",
    "autotrader_ca",
    "kijiji",
    "cargurus_ca",
    "fb_marketplace",
]


def load_sources(names=None):
    mods = []
    for n in SOURCE_MODULES:
        if names and n not in names:
            continue
        mods.append(import_module(f"crawler.sources.{n}"))
    return mods
