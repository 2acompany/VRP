import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def generate_locations(num_locations, max_distance, alpha):
    # Generate random locations with power-law distribution
    r = max_distance * (np.random.power(alpha, num_locations))
    theta = np.random.uniform(0, 2*np.pi, num_locations)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def assign_demand(num_locations):
    # Assign random demand to each location
    demand = np.random.randint(1, 10, num_locations)
    return demand

def find_clusters(x, y, eps, min_samples):
    # Use DBSCAN algorithm to find clusters
    locations = np.column_stack((x, y))
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(locations)
    return db.labels_

def minimize_vehicles(num_clusters, demand, capacity):
    # Find minimum number of vehicles needed to serve the demand at each cluster
    vehicles = np.zeros(num_clusters)
    for i in range(num_clusters):
        vehicles[i] = np.ceil(np.sum(demand[labels == i]) / capacity)
    return int(np.max(vehicles))

# Input parameters
num_locations = 100
max_distance = 10
alpha = 2
eps = 1
min_samples = 3
capacity = 10

# Generate random locations and demand
x, y = generate_locations(num_locations, max_distance, alpha)
demand = assign_demand(num_locations)

# Find clusters
labels = find_clusters(x, y, eps, min_samples)
num_clusters = len(np.unique(labels))

# Find minimum number of vehicles needed
num_vehicles = minimize_vehicles(num_clusters, demand, capacity)

# Plot locations with outliers in black
plt.scatter(x, y, c=labels)
plt.scatter(x[labels == -1], y[labels == -1], c='black')
plt.show()

print("Number of clusters:", num_clusters)
print("Number of vehicles needed:", num_vehicles)
