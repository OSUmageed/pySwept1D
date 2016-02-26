# The Swept Rule functions.


# Communication takes the last timestep upper triangle for each node as vect and strips the last two values from either
# the left (if the timestep (stage) is odd) or right side (if even) for each subtimestep.  So it returns a list of
# length l_nodes/2 with two values in each element.
def communication(vect, stage):

    if stage % 2:
        comm = [vect[t][-2:] for t in range(len(vect))]
        
    else:
        comm = [vect[t][:2] for t in range(len(vect))]

    return comm


# topTriangle takes the Fourier number, the initial conditions (a list of length l_nodes), and an indicator for whether
# or not the last node is split.
def topTriangle(F, IC, split):
    
    out_a = [IC]
    if split:
        while len(out_a[-1]) > 2:
    
            h1 = [2 * F * (out_a[-1][n - 1] - out_a[-1][n]) + out_a[-1][n] for n in range(1, len(out_a[-1])/2)]
            h2 = [2 * F * (out_a[-1][n + 1] - out_a[-1][n]) + out_a[-1][n] for n in range(len(out_a[-1])/2, len(out_a[-1]) - 1)]
            out_a.append(h1+h2)
            
        return out_a
  
    else:
        # Each subtimestep is evaluated with the forward euler decomposition until only two values can be evaluated at
        # the subtimestep.
        while len(out_a[-1]) > 2:
    
            holder = [F * (out_a[-1][n - 1] + out_a[-1][n + 1]) + (1- 2*F)*out_a[-1][n] for n in range(1, len(out_a[-1]) - 1)]
            out_a += [holder]
    
        return out_a


# bottomTriangle takes the Fourier number, the initial conditions as a list of two lists (the first one is the previous
# timestep for the current node the second one is the communicated information from the partner node).  It also takes
# the l_nodes, the current timestep, current node and ending flag.  This allows it to determine whether or not the node
# must be split and whether to call topTriangle.
def bottomTriangle(F, IC, l_no, timestep, node, ed):
    # Like it topTriangle, first check to see if the node is split.  Only the last node in an odd timestep is split.
    if node+1 == l_no/2 and timestep % 2:
        out_a = []
        
        init_o = IC[0][(-l_no/2)][-2:] + IC[1][0]
            
        for i in range(l_no/2):
            h1 = [2 * F * (init_o[n - 1] - init_o[n]) + init_o[n] for n in range(1, len(init_o)/2)]
            h2 = [2 * F * (init_o[n + 1] - init_o[n]) + init_o[n] for n in range(len(init_o)/2, len(init_o) - 1)]
            
            if i < l_no/2-1: 
                out_a.append(h1+h2) 
                init_o = IC[0][((i+1)-l_no/2)][-2:] + out_a[i] + IC[1][i+1]
                
        if ed:
            out_a.append(h1+h2)
            return out_a 
        
        out_a += topTriangle(F, h1+h2, 1)        
        return out_a

    # If the node is not split, the initial conditions are dependent upon the timestep.  They're collected by taking
    # the information kept by the node, IC[0], needed and adding the information passed, IC[1].  With each subtimestep
    # that the function takes, the results are added to the initial conditions. Then the final timestep is given as the
    # initial condition to topTriangle.
    else:    
        out_a = []
        
        if timestep % 2:        
            init_o = IC[0][(-l_no/2)][-2:] + IC[1][0]
            
        else:
            init_o = IC[1][0] + IC[0][(-l_no/2)][:2] 
            
        for i in range(l_no/2):

            holder = [F * (init_o[n - 1] + init_o[n + 1]) + (1 - 2 *F) * init_o[n] for n in range(1, len(init_o) - 1)]
    
            if i < l_no/2-1:
                out_a.append(holder)            
                
                if timestep%2:            
                    init_o = IC[0][((i+1)-l_no/2)][-2:] + out_a[i] + IC[1][i+1]
                    
                else:
                    init_o = IC[1][i+1]+ out_a[i] + IC[0][((i+1)-l_no/2)][:2]
    
        if ed:
            out_a.append(holder)
            return out_a 
                
        out_a += topTriangle(F, holder, 0)        
        return out_a
        
            







