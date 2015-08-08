# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:09:42 2015

@author: mdzikowski

"""
import modred as MR
from RedReader import *


class Modes:
    def __init__(self, RedDataFilesList, **kargs):
        
        if kargs.has_key('num_modes'):
            self.num_modes = kargs['num_modes']
        else:
            self.num_modes = len(RedDataFilesList)
        Nvars = len(RedDataFilesList[0].data[0,2:])
        N = RedDataFilesList[0].params['N']
        podInput = np.array([ rr.data[:,2:].reshape(rr.params['N']*len(rr.data[0,2:])) for rr in RedDataFilesList ])
        modes, self.eig_vals = MR.compute_POD_matrices_snaps_method(podInput.T, range(self.num_modes))
        
        self.modes = list()
    
        for m in modes.T:
            self.modes.append( m.reshape((N,Nvars))  )
        
        self.baseRedFile = RedDataFilesList[0].copyForWriting()
        print self.baseRedFile.data.shape
        print RedDataFilesList[0].data.shape       
        
        for v in RedDataFilesList[0].variables[2:]:
            self.baseRedFile.appendVariable(v+'_mode')
    def writeModes(self, fname):
        for d,m in enumerate(self.modes):
            self.baseRedFile.data[:,2:] = m
            self.baseRedFile.writeData(fname%d)
        
        self.baseRedFile.data[:,2:] = np.zeros_like(self.baseRedFile.data[:,2:])



#==============================================================================
# if __name__ == '__main__':
#     import numpy as np
# 
#     fname0 = '/home/michal/avio/naca0012/single_sweapt/input/fin_%d.dat'
# 
#     rtfs = list()
#     
#     for i in range(1,10):        
#         rtf = RedTecplotFile(fname0%i)
#         data = rtf.data
#         kappa = 1.4
#         p = (kappa-1.) * data[:,2] * ( data[:,3] - (data[:,4]**2 + data[:,5]**2) / data[:,2] / 2. )
#         rtf.appendData('p', p)  
#         
#         rtfs.append( rtf )
#      
# 
#     modes = Modes(rtfs, num_modes=5)    
#     modes.writeModes('/tmp/test%d.vti')
#==============================================================================
