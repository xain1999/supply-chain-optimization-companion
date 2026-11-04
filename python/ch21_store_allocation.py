"""
Allocating a scarce shipment by marginal value (Case B)
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 21.
Book answers: optimal 352/281/51/116 units, expected value $67,308 vs $64,490 for proportional allocation (284/231/196/89).
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
          pip install scipy   (no LP solver needed)
"""
from scipy.stats import norm

stores = {"Flagship": (320, 60, 99), "Mall": (260, 50, 89),
          "Outlet": (220, 110, 45), "Airport": (100, 25, 109)}   # mean, std dev, price
salvage, supply = 20, 800

def expected_sales(q, mu, sd):
    z = (q - mu) / sd
    return mu - sd * (norm.pdf(z) - z * (1 - norm.cdf(z)))
def value_of(alloc):
    return sum(p * expected_sales(q, mu, sd) + salvage * (q - expected_sales(q, mu, sd))
               for (mu, sd, p), q in ((stores[k], alloc[k]) for k in stores))
def marginal(k, q):
    mu, sd, p = stores[k]
    return salvage + (p - salvage) * (1 - norm.cdf((q + 0.5 - mu) / sd))

alloc = {k: 0 for k in stores}
for _ in range(supply):                       # give each unit to the store where it is worth most
    best = max(stores, key=lambda k: marginal(k, alloc[k])); alloc[best] += 1
proportional = {"Flagship": 284, "Mall": 231, "Outlet": 196, "Airport": 89}   # whole jackets
print("Optimal:", alloc, f"value ${value_of(alloc):,.0f}")
print("Proportional:", {k: round(v) for k, v in proportional.items()}, f"value ${value_of(proportional):,.0f}")
