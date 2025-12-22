import numpy as np
import matplotlib.pyplot as plt

# Creates 2 arrays with data using numpy
DATA_SUCCESS = np.array([
    [0, 0, 0, 0],
    [1, 3, 2, 0],
    [5, 5, 3, 1],
    [5, 5, 0, 0],
    [5, 3, 0, 0],
    [5, 0, 0, 0]
])
DATA_LAPTIME = np.array([
    ['0s','0s','0s','0s'],
    ['12.42s','10.57s','10.43s','0s'],
    ['12.67s','10.61s','10.70s','11.08s'],
    ['12.95s','11s','0s','0s'],
    ['14s','11.57s','0s','0s'],
    ['13.11s','0s','0s','0s'],
])

# Creating a subplot, so we can add advanced figures
fig, ax = plt.subplots()

# Makes a graph, where the values in the matrix are transformed into colors.
# The cmap variable changes what colors are in the colormap.
# The aspect variable is set at auto, which makes the boxes appear equal and therefore looks better.
colormap_ax = ax.imshow(DATA_SUCCESS, cmap='summer', aspect='auto')

# This adds the colorbar next to the graph, which shows what value the color corresponds to
colormap_bar = fig.colorbar(colormap_ax)
colormap_bar.set_label('Number of successful Laps')

# The names of the axes, and the values that corresponds to rows and coloumns in the graph
sensor_delays = [10, 50, 75, 100]   # x-axis
kp_values = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]   #y-axis

# Making the markers on the side of the graph, which are called ticks in matplotlib:
    # The ticks for the Sensordelay:
ax.set_xticks(np.arange(len(sensor_delays)))
ax.set_xticklabels(sensor_delays)
    # The ticks for the kp_values
ax.set_yticks(np.arange(len(kp_values)))
ax.set_yticklabels(kp_values)

# Making the x and y labels
ax.set_xlabel('SensorDelay (How many iterations before getting sensordata)')
ax.set_ylabel('K_p (The p-Control variabel)')

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