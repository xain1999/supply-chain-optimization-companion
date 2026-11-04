"""
Reading model data from Excel and writing the plan back
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 18.
Book answer: $5,650. Creates network.xlsx with sample data if it does not exist.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
          pip install pandas openpyxl
"""
import os
import pandas as pd

if not os.path.exists("network.xlsx"):
    with pd.ExcelWriter("network.xlsx") as w:
        pd.DataFrame({"plant": ["P1", "P2"], "supply": [500, 400]}).to_excel(w, sheet_name="supply", index=False)
        pd.DataFrame({"depot": ["D1", "D2", "D3"], "demand": [300, 350, 250]}).to_excel(w, sheet_name="demand", index=False)
        pd.DataFrame({"plant": ["P1"]*3 + ["P2"]*3, "depot": ["D1","D2","D3"]*2,
                      "cost": [8, 6, 10, 9, 7, 4]}).to_excel(w, sheet_name="costs", index=False)

from pulp import (LpProblem, LpMinimize, LpSolveStatus,
                  HiGHS, lpSum, value)

# Read the three sheets of the workbook
book = pd.read_excel("network.xlsx", sheet_name=None)
sup, dem = book["supply"], book["demand"]
lanes = book["costs"]
supply = dict(zip(sup["plant"], sup["supply"]))
demand = dict(zip(dem["depot"], dem["demand"]))
cost = {(r.plant, r.depot): r.cost
        for r in lanes.itertuples()}

# Basic data checks before building the model
assert not lanes.duplicated(["plant", "depot"]).any()
assert lanes.notna().all().all()
assert (lanes["cost"] >= 0).all()

model = LpProblem("distribution", LpMinimize)
x = {k: model.add_variable(f"x_{k[0]}_{k[1]}", lowBound=0)
     for k in cost}
model += lpSum(cost[k] * x[k] for k in cost)
for i in supply:
    out = [x[k] for k in cost if k[0] == i]
    model += lpSum(out) <= supply[i]
for j in demand:
    inbound = [x[k] for k in cost if k[1] == j]
    model += lpSum(inbound) >= demand[j]

result = model.solve(HiGHS(msg=False))
if result.status != LpSolveStatus.Optimal:
    raise SystemExit(f"Not optimal: {result.status.name}")

# Write the plan to a new workbook for the planners
lanes["ship"] = [value(x[(r.plant, r.depot)])
                 for r in lanes.itertuples()]
lanes.to_excel("plan.xlsx", index=False)
print("Total cost:", value(model.objective))
