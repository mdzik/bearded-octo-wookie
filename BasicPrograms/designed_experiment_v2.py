# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 17:35:21 2015

@author: michal
"""

class require:
    def __init__(self, *args, **kargs):
        for i,a in enumerate(args):
            if not a:
                raise "Rquired from-uppr argument number ", i , " failed"
        pass
    def __call__(self, func):
        return func
    

import matplotlib.pyplot as plt
import numpy as np
import bearded_octo_wookie.RED.RedReader as RedReader
import bearded_octo_wookie.RED.POD as POD
from scipy.spatial import cKDTree
from scipy.interpolate import interp1d 
from scipy.interpolate import UnivariateSpline


dir0 = '/home/michal/avio/naca0012/multi_sweapt_1/all/'
#dir0 = '/home/michal/avio/naca0012/multi_sweapt_1/mach.65/'
fname0 = dir0+'input/fin_%d.dat'
geometryFile = '/home/michal/avio/naca0012/multi_sweapt_1/all/name.get'
boundaryFile = '/home/michal/avio/naca0012/multi_sweapt_1/all/boundary.dat'
fpoints=dir0+'designed_points'
num_files = 121

kappa = 1.4


rtfs = [RedReader.RedTecplotFile(fname0%i) for i in range(1,num_files+1)]
    
#==============================================================================
# for rtf in rtfs:            
#     data = rtf.data        
#     p = (kappa-1.) * data[:,2] * ( data[:,3] - (data[:,4]**2 + data[:,5]**2) / data[:,2] / 2. )
#     rtf.appendData('p', p)          
#==============================================================================
num_modes = 10
modesH = POD.Modes(rtfs, num_modes=num_modes)    
modesH.writeModes('/tmp/test%d.vti')

mesh = cKDTree(modesH.baseRedFile.data[:,:2])

#==============================================================================
# SHOW RECONSTRUCTION 
#==============================================================================
# plt.figure()
# for fid, field in enumerate(rtfs[0].variables[2:]):
#     plt.subplot(3,2,fid+1)
#     plt.title(field)
#     for i,rtf in enumerate(rtfs):
#         shape = rtf.data[:,2:].shape
#         shape1d = shape[0] * shape[1]
#         v0 = rtf.data[:,2:].reshape((1,shape1d))
#         v = np.zeros_like(v0)
#         cs = list()
#         en = list()
#         for m in modesH.modes:
#             c = v0.dot(m.reshape(shape1d).T)[0,0]
#             v = v + c * m.reshape(shape1d)
#             print v[:,fid]
#             e = np.max(np.abs(v[:,fid] - v0[:,fid] ))
#             en.append( e )
#         plt.plot(en,label='m='+str(i))
#             
#         print "EOF #############"
#==============================================================================
        
get = RedReader.GetReader(geometryFile)

boundary_nodes = np.loadtxt(boundaryFile)[:,:2]
boundary_nodes_params = np.array(get.getParamList(boundary_nodes[:,:2].tolist(), 1))

bids = mesh.query(boundary_nodes)[1]        
#==============================================================================
#DISPLAY  BOUNDARY NODES PARAMETRISATION        
#==============================================================================
# plt.figure()
# xy = np.array( get.getXYList(np.linspace(0.,1.,200),1) )
# xxyy = np.array( get.getXYList(boundary_nodes_params,1) )
# plt.plot(xxyy[:,0],xxyy[:,1], 'o')
# plt.plot(xy[:,0],xy[:,1])
#plt.figure()
#plt.plot(modesH.baseRedFile.data[bids,0], modesH.baseRedFile.data[bids,1], 'o' )
#plt.plot(boundary_nodes[:,0], boundary_nodes[:,1] , 'x' )
#==============================================================================

work_on_param = 0

modes_interpolators = list()
for m in modesH.modes:
    mt = np.squeeze(np.array(m[bids,work_on_param]))
    mi = interp1d(boundary_nodes_params, mt,kind='cubic')
    #mi = UnivariateSpline(boundary_nodes_params, mt)
    #mi.set_smoothing_factor(0.)
    modes_interpolators.append(mi)

#==============================================================================
# DISPLAY POD VECTORS VALUES INTERPOLATION ON BOUNDARY
#==============================================================================
# 
# plt.figure()
# l = np.linspace(0.,1., 5000)
# for m, mi in zip(modesH.modes, modes_interpolators):
#     plt.plot(boundary_nodes_params, m[bids,0], 'o')
#     plt.plot(l, mi(l))
#==============================================================================


#testpoints = boundary_nodes_params#np.linspace(0.,1., num_test_points)
#num_test_points = len(testpoints)
#
#
#make test matrix

@require(
    num_modes>0,
    not 'A' in locals(),
    not 'A' in globals(),
    'modes_interpolators' in locals()
)
def getInformationMatric(test_points_):
    A = np.zeros((len(test_points_),num_modes))
    for pid, point in enumerate(test_points_):
        for mid, mi in enumerate(modes_interpolators):
            A[pid,mid] = mi(point)
    return A
@require(
    num_modes>0,
    not 'A' in locals(),
    not 'A' in globals(),
    'modes_interpolators' in locals()
)  
def getInformationMatric_ComputeSingleCol(test_points_, pid):
    A = np.zeros((len(test_points_),num_modes))
    point = test_points_[pid]
    for mid, mi in enumerate(modes_interpolators):
        A[pid,mid] = mi(point)
    return A
#==============================================================================
# TEST THE MATRIX
#==============================================================================
# num_test_points = 15
# testpoints = np.linspace(0.,1., num_test_points)
#
# A = getInformationMatric(testpoints)
# 
# ## fake experimanta data
# experiment_values_interpolate = interp1d(boundary_nodes_params, np.array(rtfs[0].data[bids,2+work_on_param]), kind='cubic')
# experiment_values = experiment_values_interpolate(testpoints)
# 
# #reconstruct coefficents
# cs_A = np.linalg.solve(A.T.dot(A),A.T.dot(experiment_values))
# 
# #reconstruct coeficients ased on whole solution
# shape = rtfs[0].data[:,2:].shape
# shape1d = shape[0] * shape[1]
# v0 = rtfs[0].data[:,2:].reshape((1,shape1d))
# cs_org = list()
# 
# for m in modesH.modes:
#     cs_org.append(v0.dot(m.reshape(shape1d).T)[0,0])
# 
# cs_org = np.array(cs_org)
# 
# 
# #profile is aligned with XY coordinate system
# profile_length_param = boundary_nodes[:,0]
# 
# #reconstruct full field, basing on modes. recon SHOULD BE EXACT, reconA contains error
# recon = np.squeeze(np.array(modesH.modes).T.dot(cs_org.reshape((1,9,1))))
# reconA = np.squeeze(np.array(modesH.modes).T.dot(cs_A.reshape((1,9,1))))
# 
# #plot beutifully
# for fid, field in enumerate(rtfs[0].variables[2:]):
#     print fid,field
#     plt.subplot(3,2,fid+1)
#     plt.title(field)
#     values = rtfs[0].data[bids,2+fid]    
#    # plt.plot(profile_length_param, values)    
#     v = np.zeros_like(profile_length_param)
#     plt.plot(profile_length_param, recon[fid,bids],'o')
#     plt.plot(profile_length_param, reconA[fid,bids],'rx')
#     plt.twinx()
#     err = np.absolute(recon[fid,bids] - reconA[fid,bids])
#     plt.semilogy(profile_length_param, err,'k-')    
#==============================================================================
    

#==============================================================================
# SHOW HOW SINGLE POINT MOVEMEN WRT TO ORIGINAL POSITIONT CHENGE cond(A)
#==============================================================================
# testpoints = np.linspace(0.,1., num_test_points)
# 
# for move_point in range(1,num_test_points-1):
# 
#     maxmove = 0.9*(testpoints[move_point+1] - testpoints[move_point-1]) 
#     move = np.linspace(-maxmove/2.,maxmove/2., 40)
#     test_new_positions = testpoints[move_point] + move
#         
#     
#     testpoints_modified = np.array([ testpoints for t in test_new_positions ])
#     testpoints_modified[:,move_point] = test_new_positions
#     
#     
#     Amodified = [ getInformationMatric(t) for t in testpoints_modified ]
#     
#         
#     Aoptimality = np.array([ np.trace(np.linalg.inv(AA.T.dot(AA))) for AA in Amodified ])
#     Aoptimality = Aoptimality 
#     plt.semilogy(move,Aoptimality)
#
#    plt.grid(which='both')
#==============================================================================  

@require(
    not 'A' in locals(),
    not 'A' in globals()
)
def getTraceOfMatrixInverse(A):
    D = np.linalg.eigvalsh(A)
    if np.any(D < 0.):
        r = np.inf
    else:
        r = np.sum(1./ D)
    return r


def getACriterion(A):
    shape = A.shape
    if shape[0] < shape[1]:
        _A = A[:,:shape[0]]
    else:
        _A = A     
    return getTraceOfMatrixInverse(_A.T.dot(_A))

#==============================================================================
# SHOW HOW SINGLE EXTRA POINT ALONG PROFILE CHENGE cond(A)
#==============================================================================
num_test_points = num_modes / 2
testpoints = np.linspace(0.,1., num_test_points)

testpoints0 = np.copy(testpoints)


Aoptim_min = list()
Aoptim_uniform = list()


testpoints_all_combinations = list()


for extrapoint in range(2 * num_modes):
    print "RUN NUMBER",extrapoint,"/",2*num_modes
    num_test_points = num_test_points + 1
    
    _testpoints = np.array(testpoints)

    testpoints = np.zeros(num_test_points)
    
    testpoints[:-1] = _testpoints
     
    
    test_new_positions = np.linspace(0.,1., 3 * num_test_points)
        
    
    testpoints_modified = np.array([ testpoints for t in test_new_positions ])
    testpoints_modified[:,-1] = test_new_positions
    
    #Amodified = [ getInformationMatric(t) for t in testpoints_modified ]
    A0 = getInformationMatric(testpoints_modified[0])
    A0[-1,:] = 0
    Amodified = [ A0 + getInformationMatric_ComputeSingleCol(t,num_test_points-1) for t in testpoints_modified ]
    
    
        
    Aoptimality = np.array([ getACriterion(AA) for AA in Amodified ])
    Aoptimality = Aoptimality 
    plt.semilogy(test_new_positions,Aoptimality)
    
    #plt.semilogy(testpoints[:-1],np.ones_like(testpoints[:-1])*np.average(Aoptimality), 'o')
    
    plt.grid(which='both')

    print "Amax = ", np.max(Aoptimality)
    print "Amin = ", np.min(Aoptimality)
    sorte = np.argsort(Aoptimality)
    
    optim = 0
    for optim_ in sorte:
        print "check point ", optim_
        if not test_new_positions[optim_] in testpoints[:-1]:
            optim = optim_
            print "     ok point ", optim_
            break
        else:
            print "     repeated point ", optim_
    
    testpoints[-1] = test_new_positions[optim]
    
    testpoints_all_combinations.append(np.copy(testpoints))
    
    plt.semilogy(testpoints[-1],Aoptimality[optim], 'o')
    
    Aoptim_min.append( Aoptimality[optim] )
    Aunif = getInformationMatric(np.linspace(0,1.,num_test_points))
    Aoptim_uniform.append(getACriterion(Aunif))


#==============================================================================
# SAVE DESIRABLE EXPOERIMENT POINTS
#==============================================================================
np.savez(fpoints, testpoints_all_combinations=testpoints_all_combinations)
         

testpoints = np.unique(testpoints)
testpoints_uniform = np.linspace(0,1.,len(testpoints))

testpoints_xy = np.array(get.getXYList(testpoints,1))
testpoints0_xy = np.array(get.getXYList(testpoints0,1))
testpoints_uniform_xy = np.array(get.getXYList(testpoints_uniform,1))


plt.figure()
plt.semilogy(Aoptim_uniform, 'k')
plt.semilogy(Aoptim_min, 'r')

plt.figure()
plt.plot(testpoints_xy[:,0], testpoints_xy[:,1],'ro', ms=30)
plt.plot(testpoints0_xy[:,0], testpoints0_xy[:,1],'ko' , ms=20)
plt.plot(testpoints_uniform_xy[:,0], testpoints_uniform_xy[:,1],'bo' , ms=10)

plt.figure()

A = getInformationMatric(testpoints)
A0 = getInformationMatric(testpoints0)
A_uniform = getInformationMatric(testpoints_uniform)

experiment_values_interpolate = interp1d(boundary_nodes_params, np.array(rtfs[0].data[bids,2+work_on_param]), kind='cubic')
experiment_values = experiment_values_interpolate(testpoints)
experiment_values0 = experiment_values_interpolate(testpoints0)
experiment_values_uniform  = experiment_values_interpolate(testpoints_uniform)

#reconstruct coefficents
cs_A = np.linalg.solve(A.T.dot(A),A.T.dot(experiment_values))
initial_is_singular = False
try:
    cs_A0 = np.linalg.solve(A0.T.dot(A0),A0.T.dot(experiment_values0))
except np.linalg.linalg.LinAlgError:
    print "======================================================="
    print "INITIAL DISTRIBUTION MATRIX IS SINGULAR!!!!!!!!!!!!!!!!"
    print "======================================================="
    initial_is_singular = True
    cs_A0 = np.linalg.solve(A.T.dot(A),A.T.dot(experiment_values))    
    
cs_A_uniform = np.linalg.solve(A_uniform.T.dot(A_uniform),A_uniform.T.dot(experiment_values_uniform))


#reconstruct coeficients ased on whole solution
shape = rtfs[0].data[:,2:].shape
shape1d = shape[0] * shape[1]
v0 = rtfs[0].data[:,2:].reshape((1,shape1d))
cs_org = list()

for m in modesH.modes:
    cs_org.append(v0.dot(m.reshape(shape1d).T)[0,0])

cs_org = np.array(cs_org)


#profile is aligned with XY coordinate system
profile_length_param = boundary_nodes[:,0]

#reconstruct full field, basing on modes. recon SHOULD BE EXACT, reconA contains error
recon = np.squeeze(np.array(modesH.modes).T.dot(cs_org.reshape((1,num_modes,1))))

reconA = np.squeeze(np.array(modesH.modes).T.dot(cs_A.reshape((1,num_modes,1))))

reconA0 = np.squeeze(np.array(modesH.modes).T.dot(cs_A0.reshape((1,num_modes,1))))

reconA_uniform = np.squeeze(np.array(modesH.modes).T.dot(cs_A_uniform.reshape((1,num_modes,1))))

#plot beutifully
field  = rtfs[0].variables[2+work_on_param]

plt.title(field)

v = np.zeros_like(profile_length_param)

plt.subplot(311)
plt.plot(profile_length_param, recon[work_on_param,bids],'-')
plt.plot(testpoints_xy[:,0], experiment_values,'ro')

plt.subplot(312)
plt.plot(profile_length_param, recon[work_on_param,bids],'-')
plt.plot(testpoints0_xy[:,0], experiment_values0,'ko')

plt.subplot(313)
plt.plot(profile_length_param, recon[work_on_param,bids],'-')
plt.plot(testpoints_uniform_xy[:,0], experiment_values_uniform,'bo')


plt.figure()

#plot beutifully
for fid, field in enumerate(rtfs[0].variables[2:]):
    print fid,field
    plt.subplot(3,2,fid+1)
    plt.title(field)
    values = rtfs[0].data[bids,2+fid]    
   # plt.plot(profile_length_param, values)    
    v = np.zeros_like(profile_length_param)
    plt.plot(profile_length_param, recon[fid,bids],'o')
    #plt.plot(profile_length_param, reconA[fid,bids],'rx')
    #plt.plot(profile_length_param, reconA0[fid,bids],'kx')
    plt.plot(profile_length_param, reconA_uniform[fid,bids],'bx')

plt.figure()

#plot beutifully
for fid, field in enumerate(rtfs[0].variables[2:]):
    print fid,field
    plt.subplot(3,2,fid+1)
    plt.title(field)
    values = rtfs[0].data[bids,2+fid]    
   # plt.plot(profile_length_param, values)    
    v = np.zeros_like(profile_length_param)
    plt.plot(profile_length_param, recon[fid,bids],'o')
    plt.plot(profile_length_param, reconA[fid,bids],'rx')
    #plt.plot(profile_length_param, reconA0[fid,bids],'kx')
    #plt.plot(profile_length_param, reconA_uniform[fid,bids],'bx')



plt.figure()


for fid, field in enumerate(rtfs[0].variables[2:]):
    print fid,field
    plt.subplot(3,2,fid+1)
    plt.title(field)


    err0 = np.absolute(recon[fid,bids] - reconA0[fid,bids])
    plt.semilogy(profile_length_param, err0,'k-')   
 
    err = np.absolute(recon[fid,bids] - reconA[fid,bids])
    plt.semilogy(profile_length_param, err,'r-')    

    err_unif = np.absolute(recon[fid,bids] - reconA_uniform[fid,bids])
    plt.semilogy(profile_length_param, err_unif,'b-')   

if not initial_is_singular:
    plt.figure()
    
    for fid, field in enumerate(rtfs[0].variables[2:]):
        print fid,field
        plt.subplot(3,2,fid+1)
        plt.title(field)
        
        err = np.absolute(reconA0[fid,bids] - reconA[fid,bids])
        plt.semilogy(profile_length_param, err,'ro-')    
    
        err_unif = np.absolute(reconA0[fid,bids] - reconA_uniform[fid,bids])
        plt.semilogy(profile_length_param, err_unif,'bo-')    

    
plt.show()