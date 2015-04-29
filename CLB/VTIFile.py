# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:56:27 2015

@author: mdzikowski
"""

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

    def get(self, name, vector=False):
        if vector:
            return VN.vtk_to_numpy(self.data.GetCellData().GetArray(name)).reshape(self.s_vec)
        else:
            return VN.vtk_to_numpy(self.data.GetCellData().GetArray(name)).reshape(self.s_scal)
 
    def spacing(self,i=0):
        return self.data.GetSpacing()[i]           
        
    def axisIterator(self,i=0,start=0, step=1):
        for j in range(start, self.s_scal[i], step):
            yield j
            
    def len(self,i=0):
        return self.s_scal[i]
            