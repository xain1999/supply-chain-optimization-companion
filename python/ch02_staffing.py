"""
Five-day work week staffing
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 2.
Minimize pickers when each works 5 consecutive days. Book answer: 16 pickers (LP relaxation 15.33).
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMinimize, HiGHS, lpSum, value

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
required = [12, 10, 11, 14, 13, 9, 7]

def solve(integer=True):
    m = LpProblem("staffing", LpMinimize)
    cat = "Integer" if integer else "Continuous"
    start = {d: m.add_variable(f"start_{days[d]}", lowBound=0, cat=cat) for d in range(7)}
    m += lpSum(start.values())
    for t in range(7):               # day t is covered by starts on t, t-1, ..., t-4
        m += lpSum(start[(t - k) % 7] for k in range(5)) >= required[t], f"cover_{days[t]}"
    m.solve(HiGHS(msg=False))
    return value(m.objective), {days[d]: value(start[d]) for d in range(7)}

lp_total, _ = solve(integer=False)
ip_total, plan = solve(integer=True)
print(f"LP relaxation: {lp_total:.2f} pickers")
print(f"Integer optimum: {ip_total:.0f} pickers")
print("Starts by day:", {d: int(round(v)) for d, v in plan.items()})
