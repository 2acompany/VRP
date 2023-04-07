
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# set parameters
num_locs = 500
power_law_param = 2.5
max_distance = 10
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
