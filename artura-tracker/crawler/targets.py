"""Manage the cars being hunted.

    python -m crawler.targets list
    python -m crawler.targets add "Ferrari" "296 GTB" --years 2022-2026 --vin ZFF --dealers ferrari
    python -m crawler.targets disable huracan | enable huracan | remove huracan

Only make and model are required. Optional but worth filling in later (run once and read the source-health notes):
  --cargurus d1234   the entity id in a CarGurus URL   (.../l-Used-Ferrari-296-GTB-d1234)
  --carfax Used-Ferrari-296-GTB_w1234   the path of the CARFAX search page
"""
from __future__ import annotations

import argparse
import json
import sys

from . import config

# World Manufacturer Identifier prefixes for the usual suspects
WMI = {"mclaren": ["SBM"], "lamborghini": ["ZHW"], "ferrari": ["ZFF"], "porsche": ["WP0", "WP1"], "aston martin": ["SCF"],
       "bentley": ["SCB"], "rolls-royce": ["SCA"], "maserati": ["ZAM", "ZN6"], "lotus": ["SCC"], "mercedes-benz": ["W1K", "WDD", "W1N"],
       "bmw": ["WBA", "WBS", "WBY"], "audi": ["WAU", "WUA"], "chevrolet": ["1G1"], "ford": ["1FA"], "nissan": ["JN1"], "acura": ["19U"],
       "dodge": ["2C3"], "tesla": ["5YJ", "7SA"], "lexus": ["JTH"], "jaguar": ["SAJ"], "land rover": ["SAL"], "bugatti": ["VF9"]}


def _load():
    return json.load(open(config.TARGETS_FILE, encoding="utf-8"))


def _save(d):
    json.dump(d, open(config.TARGETS_FILE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def main(argv=None):
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("list")
    a = sp.add_parser("add")
    a.add_argument("make"); a.add_argument("model")
    a.add_argument("--key", default=None); a.add_argument("--years", default=f"{config.YEAR_MIN}-{config.YEAR_MAX}")
    a.add_argument("--vin", default=None, help="VIN prefix(es), comma-separated; defaults from the make")
    a.add_argument("--dealers", default=None, help="dealer network name in config.DEALER_NETWORKS (mclaren, lamborghini)")
    a.add_argument("--cargurus", default=""); a.add_argument("--carfax", default="")
    a.add_argument("--trims", default="", help='comma-separated trim names, e.g. "GTS,Spider,Assetto Fiorano"')
    a.add_argument("--floor", type=int, default=config.PRICE_FLOOR)
    for c in ("enable", "disable", "remove"):
        sp.add_parser(c).add_argument("key")
    args = ap.parse_args(argv)
    d = _load()
    if args.cmd == "list":
        for k, t in d.items():
            print(f"{k:12} {t['make']} {t['model']:16} years={t.get('years')} enabled={t.get('enabled', True)} dealers={t.get('dealer_network', '-')}")
        return 0
    if args.cmd == "add":
        key = args.key or config._slug(args.model).replace("-", "")
        y0, y1 = (int(x) for x in args.years.split("-"))
        vin = [v.strip().upper() for v in (args.vin.split(",") if args.vin else WMI.get(args.make.lower(), []))]
        trims = [[t.strip(), r"\\b" + config.re.escape(t.strip().lower()) + r"\\b"] for t in args.trims.split(",") if t.strip()]
        d[key] = {"make": args.make, "model": args.model, "years": [y0, y1], "price_floor": args.floor, "vin_prefixes": vin,
                  "trims": trims, "default_trim": "Coupe", "cargurus_entity": args.cargurus, "carfax_path": args.carfax,
                  "dealer_network": (args.dealers or args.make).lower(), "enabled": True}
        _save(d)
        print(f"added '{key}': {args.make} {args.model} {y0}-{y1}, vin {vin or 'ANY (fill --vin!)'}, dealer network '{d[key]['dealer_network']}'")
        if not vin:
            print("  warning: no VIN prefix known for this make; VIN-based matching is off until you set vin_prefixes")
        if not args.cargurus:
            print("  note: CarGurus is skipped for this car until cargurus_entity is set (copy the dXXXX from a CarGurus search URL)")
        return 0
    if args.key not in d:
        print(f"no such target: {args.key}", file=sys.stderr)
        return 1
    if args.cmd == "remove":
        del d[args.key]
    else:
        d[args.key]["enabled"] = args.cmd == "enable"
    _save(d)
    print(f"{args.cmd}d {args.key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
