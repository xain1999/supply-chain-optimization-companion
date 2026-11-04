"""
Cost against carbon: the epsilon-constraint method
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 4.
Truck versus rail for 1,000 tons under a series of CO2 caps. Book answers: $40,000 uncapped, $44,286 at 80 t, $50,500 at the 51 t minimum.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
"""
from pulp import LpProblem, LpMinimize, HiGHS, value

for cap in [None, 80, 70, 60, 51]:
    m = LpProblem("modes", LpMinimize)
    truck = m.add_variable("truck_tons", lowBound=0)
    rail = m.add_variable("rail_tons", lowBound=0, upBound=700)
    m += 40 * truck + 55 * rail
    m += truck + rail == 1000
    if cap is not None:
        m += 0.10 * truck + 0.03 * rail <= cap
    m.solve(HiGHS(msg=False))
    co2 = 0.10 * truck.value() + 0.03 * rail.value()
    print(f"cap {cap}: cost ${value(m.objective):,.0f}, rail {rail.value():.0f} t, CO2 {co2:.1f} t")
