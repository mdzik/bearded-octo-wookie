# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 10:04:30 2015

@author: mdzikowski
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May  2 22:37:49 2015

@author: michal
"""

import numpy as np
import matplotlib.pyplot as plt

# all basic const and tools for lbm are here
import bearded_octo_wookie.lbm as lbm
import bearded_octo_wookie.MRT as MRT
import bearded_octo_wookie.ZouHeBC as BC


tau0 = 1.
dx0=1.


x0 = 0.
y0 = 0.


nx0 = 25

ny0 = 100

nt = 2000

e0 = lbm.e
e = lbm.e
e_opp = lbm.e_opp
forAll9do = lbm.forAll9do
W = lbm.W
x0,y0 = np.meshgrid(np.arange(nx0), np.arange(ny0), indexing='ij')
#x0=x0.T
#y0=y0.T

################################################################
## INIT GRID 0
iy0n = list()
ix0n = list()
ix00,iy00 = np.meshgrid(np.arange(nx0), np.arange(ny0), indexing='ij')
#ix00=ix00.T
#iy00=iy00.T


bx0 = list()
by0 = list()

#for ix,iy in zip(ix00.reshape(nx0*ny0), iy00.reshape(nx0*ny0)):
#    #if m == 1:
#    if (ix == 0 and iy==ny0-1) or (ix == nx0-1 and iy==ny0-1) or (ix == 0 and iy==0) or (ix == nx0-1 and iy==0):
#        bx0.append(ix)
#        by0.append(iy)
        

for i in range(0,9):
    ixt = np.roll(np.roll(ix00[:,:],shift=e0[i][1],axis=0),shift=e0[i][0],axis=1)
    iyt = np.roll(np.roll(iy00[:,:],shift=e0[i][1],axis=0),shift=e0[i][0],axis=1)
    ix0n.append(ixt)
    iy0n.append(iyt)
    
ix0= np.array(ix0n)
iy0= np.array(iy0n)


f_in0 = np.zeros((nx0,ny0,9))
f_out0 = np.zeros_like(f_in0)




def init(_i, _W, _e, _rho, _U, _fin):
    _fin[:,:,_i] =  _W[_i] * _rho[:,:]
    cu  = 3. * ( _U[:,:,0] * _e[_i,0] + _U[:,:,1] * _e[_i,1])
    _fin[:,:,_i] = _W[_i] * _rho[:,:] * (1. + cu[:,:] + 0.5*cu[:,:]*cu[:,:] - (3./2.) * ( _U[:,:,0]**2 + _U[:,:,1]**2 ) )


def stream(_i, _ox, _oy, _fin, _fou):
    _fin[:,:,_i] = _fou[_ox[_i],_oy[_i],_i] 
    
def BGK(_i, _U, _rho, _e, _W, _tau, _F, _fin, _fou):

    cu  = 3. * ( _U[:,:,0] * _e[_i,0] + _U[:,:,1] * _e[_i,1])
    feq1 = _W[_i] * _rho[:,:] * (1. + cu[:,:] + 0.5*cu[:,:]*cu[:,:] - (3./2.) * ( _U[:,:,0]**2 + _U[:,:,1]**2 ) )

    cu  = 3. * ( (_U[:,:,0]+_F[:,:,0]) * _e[_i,0] + (_U[:,:,1] + _F[:,:,1]) * _e[_i,1])    
    feq2 = _W[_i] * _rho[:,:] * (1. + cu[:,:] + 0.5*cu[:,:]*cu[:,:] - (3./2.) * ( (_U[:,:,0]+_F[:,:,0])**2 + (_U[:,:,1]+_F[:,:,1])**2 ) )

    _fou[:,:,_i] = _fin[:,:,_i] + (_tau) * ( feq1[:,:] - _fin[:,:,_i] ) + (feq2[:,:]-feq1[:,:])


def BB(_i, _bx, _by, _e_opp, _fin, _fou):
    for bx,by in zip(_bx,_by):  
        _fou[bx,by,_i] = _fin[bx,by,_e_opp[_i]]     



def MRT_meq(_i, _U, _rho, _fmeq, _meq):
    _meq[_i] = _fmeq[i](_rho, _U[:,:,0], _U[:,:,1])

def applyBC(A, f):
    shape = f.shape
    _f = np.ones((shape[0]+1, shape[1]+1))
    _f[:,:-1] = f
    return A.dot(_f.T).T

def applyCornerBC(A, f):
    shape = f.shape
    _f = np.ones(shape[0]+1)
    _f[:-1] = f
    return A.dot(_f.T).T

def applyWideBC(A, f):
    shape = f.shape
    _f = np.ones((shape[0], shape[1]+1))
    _f[:,:-1] = f
    assert len(A[:,0,0] == len(_f[:,0]))
    for i, ff in enumerate(_f):
        f[i,:] = A[i,:,:].dot(_f[i,:]).T
    return f
    
meq0, M0 = MRT.getMRT(e0)

M0 = np.array(M0, dtype=float)
M0inv = np.linalg.inv(M0)

rho0 = np.ones_like(f_in0[:,:,0])
U0 = np.zeros_like(f_in0[:,:,:2])

forAll9do(init, W, e, rho0, U0,  f_in0)





_tau = 1.
F0 = np.zeros_like(U0)
F0[:,:,0] = 0.0000



#==============================================================================
# BOUNDARY CONDYTIONS
#==============================================================================


#Uxm = 0.000
#Uym = 0.0001
#ubc = lambda x,y : (y/float(ny0) * Uxm, x/float(nx0) * Uym)
#ubc = lambda x,y : (x/float(nx0) * Uxm, y/float(ny0) * Uym)

Uscale = 0.0001
def ubc(x,y) : 
    x = x / float(nx0) - 0.5   
    y = y / float(ny0)- 0.5   
    
    return (-Uscale*y, Uscale*x)

#==============================================================================
# x, y : 1d arrays
# an evenly spaced grid.
# u, v : 2d arrays
# x and y-velocities. Number of rows should match length of y, and the number of columns should match x.
#==============================================================================
#ux,uy = ubc(x0,y0)
#plt.streamplot(np.arange(ny0),np.arange(nx0),uy,ux )
#plt.show()

ubcC = ubc

#==============================================================================
# BC_fun_Left, BC_A_Left = BC.getUBc([0,1], 0., 0.)
# BC_fun_Right, BC_A_Right = BC.getUBc([0,-1], 0., 0.)
# BC_fun_Top, BC_A_Top = BC.getUBc([-1,0], 0., 0.0)
# BC_fun_Bottom, BC_A_Bottom = BC.getUBc([1,0], 0., 0.)
#==============================================================================

e_l = np.array([1,0])
e_r = np.array([-1,0])
e_t = np.array([0,-1])
e_b = np.array([0,1])

BC_fun_Left, BC_A_Left = BC.getUBc(e_l, 0., 0.)
BC_fun_Right, BC_A_Right = BC.getUBc(e_r, 0., 0.)
BC_fun_Top, BC_A_Top = BC.getUBc(e_t, 0., 0.0)
BC_fun_Bottom, BC_A_Bottom = BC.getUBc(e_b, 0., 0.)






BC_A_Right = list()            
for y,x in zip(y0[1:-1,-1], x0[1:-1,-1]): 
    BC_A_Right.append( BC_fun_Right( *ubc(x,y) ) )
BC_A_Right = np.array(BC_A_Right)                    

BC_A_Left = list()            
for y,x in zip(y0[1:-1,0], x0[1:-1,0]): 
    BC_A_Left.append( BC_fun_Left( *ubc(x,y) ) )
BC_A_Left = np.array(BC_A_Left)        

BC_A_Top = list()            
for y,x in zip(y0[-1,1:-1], x0[-1,1:-1]): 
    BC_A_Top.append( BC_fun_Top( *ubc(x,y) ) )
BC_A_Top = np.array(BC_A_Top)        

BC_A_Bottom = list()            
for y,x in zip(y0[0,1:-1], x0[0,1:-1]): 

    BC_A_Bottom.append( BC_fun_Bottom( *ubc(x,y) ) )
BC_A_Bottom = np.array(BC_A_Bottom)        



BC_fun_Left_Top, BC_A_Left_Top = BC.getCornerUBc(e_l+e_t, 0., 0.)
BC_fun_Left_Bottom, BC_A_Left_Bottom = BC.getCornerUBc(e_l+e_b, 0., 0.)

BC_fun_Right_Top, BC_A_Right_Top = BC.getCornerUBc(e_r+e_t, 0., 0.)
BC_fun_Right_Bottom, BC_A_Right_Bottom = BC.getCornerUBc(e_r+e_b, 0., 0.)





for it in range(nt):

    
    rho0[:,:] = np.sum( f_in0[:,:,:], 2 )
    
#==============================================================================
#     ### left
    f_in0[1:-1,0,:] = applyWideBC(BC_A_Left, f_in0[1:-1,0,:])
#     ### right
    f_in0[1:-1,-1,:] = applyWideBC(BC_A_Right, f_in0[1:-1,-1,:])
# 
#     ### bottom
    f_in0[0,1:-1,:] = applyWideBC(BC_A_Bottom, f_in0[0,1:-1,:])
#     ### top
    f_in0[-1,1:-1,:] = applyWideBC(BC_A_Top, f_in0[-1,1:-1,:])
#==============================================================================



    ### left top
    f_in0[-1,0,:] = applyCornerBC(BC_fun_Left_Top( rho0[-2,1], *ubcC(x0[-1,0], y0[-1,0] ) ) , f_in0[-1,0,:])
 
    ### left bottom
    f_in0[0,0,:] = applyCornerBC(BC_fun_Left_Bottom( rho0[1,1], *ubcC(x0[0,0], y0[0,0] ) ), f_in0[0,0,:])
 
    ### right top
    f_in0[-1,-1,:] = applyCornerBC(BC_fun_Right_Top( rho0[-2,-2], *ubcC(x0[-1,-1], y0[-1,-1] ) ), f_in0[-1,-1,:])    
    ### right bottom
    f_in0[0,-1,:] = applyCornerBC(BC_fun_Right_Bottom( rho0[1,-2], *ubcC(x0[0,-1], y0[0,-1] ) ), f_in0[0,-1,:])    


    
    rho0[:,:] = np.sum( f_in0[:,:,:], 2 )

   
    U0[:,:] = 0.
    for i in range(1,9):
        U0[:,:,0] =  U0[:,:,0] + e[i][0]*f_in0[:,:,i]  
        U0[:,:,1] =  U0[:,:,1] + e[i][1]*f_in0[:,:,i]
    U0[:,:,0] =  U0[:,:,0] / rho0
    U0[:,:,1] =  U0[:,:,1] / rho0
   

    #forAll9do(BGK, U0, rho0, e, W, tau0, F0, f_in0, f_out0)
    
    for i,f in enumerate(f_in0):
        f = f.T
        m =  (M0.dot(f))
        meq_0 = meq0(rho0[i,:], U0[i,:,0], U0[i,:,1])
        meq_1 = meq0(rho0[i,:], U0[i,:,0] + F0[i,:,0], U0[i,:,1] + F0[i,:,1])
        f_out = M0inv.dot( m + (_tau) * ( meq_0 - m ) + (meq_1 - meq_0) )
        f_out0[i,:,:] = f_out.T
 


   
    if it > 0 and np.mod(it, 500) == 0:
        rho0[:,:] = np.sum( f_in0[:,:,:], 2 )
         
        U0[:,:] = 0.
        for i in range(1,9):
            U0[:,:,0] =  U0[:,:,0] + e[i][0]*f_in0[:,:,i]  
            U0[:,:,1] =  U0[:,:,1] + e[i][1]*f_in0[:,:,i]
        U0[:,:,0] =  U0[:,:,0] / rho0
        U0[:,:,1] =  U0[:,:,1] / rho0
        
        
        iii = 0
        plt.cla()
        
        plt.subplot(2,2,1)
        plt.contourf(x0,y0,U0[:,:,0])
        #plt.imshow(U0[:,:,0],interpolation='nearest')
        #print np.max(np.sqrt(U0[:,:,0]**2))
        plt.colorbar()        
        
        plt.subplot(2,2,2)
        plt.contourf(x0,y0,U0[:,:,1])        
        #plt.imshow(U0[:,:,1],interpolation='nearest')
        print np.max(np.sqrt(U0[:,:,1]**2))
        plt.colorbar()        
    
        plt.subplot(2,2,3)
        #plt.contourf(ix00,iy00,np.sqrt(U0[:,:,0]**2 + U0[:,:,1]**2))
        plt.quiver(x0,y0,U0[:,:,0], U0[:,:,1] )
        plt.streamplot(np.arange(nx0),np.arange(ny0),U0[:,:,0].T,U0[:,:,1].T)
        plt.subplot(2,2,4)
        plt.contourf(x0,y0,rho0[:,:])        
        #plt.imshow(rho0[:,:],interpolation='nearest')
        plt.colorbar()
       

#==============================================================================
#         plt.figure()
#         plt.plot(U0[:,0,1])
#         plt.plot(U0[:,0,0])
#==============================================================================
        
        plt.show()

    #forAll9do(BB, bx0, by0, e_opp, f_in0, f_out0)
    
    forAll9do(stream, ix0, iy0, f_in0, f_out0)

plt.contourf(x0,y0,U0[:,:,0])

plt.show()