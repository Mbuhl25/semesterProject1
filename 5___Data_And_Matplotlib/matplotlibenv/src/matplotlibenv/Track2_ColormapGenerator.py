import numpy as np
import matplotlib.pyplot as plt

# Creates 2 arrays with data using numpy
DATA_SUCCESS = np.array([
    [5, 5, 5, 5],
    [5, 5, 5, 5],
    [5, 5, 3, 3],
    [5, 5, 5, 5],
    [3,5, 5, 5],
    [3, 5, 5, 5]
])
DATA_LAPTIME = np.array([
    [0,0,0,0],
    [12.42,10.57,10.43,0],
    [12.67,10.61,10.70,11.08],
    [12.95,11,0,0],
    [14,11.57,0,0],
    [13.11,0,0,0],
])

# Creating a subplot, so we can add advanced figures
fig, ax = plt.subplots()

# Makes a graph, where the values in the matrix are transformed into colors.
# The cmap variable changes what colors are in the colormap.
# The aspect variable is set at auto, which makes the boxes appear equal and therefore looks better.
colormap_ax = ax.imshow(DATA_SUCCESS, cmap='summer', vmin='6', vmax='10', aspect='auto')

# This adds the colorbar next to the graph, which shows what value the color corresponds to
colormap_bar = fig.colorbar(colormap_ax)
colormap_bar.set_label('Number of successful Laps')

colormap_bar = fig.colorbar(colormap_ax)
colormap_bar.set_ticks([6, 7, 8, 9, 10])

# The names of the axes, and the values that corresponds to rows and coloumns in the graph
sensor_delays = []   # x-axis
kp_values = []   #y-axis

# Making the markers on the side of the graph, which are called ticks in matplotlib:

# Adding graph title
plt.title('Heatmap of Values by K_p and Sensor Delay')

# for each row, i
for i in range(DATA_LAPTIME.shape[0]):
    # for each coloumn, j
    for j in range(DATA_LAPTIME.shape[1]):
        # adds a text at position i, j
        # ha = horizontal allignment
        # va = vertical allignment
        ax.text(j, i, DATA_LAPTIME[i, j], ha='center', va='center', color='black')

plt.show()