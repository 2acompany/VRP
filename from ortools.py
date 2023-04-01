from ortools.constraint_solver import routing_enums_pb2, pywrapcp
import numpy as np


def create_data_model(n_nodes, n_vehicles, depot, time_matrix, time_windows, pickup_capacity, delivery_capacity, vehicle_capacity):
    data = {}
    data['distance_matrix'] = time_matrix.tolist()
    data['num_vehicles'] = n_vehicles
    data['depot'] = depot
    data['time_windows'] = time_windows.tolist()
    data['pickup_delivery'] = np.vstack(
        (pickup_capacity, delivery_capacity)).T.tolist()
    data['vehicle_capacities'] = [vehicle_capacity] * n_vehicles
    return data


def print_solution(data, manager, routing, solution):
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            next_node_index = manager.IndexToNode(
                solution.Value(routing.NextVar(index)))
            route_distance += routing.GetArcCostForVehicle(
                node_index, next_node_index, vehicle_id)
            plan_output += ' {0} ->'.format(node_index)
            index = solution.Value(routing.NextVar(index))
        node_index = manager.IndexToNode(index)
        plan_output += ' {0}\n'.format(node_index)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)


def main(n_nodes, n_vehicles, depot, time_matrix, time_windows, pickup_capacity, delivery_capacity, vehicle_capacity):
    data = create_data_model(n_nodes, n_vehicles, depot, time_matrix,
                             time_windows, pickup_capacity, delivery_capacity, vehicle_capacity)

    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_windows'][from_node][0] + data['distance_matrix'][from_node][to_node]

    time_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.AddDimension(
        time_callback_index,
        1440,  # maximum time per vehicle
        1440,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        'Time')
    time_dimension = routing.GetDimensionOrDie('Time')
    for node in range(n_nodes):
        start = data['time_windows'][node][0]
        end = data['time_windows'][node][1]
        time_dimension.CumulVar(manager.NodeToIndex(node)).SetRange(start, end)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['pickup_delivery'][from_node][0] - data['pickup_delivery'][from_node][1]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    capacity_dimension = routing.GetDimensionOrDie('Capacity')

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('No solution found !')


n_nodes = 6
n_vehicles = 6
depot = 0
time_matrix = np.array([[0, 1, 1, 1, 1, 1],
                        [1, 0, 1, 1, 1, 1],
                        [1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 0, 1],
                        [1, 1, 1, 1, 1, 0]])
time_windows = np.array([[0, 2], [0, 2], [0, 2], [
                        0, 2], [0, 2], [0, 2]])
pickup_capacity = np.array([0, 1, 1, 1, 1, 1])
delivery_capacity = np.array([1, 0, 1, 0, 1, 1])
vehicle_capacity = 15

main(n_nodes, n_vehicles, depot, time_matrix, time_windows,
     pickup_capacity, delivery_capacity, vehicle_capacity)


"""""
This code creates a data model, sets up a routing model with constraints for time windows and capacity,
 solves the problem, and prints out the results. Note that the time window constraints are modeled as a separate dimension,
 and the capacity constraints are modeled as a dimension with vehicle capacities. The example data inputs and results are
 just for demonstration purposes and can be replaced with your own data.
"""