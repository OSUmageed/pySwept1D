#The Swept Rule functions.


def communication(vect, stage):
    #When it isn't divisible by 2, it's true.  Dammit.  I need to get only the top parts to communicate.
    if stage % 2:
        Comm = [vect[t][-2:] for t in range(len(vect))]
    else:
        Comm = [vect[t][:2] for t in range(len(vect))]

    return Comm

def topTriangle(F, IC):
    out_a = [IC]
    while len(out_a[-1]) > 2:

        holder = [F * (out_a[-1][n - 1] + out_a[-1][n + 1] - 2 * out_a[-1][n]) + out_a[-1][n] for n in range(1, len(out_a[-1]) - 1)]
        out_a += [holder]


    return out_a

def bottomTriangle(F, IC, l_nodes):
    out_a = IC[0].extend(IC[-1])
    while len(out_a[-1]) < l_nodes:
        holder = [F * (out_a[-1][n - 1] + out_a[-1][n + 1] - 2 * out_a[-1][n]) +
                  out_a[-1][n] for n in range(1, len(out_a[-1]) - 1)]
        holder.reverse()
        holder.extend(IC[len(out_a)])
        holder.reverse()
        holder.extend(IC[-len(out_a)])
        out_a += [holder]

    out_a += [topTriangle(F,out_a[-1])]

    return out_a
