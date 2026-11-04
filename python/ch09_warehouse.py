"""
Slotting, forward pick allocation, and dock door assignment
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 9.
Book answers: slotting 16,390 -> 12,290 m/day, square-root allocation 17.1/8.6/4.3 m3 (1.63 replenishments/week), doors 610 -> 490 m.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
import math
from pulp import LpProblem, LpMinimize, HiGHS, lpSum, value

# Slotting by velocity
picks = {"A":120, "B":35, "C":260, "D":15, "E":80, "F":190, "G":45, "H":10}
slot_m = [10, 14, 18, 22, 26, 30, 34, 38]
walk = lambda order: sum(picks[p] * slot_m[i] for i, p in enumerate(order))
alpha = sorted(picks); velocity = sorted(picks, key=picks.get, reverse=True)
print("Alphabetical:", walk(alpha), "m/day | By velocity:", walk(velocity), "m/day", velocity)

# Square-root allocation of forward space
flow, space = [16, 4, 1], 30
roots = [math.sqrt(f) for f in flow]
alloc = [space * r / sum(roots) for r in roots]
print("Forward space:", [round(a, 1) for a in alloc],
      "replenishments/week:", round(sum(f / a for f, a in zip(flow, alloc)), 2))

# Dock door assignment
travel = [[100,120,300,320], [110,250,280,300], [300,280,120,260], [310,300,130,140]]
m = LpProblem("doors", LpMinimize)
x = {(t, d): m.add_variable(f"x_{t}_{d}", cat="Binary") for t in range(4) for d in range(4)}
m += lpSum(travel[t][d] * x[t, d] for t in range(4) for d in range(4))
for t in range(4): m += lpSum(x[t, d] for d in range(4)) == 1
for d in range(4): m += lpSum(x[t, d] for t in range(4)) == 1
m.solve(HiGHS(msg=False))
print("Door plan:", {f"trailer {t+1}": f"door {d+1}" for (t, d) in x if x[t, d].value() > 0.5},
      "total", value(m.objective), "m")
