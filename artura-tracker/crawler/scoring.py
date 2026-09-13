"""Market model + deal scoring.

A tiny least-squares fit price ~ a + b*mileage + c*(year-2023) over the
clean-title candidate pool gives an "expected asking price" for each car.
deal_pct = how far below expectation the car is priced. It is deliberately
simple and transparent: the point is ranking, not valuation.
"""
from __future__ import annotations

from statistics import median


def _solve3(A, b):
    """Gaussian elimination for a 3x3 system (no numpy dependency)."""
    n = 3
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(M[r][i]))
        if abs(M[piv][i]) < 1e-12:
            return None
        M[i], M[piv] = M[piv], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                for c in range(i, n + 1):
                    M[r][c] -= f * M[i][c]
    return [M[i][n] / M[i][i] for i in range(n)]


def fit_market(rows: list[dict]) -> dict:
    pts = [(r["price"], r.get("mileage") or 0, (r.get("year") or 2023) - 2023) for r in rows
           if r.get("price") and r.get("candidate") and r.get("title_status") != "branded" and r.get("listing_type") != "auction"
           and r.get("condition") != "new" and (r.get("mileage") or 0) >= 100 and r.get("status", "active") == "active"]
    model = {"n": len(pts), "intercept": None, "per_mile": None, "per_year": None,
             "median": median([p for p, _, _ in pts]) if pts else None}
    if len(pts) < 8:
        return model
    # normal equations for [1, miles/1000, year_offset]
    X = [(1.0, m / 1000.0, y) for _, m, y in pts]
    Y = [float(p) for p, _, _ in pts]
    A = [[sum(x[i] * x[j] for x in X) for j in range(3)] for i in range(3)]
    b = [sum(x[i] * y for x, y in zip(X, Y)) for i in range(3)]
    coef = _solve3(A, b)
    if not coef:
        return model
    a, per_k_mile, per_year = coef
    # sanity: mileage should not *raise* price; clamp to sensible bands
    per_k_mile = min(per_k_mile, 0.0)
    per_k_mile = max(per_k_mile, -4000.0)
    model.update({"intercept": round(a), "per_mile": round(per_k_mile / 1000.0, 2), "per_year": round(per_year)})
    return model


def expected_price(model: dict, row: dict):
    if model.get("intercept") is None:
        return model.get("median")
    miles = row.get("mileage") or 0
    yoff = (row.get("year") or 2023) - 2023
    return model["intercept"] + model["per_mile"] * miles + model["per_year"] * yoff


def score_all(rows: list[dict]) -> dict:
    model = fit_market(rows)
    for r in rows:
        exp = expected_price(model, r) if r.get("price") else None
        r["expected_price"] = round(exp) if exp else None
        r["deal_pct"] = round((exp - r["price"]) / exp * 100, 1) if exp and r.get("price") else None
        r["price_per_mile_note"] = None
    # rank among clean candidates by price
    pool = sorted([r for r in rows if r.get("candidate") and r.get("title_status") != "branded" and r.get("status") == "active"],
                  key=lambda r: r["price"])
    for i, r in enumerate(pool, 1):
        r["rank_cheapest_clean"] = i
    return model
