
from sweptRuleFunctions import *
import math
import itertools as it
import matplotlib.pyplot as plt

# Initial conditions.  Material = Aluminum
x = [t * .2 for t in range(50)]
node = 5

while len(x)%node != 0:
    print 'The length of x is:', len(x) 
    node = int(raw_input('The length of x must be a integer multiple of the number of nodes, input number of nodes: '))
    
# Do this.
l_nodes = len(x) / node
# Temperature along the bar in C
Nodes =[[(500.0 * math.exp(-x[(m*l_nodes+n)] / 5.0)) for n in range(l_nodes)] for m in range(node)]



Alal = 8.418e-5  # Thermal diffusivity. in m^2/s
kAl = 247.0  # Thermal Conductivity in W/mK
dt = 10  # delta T in seconds

Fo = dt * Alal / (x[1] ** 2)

#Nodes.  First element is node, second is timestep, third is subtimesteps.  It could go on for as many timesteps as desired.
#This needs to be odd.
ending = 500

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
            
            
    ID = [communication(Nodes[-m][k][-l_nodes/2:], k) for m in range(1,node+1)]
    ID = ID[::-1]

tlen = l_nodes/2*(ending-2)+1
tar = [p*dt for p in range(tlen)]
Full_Nodes = []
Full_Nodes.append([y for z in range(len(Nodes)) for y in Nodes[z][0][0]])
leadingts = 1
sub_leadingts = 0
trailingts = 0
sub_trailingts = 1
#There are not two timesteps at subtimesteps 0:l_nodes/2:end.  The last node isn't split at multiples of lnodes.
#You just need to handle every edge case in this one loop. Loop every ts.
for k in range(1,tlen):
    
    if k % (l_nodes) == 0:
        Full_Nodes.append([y for z in range(len(Nodes)) for y in Nodes[z][leadingts][sub_leadingts]])
        sub_trailingts = sub_leadingts
        sub_leadingts = 0
        leadingts += 1  
        trailingts += 1
        
        
    elif k % (l_nodes/2) == 0:
        if leadingts % 2:
            sp = len(Nodes[-1][leadingts][sub_leadingts])/2
        else:
            sp = len(Nodes[-1][trailingts][sub_trailingts])/2
            
        Full_Nodes.append(Nodes[-1][leadingts][sub_leadingts][-sp:] + 
        [y for z in range(len(Nodes)-1) for y in Nodes[z][leadingts][sub_leadingts]] + 
        Nodes[-1][leadingts][sub_leadingts][:sp])
        sub_trailingts = sub_leadingts
        sub_leadingts = 0
        leadingts += 1
        trailingts += 1
        print k
        
    else:
        if leadingts % 2:
            sp = len(Nodes[-1][leadingts][sub_leadingts])/2
        else:
            sp = len(Nodes[-1][trailingts][sub_trailingts])/2
            
        if leadingts % 2:
 
            Full_Nodes.append(Nodes[-1][leadingts][sub_leadingts][-sp:] + 
            [y for z in range(len(Nodes)-1) for y in Nodes[z][trailingts][sub_trailingts] + 
            Nodes[z][leadingts][sub_leadingts]] + Nodes[-1][trailingts][sub_trailingts] + 
            Nodes[-1][leadingts][sub_leadingts][:sp])
            
        else:
            Full_Nodes.append(Nodes[-1][trailingts][sub_trailingts][-sp:] + 
            [y for z in range(len(Nodes)-1) for y in Nodes[z][leadingts][sub_leadingts] + 
            Nodes[z][trailingts][sub_trailingts]] + Nodes[-1][leadingts][sub_leadingts] +
            Nodes[-1][trailingts][sub_trailingts][:sp])
            
        sub_leadingts += 1

    sub_trailingts += 1    


print 'Done'

for k in range(0,tlen,tlen/5):
    plt.plot(x,Full_Nodes[k])
    
plt.show()
