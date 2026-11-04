"""
Two-product plant
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 1.
Maximize contribution under two department-hour limits. Book answer: 20 Standard, 15 Premium, $1,700.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMaximize, LpSolveStatus, HiGHS, value

model = LpProblem("two_product_plant", LpMaximize)
x = model.add_variable("standard", lowBound=0)
y = model.add_variable("premium", lowBound=0)
model += 40 * x + 60 * y, "contribution"
model += 2 * x + 4 * y <= 100, "machining_hours"
model += 3 * x + 2 * y <= 90, "finishing_hours"

result = model.solve(HiGHS(msg=False))
if result.status == LpSolveStatus.Optimal:
    print("Standard:", value(x))
    print("Premium :", value(y))
    print("Profit  :", value(model.objective))
