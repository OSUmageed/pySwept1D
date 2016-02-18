
from sweptRuleFunctions import *
import math
import itertools as it
import matplotlib.pyplot as plt

# Initial conditions.  Material = Aluminum
x = [t * .2 for t in range(50)]
node = 5

while len(x)%node != 0:
    node = int(raw_input('The length of x must be a integer multiple of the number of nodes: '))
    
# Do this.
l_nodes = len(x) / node
# Temperature along the bar in C
Nodes =[[(500.0 * math.exp(-x[(m*l_nodes+n)] / 5.0)) for n in range(l_nodes)] for m in range(node)]

Tri_ht = l_nodes / 2

Alal = 8.418e-5  # Thermal diffusivity. in m^2/s
kAl = 247.0  # Thermal Conductivity in W/mK
dt = 10  # delta T in seconds

Fo = dt * Alal / (x[1] ** 2)

#Nodes.  First element is node, second is timestep, third is subtimesteps.  It could go on for as many timesteps as desired.
#This needs to be odd.
ending = 5

for k in range(ending):

    for n in range(node):

        # The first triangles work.  They return the list Nodes which has length number of nodes.  Each element in
        # Nodes has length of a timestep initially.  So Nodes[0][1] is the first subtimestep in the first Node.  It has
        # length number of nodes -2.  In this case, 8.
        if k == 0:
            Nodes[n] = [topTriangle(Fo, Nodes[n],0)]

        else:
            if k % 2:               
                if n == node-1:                    
                    Nodes[n] += [ID[0]]
                          
                else:                   
                    Nodes[n] += [ID[n+1]]
  
            else:               
                if n == 0:                    
                    Nodes[n] += [ID[-1]]
                    
                else:
                    Nodes[n] += [ID[n-1]]
            
            #Need to give the bottom triangle the Node's information and the communicated information.
            Nodes[n][k] = bottomTriangle(Fo, Nodes[n][-2:], l_nodes, k, n, k == ending-1)
            
            
    ID = [communication(Nodes[-m][k], k) for m in range(1,node+1)]
    ID = ID[::-1]
    
Nrng = [y*2 for n in range(node)]
tsrng = range(2)*node
subtrng = range(2)*node
Nd_ext = range(1,node+1)+range(1,node)[::-1]

tlen = sum([len(Nodes[0][n])for n in range(len(Nodes[0]))])
tar = [p*dt for p in range(tlen)]
Full_Nodes = []
Full_Nodes.extend([[y for z in range(len(Nodes)) for y in Nodes[z][0][0]]])
c = 1
cnt = 0

#What a bunch of nonsense.

a2=1
    
for a1 in range(0,ending,2):

    for b in range(len(Nodes[0][1])):
        
         if b == len(Nodes[0][0])-1:
            
            c = 0
            if a%2:
                Full_Nodes.append([y for z in range(len(Nodes)) for y in Nodes[z][a2][b]])
                
            else:
                Full_Nodes.append(Nodes[-1][a2][b][-Nd_ext[cnt]:]+[y for z in range(len(Nodes)-1) for y in Nodes[z][a2][b]]+Nodes[-1][a2][b][:Nd_ext[cnt]])            
            if a1 == 0:
                break
            cnt += 1
              
                                  
         else:
            #I'm acting like I'm flipping the a values over to a new timestep but I'm not.  In this kind of schme
            # The a and a+1 terms will step forward together instead of leap frogging.
            Full_Nodes.append(Nodes[-1][a2][cnt][-Nd_ext[cnt]:] + [y for n in range(node-1) for y in Nodes[n][a1][b+c]+Nodes[n][a2][cnt]] + Nodes[-1][a1][b+c] + Nodes[-1][a2][cnt][:Nd_ext[cnt]])
            print a1, b, len(Full_Nodes[-1])
            
            cnt +=1
            if cnt == len(Nodes[0][1])-1:
                cnt = 0
                
    if a1 == 2:
        a2 += 2
            

print 'Done'
