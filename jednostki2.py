# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 17:45:08 2013

@author: michal
"""

import numpy as np
import scipy.optimize
#import matplotlib.pyplot as plt
import scipy.integrate
import scipy.interpolate as inter



g = -1.
cs2 = 1./3.

a2 = 3.852462271644162
b2 = 0.1304438860971524 * 4.0
c2 = 2.785855170470555

def PR(rho,T):
    return c2*rho*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(1-b2*rho/4)**3-a2*rho**2
    
def PV(v,T):   
    return c2*(b2/(4*v)+b2**2/(16*v**2)-b2**3/(64*v**3)+1)*T/((1-b2/(4*v))**3*v)-a2/v**2
    
    
def Psi(rho,T):
    return scipy.sqrt( scipy.absolute( 2.*(PR(rho,T)-rho*cs2)/(cs2*g) ))

 
def dP_dRho(rho,T):
    return c2*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(1-b2*rho/4)**3+3*b2*c2*rho*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(4*(1-b2*rho/4)**4)+c2*rho*(-3*b2**3*rho**2/64+b2**2*rho/8+b2/4)*T/(1-b2*rho/4)**3-2*a2*rho

def d2P_dRho(rho,T): 
    return 3*b2*c2*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(2*(1-b2*rho/4)**4)+3*b2**2*c2*rho*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(4*(1-b2*rho/4)**5)+2*c2*(-3*b2**3*rho**2/64+b2**2*rho/8+b2/4)*T/(1-b2*rho/4)**3+3*b2*c2*rho*(-3*b2**3*rho**2/64+b2**2*rho/8+b2/4)*T/(2*(1-b2*rho/4)**4)+c2*rho*(b2**2/8-3*b2**3*rho/32)*T/(1-b2*rho/4)**3-2*a2
  
def dPsi_dRho(rho,T):
    #return scipy.sqrt(6.)*(c2*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(1-b2*rho/4)**3+3*b2*c2*rho*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(4*(1-b2*rho/4)**4)+c2*rho*(-3*b2**3*rho**2/64+b2**2*rho/8+b2/4)*T/(1-b2*rho/4)**3-2*a2*rho-1/3)*(c2*rho*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(1-b2*rho/4)**3-a2*rho**2-rho/3)/(2*scipy.sqrt( scipy.absolute(g))* scipy.absolute(c2*rho*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(1-b2*rho/4)**3-a2*rho**2-rho/3)**(3/2))
    dh = 0.00001    
    return (Psi(rho+dh)**2-Psi(rho-dh)**2) / (4.*dh) 
    #return (c2*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(1-b2*rho/4)**3 +3*b2*c2*rho*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(4*(1-b2*rho/4)**4) +c2*rho*(-3*b2**3*rho**2/64+b2**2*rho/8+b2/4)*T/(1-b2*rho/4)**3-2*a2*rho-cs2) *(c2*rho*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T/(1-b2*rho/4)**3  -a2*rho**2-cs2*rho) /(scipy.sqrt(2)*scipy.sqrt(scipy.fabs(cs2))*scipy.sqrt(scipy.fabs(g))          *scipy.fabs(c2*rho*(-b2**3*rho**3/64+b2**2*rho**2/16+b2*rho/4+1)*T                /(1-b2*rho/4)**3                -a2*rho**2-cs2*rho)           **(3/2))
def iPR(pa,rhov, rhol,T):
    return b2**2*c2*rhov**2*scipy.log(rhov)*T/(b2**2*rhov**2-8*b2*rhov+16) -8*b2*c2*rhov*scipy.log(rhov)*T/(b2**2*rhov**2-8*b2*rhov+16) +16*c2*scipy.log(rhov)*T/(b2**2*rhov**2-8*b2*rhov+16) -8*b2*c2*rhov*T/(b2**2*rhov**2-8*b2*rhov+16)+48*c2*T/(b2**2*rhov**2-8*b2*rhov+16) -b2**2*c2*rhol**2*scipy.log(rhol)*T/(b2**2*rhol**2-8*b2*rhol+16) +8*b2*c2*rhol*scipy.log(rhol)*T/(b2**2*rhol**2-8*b2*rhol+16) -16*c2*scipy.log(rhol)*T/(b2**2*rhol**2-8*b2*rhol+16) +8*b2*c2*rhol*T/(b2**2*rhol**2-8*b2*rhol+16)-48*c2*T/(b2**2*rhol**2-8*b2*rhol+16) +16*pa/(b2**2*rhov**3-8*b2*rhov**2+16*rhov) -a2*b2**2*rhov**3/(b2**2*rhov**2-8*b2*rhov+16) +8*a2*b2*rhov**2/(b2**2*rhov**2-8*b2*rhov+16) +b2**2*pa*rhov/(b2**2*rhov**2-8*b2*rhov+16) -16*a2*rhov/(b2**2*rhov**2-8*b2*rhov+16)-8*b2*pa/(b2**2*rhov**2-8*b2*rhov+16) -16*pa/(b2**2*rhol**3-8*b2*rhol**2+16*rhol) +a2*b2**2*rhol**3/(b2**2*rhol**2-8*b2*rhol+16) -8*a2*b2*rhol**2/(b2**2*rhol**2-8*b2*rhol+16) -b2**2*pa*rhol/(b2**2*rhol**2-8*b2*rhol+16) +16*a2*rhol/(b2**2*rhol**2-8*b2*rhol+16)+8*b2*pa/(b2**2*rhol**2-8*b2*rhol+16)



def surTension(T):
    return 0.017*(1.-T)**1.498
    
_luk = np.array([
[0.3, 2.23100559782892],
[0.35, 1.99054269043015],
[0.4, 1.75985109979594],
[0.45, 1.53929878324104],
[0.5, 1.32930158966126],
[0.55, 1.13033480926852],
[0.6, 0.942949076889676],
[0.65, 0.767793010020819],
[0.7, 0.605646787446737],
[0.75, 0.45747463374574],
[0.8, 0.324512726792806],
[0.85, 0.20843128784423],
[0.9, 0.111679954338428],
[0.95, 0.0384342775221782],
[1, 0]])
_stL = inter.interp1d(_luk[:,0],_luk[:,1])    

def surTension_v2(T,k = 1.):
    return _stL(T) * (k**0.5)

class SzukajP_Maxcwell:
    T = 0.
    def __call__(self, p):
        f = lambda rho: p  - PR(rho,self.T)
        self.r1 = scipy.optimize.bisect(f, 0, self.r01)
        self.r2 = scipy.optimize.bisect(f, self.r02, 5.)
        return  iPR(p, self.r1,self.r2, self.T)


    def getRhos(self, T):
        f = lambda(x): dP_dRho(x,T)
        rh1 = scipy.optimize.bisect(f, 0, 1.)
        rh2c = scipy.optimize.bisect(f, 0.9, 4)
        rh2 = rh2c
        self.T = T   
        if PR(rh2,T) < 0 :
            f = lambda(x): PR(x,T)
            rh21 = scipy.optimize.bisect(f, rh2, 4)
            while f(rh21) <= 0:
                rh21=rh21*1.000000001
            rh2 = rh21
        
        
        self.r01 = rh1 
        self.r02 = rh2     
    
        p0 = scipy.optimize.bisect( self, PR(rh2,T), PR(rh1,T) )
        
        return self.T, self.r1, self.r2, p0, rh2c, PR(rh2c,T)
    






def Params(T):
    #a = -3.861773
    #b = 5.425680685
    sm = SzukajP_Maxcwell()
    rs = sm.getRhos(T)
    return rs
    
    
def GetReCa(T,Nx,k,omega,U):
    tp = Params(T)
    nu = (1./3.)*(1./omega-0.5)
    r = tp[2]

    s = surTension_v2(T,k)
    Re = U * Nx / nu
    Ca = U * r * nu / s
    h6 = 0.417* ( 1. - np.exp(-1.69*Ca**0.5025)) 
    return dict([('Re',Re), ('Ca',Ca), ('h6', h6)])
    
#if __name__ == '__main__':
#    sm = SzukajP_Maxcwell() 
#    params = list()    
#    Ts = np.linspace(0.8,0.98,num=20)
#    for t in Ts:
#        row = sm.getRhos(t)
#        print row
#        params.append(row)
#    
#    params = np.array(params).T
#    
#    plt.plot(Ts,PR(params[2],Ts)-PR(params[4],Ts))
#    
#    
#    Pref = 102400.
#    rhoLref = 1000.
#    
#    
#    #Toper = 0.98
#    for Toper in np.linspace(0.6,0.98,num=20):
#        RefParams = sm.getRhos(Toper)
#        
#        Pc = Pref/RefParams[3]
#        RhoC = rhoLref/RefParams[2]
#        
#        print "Tref: ",Toper," Pc: ", Pc, " Rhoc: ", RhoC, "dP_crit:", Pc*(PR(RefParams[2],Toper)-PR(RefParams[4],Toper))/Pref
#
#



#plt.show()
#    
#def sigma(k,T):
#    b = 1.498
#    a = 0.017
#    return np.sqrt(k)*a*(1.-T)**b
#    
#def NuWb(nx,k):
#    dx = 1. / nx
#    dt = np.sqrt(k*dx*dx)
#
#    U0 = dx/dt
#
#    u_lb = u/U0
#
#    nu_lb = nx*u_lb/Re
#    
#    Wb_lb = RhoL(T)*u_lb*u_lb*nx/sigma(k)
#    
#    return (Wb_lb,nu_lb)
#    
#    
#    
#    
#class SeekK:    
#    def __init__(self, nx):
#        self.nx = nx
#    
#    
#    def __call__(self, k):
#        Wb_lb,nu_lb = NuWb(self.nx, k)
#        return Wb - Wb_lb
#        
#        
#
#nxs = list()
#nus = list()
#ks = list()
#
#nu_lb = 0.01
#
#for nx in range(50,200,10):
#    nxs.append(nx)
#    seeker = SeekK(nx)
#    
#    print seeker(0.001)," xxx " ,seeker(1.)
#    
#    k1 = scipy.optimize.bisect(seeker, 0.0001, 1.)
#    
#    ks.append(k1)
#    Wb_lb,nu_lb = NuWb(nx, k1)
#    nus.append(nu_lb)
#    
#print nus
#
#plt.figure()
#plt.plot(nxs,ks, nxs, np.ones(len(nxs))*0.01)
#
#plt.show()
#
#













    