import numpy as np
import matplotlib.pyplot as plt

# Creates 2 arrays with data using numpy
DATA_SUCCESS = np.array([
    [0],
    [0]
])

# Creating a subplot, so we can add advanced figures
fig, ax = plt.subplots()

# The names of the axes, and the values that corresponds to rows and coloumns in the graph
sensor_delays = ["Track 2"]   # x-axis
Track_2 = []   #y-axis

# Making the markers on the side of the graph, which are called ticks in matplotlib:
    # The ticks for the Sensordelay:
ax.set_xticks(np.arange(len(sensor_delays)))
ax.set_xticklabels(sensor_delays)
    # The ticks for the kp_values
ax.set_yticks(np.arange(len(Track_2)))
ax.set_yticklabels(Track_2)

# Makes a graph, where the values in the matrix are transformed into colors.
# The cmap variable changes what colors are in the colormap.
# The aspect variable is set at auto, which makes the boxes appear equal and therefore looks better.
colormap_ax = ax.imshow(DATA_SUCCESS, cmap='summer_r', vmin='6', vmax='10', aspect='auto')
colormap_ax.set_label('Number of successful Laps')

colormap_ax = fig.colorbar(colormap_ax)
colormap_ax.set_ticks([6, 7, 8, 9, 10])
colormap_ax.set_label('Number of successful Laps')
plt.legend()


plt.show()
