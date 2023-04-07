
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# set parameters
num_locs = 40
power_law_param = 2.5
max_distance = 1
demand_mean = 10
demand_std = 3
vehicle_capacity = 50

# generate random locations distributed by power-law
x = np.random.power(power_law_param, size=num_locs)
y = np.random.power(power_law_param, size=num_locs)

# calculate distances between locations
distances = np.sqrt((x[:, np.newaxis] - x)**2 + (y[:, np.newaxis] - y)**2)

# find outlier locations
outliers = np.any(distances > max_distance, axis=1)

# plot locations and outliers
plt.scatter(x, y, c=~outliers, cmap='viridis')
plt.scatter(x[outliers], y[outliers], c='k')
plt.show()

# calculate demand at each location
demands = np.random.normal(loc=demand_mean, scale=demand_std, size=num_locs)

# find optimal number of clusters using elbow method
sum_of_squared_distances = []
K = range(1, num_locs//10)
for k in K:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(np.column_stack((x, y)))
    sum_of_squared_distances.append(kmeans.inertia_)
plt.plot(K, sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum of squared distances')
plt.title('Elbow method for optimal k')
plt.show()
num_clusters = int(input("Enter the number of clusters to use: "))

# calculate number of vehicles needed
total_demand = demands.sum()
num_vehicles = int(np.ceil(total_demand / vehicle_capacity))

# plot boundaries of clusters
kmeans = KMeans(n_clusters=num_clusters, n_init=10).fit(np.column_stack((x, y)))
for i in range(num_clusters):
    cluster_locs = (kmeans.labels_ == i)
    plt.scatter(x[cluster_locs], y[cluster_locs])
    cluster_x, cluster_y = kmeans.cluster_centers_[i]
    circle = plt.Circle((cluster_x, cluster_y), max_distance, color='r', fill=False)
    plt.gca().add_artist(circle)
plt.show()

print(f"Number of clusters: {num_clusters}")
print(f"Number of vehicles needed: {num_vehicles}")

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

def get_clusters(num_clusters, num_locations, power_low_alpha, max_distance, demand_per_location, vehicle_capacity):
    # Generate random locations
    locations = np.random.power(power_low_alpha, size=(num_locations, 2))

    # Calculate pairwise distances between locations
    distances = cdist(locations, locations)

    # Set diagonal elements to a large value to avoid selecting the same location as a neighbor
    np.fill_diagonal(distances, np.inf)

    # Find neighbors for each location
    neighbors = np.argsort(distances, axis=1)[:, :10]

    # Find outlier locations that are more than max_distance away from any other location
    max_distances = np.max(distances, axis=1)
    outliers = np.where(max_distances > max_distance)[0]

    # Set first location as the depot
    depot_index = 0

    # Initialize list to store cluster assignments for each location
    cluster_assignments = np.zeros(num_locations, dtype=int)

    # Initialize list to store cluster boundaries
    cluster_boundaries = []

    # Initialize list to store vehicle assignments for each cluster
    cluster_vehicles = []

    # Cluster locations using KMeans algorithm
    kmeans = KMeans(n_clusters=num_clusters, n_init=10).fit(locations)


    # Assign each location to its nearest cluster
    for i, label in enumerate(kmeans.labels_):
        cluster_assignments[i] = label

    # Find the boundaries of each cluster
    for i in range(num_clusters):
        cluster_boundary = locations[cluster_assignments == i]
        cluster_boundaries.append(cluster_boundary)
        # Find the number of vehicles required for this cluster
        cluster_demand = np.sum(demand_per_location[cluster_assignments == i])
        num_vehicles = int(np.ceil(cluster_demand / vehicle_capacity))
        cluster_vehicles.append(num_vehicles)

    # Plot the locations and cluster boundaries
    colors = ['r', 'g', 'b', 'c', 'm', 'y']
    fig, ax = plt.subplots()
    for i in range(num_clusters):
        ax.scatter(cluster_boundaries[i][:, 0], cluster_boundaries[i][:, 1], color=colors[i % len(colors)])
        ax.plot(cluster_boundaries[i][:, 0], cluster_boundaries[i][:, 1], color=colors[i % len(colors)])
    ax.scatter(locations[outliers][:, 0], locations[outliers][:, 1], color='k')
    ax.set_aspect('equal')
    plt.show()

    # Print the outlier locations
    print("Outlier locations:")
    print(locations[outliers])

    # Print the locations in each cluster
    for i in range(num_clusters):
        print(f"Cluster {i} locations:")
        print(cluster_boundaries[i])

    # Print the distances between locations
    print("Distances between locations:")
    print(distances)

    # Print the number of vehicles required for each cluster
    print("Vehicles per cluster:")
    print(cluster_vehicles)

    return cluster_boundaries, cluster_vehicles, distances, locations[outliers]

# calculate demand at each location
demand_per_location = np.random.normal(loc=demand_mean, scale=demand_std, size=num_locs)
get_clusters(num_clusters, num_locs, power_law_param, max_distance, demand_per_location, vehicle_capacity)