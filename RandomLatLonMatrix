import random
from geopy.distance import distance
import folium

# Number of nodes
num_nodes = random.randint(1, 10)

# Generate random latitude and longitude coordinates for each node
coords = [(random.uniform(-90, 90), random.uniform(-180, 180)) for _ in range(num_nodes)]

# Calculate the distance matrix between the nodes
dist_matrix = [[0] * num_nodes for _ in range(num_nodes)]
for i in range(num_nodes):
    for j in range(num_nodes):
        if i == j:
            continue
        dist_matrix[i][j] = distance(coords[i], coords[j]).km

# Print the distance matrix
for row in dist_matrix:
    print(row)

# Create a map and add markers for each node
m = folium.Map(location=[0, 0], zoom_start=2)
for i in range(num_nodes):
    folium.Marker(location=coords[i]).add_to(m)

# Display the map
m
