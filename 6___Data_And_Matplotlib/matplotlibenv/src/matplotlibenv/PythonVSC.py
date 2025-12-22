import matplotlib.pyplot as plt
import numpy as np

# Data
x_labels = [10**7, 10**8, 10**9]
c_times = [0.0101, 0.2307, 2.2992]
python_times = [0.6054, 5.5510, 78.8353]

x = np.arange(len(x_labels))  # the label locations
width = 0.35  # width of the bars

fig, ax = plt.subplots(figsize=(8,5))
rects1 = ax.bar(x - width/2, c_times, width, label='C++', color='#aad466')
rects2 = ax.bar(x + width/2, python_times, width, label='Python', color='#285134')

# Labels and titles
ax.set_xlabel('Number of iterations run through')
ax.set_ylabel('Time (seconds)')
ax.set_title('C++ vs Python Execution Time')

ax.set_xticks(x)
ax.set_xticklabels([f'$10^{int(np.log10(val))}$' for val in x_labels])
ax.legend()

# Optional: add values on top of bars
for rects in [rects1, rects2]:
        for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.2f}',
                xy=(rect.get_x() + rect.get_width() / 2,
                height),xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

plt.tight_layout()
plt.show()
