import random
import matplotlib.pyplot as plt
import numpy as np
dist = []
prob = 0.05
for i in range(1000):
    HRcount = 0
    done = False
    while done == False:
        if random.random() < prob:
            HRcount += 1
        else:
            done = True
    #print(HRcount)
    dist.append(HRcount)
plt.hist(dist)
plt.show()
