#The Swept Rule functions.


def communication(vect, stage):

    # When it isn't divisible by 2, it's true.  Dammit.  I need to get only the top parts to communicate.
    if stage % 2:
        comm = [vect[t][-2:] for t in range(len(vect))]
        
    else:
        comm = [vect[t][:2] for t in range(len(vect))]

    return comm


def topTriangle(F, IC, split):
    
    out_a = [IC]
    
    if split:
        while len(out_a[-1]) > 2:
    
            h1 = [F * (init_o[-1][n - 1] - 2 * init_o[-1][n]) + init_o[-1][n] for n in range(1, len(out_a)/2)]
            h2 = [F * (init_o[-1][n + 1] - 2 * init_o[-1][n]) + init_o[-1][n] for n in range(len(out_a)/2, len(out_a) - 1)]        
            out_a += [h1+h2]
    
        return out_a
  
    else:
        while len(out_a[-1]) > 2:
    
            holder = [F * (out_a[-1][n - 1] + out_a[-1][n + 1] - 2 * out_a[-1][n]) + out_a[-1][n] for n in range(1, len(out_a[-1]) - 1)]
            out_a += [holder]
    
        return out_a


def bottomTriangle(F, IC, l_no, timestep, node, ed):
    #The next timestep's values are the passed values.  They go from top to bottom.
    
    #This is where to handle the split triangle.
    if node>l_no/2-1 and timestep % 2:
        out_a = []
        #This array goes
        init_o =  IC[0][(-l_no/2)][-2:] + IC[1][0] 
            
        for i in range(l_no/2):
            h1 = [F * (init_o[n - 1] - 2 * init_o[n]) + init_o[n] for n in range(1, len(init_o)/2)]
            h2 = [F * (init_o[n + 1] - 2 * init_o[n]) + init_o[n] for n in range(len(init_o)/2, len(init_o) - 1)]
            
            if i < l_no/2-1: 
                out_a.append(h1+h2) 
                init_o = IC[0][(i-l_no/2)][-2:] + out_a[i] + IC[1][i]
                
        if ed:
            out_a.append(h1+h2)
            return out_a 
        
        out_a += topTriangle(F, holder, 1)        
        return out_a
        
    else:    
        out_a = []
        
        if timestep % 2:        
            init_o = IC[0][(-l_no/2)][-2:] + IC[1][0]
            
        else:
            init_o = IC[1][0] + IC[0][(-l_no/2)][:2] 
            
        for i in range(l_no/2):

            holder = [F * (init_o[n - 1] + init_o[n + 1] - 2 * init_o[n]) + init_o[n] for n in range(1, len(init_o) - 1)]
    
            if i < l_no/2-1:
                out_a.append(holder)            
                
                if timestep%2:            
                    init_o = IC[0][(i-l_no/2)][-2:] + out_a[i] + IC[1][i]
                    
                else:
                    init_o = IC[1][i]+ out_a[i] + IC[0][(i-l_no/2)][:2]
    
        if ed:
            out_a.append(holder)
            return out_a 
                
        out_a += topTriangle(F, holder, 0)        
        return out_a
        
            







