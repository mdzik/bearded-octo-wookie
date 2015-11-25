# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:56:27 2015

@author: mdzikowski
"""

import numpy as np
import vtk
import vtk.util.numpy_support as VN

class VTIFile:
    def __init__(self, vtifname, parallel=False):
        if parallel:
                self.reader = vtk.vtkXMLPImageDataReader()
        else:
                self.reader = vtk.vtkXMLImageDataReader()
        self.reader.SetFileName(vtifname)
        self.reader.Update()
        self.data = self.reader.GetOutput()  
        self.dim = self.data.GetDimensions()   
        self.s_scal = [self.dim[1]-1, self.dim[0]-1]
        self.s_vec = [self.dim[1]-1, self.dim[0]-1,3]
        
        self.trim_0 = [0,0]
        self.trim_1 = [x-1 for x in self.dim]

    def get(self, name, vector=False):     

        if vector:
            subspace = np.meshgrid(
                range(self.trim_0[0],self.trim_1[0]),
                range(self.trim_0[1],self.trim_1[1]),
                range(3)
            )            
            return np.transpose(VN.vtk_to_numpy(self.data.GetCellData().GetArray(name)).reshape(self.s_vec), (1,0,2))[subspace]
        else:
            subspace = np.meshgrid(*[range(self.trim_0[i],self.trim_1[i]) for i in range(2) ])
            return VN.vtk_to_numpy(self.data.GetCellData().GetArray(name)).reshape(self.s_scal).T[subspace]
            
    def spacing(self,i=0):
        return self.data.GetSpacing()[i]           
        
    def axisIterator(self,i=0,start=0, step=1):
        for j in range(start, self.s_scal[i], step):
            yield j
            
    def len(self,i=0):
        return self.s_scal[i]
        
    def trim(self, **kwargs):
            for i,k in enumerate(['x0', 'y0']):
                if kwargs.has_key(k):
                    self.trim_0[i] = kwargs[k]
            for i,k in enumerate(['x1', 'y1']):
                if kwargs.has_key(k):
                    if kwargs[k] < 0:
                        self.trim_1[i] = self.trim_1[i] + kwargs[k]
                    else:
                        self.trim_1[i] = kwargs[k]
                    
    def getMeshGrid(self):
        return np.meshgrid(*[range(self.trim_0[i],self.trim_1[i]) for i in range(2) ])

