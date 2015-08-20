 # -*- coding: utf-8 -*-
"""
Created on Tue May 12 12:57:41 2015

@author: michal
"""

from bearded_octo_wookie.lbm import *

from sympy import *
from fractions import Fraction

W = np.array([Rational(_W) / Rational(36) for _W in W[:] * 36.])

U = [var('U_0'), var('U_1')]
rho = var('rho')


def genFeq(_e):

    cu =  3 * ( U[0] * _e[:,0] + U[1] * _e[:,1] ) 

    feq = W[:] * rho * (1 + cu[:] + Fraction(1./2.)*cu[:]*cu[:] - Fraction(3./2.) * ( U[0]**2 + U[1]**2 ) )

    feq = np.array( [ cancel(f) for f in feq] )

    return feq
    #pprint(feq)

def genM(_e):
    _M = np.zeros((9,9)).tolist()
    
    for i, v in enumerate(e):
        xp = 0
        if v[0] == 1.:
            xp = 1
        elif v[0] == -1.:
            xp = 2

        yp = 0
        if v[1] == 1.:
            yp = 1
        elif v[1] == -1.:
            yp = 2      
         
        for j, _v in enumerate(_e):
            _M[i][j] = _v[0] ** xp * _v[1] ** yp

    return np.array(_M)

def getMRT(e0):

    feq0 = genFeq(e0)
    
    M0 = genM(e0)
    
    meq = list()
    for i, ms in enumerate( M0.dot(feq0)  ):
        meq.append(lambdify((rho, U[0], U[1]), ms))
    
    return lambda r,ux,uy: np.array([f(r,ux,uy) for f in meq]), M0
def getMRT_CLB_d2q9(e0):

    feq0 = genFeq(e0)
    
    M0 = np.array([[1,  1,  1,  1,  1,  1,  1,  1,  1],
      [0,  1,  0, -1,  0,  1, -1, -1,  1],
      [0,  0,  1,  0, -1,  1,  1, -1, -1],
     [-4, -1, -1, -1, -1,  2,  2,  2,  2],
      [4, -2, -2, -2, -2,  1,  1,  1,  1],
      [0, -2,  0,  2,  0,  1, -1, -1,  1],
      [0,  0, -2,  0,  2,  1,  1, -1, -1],
      [0,  1, -1,  1, -1,  0,  0,  0,  0],
      [0,  0,  0,  0,  0,  1, -1,  1, -1]
      ])
    #print latex(M0)
    meq = list()
    for i, ms in enumerate( M0.dot(feq0)  ):
        meq.append(lambdify((rho, U[0], U[1]), ms))
    
    return lambda r,ux,uy: np.array([f(r,ux,uy) for f in meq]), M0
    #return  meq, M0
if __name__ == "__main__":
    from bearded_octo_wookie.lbm import e
    fM, M =getMRT_CLB_d2q9(e)
    print(latex(Matrix(M)))