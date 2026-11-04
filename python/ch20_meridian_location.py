"""
Meridian Foods fixed-charge location model
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 20.
Book answers: open site B, total $1,546.5k per year. Peak plan 500/550/550/300 with no overtime, $38,750k.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMinimize, HiGHS, lpSum, value

regions = ["R1", "R2", "R3", "R4"]
demand = {"R1": 120, "R2": 95, "R3": 140, "R4": 85}          # thousands of units/year
dcs = ["DC0", "A", "B", "C"]
fixed = {"DC0": 0, "A": 300, "B": 260, "C": 240}               # $000/year
freight = {"DC0": {"R1":3.2, "R2":4.1, "R3":5.6, "R4":4.8},
           "A":   {"R1":2.9, "R2":3.0, "R3":3.4, "R4":5.5},
           "B":   {"R1":4.0, "R2":2.6, "R3":2.8, "R4":3.1},
           "C":   {"R1":3.1, "R2":3.8, "R3":4.4, "R4":3.0}}     # $/unit

m = LpProblem("meridian", LpMinimize)
y = {d: m.add_variable(f"open_{d}", cat="Binary") for d in dcs}
x = {(d, r): m.add_variable(f"ship_{d}_{r}", lowBound=0) for d in dcs for r in regions}
m += lpSum(fixed[d] * y[d] for d in dcs) + lpSum(freight[d][r] * x[d, r] for d in dcs for r in regions)
m += y["DC0"] == 1                                              # the existing DC stays open
for r in regions:
    m += lpSum(x[d, r] for d in dcs) == demand[r]
    for d in dcs:
        m += x[d, r] - demand[r] * y[d] <= 0
m.solve(HiGHS(msg=False))
print("Open:", [d for d in dcs if y[d].value() > 0.5])
for r in regions:
    print(f"  {r} served by", [d for d in dcs if x[d, r].value() > 1e-6])
print(f"Total annual cost: ${value(m.objective):,.1f}k")

# Step 4: planning for the peak (thousands of units)
demand, cap = [400, 500, 700, 300], 550
p = LpProblem("meridian_plan", LpMinimize)
T = range(4)
R = {t: p.add_variable(f"reg_{t}", lowBound=0, upBound=cap) for t in T}
O = {t: p.add_variable(f"ot_{t}", lowBound=0, upBound=100) for t in T}
I = {t: p.add_variable(f"inv_{t}", lowBound=0) for t in T}
p += lpSum(20 * R[t] + 32 * O[t] + 3 * I[t] for t in T)
for t in T:
    p += I[t] == (I[t - 1] if t else 0) + R[t] + O[t] - demand[t]
p.solve(HiGHS(msg=False))
print("Peak plan: regular", [R[t].value() for t in T], "overtime", [O[t].value() for t in T],
      f"cost ${value(p.objective):,.0f}k")
