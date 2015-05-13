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


#def f(i, a,b) : 
#    print a,b        
#forAll9do(f, 'a', 1)
