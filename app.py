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
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class VRPModelInput(BaseModel):
    distance_matrix: list
    num_vehicles: int
    depot: int

class VRPModelInputRandomLocation(BaseModel):
    num_locations: int
    num_vehicles: int
    depot: int
    
@app.route('/vehicle_routes', methods=['POST'])
@cross_origin()
def vehicle_routes():
    data = request.json
    distance_matrix = data['distance_matrix']
    num_vehicles = data['num_vehicles']
    depot = 0
    routes = VRPTimeLimitAPI.main(distance_matrix, num_vehicles, depot)
    return jsonify({"routes": routes})

@app.route('/vehicle_routes_random_location', methods=['POST'])
@cross_origin()
def vehicle_routes_random_location():

    data = request.json
    num_locations = data['num_locations']
    num_vehicles = data['num_vehicles']
    depot = 0
    routes = VRPTimeLimitAPIRandom.main(num_locations, num_vehicles, depot)
    return jsonify({"routes": routes})
    
@app.route("/randomnodes")
@cross_origin()
def map():
    return MapFolium.map()

if __name__ == "__main__":
    app.run(debug=True,  port=5000)
    
    
    
#To run this in console 
#python app.py or flask run 
