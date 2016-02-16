#The Swept Rule functions.


def communication(vect, stage):

    # When it isn't divisible by 2, it's true.  Dammit.  I need to get only the top parts to communicate.
    if stage % 2:
        comm = [vect[t][:2] for t in range(len(vect))]
    else:
        comm = [vect[t][-2:] for t in range(len(vect))]

    return comm


def topTriangle(F, IC):

    out_a = [IC]
    while len(out_a[-1]) > 2:

        holder = [F * (out_a[-1][n - 1] + out_a[-1][n + 1] - 2 * out_a[-1][n]) + out_a[-1][n] for n in range(1, len(out_a[-1]) - 1)]
        out_a += [holder]

    return out_a


def bottomTriangle(F, IC, l_no, ed):
    #The next timestep's values are the passed values.  They go from top to bottom.
    
    init_o = IC[0][(-l_no/2)][-2:] + IC[1][0]
    holder = []
    
    for i in range(l_no/2):

    #Still need to handle side to side motion
        Jim = [F * (init_o[n - 1] + init_o[n + 1] - 2 * init_o[n]) + init_o[n] for n in range(1, len(init_o) - 1)]

        if i < l_no/2-1:
            holder.append(Jim)

            init_o = IC[0][(i-l_no/2)][-2:] + holder[i] + IC[1][i]

    if ed:
        return holder 
            
    holder += topTriangle(F,Jim)
    
    return holder

        
            







