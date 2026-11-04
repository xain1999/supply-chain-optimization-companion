"""
Last-mile delivery: daily routes versus alternate-day zones (Case A)
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 21.
Exact routing by dynamic programming. Book answers: small vans daily $2,376/week, zones $2,671, large vans zones $1,567.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
(No solver needed for this file. Runs in a few seconds.)
"""
import math
from functools import lru_cache

pts = {"DC": (0, 0), "C1": (4, 9), "C2": (-3, 8), "C3": (7, 4), "C4": (-8, 3), "C5": (2, -6),
       "C6": (-5, -7), "C7": (9, -3), "C8": (-1, 11), "C9": (6, -9), "C10": (-9, -4)}
daily = {"C1":6, "C2":5, "C3":7, "C4":4, "C5":6, "C6":5, "C7":8, "C8":4, "C9":5, "C10":6}
cust = list(daily); n = len(cust)
dist = lambda a, b: round(math.hypot(pts[a][0] - pts[b][0], pts[a][1] - pts[b][1]), 1)

# Shortest closed tour from the DC through every subset of customers (Held-Karp)
best = [[math.inf] * n for _ in range(1 << n)]
for i, c in enumerate(cust): best[1 << i][i] = dist("DC", c)
for mask in range(1 << n):
    for i in range(n):
        if best[mask][i] == math.inf: continue
        for j in range(n):
            if not mask >> j & 1:
                v = best[mask][i] + dist(cust[i], cust[j])
                if v < best[mask | 1 << j][j]: best[mask | 1 << j][j] = v
tour = [0] + [min(best[m][i] + dist(cust[i], "DC") for i in range(n) if m >> i & 1) for m in range(1, 1 << n)]

def plan(customers, capacity, mult, van_day, per_km):
    target = sum(1 << cust.index(c) for c in customers)
    load = lambda m: sum(daily[cust[i]] * mult for i in range(n) if m >> i & 1)
    @lru_cache(None)
    def f(m):
        if m == 0: return 0.0
        low, sub, out = m & -m, m, math.inf
        while sub:
            if sub & low and load(sub) <= capacity:
                out = min(out, van_day + per_km * tour[sub] + f(m ^ sub))
            sub = (sub - 1) & m
        return out
    return f(target)

north = [c for c in cust if pts[c][1] >= 0]; south = [c for c in cust if pts[c][1] < 0]
for name, cap, fix, km in [("30-crate vans", 30, 150, 1.2), ("60-crate vans", 60, 200, 1.5)]:
    daily_week = 6 * plan(cust, cap, 1, fix, km)
    zones_week = 3 * plan(north, cap, 2, fix, km) + 3 * plan(south, cap, 2, fix, km)
    print(f"{name}: daily ${daily_week:,.2f}/week, alternate-day zones ${zones_week:,.2f}/week")
