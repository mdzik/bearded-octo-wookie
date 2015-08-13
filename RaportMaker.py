# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 10:35:30 2015

@author: mdzikowski
"""


import functools
import types
from matplotlib.pyplot import *


#==============================================================================
# DECORATOR FOR HELPER FUNCTIONS
#==============================================================================
def finalize(func):
    def fin(self, *args, **kwargs):
        func(self, *args, **kwargs)
        if not self.dont_show and not args[0] == '--internal--':
            self.originals[args[0]](*(args[1:]), **kwargs)
    return fin
        
def info(func):
    def fin(self, *args, **kwargs):
        print "INTERCEPTED: ", args[0]
        func(self, *args, **kwargs)
    return fin

def shift_plots(func):
    def fin(self, *args, **kwargs):
        if not self.currentPlot == {} and not self.currentPlot == 0:
            self.plots.append(self.currentPlot)
        self.currentPlot = {}
        func(self, *args, **kwargs)
    return fin
    
    
    
#==============================================================================
# MAIN INTERCEPTION CLASS    
#==============================================================================
class RaportMaker(object):
    def __init__(self, **kargs):
        if kargs.has_key('dont_show') and kargs['dont_show']:
            self.dont_show = True
        else:
            self.dont_show = False
        self.originals = {}
        self.currentPlot = 0
        self.plots = []
        self.figures = {}
        self.path = '/dev/null'
        self.fid = 0

    @info
    @shift_plots
    @finalize
    def record(self, name, *args, **kwargs):
        self.currentPlot['fun_name'] = name
        self.currentPlot['args'] = args
        self.currentPlot['kwargs'] = kwargs

#==============================================================================
#     @info
#     @finalize
#     def modify(self, name, *args, **kwargs):
#         self.currentPlot['fun_name'] = name
#         self.currentPlot['args'] = args
#         self.currentPlot['kwargs'] = kwargs
#==============================================================================
        
    @info  
    @shift_plots
    @finalize        
    def store(self, name, *args, **kwargs):
        if not self.plots == {}:
            self.new_figure('--internal--')
        np.savez(self.path, **self.figures)
    
    @info
    @shift_plots    
    @finalize        
    def new_figure(self, *args, **kwargs):
        if len(self.plots) > 0:
            if len(args) > 1 and isinstance(args[1], str):
                self.figures[args[0]] = self.plots
            else:
                self.fid = self.fid + 1
                self.figures[str(self.fid)] = self.plots
        self.plots = []



                
    def RecordingDecorator(self, func):
        self.originals[func.func_name] = func
        class _wrapper:
            def __init__(self, parent, func):
                self.parent = parent
                self.func = func
                
            @functools.wraps(func)
            def __call__(self, *args, **kwargs):
                self.parent.record(func.func_name, *args,**kwargs)
        
        return _wrapper(self, func)
        
#==============================================================================
#     def ModifingDecorator(self, func):
#         self.originals[func.func_name] = func
#         class _wrapper:
#             def __init__(self, parent, func):
#                 self.parent = parent
#                 self.func = func
#                 
#             @functools.wraps(func)
#             def __call__(self, *args, **kwargs):
#                 self.parent.create(func.func_name, *args,**kwargs)
#         
#         return _wrapper(self, func)
#==============================================================================
        
    def ShowDecorator(self, func):
        self.originals[func.func_name] = func
        class _wrapper:
            def __init__(self, parent, func):
                self.parent = parent
                self.func = func
                
            @functools.wraps(func)
            def __call__(self, *args, **kwargs):
                self.parent.store(func.func_name, *args,**kwargs)
        
        return _wrapper(self, func)

    def FigureDecorator(self, func):
        self.originals[func.func_name] = func
        class _wrapper:
            def __init__(self, parent, func):
                self.parent = parent
                self.func = func
                
            @functools.wraps(func)
            def __call__(self, *args, **kwargs):
                self.parent.new_figure(func.func_name, *args,**kwargs)
        
        return _wrapper(self, func)
        
        
#==============================================================================
# def NotDecorated(func):
#     def f(*args, **kwargs):
#         print "NOT INTERCEPTED: ", func.func_name
#         return func(*args, **kwargs)
#     return f
#==============================================================================
    
    
raport = RaportMaker()
    
for k,v in vars(matplotlib.pyplot).items():
    if isinstance(v, types.FunctionType):
        globals()[k] = raport.RecordingDecorator(v)
        


        
#==============================================================================
# PLOTTING_FUNCTIONS = [
#     'plot',
#     'semilogx',
#     'semilogy',
#     'loglog'
# ]
# 
# 
# for name in PLOTTING_FUNCTIONS:
#     globals()[name] = raport.PlottingDecorator(getattr(matplotlib.pyplot, name))
#==============================================================================

        
globals()['show'] = raport.ShowDecorator(getattr(matplotlib.pyplot, 'show'))
globals()['figure'] = raport.FigureDecorator(getattr(matplotlib.pyplot, 'figure'))





