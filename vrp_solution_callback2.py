#!/usr/bin/env python3
# Copyright 2010-2022 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START program]
"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.

   The solver stop after improving its solution 15 times or after 5 seconds.

   Distances are in meters.
"""

# [START import]
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math

# [END import]

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

# Example locations with latitude and longitude
locations = [
    {'name': 'A', 'lat': 52.3702, 'lon': 4.8952},
    {'name': 'B', 'lat': 51.5074, 'lon': -0.1278},
    {'name': 'C', 'lat': 48.8566, 'lon': 2.3522},
    {'name': 'D', 'lat': 41.9028, 'lon': 12.4964},
    {'name': 'E', 'lat': 40.4168, 'lon': -3.7038},
    {'name': 'F', 'lat': 41.3851, 'lon': 2.1734},
    {'name': 'G', 'lat': 45.4642, 'lon': 9.1900},
    {'name': 'H', 'lat': 52.5200, 'lon': 13.4050},
    {'name': 'I', 'lat': 51.7520, 'lon': -1.2577},
    {'name': 'J', 'lat': 51.5074, 'lon': 0.1278}
]

# Create the time matrix using haversine distance formula
n_nodes = len(locations)
time_matrix = []
for i in range(n_nodes):
    row = []
    for j in range(n_nodes):
        if i == j:
            row.append(0)
        else:
            dist = haversine_distance(locations[i]['lat'], locations[i]['lon'], locations[j]['lat'], locations[j]['lon'])
            dist = int(dist)
            time = dist / 50  # Assuming average speed of 50 km/h
            time=int(time)
            row.append(time)
    time_matrix.append(row)

print(time_matrix)

# [START data_model]
def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix']=time_matrix
    data['num_vehicles'] = 4
    data['depot'] = 0
    return data
    # [END data_model]

def get_solution_routes(routing_manager: pywrapcp.RoutingIndexManager,
                        routing_model: pywrapcp.RoutingModel) :
    """Returns a list of solution routes for each vehicle."""
    solution_routes = []
    for vehicle_id in range(routing_manager.GetNumberOfVehicles()):
        index = routing_model.Start(vehicle_id)
        route = []
        while not routing_model.IsEnd(index):
            node_index = routing_manager.IndexToNode(index)
            route.append(node_index)
            index = routing_model.NextVar(index).Value()
        node_index = routing_manager.IndexToNode(index)
        route.append(node_index)
        route_str = f'Route for vehicle {vehicle_id}: {route}'
        solution_routes.append(route_str)
    return solution_routes


# [START solution_callback_printer]
def print_solution(routing_manager: pywrapcp.RoutingIndexManager,
                   routing_model: pywrapcp.RoutingModel):
    """Prints solution on console."""
    print('################')
    print(f'Solution objective: {routing_model.CostVar().Value()}')
    total_distance = 0
    solution_routes = get_solution_routes(routing_manager, routing_model)
    for route_str in solution_routes:
        print(route_str)
    total_distance += routing_model.GetTotalCost()
    print(f'Total Distance of all routes: {total_distance}')   
# [END solution_callback_printer]

class SolutionCallback:
    """Create a solution callback."""

    def __init__(self, manager: pywrapcp.RoutingIndexManager,
                 model: pywrapcp.RoutingModel, limit: int):
        self._routing_manager = manager
        self._routing_model = model
        self._counter = 0
        self._counter_limit = limit
        self.objectives = []
        self.solution_routes = []

    def __call__(self):
        objective = int(self._routing_model.CostVar().Value())
        if not self.objectives or objective < self.objectives[-1]:
            self.objectives.append(objective)
            self.solution_routes = get_solution_routes(self._routing_manager, self._routing_model)
            self._counter += 1
        if self._counter > self._counter_limit:
            self._routing_model.solver().FinishCurrentSearch()

# [START solution_callback]
class SolutionCallback:
    """Create a solution callback."""

    def __init__(self, manager: pywrapcp.RoutingIndexManager,
                 model: pywrapcp.RoutingModel, limit: int):
        self._routing_manager = manager
        self._routing_model = model
        self._counter = 0
        self._counter_limit = limit
        self.objectives = []

    def __call__(self):
        objective = int(self._routing_model.CostVar().Value())
        if not self.objectives or objective < self.objectives[-1]:
            self.objectives.append(objective)
            print_solution(self._routing_manager, self._routing_model)
            self._counter += 1
        if self._counter > self._counter_limit:
            self._routing_model.solver().FinishCurrentSearch()
# [END solution_callback]


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    # [START data]
    data = create_data_model()
    # [END data]

    # Create the routing index manager.
    # [START index_manager]
    routing_manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                                   data['num_vehicles'],
                                                   data['depot'])
    # [END index_manager]

    # Create Routing Model.
    # [START routing_model]
    routing_model = pywrapcp.RoutingModel(routing_manager)

    # [END routing_model]

    # Create and register a transit callback.
    # [START transit_callback]
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = routing_manager.IndexToNode(from_index)
        to_node = routing_manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing_model.RegisterTransitCallback(
        distance_callback)
    # [END transit_callback]

    # Define cost of each arc.
    # [START arc_cost]
    routing_model.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    # [END arc_cost]

    # Add Distance constraint.
    # [START distance_constraint]
    dimension_name = 'Distance'
    routing_model.AddDimension(
        transit_callback_index,
        0,  # no slack
        2549,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing_model.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)
    # [END distance_constraint]

    # Attach a solution callback.
    # [START attach_callback]
    solution_callback = SolutionCallback(routing_manager, routing_model, 15)
    routing_model.AddAtSolutionCallback(solution_callback)
    # [END attach_callback]

    # Setting first solution heuristic.
    # [START parameters]
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(5)
    # [END parameters]

    # Solve the problem.
    # [START solve]
    solution = routing_model.SolveWithParameters(search_parameters)
    # [END solve]

    # Print solution on console.
    # [START print_solution]
    if solution:
        print(f'Best objective: {solution_callback.objectives[-1]}')
        solution_routes = solution_callback.solution_routes
        for route_str in solution_routes:
            print(route_str)
    else:
        print('No solution found !')
    # [END print_solution]


if __name__ == '__main__':
    main()
# [END program]
