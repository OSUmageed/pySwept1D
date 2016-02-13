import numpy as np
from sweptRuleFunctions import *
import math
import matplotlib.pyplot as plt

# Initial conditions.  Material = Aluminum
x = [t * .2 for t in range(50)]
node = 5
l_nodes = len(x) / node
# Temperature along the bar in C
ID = [[(500.0 * math.exp(-x[(m*l_nodes+n)] / 5.0)) for n in range(l_nodes)] for m in range(node)]

Tri_ht = l_nodes / 2

Alal = 8.418e-5  # Thermal diffusivity. in m^2/s
kAl = 247.0  # Thermal Conductivity in W/mK
dt = 10  # delta T in seconds

Fo = dt * Alal / (x[1] ** 2)

ending = 5

Full_Nodes = []

for k in range(ending):
    Nodes = []
    for n in range(node):
        if k == 0:
            Nodes += [topTriangle(Fo, ID[n][:])]

        else:
            if k % 2:

                if n == node-1:
                    g = n
                    n = 0
                    IDb = ID[1][n][::-1] + ID[0][n+1]
                    n = node-1
                else:
                    IDb = ID[1][n][::-1] + ID[0][n+1]
                    print ID[1][n], ID[0][n+1]
                    print IDb

            else:
                IDb = ID[0][n+1] + ID[1][n]

            Nodes += bottomTriangle(Fo, IDb, l_nodes, k == ending-1)

    Full_Nodes += Nodes
    # The communication.  So ID[0] is the communication part and ID[1] is the keeping part.
    ID = [[communication(Nodes[-m], k + 1) for m in range(1,node+1)]]
    # The keeping
    ID += [[communication(Nodes[-m], k) for m in range(1,node+1)]]


print 'Done'
