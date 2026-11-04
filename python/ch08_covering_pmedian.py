"""
Set covering and p-median location
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 8.
Book answers: covering within 45 km needs T2 and T6, and the 2-median is T1 and T3 (22.9 km on average).
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMinimize, HiGHS, lpSum, value

towns = ["T1", "T2", "T3", "T4", "T5", "T6"]
pop = [40, 25, 30, 15, 35, 20]
dist = [[0,30,55,80,60,95], [30,0,35,60,50,80], [55,35,0,30,45,50],
        [80,60,30,0,55,40], [60,50,45,55,0,45], [95,80,50,40,45,0]]
n = len(towns)

def covering(radius):
    m = LpProblem("covering", LpMinimize)
    y = {j: m.add_variable(f"open_{towns[j]}", cat="Binary") for j in range(n)}
    m += lpSum(y.values())
    for i in range(n):
        m += lpSum(y[j] for j in range(n) if dist[i][j] <= radius) >= 1
    m.solve(HiGHS(msg=False))
    return [towns[j] for j in range(n) if y[j].value() > 0.5]

def p_median(p):
    m = LpProblem("p_median", LpMinimize)
    y = {j: m.add_variable(f"open_{towns[j]}", cat="Binary") for j in range(n)}
    x = {(i, j): m.add_variable(f"serve_{i}_{j}", lowBound=0) for i in range(n) for j in range(n)}
    m += lpSum(pop[i] * dist[i][j] * x[i, j] for i in range(n) for j in range(n))
    m += lpSum(y.values()) == p
    for i in range(n):
        m += lpSum(x[i, j] for j in range(n)) == 1
        for j in range(n):
            m += x[i, j] - y[j] <= 0
    m.solve(HiGHS(msg=False))
    return [towns[j] for j in range(n) if y[j].value() > 0.5], value(m.objective) / sum(pop)

print("Covering within 45 km:", covering(45))
for p in (1, 2, 3):
    sites, avg = p_median(p)
    print(f"{p}-median: {sites}, average distance {avg:.1f} km")
