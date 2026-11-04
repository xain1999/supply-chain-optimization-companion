"""
Periodic review, fill rate, ABC, and space-constrained ordering
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 12.
Book answers: order-up-to 632.1, fill rate 99.88%, ABC class A items P01, P04, P09, P06, and a space shadow price of about $55/m2.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
          pip install scipy
"""
import math
from scipy.stats import norm

d, sigma, L, R, z = 50, 15, 4, 7, 1.65
print(f"Periodic review: S = {d*(R+L) + z*sigma*math.sqrt(R+L):.1f}")

G = lambda z: norm.pdf(z) - z * (1 - norm.cdf(z))       # standard normal loss function
sigma_L, Q = sigma * math.sqrt(L), 500
print(f"Fill rate at z=1.65, Q=500: {100*(1 - sigma_L*G(1.65)/Q):.2f}%")

items = {"P01":(1200,45), "P02":(300,12), "P03":(5000,2.5), "P04":(80,310), "P05":(2500,1.2),
         "P06":(650,30), "P07":(150,8), "P08":(9000,0.9), "P09":(400,55), "P10":(220,4.5)}
usage = {k: u * c for k, (u, c) in items.items()}; total = sum(usage.values()); cum = 0
for k in sorted(usage, key=usage.get, reverse=True):
    cum += usage[k]
    cls = "A" if cum / total <= 0.81 else ("B" if cum / total <= 0.95 else "C")
    print(f"  {k}: ${usage[k]:>9,.0f}  cumulative {100*cum/total:5.1f}%  class {cls}")

# Space-constrained order quantities: find the space price (lambda) by bisection
data = [(12000, 75, 3.0, 0.02), (6000, 120, 4.0, 0.05), (20000, 50, 1.5, 0.01)]   # D, S, H, m2/unit
W = 40
lo, hi = 0.0, 1000.0
for _ in range(100):
    lam = (lo + hi) / 2
    Q = [math.sqrt(2*D*S / (H + 2*lam*f)) for D, S, H, f in data]
    if sum(q * f for q, (D, S, H, f) in zip(Q, data)) > W: lo = lam
    else: hi = lam
print("Space price per m2:", round(lam, 2), "order quantities:", [round(q) for q in Q])
