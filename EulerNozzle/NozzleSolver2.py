# -*- coding: utf-8 -*-
"""
Created on Mon May 11 14:09:59 2015

@author: mdzikowski
"""

from bearded_octo_wookie import *
import numpy as np
import matplotlib.pyplot as plt


kappa = 1.4
R = 1.


def getMa(u):
    rho = u[:,0]
    rhoU = u[:,1]
    rhoE = u[:,2]
    
    rhoU2 = rhoU**2/rho
    p = (kappa-1.)*(rhoE-rhoU2/2.)
    
    c = np.sqrt(kappa * p / rho)
    
    return rhoU/rho / c

def getP(u):
    rho = u[:,0]
    rhoU = u[:,1]
    rhoE = u[:,2]
    
    rhoU2 = rhoU**2/rho
    p = (kappa-1.)*(rhoE-rhoU2/2.)
    return p

def getT(u):
    rho = u[:,0]
    rhoU = u[:,1]
    rhoE = u[:,2]
    
    rhoU2 = rhoU**2/rho
    p = (kappa-1.)*(rhoE-rhoU2/2.)
    return p / rho / R
    
def getF(u,F):
    rho = u[:,0]
    rhoU = u[:,1]
    rhoE = u[:,2]
    
    rhoU2 = rhoU**2/rho
    p = (kappa-1.)*(rhoE-rhoU2/2.)
    
    F[:,0] = rhoU
    F[:,1] = rhoU2 + p
    F[:,2] = (rhoE+p)*rhoU/rho
    
class NozzleFlow2:
    NX = 100
   
    def __init__(self, FluxClass,  **kargs):
        self.FC = FluxClass()
        #elf#FM = FluxClass.FM
        self.CFL = kargs['CFL']
        
        
        self.r = kargs['r']
        self.dt = 1.
        self.dx = 1. / self.NX
        self.p_r = 0.9      
        self.rho_bc = 0.9
        self.rho_r = 1.
        self.X = np.linspace(0.,1., self.NX)
        self.p_bc = 1.        
        self.U = np.zeros((self.NX, 3))
        u = self.U
        u[:,0] = self.rho_bc + (self.rho_r-self.rho_bc) * self.X / float(self.NX)
        u[:,1] = 0.#self.u_bc*u[:,0] * self.X / float(self.NX)
        pp = self.p_bc + (self.p_r-self.p_bc)* self.X / float(self.NX)
        u[:,2] = u[0,0]*( 1. / (kappa-1.) * pp / u[0,0] + (u[0,1]/u[0,0])**2)


        
    def FM(self, *args):
        return self.FC.FP(*args) 
        
    def FP(self, *args):
        return self.FC.FP(*args)
        
    def getS(self, U):
        rho = U[:,0]
        rhoU = U[:,1]
        u = rhoU / rho
        rhoE = U[:,2]
        rhoU2 = rhoU**2/rho
        p = (kappa-1.)*(rhoE-rhoU2/2.)
        r2 = np.zeros(len(self.r)+2)
        r2[1:-1] = self.r
        r2[0] = r2[1] + (r2[1] - r2[2])
        r2[-1] = 2. * r2[-2] - r2[-3]

        #plt.plot(r)
        #plt.plot(np.arange(-1,len(self.r)+1), r2,'o')
        
        
        
        rdrdx = 1. / self.r * (r2[2:] - r2[:-2]) / self.dx
        #plt.plot(rdrdx)
        #plt.show()
        S0 = np.array( [  rho/ rdrdx,  rhoU/ rdrdx,  (rhoE + p)/ rdrdx] ).T

        return  - 2. * S0 
        
    def step(self):

        self.resetDt()
        
        
        U = self.U
        
        UP = np.zeros_like(U)
        UP[:-1] = U[1:]
        UP[-1] = U[-1]
        UP[-1,2] = U[-1,0]*( 1. / (kappa-1.) * self.p_r / U[-1,0] + (U[-1,1]/U[-1,0])**2)    
        #UP = UPM[:-1,:]   
        

        UM = np.zeros_like(U)
        UM[1:] = U[:-1] 
        UM[0] = U[0]
        UM[0,0] = self.rho_bc
        UM[0,2] = U[0,0]*( 1. / (kappa-1.) * self.p_bc / U[0,0] + (U[0,1]/U[0,0])**2)     
        #UM = UM[:-1,:]
        #plt.plot(U[:,0])
        
        #plt.plot(UP[:,0], 'r-')
        #plt.plot(UM[:,0], 'k-')
        #plt.show()
        self.U = self.U - self.dt / self.dx * ( self.FP(U, UP, self.dt, self.dx) - self.FM(UM, U, self.dt, self.dx) ) + self.getS(U) * self.dt
        
    def resetDt(self):
        u = self.U
        rho = u[:,0]
        rhoU = u[:,1]
        rhoE = u[:,2]
        
        rhoU2 = rhoU**2/rho
        p = (kappa-1.)*(rhoE-rhoU2/2.)
        
        c = np.sqrt(kappa * p / rho)
        
        umax = np.max( np.absolute(rhoU/rho) + c )    
        
        self.dt =  self.CFL * self.dx  / umax

class Lax_Friedrichs_Flux:
    
    def FP(self, uL, uR, dt, dx):
        
        F1 = np.zeros_like(uL)
        F2 = np.zeros_like(uL)
        
        getF( uL, F1 )
        getF( uR, F2 )
        
        return 0.5 * ( F1 + F2 ) - dx/2./dt * ( uR - uL )
    
#    def FM(self, uL, uR, dt, dx):
#    
#        F1 = np.zeros_like(uL)
#        F2 = np.zeros_like(uL)
#        
#        getF( uL, F1 )
#        getF( uR, F2 )
#        return 0.5 * ( F1 + F2 ) - dx/2./dt * (  uL - uR )               
    
if __name__ == "__main__":
    
    X = np.linspace(0., 1., NozzleFlow2.NX)    
    d2 = 0.1
    f0 = lambda(x):  (1.-d2)*(2.*(x-0.5))**2 + d2

    r = np.array([f0(y) for y in X])

    plt.plot(np.pi * r ** 2)
    plt.show()
    
    NF2 = NozzleFlow2(Lax_Friedrichs_Flux, CFL=0.2, r=r)
    #plt.plot(NF2.U)
    #plt.show()
    it = 0
    while True:
        it = it + 1
        
        NF2.step()
        if np.mod(it, 100) ==0:
            plt.plot(NF2.U[:,0], label=r'$\rho$')
            plt.plot(NF2.U[:,1], label=r'$\rho u$')
            plt.plot(getP(NF2.U), label=r'$p$')
            plt.grid(which='both')
            plt.legend()
            plt.show()

        
    
    print "akuku"    