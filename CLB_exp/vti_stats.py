# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import vtk
import vtk.util.numpy_support
import sys

vtifname = sys.argv[1]

parallel = False
#vtifname = '/home/michal/tach-17/tmp/TCLB/output/drop_VTK_P00_00000100.vti'
#i0 = 5
if len(sys.argv) > 2:
    i0 = int(sys.argv[2])
else:
    i0 = -1
    
if parallel:
        reader = vtk.vtkXMLPImageDataReader()
else:
        reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(vtifname)
reader.Update()
data = reader.GetOutput()  
print "DIMENSIONS: ", data.GetDimensions()   
celldata = data.GetCellData()


if i0 == -1:
    for i in range(celldata.GetNumberOfArrays()):
        print "FIELD: ", i
        print "     name:", celldata.GetArrayName(i)
        print "     range: ", celldata.GetArray(i).GetRange()
else:
   print "FIELD: ", celldata.GetArrayName(i0)
   print "     range: ", celldata.GetArray(i0).GetRange()    