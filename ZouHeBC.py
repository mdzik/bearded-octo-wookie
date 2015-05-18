from bearded_octo_wookie.lbm import *

from sympy import *
from fractions import Fraction
from  bearded_octo_wookie.MRT import genFeq, getMRT

W = np.array([Rational(_W) / Rational(36) for _W in W[:] * 36.])

U = [var('U_0'), var('U_1')]
rho = var('rho')

D = 2
Q = 9




def getUBc(wall_e, ux, uy):
    eqs = list()
    
    feq = genFeq(e)
    meq, M = getMRT(e)
       
    t = 'f_0'
    t2 = 'if_0'
    for i in range(1,Q):
        t = t + ',f_'+str(i)
        t2 = t2 + ',if_'+str(i)
    
    fs = np.array(var(t))
    ifs = np.array(var(t2))   
    
    ### incoming
    i_known = list()
    i_unknown = list()
    
    unknowns = list()
    for i in range(1,Q):
        if e[i][0]*wall_e[0] + e[i][1]*wall_e[1] <= 0:
            fs[i] = ifs[i]
            i_known.append(i)
        else:
            unknowns.append(fs[i])
            i_unknown.append(i)
    
    fs[0] = ifs[0]
    i_known.append(0)  
    
    m = M.dot(fs)
    meq = M.dot(feq)
    
    
    for i in range(3):
        eqs.append(meq[i] - m[i])
    
    
    ### NORMAL PART REFLECTION
    
    for i in range(1,Q):
        for i2 in range(1,Q):
            if ( e[i][0] + wall_e[0] == 0  and  e[i][1] + wall_e[1] == 0 ) \
            and ( e[i][0] + e[i2][0] == 0 and  e[i][1] + e[i2][1] == 0 ):             
                    eqs.append(fs[i] - feq[i] - (fs[i2] - feq[i2]))
        
    unknowns.append(rho)
    sol = solve(eqs, unknowns)


    
    A = np.zeros((9,9)).tolist()
    for i in range(Q):
        if i in i_known:
            A[i][i] = 1
        elif i in i_unknown:
            for i2 in range(Q):
                eq = sol[ fs[i] ]
                A[i][i2] = expand(eq).coeff(ifs[i2])
                #A[i][i2] = A[i][i2].subs(U[0], ux).subs(U[1], uy)
                
            #transport_f.append( lambdify(ifs, sol[ fs[i] ] ) )

    f = lambdify(U, A) 
    return f, f(ux,uy)
    
    
    
    
def getRhoBc(wall_e, rhobc):
    eqs = list()
    
    feq = genFeq(e)
    meq, M = getMRT(e)
       
    t = 'f_0'
    t2 = 'if_0'
    for i in range(1,Q):
        t = t + ',f_'+str(i)
        t2 = t2 + ',if_'+str(i)
    
    fs = np.array(var(t))
    ifs = np.array(var(t2))   
    
    ### incoming
    i_known = list()
    i_unknown = list()
    
    unknowns = list()
    for i in range(1,Q):
        if e[i][0]*wall_e[0] + e[i][1]*wall_e[1] <= 0:
            fs[i] = ifs[i]
            i_known.append(i)
        else:
            unknowns.append(fs[i])
            i_unknown.append(i)
    
    fs[0] = ifs[0]
    i_known.append(0)  
    
    m = M.dot(fs)
    meq = M.dot(feq)
    
    
    for i in range(3):
        eqs.append(meq[i] - m[i])
    
    
    ### NORMAL PART REFLECTION
    
    for i in range(1,Q):
        for i2 in range(1,Q):
            if ( e[i][0] + wall_e[0] == 0  and  e[i][1] + wall_e[1] == 0 ) \
            and ( e[i][0] + e[i2][0] == 0 and  e[i][1] + e[i2][1] == 0 ):             
                    eqs.append(fs[i] - feq[i] - (fs[i2] - feq[i2]))
        
        
    wall_e_t = np.array(var("x1,y1"))
    wall_e_t = solve([wall_e_t.dot(wall_e), wall_e_t.dot(wall_e_t) - 1.] , wall_e_t.tolist())
    wall_e_t = np.array(wall_e_t[0])
    wall_e = np.array(wall_e)
    Un = var("Un")
    eqs.append( wall_e.dot(U) - Un )   
    eqs.append(wall_e_t.dot(U))
        
    
    unknowns.append(Un)
    sol = solve(eqs, unknowns)

    for s in unknowns:
        pprint(s)
    sfsdfsdf
    A = np.zeros((9,9)).tolist()
    for i in range(Q):
        if i in i_known:
            A[i][i] = 1
        elif i in i_unknown:
            for i2 in range(Q):
                eq = sol[ fs[i] ]
                A[i][i2] = expand(eq).coeff(ifs[i2])
                #A[i][i2] = A[i][i2].subs(U[0], ux).subs(U[1], uy)
                
            #transport_f.append( lambdify(ifs, sol[ fs[i] ] ) )

    f = lambdify(U, A) 
    return f, f(ux,uy)
    
#print getUBc([0,1], 0., 0.01 )
print getRhoBc([0,1], 1. )

