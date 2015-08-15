# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:42:05 2015

@author: mdzikowski
"""

import matplotlib.pyplot as plt
import numpy as np

def generic_figure_processor(func):
    def f(*args, **kwargs):    
        func(*args, **kwargs)
        plt.figure()
    return f

def generic_plot_processor(func):
    def f(*args, **kwargs):  
        func(*args, **kwargs)
        plot = args[0]
        getattr(plt, plot['fun_name'])(*plot['args'],**plot['kwargs'])
    return f

def decorate_with_call(decorator, *args_,**kwargs_):
    def fd(func):
        def f(*args, **kwargs):  
            plot = args[0]
            if kwargs_.has_key('for_fig') :
                if plot['fid'] in kwargs_['for_fig']:
                    tmp = kwargs_.copy()
                    tmp.pop('for_fig')
                    decorator(*args_, **tmp)
            else:
                    decorator(*args_, **kwargs_)
                    
            func(*args, **kwargs)

        return f
    return fd

def decorate_with_alter(decorator, *args_,**kwargs_):
    def fd(func):
        def f(*args, **kwargs):  
            plot = args[0]
            if kwargs_.has_key('for_fig') :
                if plot['fid'] in kwargs_['for_fig']:
                    tmp = kwargs_.copy()
                    tmp.pop('for_fig')
                    decorator(plot, *args_, **tmp)
            else:
                    decorator(plot, *args_, **kwargs_)
                    
            func(*args, **kwargs)

        return f
    return fd

#==============================================================================
# 
# @generic_figure_processor
# def pf(*args, **kwargs):
#     pass
# 
# @decorate_with_call(plt.grid, which='both', for_fig='2')
# @decorate_with_call(plt.xlabel, 'X')
# @generic_plot_processor
# def pp(*args, **kwargs):
#    pass
#==============================================================================




def render(fname, processplot, processfigure, **kwargs):
    
    data = np.load(fname)
    
    for fid in data.keys():
        figure = data[fid]
        print "New figure ", fid
        
        for plot in figure:
            plot['fid'] = fid
            print "REPLAING: ", plot['fun_name'], plot['kwargs']
            #getattr(plt, plot['fun_name'])(*plot['args'],**plot['kwargs'])
            processplot(plot)
        processfigure({'fid':fid})
    if kwargs.has_key('show'):
        if kwargs['show']:
            plt.show()
    else:
        plt.show()

    
    
    
    
    
    