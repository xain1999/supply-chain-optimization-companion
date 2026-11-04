# Supply Chain Optimization: Companion Code

Companion files for the book ***Supply Chain Optimization: A Practical Guide to Linear Programming,
Transportation, Inventory, and Production Planning: From Linear Programming to Real-World Supply Chain
Decisions*** by Mohammed Islam Hadjoudj.

First Edition (2026) · companion package version 1.2

Every main model in the book, as code you can run and spreadsheets you can solve.
Each script reproduces the numbers printed in the book. Where a model has several
optimal solutions with the same objective (the transportation example, for instance),
a different solver version may return a different but equally good plan. Change the data to your own
operation and the answers follow.

## Download

Clone this repository, or click **Code > Download ZIP** at the top of this page.
The same files are also available on Google Drive:
https://drive.google.com/drive/folders/1eNGc0C7Wnv7w2A6_D90f14fRpVrbpJCG?usp=sharing

## What's inside

```
python/     23 runnable scripts, named by chapter
excel/      Solver-ready workbooks (open, then Data > Solver)
notebook/   supply_chain_models.ipynb: every script in one notebook
```

## Tested environment

Python 3.12.3, PuLP 4.0.0, HiGHS 1.13.1 (`highspy`), OR-Tools 9.15.6755, pandas 3.0.2,
NumPy 2.4.4, SciPy 1.17.1. The PuLP 3.x notes were tested with PuLP 3.3.0.
All 23 scripts were checked again in November 2026 with PuLP 4.2.0 and HiGHS 1.15.1
and still reproduce the book's numbers.

## Installing

You need **Python 3.12 or newer**. Then, from a terminal:

```bash
pip install "pulp[highs]" ortools scipy numpy pandas openpyxl
```

Run any script with `python python/ch01_two_product_plant.py`.

**PuLP 4.0.** The scripts use version 4.0 of PuLP (September 2026), which no longer
bundles a solver, hence `pulp[highs]` above. Variables are created with
`model.add_variable(...)` and models are solved with `model.solve(HiGHS(msg=False))`.
On older Python you will get PuLP 3.x. Replace `model.add_variable(...)` with
`LpVariable(...)` and `HiGHS(msg=False)` with `PULP_CBC_CMD(msg=False)`.
Chapter 18 and Appendix D explain both styles.

## Scripts by chapter

| Ch. | File | Model |
|----:|------|-------|
| 1 | `ch01_two_product_plant.py` | Two-product plant |
| 2 | `ch02_staffing.py` | Five-day work week staffing |
| 3 | `ch03_sensitivity_and_dual.py` | Shadow prices and the dual |
| 4 | `ch04_cost_vs_carbon.py` | Cost against carbon: the epsilon-constraint method |
| 4 | `ch04_product_launch.py` | Product launch with setups, minimum lots, and a dependency |
| 5 | `ch05_transportation.py` | Transportation problem with an optional lane cap |
| 6 | `ch06_networks.py` | Shortest path, assignment, and minimum-cost flow |
| 7 | `ch07_routing_heuristics.py` | Nearest neighbor, 2-opt, and Clarke-Wright savings |
| 7 | `ch07_routing_ortools.py` | Capacitated vehicle routing with OR-Tools |
| 8 | `ch08_covering_pmedian.py` | Set covering and p-median location |
| 9 | `ch09_warehouse.py` | Slotting, forward pick allocation, and dock door assignment |
| 10 | `ch10_forecasting.py` | Moving average, exponential smoothing, and Holt's method |
| 11 | `ch11_inventory.py` | EOQ, cost penalty, reorder point, and newsvendor ratio |
| 12 | `ch12_inventory_policies.py` | Periodic review, fill rate, ABC, and space-constrained ordering |
| 13 | `ch13_procurement.py` | Quantity discounts and supplier selection |
| 14 | `ch14_planning.py` | Aggregate production plan and workforce planning |
| 15 | `ch15_lot_sizing_scheduling.py` | Wagner-Whitin, Silver-Meal, dispatching rules, and Johnson's rule |
| 16 | `ch16_uncertainty.py` | Scenario planning, EVPI, and Monte Carlo simulation |
| 17 | `ch17_carbon_abatement.py` | Carbon abatement curve from an emissions-cap sweep |
| 18 | `ch18_excel_data_model.py` | Reading model data from Excel and writing the plan back |
| 20 | `ch20_meridian_location.py` | Meridian Foods fixed-charge location model |
| 21 | `ch21_last_mile.py` | Last-mile delivery: daily routes versus alternate-day zones (Case A) |
| 21 | `ch21_store_allocation.py` | Allocating a scarce shipment by marginal value (Case B) |

## Excel workbooks

| Workbook | Chapter | Reproduces |
|----------|---------|------------|
| `two_product_plant.xlsx` | 1, 18 | Contribution $1,700 |
| `transportation.xlsx` | 5, 18 | Total cost $5,650 |

Each workbook has a *Model* sheet (yellow decision cells, a `SUMPRODUCT` objective,
constraint cells) and an *Instructions* sheet listing exactly what to enter in the
Solver dialog. Enable Solver via *File > Options > Add-ins > Excel Add-ins > Solver*,
and choose the **Simplex LP** engine.

## Record your versions

When you adapt a model for real use, save the library versions it was tested with:
`pip freeze > requirements.txt`.

---
*These files are provided for learning. The models are simplified to teach the
method. Adapt them to the full complexity of your own operation before relying on
the results.*

## License

The code in this repository is released under the MIT License (see `LICENSE`).
The book itself is copyright © 2026 Mohammed Islam Hadjoudj. All rights reserved.
