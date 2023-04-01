import numpy as np
from collections import defaultdict



def vrp_pickup_delivery(n_nodes, n_vehicles, depot, distance_matrix, pickup_capacity, delivery_capacity, vehicle_capacity):
    # Compute the savings for each pair of nodes
    savings = defaultdict(int)
    for i in range(1, n_nodes):
        for j in range(i+1, n_nodes):
            savings[(i,j)] = distance_matrix[depot][i] + distance_matrix[depot][j] - distance_matrix[i][j]

    # Sort the savings in decreasing order
    sorted_savings = sorted(savings.items(), key=lambda x: -x[1])

    # Initialize the routes for each vehicle
    routes = [[] for _ in range(n_vehicles)]

    # Assign the pickups and deliveries to the routes
    for (i,j), s in sorted_savings:
        if pickup_capacity[i] + delivery_capacity[j] <= vehicle_capacity:
            assigned = False
            for k in range(n_vehicles):
                if assigned:
                    break
                if pickup_capacity[i] <= vehicle_capacity - sum([pickup_capacity[x] + delivery_capacity[x] for x in routes[k]]):
                    for l in range(len(routes[k])-1):
                        if routes[k][l] == i and routes[k][l+1] == depot:
                            routes[k].insert(l+1, j)
                            routes[k].insert(l+1, i)
                            assigned = True
                            break

            if not assigned:
                for k in range(n_vehicles):
                    if assigned:
                        break
                    if len(routes[k]) == 0:
                        if pickup_capacity[i] + delivery_capacity[j] <= vehicle_capacity:
                            routes[k] = [depot, j, i, depot]
                            assigned = True

            if not assigned:
                print("Warning: node", i, "and", j, "were not assigned to any route")

    # Remove empty routes
    routes = [r for r in routes if len(r) > 0]

    # Check that each node is visited exactly once
    visited = set()
    for r in routes:
        for i in range(1, len(r)-1):
            if r[i] in visited:
                print("Error: node", r[i], "is visited more than once")
            visited.add(r[i])
    if len(visited) != n_nodes-1:
        print("Error: not all nodes were visited")

    return routes



n_nodes = 6
n_vehicles = 3
depot = 0
distance_matrix = np.array([[0, 10, 20, 15, 25, 30],
                            [10, 0, 25, 20, 30, 35],
                            [20, 25, 0, 10, 15, 20],
                            [15, 20, 10, 0, 10, 15],
                            [25, 30, 15, 10, 0, 5],
                            [30, 35, 20, 15, 5, 0]])
pickup_capacity = [0, 1, 2, 3, 2, 1]
delivery_capacity = [1, 1, 1, 1, 1, 1]
vehicle_capacity = 5

routes = vrp_pickup_delivery(n_nodes, n_vehicles, depot, distance_matrix, pickup_capacity, delivery_capacity, vehicle_capacity)

print(routes)
