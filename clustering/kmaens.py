import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Generate random latitudes and longitudes
latitudes = np.random.uniform(low=20, high=50, size=(1000,))
longitudes = np.random.uniform(low=-120, high=-70, size=(1000,))

# Create an array of latitudes and longitudes
locations = np.column_stack((latitudes, longitudes))

# Specify the number of clusters
n_clusters = 50

# Create a KMeans object
kmeans = KMeans(n_clusters=n_clusters)

# Fit the KMeans model to the locations
kmeans.fit(locations)


# Get the cluster labels
cluster_labels = kmeans.labels_

# Visualize the clusters
plt.figure(figsize=(8,6))
plt.scatter(locations[:, 1], locations[:, 0], c=cluster_labels, cmap='rainbow')
plt.title('Location Clusters')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
print("done")
