import numpy as np
import matplotlib.pyplot as plt

# create a numpy array from the distance matrix
distance_matrix = np.array([
        [0, 10, 15],
        [10, 0, 15],
        [15, 10, 0]
])

# plot the distance matrix using imshow
fig, ax = plt.subplots()
im = ax.imshow(distance_matrix)

# set the ticks and tick labels
ax.set_xticks(np.arange(len(distance_matrix)))
ax.set_yticks(np.arange(len(distance_matrix)))
ax.set_xticklabels(['A', 'B', 'C'])
ax.set_yticklabels(['A', 'B', 'C'])

# set the axis labels
ax.set_xlabel('Destination')
ax.set_ylabel('Source')

# set the colorbar
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("Distance", rotation=-90, va="bottom")

# show the plot
plt.show()
