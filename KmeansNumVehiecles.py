import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Generate random locations with a power-law distribution
num_locations = 1000
alpha = 1.5
xmin = 0.1
xmax = 10
r = np.random.power(alpha, size=num_locations)
locations = xmin * (1.0 - r) / r


def get_distances(locations, max_distance):
    n = len(locations)
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                distances[i][j] = 0
            else:
                # calculate Euclidean distance between locations i and j
                distance = np.linalg.norm(locations[i] - locations[j])
                if distance > max_distance:
                    distances[i][j] = float('inf')
                else:
                    distances[i][j] = distance
    return distances
max_distance = 100 # set maximum distance to 100 units
distances = get_distances(locations, max_distance)

# # Compute pairwise distances between locations
# distances = np.zeros((num_locations, num_locations))
# for i in range(num_locations):
#     for j in range(i + 1, num_locations):
#         distances[i, j] = locations[j] - locations[i]
#         distances[j, i] = -distances[i, j]

# # # Set distances greater than max_distance to infinity
# # max_distance = 2.0
# # distances[distances > max_distance] = np.inf

# Cluster locations using KMeans
num_vehicles = 5
kmeans = KMeans(n_clusters=num_vehicles, random_state=0).fit(distances)

# Assign locations to clusters
labels = kmeans.labels_

# Plot locations and clusters
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
# Reshape locations array to be 2D with two columns
locations_2d = locations.reshape(-1, 2)

# Select locations with distance > max_distance
outliers = locations_2d[distances > max_distance]

# Plot clusters in different colors
for i in range(num_vehicles):
    plt.scatter(locations_2d[kmeans.labels_ == i, 0], locations_2d[kmeans.labels_ == i, 1], label=f'Cluster {i+1}')

# Plot outliers in black
plt.scatter(outliers[:, 0], outliers[:, 1], color='k')

plt.legend()
plt.show()
