"""
Moving average, exponential smoothing, and Holt's method
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 10.
Book answers (scored on months 4-12, Holt initialized from months 1-3 only): MAD 8.9 (moving average), 13.1 (smoothing), 5.8 (Holt).
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
(No solver needed for this file.)
"""
demand = [120,132,126,140,135,150,144,158,152,165,160,172]
n = len(demand)

ma = [None] * n
for t in range(3, n):
    ma[t] = sum(demand[t-3:t]) / 3

alpha = 0.3
ses = [None] * n; ses[1] = demand[0]
for t in range(2, n):
    ses[t] = alpha * demand[t-1] + (1 - alpha) * ses[t-1]

a, b = 0.3, 0.2
level, trend = demand[0], (demand[2] - demand[0]) / 2   # uses months 1-3 only
holt = [None] * n
for t in range(1, n):
    holt[t] = level + trend
    new_level = a * demand[t] + (1 - a) * (level + trend)
    trend = b * (new_level - level) + (1 - b) * trend
    level = new_level

def score(f):
    e = [demand[t] - f[t] for t in range(3, n)]
    bias = sum(e) / len(e); mad = sum(abs(x) for x in e) / len(e)
    mape = 100 * sum(abs(demand[t] - f[t]) / demand[t] for t in range(3, n)) / len(e)
    return f"bias {bias:+.1f}, MAD {mad:.1f}, MAPE {mape:.1f}%"

for name, f in [("3-month MA", ma), ("Smoothing", ses), ("Holt", holt)]:
    print(f"{name:11s}: {score(f)}")
print("Holt forecast for month 13:", round(level + trend, 1))
