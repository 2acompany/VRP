import random
import sys
from flask import Flask, render_template
import folium
from geopy.distance import distance
from itertools import permutations
from VRPTimeLimitAPI import main
import datetime

app = Flask(__name__)



@app.route("/")
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
    folium.TileLayer('cartodbdark_matter').add_to(m)

    

    # Add polylines between the nodes
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            folium.PolyLine(locations=[coords[i], coords[j]], color='red' ,opacity=0).add_to(m)
 

 
        
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
    app.run(debug=True)
