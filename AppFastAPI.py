import VRPTimeLimitAPI
import VRPTimeLimitAPIRandom
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel

app = Flask(__name__)
CORS(app)

class VRPModelInput(BaseModel):
    distance_matrix: list
    num_vehicles: int
    depot: int

class VRPModelInputRandomLocation(BaseModel):
    num_locations: int
    num_vehicles: int
    depot: int

@app.route('/vehicle_routes', methods=['POST'])
def vehicle_routes():
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
    data = request.json
    distance_matrix = data['distance_matrix']
    num_vehicles = data['num_vehicles']
    depot = 0
    routes = VRPTimeLimitAPI.main(distance_matrix, num_vehicles, depot)
    return jsonify({"routes": routes})

@app.route('/vehicle_routes_random_location', methods=['POST'])
def vehicle_routes_random_location():
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
    data = request.json
    num_locations = data['num_locations']
    num_vehicles = data['num_vehicles']
    depot = 0
    routes = VRPTimeLimitAPIRandom.main(num_locations, num_vehicles, depot)
    return jsonify({"routes": routes})

if __name__ == '__main__':
    app.run(debug=True,  port=8000)

#run this in console 
#uvicorn AppFastAPI:app --reload
#python -m venv env
#env\Scripts\activate.bat
#pip install Flask and all other dependencies
#pip freeze > requirements.txt - To create the file, run this
#pip install -r requirements.txt- This will install all the packages listed in the requirements.txt file and their dependencies.
#env\Scripts\deactivate.bat - This command will deactivate the virtual environment and restore your system's original PATH
#python AppFastAPI.py - To run Code