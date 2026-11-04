"""
Shadow prices and the dual
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 3.
Read shadow prices and slacks, then solve the dual. Book answers: $12.50 and $5.00, dual value $1,700.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMaximize, LpMinimize, HiGHS, value

m = LpProblem("plant", LpMaximize)
x = m.add_variable("standard", lowBound=0)
y = m.add_variable("premium", lowBound=0)
m += 40 * x + 60 * y
m += 2 * x + 4 * y <= 100, "machining_hours"
m += 3 * x + 2 * y <= 90, "finishing_hours"
m.solve(HiGHS(msg=False))
for c in m.constraints():
    # HiGHS reports duals of this maximization as negative. Other solvers may
    # use the opposite sign. Interpret with the objective sense and constraint type.
    print(f"{c.name}: dual {c.pi:+.2f}, slack {round(c.slack + 0.0, 2)}")

# Verify the interpretation by re-solving with one more machining hour
m2 = LpProblem("plant_plus_one", LpMaximize)
x2 = m2.add_variable("standard", lowBound=0); y2 = m2.add_variable("premium", lowBound=0)
m2 += 40 * x2 + 60 * y2
m2 += 2 * x2 + 4 * y2 <= 101
m2 += 3 * x2 + 2 * y2 <= 90
m2.solve(HiGHS(msg=False))
print(f"With 101 machining hours: {value(m2.objective):.2f} (up {value(m2.objective) - 1700:.2f})")

d = LpProblem("dual", LpMinimize)
u = d.add_variable("machining_price", lowBound=0)
v = d.add_variable("finishing_price", lowBound=0)
d += 100 * u + 90 * v
d += 2 * u + 3 * v >= 40
d += 4 * u + 2 * v >= 60
d.solve(HiGHS(msg=False))
print(f"Dual: u = {value(u):.2f}, v = {value(v):.2f}, value = {value(d.objective):.0f}")
