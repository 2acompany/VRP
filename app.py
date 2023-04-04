from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
import folium
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

# app = FastAPI(
#     title="Vehicle Routing Problem API",
#     description="API for solving Vehicle Routing Problem using time limits.",
#     version="1.0",
#     docs_url="/swagger",
#     redoc_url="/redoc",
# )

# # Serve Swagger UI from the '/docs' route
# app.mount("/docs", StaticFiles(directory="swagger-ui"), name="docs")
# @app.get("/docs", response_class=HTMLResponse)
# async def read_docs():
#     return """
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <title>VRP API - Swagger UI</title>
#             <link rel="stylesheet" type="text/css" href="/docs/swagger-ui.css">
#             <script src="/docs/swagger-ui-bundle.js"></script>
#             <script src="/docs/swagger-ui-standalone-preset.js"></script>
#         </head>
#         <body>
#             <div id="swagger-ui"></div>
#             <script>
#                 const ui = SwaggerUIBundle({
#                     url: "/openapi.json",
#                     dom_id: '#swagger-ui',
#                     presets: [
#                         SwaggerUIBundle.presets.apis,
#                         SwaggerUIStandalonePreset
#                     ],
#                     layout: "BaseLayout",
#                     deepLinking: true,
#                 })
#             </script>
#         </body>
#     </html>
#     """

# Serve ReDoc from the '/redoc' route
# app.mount("/redoc", StaticFiles(directory="redoc"), name="redoc")
# @app.get("/redoc", response_class=HTMLResponse)
# async def read_redoc():
#     return """
#     <!DOCTYPE html>
#     <html>
#         <head>
#             <title>VRP API - ReDoc</title>
#             <link rel="stylesheet" type="text/css" href="/redoc/redoc.css">
#             <script src="/redoc/redoc.standalone.js"></script>
#         </head>
#         <body>
#             <redoc spec-url='/openapi.json'></redoc>
#         </body>
#     </html>
#     """

# Configure CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
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
    return jsonify({"routes": routes})
    
@app.route("/randomnodes")
def map():
    return MapFolium.map()

if __name__ == "__main__":
    app.run(debug=True,  port=5000)
    
    
    
#To run this in console 
#python app.py
#python -m venv env
#env\Scripts\activate.bat
#pip install Flask, ...... and all other dependencies
#pip freeze > requirements.txt - To create the file, run this
#pip install -r requirements.txt- This will install all the packages listed in the requirements.txt file and their dependencies.
#env\Scripts\deactivate.bat - This command will deactivate the virtual environment and restore your system's original PATH