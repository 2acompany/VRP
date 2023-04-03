
# [START program]
"""Vehicles Routing Problem (VRP)."""
"""Time Matrix Has Generated Randomly """

# [START import]
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import random
# [END import]


# [START solution_printer]
def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    for vehicle_id in range(manager.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))
# [END solution_printer]


# [START Route solution]
def get_solution_routes(manager, routing, solution):
    """Returns the solution routes for each vehicle."""
    routes = [[]]
    for vehicle_id in range(manager.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes
# [END Route solution]



# Generate a time matrix for the locations
def create_data_time_matrix(num_locations):
    time_matrix = []
    for i in range(num_locations):
        row = []
        for j in range(num_locations):
            if i == j:
                # Set the diagonal elements to 0 (travel time from a location to itself is 0)
                row.append(0)
            else:
                # Generate a random travel time between 1 and 100
                row.append(random.randint(100, 1000))
        time_matrix.append(row)

        # Print the time matrix
        print(time_matrix)
    return time_matrix


# [START create data model ]
def create_data_model(num_locations, num_vehicles, depot):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = create_data_time_matrix(num_locations)
    data['num_vehicles'] = num_vehicles
    data['depot'] = depot
    return data
# [END create data model]

def main(num_locations, num_vehicles, depot):
    """Solve the CVRP problem."""
    route=[[]]
    # Instantiate the data problem.
    # Create the data model.
    data = create_data_model(num_locations, num_vehicles, depot)

    # Create the routing index manager.
    # [START index_manager]
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    # [END index_manager]

    # Create Routing Model.
    # [START routing_model]
    routing = pywrapcp.RoutingModel(manager)

    # [END routing_model]

    # Create and register a transit callback.
    # [START transit_callback]
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    # [END transit_callback]

    # Define cost of each arc.
    # [START arc_cost]
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # [END arc_cost]

    # Add Distance constraint.
    # [START distance_constraint]
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)
    # [END distance_constraint]

    # Setting first solution heuristic.
    # [START parameters]
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.log_search = True
    search_parameters.time_limit.FromSeconds(50)
    # [END parameters]

    # Solve the problem.
    # [START solve]
    solution = routing.SolveWithParameters(search_parameters)
    # [END solve]
    def do_nothing():
        # This function does nothing and returns None
        return None
    print("There is no option for Optimal Routing! ")  # Output: None
    # Print solution on console.
    # [START print_solution]
    if solution:
        print_solution(manager, routing, solution)
        routes = get_solution_routes(manager, routing, solution)
        for i, route in enumerate(routes):
            print(f'Route for vehicle {i}: {route}')
    else:
        do_nothing()
        
    # [END print_solution]
    return routes

#Sample Test The code
num_locations =4
num_vehicles=1
depot=0
if __name__ == '__main__':
    main(num_locations, num_vehicles, depot)   
# [END program]
