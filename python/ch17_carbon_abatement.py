"""
Carbon abatement curve from an emissions-cap sweep
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 17.
Book answers: $61,000 and 48.8 t, $61,500 at 40.2 t ($58/t), and $65,000 at 32.0 t ($426/t).
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMinimize, HiGHS, lpSum, value

supply = {"P1": 800, "P2": 600}; demand = {"M1": 500, "M2": 400, "M3": 450}
km = {("P1","M1"):300, ("P1","M2"):700, ("P1","M3"):1100, ("P2","M1"):900, ("P2","M2"):400, ("P2","M3"):500}
rail_lanes = [k for k in km if km[k] >= 500]

def solve(cap=None, carbon_price=0):
    m = LpProblem("carbon", LpMinimize)
    truck = {k: m.add_variable(f"truck_{k[0]}_{k[1]}", lowBound=0) for k in km}
    rail = {k: m.add_variable(f"rail_{k[0]}_{k[1]}", lowBound=0, upBound=350) for k in rail_lanes}
    cost = lpSum(0.10 * km[k] * truck[k] for k in km) + lpSum((0.06 * km[k] + 30) * rail[k] for k in rail_lanes)
    co2 = (lpSum(0.080 * km[k] * truck[k] for k in km)
           + lpSum((0.025 * km[k] + 4.0) * rail[k] for k in rail_lanes)) * 0.001    # tons
    m += cost + carbon_price * co2
    for i in supply:
        m += lpSum(truck[k] for k in km if k[0] == i) + lpSum(rail[k] for k in rail_lanes if k[0] == i) <= supply[i]
    for j in demand:
        m += lpSum(truck[k] for k in km if k[1] == j) + lpSum(rail[k] for k in rail_lanes if k[1] == j) >= demand[j]
    if cap is not None:
        m += co2 <= cap, "co2_cap"
    m.solve(HiGHS(msg=False))
    price = [abs(c.pi) for c in m.constraints() if c.name == "co2_cap"]
    return cost.value(), co2.value(), (price[0] if price else 0)

print("Plans chosen at different carbon prices (the rows of the book's table):")
for carbon_price in (0, 60, 450):
    c, e, _ = solve(carbon_price=carbon_price)
    print(f"  price ${carbon_price}/t: cost ${c:,.0f}, CO2 {e:.1f} t/week")
print("Emissions-cap sweep (the abatement curve):")
for cap in [48.8, 45, 42, 40, 36, 34.2, 32]:
    c, e, p = solve(cap)
    print(f"  cap {cap}: cost ${c:,.0f}, cost of last ton ${p:,.0f}")
