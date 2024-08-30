import random
import matplotlib.pyplot as plt
import numpy as np
dist = []
prob = 0.05
for i in range(1000): # Sim 1000 seasons
    HRcount = 0
    for i in range(600):
        if random.random() < prob:
            HRcount += 1
        else:
            pass
    print(HRcount)
    dist.append(HRcount)
plt.hist(dist)
large = 0
small = 0
for i in dist:
    if dist[i] >= 40:
        large += 1
    elif dist[i] <= 20:
        small += 1
print(small, large)
plt.show()
