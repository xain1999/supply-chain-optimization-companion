"""
Shortest path, assignment, and minimum-cost flow
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 6.
Book answers: shortest path 10 (Exercise 6.1 network), assignment 9 driver-hours, minimum-cost flow $1,020.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMinimize, HiGHS, lpSum, value
H = lambda: HiGHS(msg=False)

# Shortest path as a unit flow from S to T
arcs = {("S","A"):3, ("S","B"):5, ("A","B"):1, ("A","C"):6, ("B","C"):4,
        ("B","D"):3, ("D","C"):1, ("C","T"):2, ("D","T"):6}
nodes = {n for a in arcs for n in a}
m = LpProblem("shortest_path", LpMinimize)
f = {a: m.add_variable(f"f_{a[0]}_{a[1]}", lowBound=0) for a in arcs}
m += lpSum(arcs[a] * f[a] for a in arcs)
for n in nodes:
    b = 1 if n == "S" else (-1 if n == "T" else 0)
    m += lpSum(f[a] for a in arcs if a[0] == n) - lpSum(f[a] for a in arcs if a[1] == n) == b
m.solve(H()); print("Shortest path cost:", value(m.objective))

# Assignment: trucks to routes
cost = {("A","R1"):9, ("A","R2"):2, ("A","R3"):7, ("B","R1"):6, ("B","R2"):4,
        ("B","R3"):3, ("C","R1"):5, ("C","R2"):8, ("C","R3"):1}
m = LpProblem("assignment", LpMinimize)
x = {k: m.add_variable(f"x_{k[0]}_{k[1]}", cat="Binary") for k in cost}
m += lpSum(cost[k] * x[k] for k in cost)
for t in "ABC":
    m += lpSum(x[k] for k in cost if k[0] == t) == 1
for r in ("R1", "R2", "R3"):
    m += lpSum(x[k] for k in cost if k[1] == r) == 1
m.solve(H()); print("Assignment:", [k for k in cost if x[k].value() > 0.5], value(m.objective))

# Minimum-cost flow: two plants, a hub, three customers
supply = {"A": 120, "B": 80, "H": 0, "C1": -60, "C2": -70, "C3": -70}
arc = {("A","H"):(2,100), ("B","H"):(3,100), ("A","C1"):(6,50), ("B","C3"):(5,40),
       ("H","C1"):(3,80), ("H","C2"):(2,80), ("H","C3"):(4,80)}
m = LpProblem("min_cost_flow", LpMinimize)
f = {k: m.add_variable(f"f_{k[0]}_{k[1]}", lowBound=0, upBound=arc[k][1]) for k in arc}
m += lpSum(arc[k][0] * f[k] for k in arc)
for n, b in supply.items():
    m += lpSum(f[k] for k in arc if k[0] == n) - lpSum(f[k] for k in arc if k[1] == n) == b
m.solve(H())
print("Min-cost flow:", value(m.objective), {k: f[k].value() for k in arc if f[k].value() > 0})
