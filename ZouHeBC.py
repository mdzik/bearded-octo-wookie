from bearded_octo_wookie.lbm import *

from sympy import *
from fractions import Fraction
from  bearded_octo_wookie.MRT import genFeq, getMRT
from sympy.utilities.codegen import codegen

#W = np.array([Rational(_W) / Rational(36) for _W in W[:] * 36.])

U = [var('U_0'), var('U_1')]
rho = var('rho')

D = 2
Q = 9


def getUBc(wall_e, ux, uy, verbose=False, corner_rho=1):
    eqs = list()
    
    feq = genFeq(e)
    meq, M = getMRT(e)
    wall_e = np.array(wall_e)
    wall_e = wall_e / np.sqrt(np.sum(wall_e**2))
    #print wall_e
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

    if verbose:
        for s in sol:
            pprint(s)
            pprint(sol[s])
            print "WWWWWWWWWWWWWWWWWW  " + str(s) + "  WWWWWWWWWWWWWWWWWWWW"
            print ccode(sol[s], s)
            print "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"            

    
    A = np.zeros((9,10)).tolist()
    for i in range(Q):
        if i in i_known:
            A[i][i] = 1
        elif i in i_unknown:
            eq = sol[ fs[i] ]
            for i2 in range(Q):         
                A[i][i2] = expand(eq).coeff(ifs[i2])
                eq = expand(eq - A[i][i2] * ifs[i2])
            A[i][9] = eq
            
            
                
    f = lambdify(U, A) 
    return lambda x,y : np.array(f(x,y), dtype=float), np.array(f(ux,uy), dtype=float)

def getCornerUBc(wall_e, ux, uy, verbose=False, corner_rho=1):
    eqs = list()
    
    feq = genFeq(e)
    meq, M = getMRT(e)
    wall_e = np.array(wall_e)
    wall_e = wall_e / np.sqrt(np.sum(wall_e**2))
    #print wall_e
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

    if verbose:
        for s in sol:
            pprint(s)
            pprint(sol[s])
            print "WWWWWWWWWWWWWWWWWW  " + str(s) + "  WWWWWWWWWWWWWWWWWWWW"
            print ccode(sol[s], s)
            print "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"            

    
    A = np.zeros((9,10)).tolist()
    for i in range(Q):
        if i in i_known:
            A[i][i] = 1
        elif i in i_unknown:
            eq = sol[ fs[i] ]
            for i2 in range(Q):         
                A[i][i2] = expand(eq).coeff(ifs[i2])
                eq = expand(eq - A[i][i2] * ifs[i2])
            A[i][9] = eq
            
            
                
    f = lambdify([rho, U], A) 
    return lambda x,y,z : np.array(f(x,y,z), dtype=float), np.array(f(ux,uy,corner_rho), dtype=float)
    
    
    
    
def getRhoBc(wall_e, rhobc, Utbc = 0.):
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
    Ut = var("Ut")
    eqs.append( wall_e.dot(U) - Un )   
    eqs.append(wall_e_t.dot(U) + Ut)
        
    
    unknowns.append(Un)
    unknowns.append(U[0])
    unknowns.append(U[1])    
    
    sol = solve(eqs, unknowns)

    A = np.zeros((9,10)).tolist()
    for i in range(Q):
        if i in i_known:
            A[i][i] = 1
        elif i in i_unknown:
            eq = sol[ fs[i] ]
            for i2 in range(Q):         
                A[i][i2] = expand(eq).coeff(ifs[i2])
                eq = expand(eq - A[i][i2] * ifs[i2])
            A[i][9] = eq

    f = lambdify([rho,Ut], A) 
    return lambda x, y : np.array(f(x,y), dtype=float), np.array(f(rhobc, Utbc), dtype=float)
    
    
def getDNBc(wall_e):
    eqs = list()
    
    feq = genFeq(e)
    meq, M = getMRT(e)
       
    t = 'f_0'
    t2 = 'if_0'
    for i in range(1,Q):
        t = t + ',f_'+str(i)
        t2 = t2 + ',if_'+str(i)
    
    fs = np.array([var('f_'+str(i)) for i in range(9)])
    ifs = np.array([var('if_'+str(i)) for i in range(9)])

    
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
    
    

    P = np.zeros((2,2)).tolist()
    for k, v in enumerate(e):
        Pij = np.array([  [v[j] * v[i] * ( feq[k] - fs[k] ) for j in range(2)]  for i in range(2) ])
        P = np.array(P) + Pij
    Pn = P.dot(wall_e)
    
    
    eqs.append(m[0] - rho)    
    
    eqs.append(m[1] - U[0] * rho)    
    eqs.append(m[2] - U[1] * rho)    
    

 

    ### NORMAL PART REFLECTION
    
#    for i in range(1,Q):
#        for i2 in range(1,Q):
#            if ( e[i][0] + wall_e[0] == 0  and  e[i][1] + wall_e[1] == 0 ) \
#            and ( e[i][0] + e[i2][0] == 0 and  e[i][1] + e[i2][1] == 0 ):             
#                    eqs.append(fs[i] - feq[i] - (fs[i2] - feq[i2]))
#        
#   
   

#    ux = 1.
#    uy = 1.     
    print eqs
    print unknowns
    sol = solve(eqs, unknowns)
    print sol
    
    A = np.zeros((9,10)).tolist()
    for i in range(Q):
        if i in i_known:
            A[i][i] = 1
        elif i in i_unknown:
            eq = sol[ fs[i] ]
            for i2 in range(Q):         
                A[i][i2] = expand(eq).coeff(ifs[i2])
                eq = expand(eq - A[i][i2] * ifs[i2])
            A[i][9] = eq

    f = lambdify((rho,U[0],U[1]), A) 
    
    unknowns = list()
    eqs = list()    
    nu = Rational(1.)/Rational(6.)

    eqs.append(Pn[0] - rho*wall_e[0] / nu)    
    eqs.append(Pn[1] - rho*wall_e[1] / nu)   
    unknowns.append(U[0])
    unknowns.append(U[1])        
   
    sol2 = solve(eqs, unknowns)    

    f2 = lambdify([rho, fs], sol2) 
    
    return f, f2
    
    
    
if __name__ == '__main__':
    
#print getDNBc([0,1])    
    getCornerUBc([1,1], 0., 0.01, True )
#fA,A = getRhoBc([1,0], 1. )
#
#f0 = W[:]
#f = np.ones(10)
#f[:-1] = f0
#f1 = A.dot(f)
##print f1
#
#rho = np.sum(f1)
#
#U0 = np.zeros(2)
#for i in range(1,9):
#    U0[0] =  U0[0] + e[i][0]*f1[i]
#    U0[1] =  U0[1] + e[i][1]*f1[i]
#U0[0] =  U0[0] / rho
#U0[1] =  U0[1] / rho
#
#print U0


