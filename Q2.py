import numpy as np
from matplotlib import pyplot as plt

"""
Create an array with 10 million entries.
Assign a load randomly.
"""


size = 10000000
servers = np.zeros(size)

for i in range(size):
    index = np.random.randint(0, size)
    servers[index] += 1

bins = [0,1,2,3,4,5,6,7,8,9,10]
plt.hist(servers, bins, rwidth=0.9)
plt.title("Histogram of Random Load Balancing")
plt.xlabel("Number of loads per server")
plt.ylabel("Number of servers")
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
#plt.ticklabel_format(useOffset=False, style='plain')
assignments = np.histogram(servers, bins=bins)

print("The total is ", np.sum(assignments[0]))
print(assignments)
plt.show()

for i in range(size):
    r1 = np.random.randint(0, size)
    r2 = np.random.randint(0, size)
    if (servers[r1]< servers[r2]):
        servers[r1] += 1
    else:
        servers[r2] += 1

plt.hist(servers, bins, rwidth=0.9)
plt.title("Histogram of Improved Random Load Balancing")
plt.xlabel("Number of loads per server")
plt.ylabel("Number of servers")
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
assignments = np.histogram(servers, bins=bins)

print("The total is ", np.sum(assignments[0]))
print(assignments)
plt.show()

