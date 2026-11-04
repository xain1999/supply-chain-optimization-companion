"""
Transportation problem with an optional lane cap
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 5.
Two plants, three depots. Book answers: $5,650, and capping lane P2-D3 at 200 raises cost to $6,000 (shadow price $7/unit).
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMinimize, HiGHS, lpSum, value

supply = {"P1": 500, "P2": 400}
demand = {"D1": 300, "D2": 350, "D3": 250}
cost = {("P1","D1"): 8, ("P1","D2"): 6, ("P1","D3"): 10,
        ("P2","D1"): 9, ("P2","D2"): 7, ("P2","D3"): 4}

def solve(lane_caps=None):
    m = LpProblem("distribution", LpMinimize)
    x = {k: m.add_variable(f"x_{k[0]}_{k[1]}", lowBound=0) for k in cost}
    m += lpSum(cost[k] * x[k] for k in cost)
    for i in supply:
        m += lpSum(x[i, j] for j in demand) <= supply[i]
    for j in demand:
        m += lpSum(x[i, j] for i in supply) >= demand[j]
    for k, cap in (lane_caps or {}).items():
        m += x[k] <= cap, f"cap_{k[0]}_{k[1]}"
    m.solve(HiGHS(msg=False))
    caps = {c.name: c.pi for c in m.constraints() if c.name.startswith("cap_")}   # signed dual
    return value(m.objective), {k: x[k].value() for k in cost if x[k].value() > 0}, caps

print("Base plan:", solve())
print("Lane P2-D3 capped at 200:", solve({("P2", "D3"): 200}))
