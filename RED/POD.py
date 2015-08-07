# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:09:42 2015

@author: mdzikowski

"""
import modred as MR



class Modes:
    def __init__(self, RedDataFilesList):
        
        

        podInput = np.array([ rr[:,2:].reshape(N*Nvars) for rr in AllData ])
    modes, eig_vals = MR.compute_POD_matrices_snaps_method(podInput.T, range(num_modes))





if __name__ == '__main__':
     import numpy as np

    fname0 = '/home/mdzikowski/avio/naca0012/single_sweapt/input/fin_%d.dat'

    rtfs = list()
    
    for i in range(10):        
        rtf = RedTecplotFile(fname0%i)
        data = rtf.data
        kappa = 1.4
        p = (kappa-1.) * data[:,2] * ( data[:,3] - (data[:,4]**2 + data[:,5]**2) / data[:,2] / 2. )
        rtf.appendData('p', p)  
        
        rtfs.append( rtf )
     

     #rtf.writeData('/tmp/test.dat')
     
     Nvars = len(AllData[0][0,:]) - 2

    num_modes = NT
    
    
