"""
Product launch with setups, minimum lots, and a dependency
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 4.
Binary run decisions, linking constraints, and "C requires A". Book answers: $4,880 without the rule, $4,680 with it.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMaximize, HiGHS, lpSum, value

products = ["A", "B", "C"]
margin = {"A": 18, "B": 36, "C": 60}
hours  = {"A": 2, "B": 3, "C": 4}
setup  = {"A": 800, "B": 1000, "C": 2400}
demand = {"A": 150, "B": 120, "C": 90}
min_lot, capacity = 50, 600

def solve(c_requires_a):
    m = LpProblem("launch", LpMaximize)
    make = {p: m.add_variable(f"make_{p}", lowBound=0, cat="Integer") for p in products}
    run  = {p: m.add_variable(f"run_{p}", cat="Binary") for p in products}
    m += lpSum(margin[p] * make[p] - setup[p] * run[p] for p in products)
    m += lpSum(hours[p] * make[p] for p in products) <= capacity
    for p in products:
        m += make[p] <= demand[p] * run[p]     # linking (gate)
        m += make[p] >= min_lot * run[p]       # minimum lot
    if c_requires_a:
        m += run["C"] <= run["A"]
    m.solve(HiGHS(msg=False))
    return value(m.objective), {p: int(make[p].value()) for p in products}

print("Without the rule:", solve(False))
print("C requires A    :", solve(True))
