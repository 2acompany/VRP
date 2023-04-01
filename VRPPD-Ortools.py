from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model(n_nodes, n_vehicles, depot, distance_matrix, pickup_capacity, delivery_capacity, vehicle_capacity):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distance_matrix
    data['pickup_delivery'] = [(i + 1, n_nodes + i + 1) for i in range(n_nodes)]
    data['vehicle_capacities'] = [vehicle_capacity] * n_vehicles
    data['pickup_capacities'] = [pickup_capacity] * n_nodes
    data['delivery_capacities'] = [delivery_capacity] * n_nodes
    data['num_vehicles'] = n_vehicles
    data['depot'] = depot
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            plan_output += ' {} -> '.format(node_index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        node_index = manager.IndexToNode(index)
        plan_output += '{}\n'.format(node_index)
        route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)


def solve_vrp(n_nodes, n_vehicles, depot, distance_matrix, pickup_capacity, delivery_capacity, vehicle_capacity):
    """Solves the VRP pickup and delivery problem."""
    # Create the data model.
    data = create_data_model(n_nodes, n_vehicles, depot, distance_matrix, pickup_capacity, delivery_capacity, vehicle_capacity)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        return data['distance_matrix'][from_index][to_index]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc for each vehicle.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Pickup and Deliveries.
    for index in range(n_nodes):
        routing.AddPickupAndDelivery(data['pickup_delivery'][index][0], data['pickup_delivery'][index][1])
        routing.solver().Add(
            routing.SizeVar(data['pickup_delivery'][index][0]) == data['pickup_capacities'][index])
        routing.solver().Add(
            routing.SizeVar(data['pickup_delivery'][index][1]) == -data['delivery_capacities'][index])

    # Define vehicle capacities.
    def vehicle_capacity_callback(vehicle_id):
        """Returns the capacity of the vehicle."""
        return data['vehicle_capacities'][vehicle_id]

    routing.AddDimensionWithVehicleCapacity(
        transit_callback_index,
        0,  # no slack
        [vehicle_capacity_callback],
        True,  # start cum
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)



n_nodes = 5
n_vehicles = 2
depot = 0
distance_matrix = [[0, 1, 2, 4, 5],
[1, 0, 3, 2, 4],
[2, 3, 0, 5, 2],
[4, 2, 5, 0, 1],
[5, 4, 2, 1, 0]]
pickup_capacity = 10
delivery_capacity = -10
vehicle_capacity = 20
solve_vrp(n_nodes, n_vehicles, depot, distance_matrix, pickup_capacity, delivery_capacity, vehicle_capacity)