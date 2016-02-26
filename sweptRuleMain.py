
from sweptRuleFunctions import *
import math
import matplotlib.pyplot as plt

# Set the mesh of the x axis and the number of points.  Then make a list of x axis points range 0 to L.
dx = .2
xlength = 50
x = [t * dx for t in range(xlength)]
node = 5 #Number of nodes in the decomposition.

while len(x)%node != 0:
    print 'The length of x is:', len(x) 
    node = int(raw_input('The length of x must be a integer multiple of the number of nodes, input number of nodes: '))
    
# The x axis length of each node at it's initial (maximum) condition.
l_nodes = len(x) / node

# Nodes:  First element is node, second is timestep, third is subtimesteps.
# Initial condition of the bar.
Nodes =[[(500.0 * math.exp(-x[(m*l_nodes+n)] / 5.0)) for n in range(l_nodes)] for m in range(node)]

# Material = Aluminum
Alal = 8.418e-5  # Thermal diffusivity. in m^2/s
kAl = 247.0  # Thermal Conductivity in W/mK
dt = 10  # subtimestep division in seconds.

Fo = dt * Alal / (dx ** 2) #Fourier number

# ending is number of timesteps.
ending = 500

#Loop over timesteps.  Then loop over each node.
for k in range(ending):
    for n in range(node):
        # For the first timestep, there's only the positive triangle.  The initial conditions are the first list for
        # each node.
        if k == 0:
            Nodes[n] = [topTriangle(Fo, Nodes[n],0)]

        # If k is odd, the initial conditions for the next timestep are communicated from the node on the left, and if
        # even from the node on the right.  The initial conditions are a list appended to the end of the nodes list.
        # The initial conditions given are only half, the other half are the edge values from the previous timestep.
        # This mimics a parallel configuration so that each GPU node has its own previous values and the information
        # from the partner node for the next timestep.
        else:
            if k % 2:
                # The last node on an even timestep needs the first node's information.
                if n == node-1:                    
                    Nodes[n] += [ID[0]]
                          
                else:                   
                    Nodes[n] += [ID[n+1]]
  
            else:
                # The first node on an odd timestep needs the last node's information.
                if n == 0:                    
                    Nodes[n] += [ID[-1]]
                    
                else:
                    Nodes[n] += [ID[n-1]]
            
            # For all timesteps after the first, bottomTriangle is called.  Bottom triangle also calls top triangle and
            # returns a full diamond.  It's given the initial conditions, the last two lists in each node, the maximum
            # x length of a node, the position within the decomposition (which timestep which node), and a flag to note
            # the final timestep where topTriangle is not called.
            Nodes[n][k] = bottomTriangle(Fo, Nodes[n][-2:], l_nodes, k, n, k == ending-1)

    # At the end of each timestep the nodes must communicate.  This calls the communication function which gets the
    # information from each node's current timestep to be communicated.  It only takes the top triangle with -l_nodes/2:
    ID = [communication(Nodes[m][k][-l_nodes/2:], k) for m in range(node)]

# After the scheme is complete the information from the nodes must be compiled in a matrix, Full_nodes, for output.
# First find the number of subtimesteps completed and then generate a time array.
tlen = l_nodes/2*(ending-2)+1
tar = [p*dt for p in range(tlen)]

# Initialize full nodes and put the first subtimestep in the first list.
Full_Nodes = []
Full_Nodes.append([y for z in range(len(Nodes)) for y in Nodes[z][0][0]])

# To combine the results we need to concatenate the lists in two adjacent timesteps.  The initial leading timestep is 1
# and the trailing timestep is 0.  The 0 subtimestep in the leading timestep must be joined to the 1 subtimestep in the
# trailing timestep.
leadingts = 1
sub_leadingts = 0
trailingts = 0
sub_trailingts = 1

# Loop over all the subtimesteps.
for k in range(1,tlen):

    # Some subtimesteps only contain information from one timestep.  When these timesteps are even, the subtimestep is
    # not split in the last node (same as the initial condition.  These subtimesteps occur when the subtimestep order is
    # evenly divisible by l_nodes/2 since that's the height of the triangle.
    # At this point the trailing timestep ends, and the leading timestep becomes the trailing timestep.
    if k % (l_nodes) == 0:
        Full_Nodes.append([y for z in range(len(Nodes)) for y in Nodes[z][leadingts][sub_leadingts]])
        sub_trailingts = sub_leadingts
        sub_leadingts = 0
        leadingts += 1  
        trailingts += 1

    # Here the subtimestep is odd so the final node is split between the first x divisions and the last ones.
    elif k % (l_nodes/2) == 0:
        if leadingts % 2:
            sp = len(Nodes[-1][leadingts][sub_leadingts])/2
        else:
            sp = len(Nodes[-1][trailingts][sub_trailingts])/2

        # This needs to append full nodes with a list of the current timestep for each node and the split timestep from
        # the final node.
        Full_Nodes.append(Nodes[-1][leadingts][sub_leadingts][-sp:] + 
        [y for z in range(len(Nodes)-1) for y in Nodes[z][leadingts][sub_leadingts]] + 
        Nodes[-1][leadingts][sub_leadingts][:sp])
        sub_trailingts = sub_leadingts
        sub_leadingts = 0
        leadingts += 1
        trailingts += 1
        print k

    # For all other timesteps, the last node is split and both timesteps must be joined.
    else:
        # sp shows how to split the final node to move half its values to the front and keep the other half at the back.
        # It needs to grow and then shrink with the diamond so it takes half the length of either the trailing or
        # leading timestep.
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

# Plot the results.
Leg = []
for k in range(0,tlen,tlen/5):
    plt.plot(x,Full_Nodes[k])
    Leg.extend(['t = ' + str(tar[k]) + ' (s)'])

plt.legend(Leg)
plt.show()
