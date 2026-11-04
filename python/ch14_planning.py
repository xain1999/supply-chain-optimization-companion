"""
Aggregate production plan and workforce planning
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 14.
Book answers: workforce plan 26, 26, 26, 22 workers at $320,000.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMinimize, HiGHS, lpSum, value

# Aggregate plan (regular, overtime, inventory)
demand, cap, ot_cap = [400, 400, 800, 300], 500, 150
m = LpProblem("aggregate", LpMinimize)
T = range(4)
R = {t: m.add_variable(f"reg_{t}", lowBound=0, upBound=cap) for t in T}
O = {t: m.add_variable(f"ot_{t}", lowBound=0, upBound=ot_cap) for t in T}
I = {t: m.add_variable(f"inv_{t}", lowBound=0) for t in T}
m += lpSum(20 * R[t] + 30 * O[t] + 3 * I[t] for t in T)
for t in T:
    m += I[t] == (I[t - 1] if t else 0) + R[t] + O[t] - demand[t]
m.solve(HiGHS(msg=False))
print("Aggregate plan: regular", [R[t].value() for t in T], "overtime", [O[t].value() for t in T],
      f"cost ${value(m.objective):,.0f}")

# Workforce planning with hiring and layoffs
demand = [2000, 2600, 3200, 2200]
m = LpProblem("workforce", LpMinimize)
W = {t: m.add_variable(f"workers_{t}", lowBound=0, cat="Integer") for t in T}
Hh = {t: m.add_variable(f"hires_{t}", lowBound=0, cat="Integer") for t in T}
F = {t: m.add_variable(f"layoffs_{t}", lowBound=0, cat="Integer") for t in T}
I = {t: m.add_variable(f"inv_{t}", lowBound=0) for t in T}
m += lpSum(3000 * W[t] + 1500 * Hh[t] + 2000 * F[t] + 5 * I[t] for t in T)
for t in T:
    m += W[t] == (W[t - 1] if t else 22) + Hh[t] - F[t]
    m += I[t] == (I[t - 1] if t else 0) + 100 * W[t] - demand[t]
m.solve(HiGHS(msg=False))
print("Workforce plan:", [int(W[t].value()) for t in T], f"cost ${value(m.objective):,.0f}")
