"""
Capacitated vehicle routing with OR-Tools
Companion file for "Supply Chain Optimization" by Mohammed Islam Hadjoudj, Chapter 7.
Book answer: three trucks, 76 km in total.
Requires: pip install "pulp[highs]"   (PuLP 4.0+, Python 3.12+)
          pip install ortools
"""
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

D = [[0, 8, 9,10, 9,10,10], [8, 0, 8,14, 7,10,18], [9, 8, 0, 8, 1,17,16],
     [10,14,8, 0, 9,21,11], [9, 7, 1, 9, 0,16,16], [10,10,17,21,16,0,19],
     [10,18,16,11,16,19,0]]
demand, capacity, trucks = [0, 4, 3, 5, 2, 6, 4], 10, 3
names = ["DC", "A", "B", "C", "D", "E", "F"]

manager = pywrapcp.RoutingIndexManager(len(D), trucks, 0)
routing = pywrapcp.RoutingModel(manager)
def distance(i, j):
    return D[manager.IndexToNode(i)][manager.IndexToNode(j)]
routing.SetArcCostEvaluatorOfAllVehicles(routing.RegisterTransitCallback(distance))
def load(i):
    return demand[manager.IndexToNode(i)]
routing.AddDimensionWithVehicleCapacity(routing.RegisterUnaryTransitCallback(load),
                                        0, [capacity] * trucks, True, "Load")
params = pywrapcp.DefaultRoutingSearchParameters()
params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.SAVINGS
params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
params.time_limit.seconds = 5
solution = routing.SolveWithParameters(params)

total = 0
for v in range(trucks):
    i, stops, km = routing.Start(v), [], 0
    while not routing.IsEnd(i):
        stops.append(names[manager.IndexToNode(i)])
        nxt = solution.Value(routing.NextVar(i))
        km += routing.GetArcCostForVehicle(i, nxt, v)
        i = nxt
    print(f"Truck {v + 1}: {' -> '.join(stops)} -> DC ({km} km)")
    total += km
print("Total distance:", total, "km")
