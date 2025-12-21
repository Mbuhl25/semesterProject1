#Importing nessecary libaries
import matplotlib.pyplot as plt
import numpy as np

# Data lists
FULL_DATA=np.array([0,2])

# Creating a subplot, so we can add advanced figures
fig, ax = plt.subplots()
# Defining the range of the x_axis
x_Axis = np.arange(len(FULL_DATA))

# Plotting the DATA as a function of x between 1 and len(DATA),
# but only the DATA points of the succesfull laps
ax.plot(x_Axis[FULL_DATA >= min(FULL_DATA)],FULL_DATA[FULL_DATA >= min(FULL_DATA)],
        label="Track 2 Line",
        markersize=10,
        color='black',
        linewidth=4
        )

# Plotting the DATA as a function of x between 1 and len(DATA),
# but only the DATA points of the UNsuccesfull laps
ax.plot(    x_Axis[FULL_DATA < min(FULL_DATA)],
        FULL_DATA[FULL_DATA < min(FULL_DATA)],
        label="Nut placements",
        marker='o',
        markersize=15,
        markerfacecolor="#007f66",
        markeredgecolor='black',
        markeredgewidth=1,
        linestyle='None'
        )

ax.plot(    x_Axis[FULL_DATA < min(FULL_DATA)],
        FULL_DATA[FULL_DATA < min(FULL_DATA)],
        label=" ",
        marker='o',
        markersize=15,
        markerfacecolor="#f9fc66",
        markeredgecolor='black',
        markeredgewidth=1,
        linestyle='None'
        )

plt.xlabel("Laps")
plt.ylabel("Time/Seconds")


# Adding a legend
ax.legend()
# Adding a title
plt.title("Times on fasttrack in the competition")

#Show the diagram
plt.show()