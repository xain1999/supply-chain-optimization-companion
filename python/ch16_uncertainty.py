"""
Scenario planning, EVPI, and Monte Carlo simulation
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 16.
Book answers: best quantity 1,000 (expected $50,400), EVPI $7,200, minimax regret 1,130 ($13,250). With lead-time variability, stockouts rise to about 18.6%.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
          pip install numpy   (no LP solver needed)
"""
import numpy as np

cost, price, rush, rush_max, salvage = 40, 100, 85, 200, 15
scenarios = [(600, 0.3), (1000, 0.5), (1400, 0.2)]

def profit(q, d):
    rushed = min(max(0, d - q), rush_max)
    return price * min(q, d) + (price - rush) * rushed + salvage * max(0, q - d) - cost * q
expected = lambda q: sum(p * profit(q, d) for d, p in scenarios)

best = max(range(0, 1801, 10), key=expected)
foresight = sum(p * profit(d, d) for d, p in scenarios)
print(f"Average-based plan (960): expected ${expected(960):,.0f}")
print(f"Best quantity {best}: expected ${expected(best):,.0f}, EVPI ${foresight - expected(best):,.0f}")

best_case = {d: profit(d, d) for d, _ in scenarios}
max_regret = lambda q: max(best_case[d] - profit(q, d) for d, _ in scenarios)
q_mr = min(range(0, 2001), key=max_regret)          # every whole-number quantity
print(f"Minimax regret: produce {q_mr}, maximum regret ${max_regret(q_mr):,.0f}, expected ${expected(q_mr):,.0f}")

rng = np.random.default_rng(42); N = 200_000; reorder_point = 249.5
fixed = rng.normal(50, 15, (N, 4)).sum(axis=1)
lead = rng.integers(3, 6, N); days = rng.normal(50, 15, (N, 5))
variable = (days * (np.arange(5)[None, :] < lead[:, None])).sum(axis=1)
print(f"Stockout rate, fixed 4-day lead time : {(fixed > reorder_point).mean():.2%}")
print(f"Stockout rate, 3-5 day lead time     : {(variable > reorder_point).mean():.2%}")
print(f"Reorder point for 5% with variability: {np.percentile(variable, 95):.0f}")
