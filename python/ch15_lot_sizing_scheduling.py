"""
Wagner-Whitin, Silver-Meal, dispatching rules, and Johnson's rule
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 15.
Book answers: Wagner-Whitin $730, Silver-Meal $770, Johnson sequence B, D, C, E, A with makespan 30.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
(No solver needed for this file.)
"""
d, S, h = [60, 100, 10, 200, 50, 80], 200, 1
n = len(d)
F, choice = [0] + [None] * n, [None] * (n + 1)
for j in range(1, n + 1):                      # Wagner-Whitin dynamic program
    for i in range(1, j + 1):
        c = F[i - 1] + S + sum(h * d[t - 1] * (t - i) for t in range(i, j + 1))
        if F[j] is None or c < F[j]: F[j], choice[j] = c, i
plan, j = [], n
while j > 0: plan.append((choice[j], j)); j = choice[j] - 1
print("Wagner-Whitin:", F[n], "runs (first week, last week):", plan[::-1])

t, total = 0, 0                                # Silver-Meal heuristic
while t < n:
    best, end = None, t
    for e in range(t, n):
        avg = (S + sum(h * d[u] * (u - t) for u in range(t, e + 1))) / (e - t + 1)
        if best is None or avg <= best: best, end = avg, e
        else: break
    total += S + sum(h * d[u] * (u - t) for u in range(t, end + 1)); t = end + 1
print("Silver-Meal:", total)

jobs = {"J1": (6, 8), "J2": (2, 20), "J3": (8, 15), "J4": (3, 6), "J5": (4, 21)}
def evaluate(seq):
    t, flows, late = 0, [], []
    for j in seq:
        t += jobs[j][0]; flows.append(t); late.append(t - jobs[j][1])
    return sum(flows) / len(seq), max(late), sum(1 for x in late if x > 0)
for rule, key in [("SPT", lambda j: jobs[j][0]), ("EDD", lambda j: jobs[j][1])]:
    seq = sorted(jobs, key=key)
    print(rule, seq, "avg flow %.1f, max lateness %d, late jobs %d" % evaluate(seq))

two = {"A": (5, 2), "B": (1, 6), "C": (9, 7), "D": (3, 8), "E": (10, 4)}
front = sorted([j for j in two if two[j][0] < two[j][1]], key=lambda j: two[j][0])
back = sorted([j for j in two if two[j][0] >= two[j][1]], key=lambda j: two[j][1], reverse=True)
seq, t1, t2 = front + back, 0, 0
for j in seq:
    t1 += two[j][0]; t2 = max(t2, t1) + two[j][1]
print("Johnson:", seq, "makespan", t2)
