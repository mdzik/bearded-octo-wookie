# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
from bearded_octo_wookie.lbm import *

raw_data = np.fromfile('/home/michal/tach-17/projekty/TCLB/output/runexternal_Save_P00_00010000_0.pri')

Nx = 256
Ny = 128
Vars = 10
skipFront2d = 1 + 3 * Nx + 1 + 3 * Ny
skipBack2d = 1 + 3 * Nx + 1 + 3 * Ny + Vars * Nx * Ny 

data = raw_data[skipFront2d:skipBack2d].reshape((Ny,Nx,Vars))

#print data[1,:,:]

f = data[:,:,:9]

U = np.zeros_like(f[:,:,:2])

for i,ee in enumerate(e):
    #U[:,:] = U[0,:,:] + ee[0] * f[i,:,:]
    U[:,:,1] = U[:,:,1] + ee[1] * f[:,:,i]
plt.imshow(U[2:-2,2:-2,1])
plt.colorbar()
plt.show()

