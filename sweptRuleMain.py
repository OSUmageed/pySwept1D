
import numpy as np
from sweptRuleFunctions import *
import math
import matplotlib.pyplot as plt

#Initial conditions.  Material = Aluminum #And Fire
x = [t/.2 for t in range(50)]
node = 5
l_nodes = len(x)/node
Tbar = [(500.0*math.exp(-x/5.0)) for x in x] #Temperature along the bar in C
#ID = Tbar.reshape((node,l_nodes))
print Tbar

#print type(ID)

Tri_ht = l_nodes/2

# plt.plot(x,Tbar)
# plt.show()
Alal = 8.418e-5 #Thermal diffusivity. in m^2/s
kAl = 247.0 #Thermal Conductivity in W/mK
dt = 10 #delta T in seconds

Fo = dt*Alal/(x[1]**2)

ending = 5

Full_Nodes = []

for k in range(ending):
    Nodes = []
    for n in range(node):
        if k == 0:
            Nodes += [topTriangle(Fo, ID[n,:])]
            print len(Nodes)
        else:
            print ID[n], len(ID)

            Nodes += bottomTriangle(Fo,ID[n], l_nodes)

    Full_Nodes += Nodes
    ID = [communication(Nodes[m], k+1) for m in range(node)]
    print ID[1]

print 'Done'



