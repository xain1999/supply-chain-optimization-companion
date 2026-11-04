"""
Nearest neighbor, 2-opt, and Clarke-Wright savings
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 7.
Book answers: nearest neighbor 64 km, after 2-opt 57 km, savings plan 76 km with three trucks.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
D = [[0, 8, 9,10, 9,10,10],     # row/column 0 is the depot DC, then customers A-F
     [8, 0, 8,14, 7,10,18],
     [9, 8, 0, 8, 1,17,16],
     [10,14,8, 0, 9,21,11],
     [9, 7, 1, 9, 0,16,16],
     [10,10,17,21,16,0,19],
     [10,18,16,11,16,19,0]]
NAMES = ["DC", "A", "B", "C", "D", "E", "F"]
length = lambda r: sum(D[r[i]][r[i + 1]] for i in range(len(r) - 1))
show = lambda r: "->".join(NAMES[i] for i in r)

def nearest_neighbor():
    route, left = [0], set(range(1, len(D)))
    while left:
        nxt = min(left, key=lambda j: (D[route[-1]][j], j))
        route.append(nxt); left.remove(nxt)
    return route + [0]

def two_opt(route):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for k in range(i + 1, len(route) - 1):
                new = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
                if length(new) < length(route):
                    route, improved = new, True
    return route

def clarke_wright(demand, capacity):
    routes = {c: [c] for c in range(1, len(D))}
    savings = sorted(((D[0][i] + D[0][j] - D[i][j], i, j)
                      for i in range(1, len(D)) for j in range(i + 1, len(D))), reverse=True)
    find = lambda c: next(k for k, r in routes.items() if c in r)
    for s, i, j in savings:
        ki, kj = find(i), find(j)
        if ki == kj: continue
        ri, rj = routes[ki], routes[kj]
        if sum(demand[c] for c in ri + rj) > capacity: continue
        if ri[-1] == i and rj[0] == j: new = ri + rj
        elif ri[0] == i and rj[-1] == j: new = rj + ri
        elif ri[-1] == i and rj[-1] == j: new = ri + rj[::-1]
        elif ri[0] == i and rj[0] == j: new = ri[::-1] + rj
        else: continue
        routes[ki] = new; del routes[kj]
    return [[0] + r + [0] for r in routes.values()]

nn = nearest_neighbor();  print("Nearest neighbor:", show(nn), length(nn), "km")
opt = two_opt(nn);        print("After 2-opt     :", show(opt), length(opt), "km")
plan = clarke_wright(demand=[0, 4, 3, 5, 2, 6, 4], capacity=10)
for r in plan: print("  truck:", show(r), length(r), "km")
print("Savings plan total:", sum(length(r) for r in plan), "km")
