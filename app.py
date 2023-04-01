from flask import Flask, render_template
import folium
import random
from geopy.distance import distance
from itertools import permutations

app = Flask(__name__)

@app.route("/")
def map():
    # Define the latitude and longitude bounds for Tehran city limits
    tehran_limits = [(35.4904, 51.1424), (35.8496, 51.6814)]

    # Number of nodes
    num_nodes = random.randint(50, 100)

    # Generate random latitude and longitude coordinates for each node within Tehran city limits
    coords = [(random.uniform(tehran_limits[0][0], tehran_limits[1][0]), 
               random.uniform(tehran_limits[0][1], tehran_limits[1][1])) for _ in range(num_nodes)]

    # Calculate the distance matrix between the nodes
    dist_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                continue
            dist_matrix[i][j] = distance(coords[i], coords[j]).km
    for row in dist_matrix:
        print(row)
        

    # Create a map centered on Tehran
    m = folium.Map(location=[35.6994, 51.3377], zoom_start=12)

    # Add markers for each node to the map
    for i in range(num_nodes):
        folium.Marker(location=coords[i]).add_to(m)

    # Add polylines between the nodes
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            folium.PolyLine(locations=[coords[i], coords[j]], color='red').add_to(m)

    # Render the map in an HTML template
    return render_template("map.html", map=m._repr_html_())

if __name__ == "__main__":
    app.run(debug=True)
