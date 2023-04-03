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
    
@app.route("/randomnodes")
def map():
    # Define the latitude and longitude bounds for Tehran city limits
    tehran_limits = [(35.4904, 51.1424), (35.8496, 51.6814)]

    # Number of nodes
    num_nodes = random.randint(50, 50)

    # Generate random latitude and longitude coordinates for each node within Tehran city limits
    coords = [(random.uniform(tehran_limits[0][0], tehran_limits[1][0]), 
               random.uniform(tehran_limits[0][1], tehran_limits[1][1])) for _ in range(num_nodes)]

    # Calculate the distance matrix between the nodes
    dist_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                continue
            dist_matrix[i][j] = int(distance(coords[i], coords[j]).km)
    for row in dist_matrix:
        print(row)
        
    #Get routes from vrp solution
    routes= main(dist_matrix, 5, 0)

    # Create a map centered on Tehran
    m = folium.Map(location=[35.6994, 51.3377], zoom_start=9)
    m.add_child(folium.LatLngPopup())

    # Add the cartodbdark_matter tile layer to the map
    #folium.TileLayer('cartodbdark_matter').add_to(m)

    

    # Add polylines between the nodes
    # for i in range(num_nodes):
    #     for j in range(i+1, num_nodes):
    #         folium.PolyLine(locations=[coords[i], coords[j]], color='red' ,opacity=0.01).add_to(m)
 

 
        
    #diffrent random color for each poly line and marker
    for route in routes:
        color = '#' + ''.join(random.choice('0123456789ABCDEF') for i in range(6))
        for i in range(len(route) - 1):
            start_node = route[i]
            end_node = route[i+1]
            folium.PolyLine(locations=[coords[start_node], coords[end_node]], color=color).add_to(m)
            folium.Marker(location=coords[start_node], icon=folium.Icon(icon='star', color=color,tooltip=f'Node {i}')).add_to(m)


            
    # Add markers for the Depot
    for i in range(1):
        color = 'green' if i == 0 else 'blue'  # Choose color based on node index
        folium.Marker(location=coords[i], icon=folium.Icon(color=color, icon='info-sign'), tooltip=f'Node {i}', icon_size=(8, 8)).add_to(m)

   

    # Render the map in an HTML template
    return render_template("map.html", map=m._repr_html_())

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