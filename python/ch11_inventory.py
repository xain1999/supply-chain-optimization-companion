"""
EOQ, cost penalty, reorder point, and newsvendor ratio
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 11.
Book answers: EOQ about 949 units, ordering 1,200 costs 2.8% more, reorder point 249.5.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
(No solver needed for this file.)
"""
import math

def eoq(D, S, H): return math.sqrt(2 * D * S / H)
def total_cost(Q, D, S, H): return D / Q * S + H * Q / 2

D, S, H = 12000, 150, 4
q = eoq(D, S, H)
print(f"EOQ: {q:.0f} units, annual cost ${total_cost(q, D, S, H):,.0f}")
for Q in (600, 1200):
    pct = 100 * (total_cost(Q, D, S, H) / total_cost(q, D, S, H) - 1)
    print(f"Ordering {Q}: ${total_cost(Q, D, S, H):,.0f} ({pct:+.1f}%)")

d, sigma, L, z = 50, 15, 4, 1.65
print(f"Safety stock {z * sigma * math.sqrt(L):.1f}, reorder point {d * L + z * sigma * math.sqrt(L):.1f}")

def critical_ratio(price, cost, salvage):
    cu, co = price - cost, cost - salvage
    return cu / (cu + co)
print("Newsvendor critical ratio (Exercise 11.3 data):", critical_ratio(12, 5, 2))
