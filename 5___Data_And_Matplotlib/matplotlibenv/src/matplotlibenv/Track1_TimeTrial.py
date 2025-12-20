#Importing nessecary libaries
import matplotlib.pyplot as plt
import numpy as np

# This variable has been chosen, so the failed laps are displayed just under the correct values
FAILED_VAL=10.58
# Data lists
FULL_DATA=np.array([10.691,13.697,10.726,10.666,10.679,10.769,10.721,10.716,10.792,10.742,10.647,10.69,10.663,10.697,10.647,10.701,10.689,10.682,12.356,10.651,10.714,10.698,10.765,26.529,20.672,10.594])
ERROR_DATA=np.array([10.691,FAILED_VAL,10.726,10.666,10.679,10.769,10.721,10.716,10.792,10.742,10.647,10.69,10.663,10.697,10.647,10.701,10.689,10.682,FAILED_VAL,10.651,10.714,10.698,10.765,FAILED_VAL,FAILED_VAL,10.594])

# Creating a subplot, so we can add advanced figures
fig, ax = plt.subplots()

# Defining the range of the x_axis
x_Axis = np.arange(len(FULL_DATA))

# Plotting the DATA as a function of x between 1 and len(DATA),
# but only the DATA points of the succesfull laps
ax.plot(x_Axis[ERROR_DATA >= min(FULL_DATA)],ERROR_DATA[ERROR_DATA >= min(FULL_DATA)],
        label="Lap-Time",
        marker=".",
        markersize=10,
        color='#007f66',
        linestyle=':',
        linewidth=3
        )

# Plotting the DATA as a function of x between 1 and len(DATA),
# but only the DATA points of the UNsuccesfull laps
ax.plot(x_Axis[ERROR_DATA < min(FULL_DATA)],ERROR_DATA[ERROR_DATA < min(FULL_DATA)],
        label="Failed Run",
        marker='x',
        markersize=10,
        color='#333531',
        linestyle='None'
        )

plt.xlabel("Laps")
plt.ylabel("Time/Seconds")

# Adding a grid
plt.grid(True)
# Adding a legend
ax.legend()
# Adding a title
plt.title("Times on fasttrack in the competition")

#Show the diagram
plt.show()