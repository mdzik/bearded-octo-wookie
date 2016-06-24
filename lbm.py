# -*- coding: utf-8 -*-
"""
Created on Sun May  3 15:18:01 2015

@author: michal

varius LBM basic consts

"""

import numpy as np


W = np.zeros(9)    
W[0] = 4./9.
W[1:5] = 1./9.
W[5:] = 1./36.

e = np.ndarray((2,9),dtype='int64')
e[0] = ( 0, 1, 0, -1, 0, 1, -1, -1, 1)
e[1] = ( 0, 0, 1, 0, -1, 1, 1, -1, -1)
e = e.T

e_opp = [0, 3, 4, 1, 2,  7 , 8, 5 , 6]

wp = np.array([ 1./9. - 1., 1./9., 1./9.,1./9.,1./9.,1./9.,1./9.,1./9.,1./9.])
wps = np.array([ 0., 1./8., 1./8., 1./8., 1./8., 1./8., 1./8., 1./8., 1./8.])
    

def forAll9do(f, *args):
    for i in range(9):
        f(i, *args)

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