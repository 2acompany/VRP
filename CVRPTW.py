from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math

# def haversine_distance(lat1, lon1, lat2, lon2):
#     # Convert latitude and longitude to radians
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

#     # Haversine formula
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
#     c = 2 * math.asin(math.sqrt(a))
#     r = 6371  # Radius of earth in kilometers
#     return c * r

# # Example locations with latitude and longitude
# locations = [
#     {'name': 'A', 'lat': 52.3702, 'lon': 4.8952},
#     {'name': 'B', 'lat': 51.5074, 'lon': -0.1278},
#     {'name': 'C', 'lat': 48.8566, 'lon': 2.3522},
#     {'name': 'D', 'lat': 41.9028, 'lon': 12.4964},
#     {'name': 'E', 'lat': 40.4168, 'lon': -3.7038},
#     {'name': 'F', 'lat': 41.3851, 'lon': 2.1734},
#     {'name': 'G', 'lat': 45.4642, 'lon': 9.1900},
#     {'name': 'H', 'lat': 52.5200, 'lon': 13.4050},
#     {'name': 'I', 'lat': 51.7520, 'lon': -1.2577},
#     {'name': 'J', 'lat': 51.5074, 'lon': 0.1278}
# ]

# # Create the time matrix using haversine distance formula
# n_nodes = len(locations)
# time_matrix = []
# for i in range(n_nodes):
#     row = []
#     for j in range(n_nodes):
#         if i == j:
#             row.append(0)
#         else:
#             dist = haversine_distance(locations[i]['lat'], locations[i]['lon'], locations[j]['lat'], locations[j]['lon'])
#             dist = int(dist)
#             time = dist / 50  # Assuming average speed of 50 km/h
#             time=int(time)
#             row.append(time)
#     time_matrix.append(row)

# print(time_matrix)

n_nodes =10
n_vehicles = 3
depot = 0
time_matrix = [
    [0, 3, 6, 5, 8, 8, 6, 2, 3, 1],
    [3, 0, 1, 6, 2, 2, 8, 6, 7, 1],
    [6, 1, 0, 5, 9, 5, 1, 8, 1, 5],
    [5, 6, 5, 0, 5, 4, 4, 3, 3, 4],
    [8, 2, 9, 5, 0, 4, 7, 4, 4, 3],
    [8, 2, 5, 4, 4, 0, 6, 9, 1, 8],
    [6, 8, 1, 4, 7, 6, 0, 6, 7, 2],
    [2, 6, 8, 3, 4, 9, 6, 0, 6, 7],
    [3, 7, 1, 3, 4, 1, 7, 6, 0, 9],
    [1, 1, 5, 4, 3, 8, 2, 7, 9, 0]
]

time_windows = [(0, 300), (160, 500), (0, 300), (0, 300), (160, 500),
                (160, 500), (160, 500), (160, 500), (0, 300), (0, 300)]
pickup_capacity = [0, 2, 2, 3, 1, 2, 1, 2, 1, 2]
delivery_capacity = [0, 1, 2, 1, 2, 1, 2, 1, 2, 1]
vehicle_capacity = 4

data = {
    'num_nodes': n_nodes,
    'num_vehicles': n_vehicles,
    'depot': depot,
    'time_matrix': time_matrix,
    'time_windows': time_windows,
    'pickup_capacity': pickup_capacity,
    'delivery_capacity': delivery_capacity,
    'vehicle_capacity': vehicle_capacity
}


def create_data_model(n_nodes, n_vehicles, depot, time_matrix, time_windows, pickup_capacity, delivery_capacity, vehicle_capacity):
    """Stores the data for the problem."""
    data = {}
    data['num_nodes'] = n_nodes
    data['num_vehicles'] = n_vehicles
    data['depot'] = depot
    data['time_matrix'] = time_matrix
    data['time_windows'] = time_windows
    data['pickup_capacity'] = pickup_capacity
    data['delivery_capacity'] = delivery_capacity
    data['vehicle_capacity'] = vehicle_capacity
    return data


def create_distance_callback(data):
    """Creates callback to return distance between points."""
    def distance_callback(from_node, to_node):
        return int(data['time_matrix'][from_node][to_node])
    return distance_callback


def create_demand_callback(data):
    """Creates callback to get demands at each location."""
    def demand_callback(from_node):
        if from_node == data['depot']:
            return 0
        elif from_node < data['num_nodes'] / 2:
            return data['pickup_capacity'][from_node]
        else:
            return -data['delivery_capacity'][from_node - data['num_nodes'] // 2]
    return demand_callback


def create_time_callback(data, distance_callback):
    """Creates callback to get total times between locations."""
    def time_callback(from_node, to_node):
        travel_time = distance_callback(from_node, to_node)
        time = data['time_windows'][to_node][0] - travel_time
        if time < data['time_windows'][from_node][0]:
            time = data['time_windows'][from_node][0]
        if time + travel_time > data['time_windows'][to_node][1]:
            return 1000000  # Return large value for infeasible arcs
        return time + travel_time
    return time_callback


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    max_route_distance = 0
    num_vehicles = data['num_vehicles']
    depot = data['depot']
    routes = []
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route = []
        route_distance = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        node_index = manager.IndexToNode(index)
        route.append(node_index)
        routes.append(route)
        max_route_distance = max(route_distance, max_route_distance)
    print('Routes:')
    for i, route in enumerate(routes):
        print('Vehicle {}: {}'.format(i, route))
    print('Maximum distance of the routes: {}m'.format(max_route_distance))


def solve_vrp(n_nodes, n_vehicles, depot, time_matrix, time_windows, pickup_capacity, delivery_capacity, vehicle_capacity):
    """Solves the VRP problem."""
    # Instantiate the data problem.
    data = create_data_model(n_nodes, n_vehicles, depot, time_matrix,
                             time_windows, pickup_capacity, delivery_capacity, vehicle_capacity)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        data['num_nodes'], data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Define distance callback.
    distance_callback = create_distance_callback(data)
    routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)

    # Define demand callback.
    demand_callback = create_demand_callback(data)
    add_dimension = routing.AddDimensionWithVehicleCapacity(
        demand_callback,
        0,  # Null capacity slack
        data['vehicle_capacity'],  # Vehicle maximum capacity
        True,  # Start cumul to zero
        'Capacity')
    for node in range(1, data['num_nodes']):
        add_dimension.CumulVar(routing.End(node)).RemoveInterval(
            0, data['time_windows'][node][0])
        add_dimension.CumulVar(node).RemoveInterval(
            data['time_windows'][node][1], routing.End(node))

    # Add time window constraints.
    time_callback = create_time_callback(data, distance_callback)
    add_dimension = routing.AddDimension(
        time_callback,
        data['num_nodes'],  # Dimension name
        2*60*60,  # Maximum time in seconds per vehicle
        False,  # Don't force start cumul to zero.
        'Time')
    for node in range(data['num_nodes']):
        index = manager.NodeToIndex(node)
        add_dimension.CumulVar(index).SetRange(
            data['time_windows'][node][0], data['time_windows'][node][1])

    # Set first solution heuristic (cheapest addition).
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('No solution found !')


# Solve the problem.
solve_vrp(n_nodes, n_vehicles, depot, time_matrix, time_windows, pickup_capacity, delivery_capacity, vehicle_capacity)
