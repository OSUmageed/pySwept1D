import numpy as np
from sweptRuleFunctions import *
import math
import matplotlib.pyplot as plt

# Initial conditions.  Material = Aluminum
x = [t * .2 for t in range(50)]
node = 5
l_nodes = len(x) / node
# Temperature along the bar in C
Nodes =[[(500.0 * math.exp(-x[(m*l_nodes+n)] / 5.0)) for n in range(l_nodes)] for m in range(node)]

Tri_ht = l_nodes / 2

Alal = 8.418e-5  # Thermal diffusivity. in m^2/s
kAl = 247.0  # Thermal Conductivity in W/mK
dt = 10  # delta T in seconds

Fo = dt * Alal / (x[1] ** 2)

ending = 5
print len(Nodes)

for k in range(ending):

    for n in range(node):

        # The first triangles work.  They return the list Nodes which has length number of nodes.  Each element in
        # Nodes has length of a timestep initially.  So Nodes[0][1] is the first subtimestep in the first Node.  It has
        # length number of nodes -2.  In this case, 8.
        if k == 0:
            Nodes[n] = [topTriangle(Fo, Nodes[n])]
            print len(Nodes[n])

        else:
            if k % 2:
                if n == node-1:
                    g = n
                    n = 0
                    IDb = ID[1][n][::-1] + ID[0][n+1]
                    n = node-1
                else:
                    IDb = ID[1][n][::-1] + ID[0][n+1]


            else:
                IDb = ID[0][n+1] + ID[1][n]
            #Need to give the bottom triangle the Node's information and the communicated information.
            Nodes += bottomTriangle(Fo, Nodes[n], IDb, l_nodes, k == ending-1)
    print len(Nodes)
    ID = [[communication(Nodes[-m], k + 1) for m in range(1,node+1)]]


print 'Done'
