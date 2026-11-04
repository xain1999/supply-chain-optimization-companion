"""
Quantity discounts and supplier selection
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 13.
Book answers: order 2,000 at $9.30 ($48,610/year), and buy 5,000 each from suppliers S1 and S2 ($88,000).
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
import math
from pulp import LpProblem, LpMinimize, HiGHS, lpSum, value

D, S, h = 5000, 100, 0.20
breaks = [(0, 10.00), (500, 9.60), (2000, 9.30)]
for i, (low, price) in enumerate(breaks):
    high = breaks[i + 1][0] - 1 if i + 1 < len(breaks) else float("inf")
    q = min(max(math.sqrt(2 * D * S / (h * price)), low), high)
    tc = D * price + D / q * S + h * price * q / 2
    print(f"${price:.2f}: best Q {q:.0f}, total ${tc:,.0f}")

sup = {"S1": (8.00, 6000, 4000, 0.030), "S2": (8.40, 5000, 2000, 0.010),
       "S3": (8.90, 8000, 1000, 0.005), "S4": (7.60, 4000, 6000, 0.050)}   # price, capacity, fixed, defects
m = LpProblem("suppliers", LpMinimize)
x = {k: m.add_variable(f"buy_{k}", lowBound=0) for k in sup}
y = {k: m.add_variable(f"use_{k}", cat="Binary") for k in sup}
m += lpSum(sup[k][0] * x[k] + sup[k][2] * y[k] for k in sup)
m += lpSum(x.values()) == 10000
for k in sup:
    m += x[k] <= sup[k][1] * y[k]
    m += x[k] >= 2000 * y[k]
m += lpSum(sup[k][3] * x[k] for k in sup) <= 0.02 * 10000
m.solve(HiGHS(msg=False))
print("Supplier plan:", {k: round(x[k].value()) for k in sup}, f"total ${value(m.objective):,.0f}")
