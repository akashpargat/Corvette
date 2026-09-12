"""KBB classifieds share Autotrader's (Cox) inventory backend but a different bot wall."""
from . import autotrader
from .base import Ctx

NAME = "kbb"
LABEL = "Kelley Blue Book"
KIND = "marketplace"
HOST = "https://www.kbb.com"
URL = HOST + "/cars-for-sale/all/mclaren/artura?searchRadius=0&sortBy=derivedpriceASC&numRecords=100&firstRecord={first}"


def fetch(client, ctx: Ctx):
    return autotrader.fetch(client, ctx, host=HOST, url_tpl=URL, name=NAME, label=LABEL)
