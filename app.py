from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from geopy.distance import distance
from itertools import permutations
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from VRPTimeLimitAPI import main
import VRPTimeLimitAPI
import VRPTimeLimitAPIRandom
import MapFolium 

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

class VRPModelInput(BaseModel):
    distance_matrix: list
    num_vehicles: int
    depot: int

class VRPModelInputRandomLocation(BaseModel):
    num_locations: int
    num_vehicles: int
    depot: int
    
# @app.route('/vehicle_routes', methods=['POST'])
# def vehicle_routes():
#     data = request.json
#     distance_matrix = data['distance_matrix']
#     num_vehicles = data['num_vehicles']
#     depot = 0
#     routes = VRPTimeLimitAPI(distance_matrix, num_vehicles, depot)
#     response = jsonify({"routes": routes})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add("Access-Control-Allow-Credentials", "true")
#     response.headers.add("Access-Control-Expose-Headers", "Content-Type")
#     response.headers.add("Access-Control-Max-Age", "3600")
#     response.headers.add("Access-Control-Allow-Methods", "POST")
#     response.headers.add("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
#     return response
# @app.route('/vehicle_routes', methods=['POST'])
# def vehicle_routes():
#     data = request.json
#     # process the request data
#     return jsonify({})
# def matrix():
#     return render_template('matrix.html')
@app.route('/')
def home():
    return render_template('routing/parsiMap.html')

# geocoding parsimap route
@app.route('/geocoding/parsiMap')
def geoParsiMap():
    return render_template('geocoding/parsiMap.html')
# geocoding neshan route
@app.route('/geocoding/neshan')
def geoNeshan():
    return render_template('geocoding/neshan.html')

# matching parsimap route
@app.route('/matching/parsiMap')
def matchingParsiMap():
    return render_template('matching/parsiMap.html')
# matching neshan route
@app.route('/matching/neshan')
def matchingNeshan():
    return render_template('matching/neshan.html')

# router parsimap route
@app.route('/router/parsiMap')
def routerParsiMap():
    return render_template('router/parsiMap.html')
# router neshan route
@app.route('/router/neshan')
def routerNeshan():
    return render_template('router/neshan.html')

# routing parsimap route
@app.route('/routing/parsiMap')
def routingParsiMap():
    return render_template('routing/parsiMap.html')
# routing neshan route
@app.route('/routing/neshan')
def routingNeshan():
    return render_template('routing/neshan.html')

# matrix route
@app.route('/matrix')
def matrix():
    return render_template('matrix.html')



@app.route('/vehicle_routes', methods=['POST'])
@cross_origin(supports_credentials=True)
def vehicle_routes():
    data = request.json
    distance_matrix = data['distance_matrix']
    num_vehicles = data['num_vehicles']
    depot = 0
    routes = VRPTimeLimitAPI.main(distance_matrix, num_vehicles, depot)
    return jsonify({"routes": routes})

@app.route('/vehicle_routes_random_location', methods=['POST'])
def vehicle_routes_random_location():

    data = request.json
    num_locations = data['num_locations']
    num_vehicles = data['num_vehicles']
    depot = 0
    routes = VRPTimeLimitAPIRandom.main(num_locations, num_vehicles, depot)
    response = jsonify({"routes": routes})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Expose-Headers", "Content-Type")
    response.headers.add("Access-Control-Max-Age", "3600")
    response.headers.add("Access-Control-Allow-Methods", "POST")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
    return response
    
@app.route("/randomnodes")
def map():
    return MapFolium.map()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    
    
#To run this in console 
#python app.py or flask run 
