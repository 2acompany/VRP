import VRPTimeLimitAPI
import VRPTimeLimitAPIRandom
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Vehicle Routing Problem API",
    description="API for solving Vehicle Routing Problem using time limits.",
    version="1.0",
    docs_url="/swagger",
    redoc_url="/redoc",
)

class VRPModelInput(BaseModel):
    distance_matrix: list
    num_vehicles: int
    depot: int


class VRPModelInputRandomLocation(BaseModel):
    num_locations: int
    num_vehicles: int
    depot: int

@app.post('/vehicle_routes', response_model=dict)
def vehicle_routes(data: VRPModelInput):
    """
    Solve the Vehicle Routing Problem using time limits.

    Given a distance matrix, the number of vehicles available, and a depot location,
    this endpoint uses the VRPTimeLimitAPI library to generate a set of vehicle routes
    that minimize total travel time, subject to a time limit for each route.

    **Input**
    - `distance_matrix`: A list of lists representing the distance matrix between locations.
    - `num_vehicles`: The number of vehicles available for routing.
    - `depot`: The location ID of the depot.

    **Output**
    - `routes`: A list of lists representing the vehicle routes.
    """
    distance_matrix = data.distance_matrix
    num_vehicles = data.num_vehicles
    depot = 0
    routes = VRPTimeLimitAPI.main(distance_matrix, num_vehicles, depot)
    return {"routes": routes}

@app.post('/vehicle_routes_random_location', response_model=dict)
def vehicle_routes_random_location(data: VRPModelInputRandomLocation):
    """
    Solve the Vehicle Routing Problem using time limits.

    Given a Number of location, the number of vehicles available, and a depot location,
    this endpoint uses the VRPTimeLimitAPI library to generate a set of vehicle routes
    that minimize total travel time, subject to a time limit for each route.

    **Input**
    - `num_locations`: The number of Locations Ramdomly Generated on map for routing.
    - `num_vehicles`: The number of vehicles available for routing.
    - `depot`: The location ID of the depot.

    **Output**
    - `routes`: A list of lists representing the vehicle routes.
    """
    num_locations = data.num_locations
    num_vehicles = data.num_vehicles
    depot = 0
    routes = VRPTimeLimitAPIRandom.main(num_locations, num_vehicles, depot)
    return {"routes": routes}
#run this in console 
#uvicorn AppFastAPI:app --reload
#python -m venv env
#env\Scripts\activate.bat
#pip install Flask and all other dependencies
#pip freeze > requirements.txt - To create the file, run this
#pip install -r requirements.txt- This will install all the packages listed in the requirements.txt file and their dependencies.
#env\Scripts\deactivate.bat - This command will deactivate the virtual environment and restore your system's original PATH
#python AppFastAPI.py - To run Code