# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 12:02:11 2015

@author: mdzikowski
"""

# THIS LIBRARY COMES FORM flow2 REPO, PUT buidl/green/xpget/libpget.so  to this directory
import libpget
import re
import os.path
import numpy as np
from bearded_octo_wookie.version import *

__version__ = update_version_py()



def flatten(d):
    return d.reshape(d.shape[0] * d.shape[1] )

class GetReader:
    def __init__(self, fname):
        self.pget = libpget.PGet()
        self.pget.init(fname)
    
    
    def getXYList(self, curve_parameters, curve_id):
        return [self.pget.getCoord(int(curve_id), float(t)) for t in curve_parameters]
    
    def getXY(self, curve_parameter, curve_id):
        return self.pget.getCoord(int(curve_id), float(curve_parameter))

    def getParam(self, pos, curve_id):
        return self.pget.getParam(int(curve_id), pos)

    def getParamList(self, pos, curve_id):
        return [self.pget.getParam(int(curve_id), t) for t in pos]
    



class nonConservative2D:
    
    variables = {
    'X': 'X',
    'Y': 'Y',
    'V01': 'Rho',
    'V02': 'P',
    'V03': 'U',
    'V04': 'V',
    }
    @staticmethod
    def __call__(row):
        kappa = 1.4
        p = (kappa-1.) * row[2] * ( row[3] - (row[4]**2 + row[5]**2) / row[2] / 2. )        
        return [ row[0], row[1], row[2], p, row[4] / row[2] , row[5] / row[2]  ]

class RedTecplotFile:
    def __init__(self, fname, useCache=True, fake=False, rowProcessor=nonConservative2D()):
        self.baseFile = fname
        self.rowProcessor = rowProcessor
        self.loaded = False 
        
        if fake:
            return
        
        if useCache:
            if  os.path.isfile(fname+'.cache.npz'):
                fdata  = np.load(fname+'.cache.npz')
                try:
                    self.params = fdata['params'].tolist()
                    self.variables = fdata['variables'].tolist()
                    self.data = fdata['data']
                    self.writer_version = fdata['writer_version']                    
                    if not self.writer_version == __version__:
                        print "=> READER VERSION INVALIDATES CACHE"
                        self.loaded = True
                except KeyError:
                    pass

        if not self.loaded:
            
            self.params = {}
            self.variables = list()
            
            #read file info
            n = 0
            for line in file(fname):
                n = n + 1
                if re.match('.*VARIABLES.*', line):
                    for var in re.findall('"([a-zA-Z,0-9]*)"',line):
                        #do not import variable we dont know
                        if self.rowProcessor.variables.has_key(var):
                            self.variables.append(self.rowProcessor.variables[var])
                        else:
                            print "skipping unknown var: ", var
                    break
                if n > 5:
                    break
                n = 0 
            
            for line in file(fname):
                n = n + 1    
                if re.match('.*ZONE.*', line):
                    dataline = line.replace('ZONE', '', 1)
                    for param in dataline.split(","):
                        for m in re.findall('([a-zA-Z,0-9]*)=([a-zA-Z,0-9]*)',param)    :
                            if m[1].isdigit():
                                self.params[m[0]] = int(m[1])
                            else:
                                self.params[m[0]] = str(m[1])
                    break
                if n > 5:
                    break
            
            self.readData(False)
            
            if useCache:
                np.savez(fname+'.cache.npz', params=self.params, variables=self.variables, data=self.data, writer_version=__version__)

    def readData(self, useCache=True):
        
        
        if self.loaded and useCache:
            return
        
        if useCache:
            self.loaded = False
            if  os.path.isfile(self.baseFile+'.cache.npz'):
                fdata  = np.load(self.baseFile+'.cache.npz')
                try:
                    self.params = fdata['params'].tolist()
                    self.variables = fdata['variables'].tolist()
                    self.data = fdata['data']
                    self.writer_version = fdata['writer_version']                    
                    if self.writer_version == __version__:
                        self.loaded = True
                except KeyError:
                    pass

        if not self.loaded:
            
            N = self.params['N']
            data = list()
            n = 0
            r = 0
            for line in file(self.baseFile):
                n = n + 1
                if n < 4:
                    pass  
                else:
                    #print line
                    datarow = list()
                    for num in re.findall('[0-9,\.,\-,e]+', line):
                        datarow.append(float(num))
                    data.append(self.rowProcessor(datarow))
                        
                            
                    r = r + 1
                if r == N :
                    print "done. ", len(data), " lines"
                    break
            self.data = np.array(data)
        
    def writeData(self, fname):
            N = self.params['N']
            fp = file(fname, 'w')
            fname = self.baseFile
            n = 0
            for line in file(fname):
                n = n + 1
                if n == 2:        
                    fp.write('VARIABLES = ' + ",". join(self.variables) + '\n')        
                elif n > 3 and  n < 4 + N:
                    fp.write(" ".join([ str(q) for q in self.data[n-4,:]]))
                    fp.write("\n")
                else:
                    fp.write(line)        
            fp.close()
            
            
    def appendData(self, colName, values):
        self.variables.append(colName)

        tmp = np.zeros( (self.params['N'],len(self.variables) ) )
        tmp[:,:-1] = self.data
        tmp[:,-1] = values
        self.data = tmp
    def appendVariable(self, colName):
        self.variables.append(colName)
        print colName
        tmp = np.zeros( (self.params['N'],len(self.variables) ) )
        tmp[:,:-1] = self.data
        tmp[:,-1] = np.zeros(self.params['N'])
        self.data = tmp       
        
    def copyForWriting(self):
        ret = RedTecplotFile('',False,True)
        ret.baseFile = self.baseFile
        ret.data = np.zeros((self.params['N'],2))
        ret.data[:,:2] = self.data[:,:2]
        ret.variables = self.variables[:2]
        ret.params = self.params
        return ret


#==============================================================================
# if __name__ == '__main__':
#     import numpy as np
#     l = np.linspace(0.,1.,100)
#     test = GetReader('/tmp/name.get')
#     xyl = test.getXYList(l, 1)
#     print xyl
#     xy = test.getXY(0.5, 1)
#     print xy
# 
#     print test.getParamList(xyl,1) - l
#     print test.getParam(xy, 1)
#==============================================================================



if __name__ == '__main__':
     import numpy as np
    
     rtf = RedTecplotFile('/home/mdzikowski/avio/naca0012/single_sweapt/input/fin_10.dat')
     
     data = rtf.data
     kappa = 1.4
#     p = (kappa-1.) * data[:,2] * ( data[:,3] - (data[:,4]**2 + data[:,5]**2) / data[:,2] / 2. )
     rtf.writeData('/tmp/test.dat')

