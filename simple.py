# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 7
mpl.rcParams['lines.markeredgewidth'] = 1.
mpl.rcParams['lines.color'] = 'w'
mpl.rcParams['text.usetex'] = True

font = {
        'size'   : 10}

mpl.rc('font', **font)

legend = {
    'fontsize' : 'medium'
}

mpl.rc('legend', **legend)


protected_figure = plt.figure


def gimmeFigureA4(ratioY=0.5, ratioX=0.7, **kwargs):
    print (ratioX*8.27, ratioY*11.7)
    tight_layout = True
    if kwargs.has_key('tight_layout'):
        tight_layout = kwargs['tight_layout']
    print "tight =", tight_layout
    if kwargs.has_key('fig'):
            kwargs['fig'].set_size_inches((ratioX*8.27, ratioY*11.7))
            return kwargs['fig']
    else:           
        return protected_figure(figsize=(ratioX*8.27, ratioY*11.7),tight_layout=tight_layout)
def gimmeFigureA4LinePlot(**kwargs):
    return gimmeFigureA4(0.25,**kwargs)
   
def gimmeAxisA4LinePlotLegendBottom(**kwargs):
    fig = gimmeFigureA4(0.3, tight_layout=False, **kwargs)
    return fig.add_subplot(111)    
 
 
def gimmeAxisHalfA4LinePlotLegendBottom(**kwargs):  

    l = 0.5 * 8.27
    fig = gimmeFigureA4(l/11.7, l/8.27, tight_layout=False)        
    ax = fig.add_subplot(111)     

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(15)        
    
    fig.subplots_adjust(top = 0.9)
    fig.subplots_adjust(bottom = 0.1)
    fig.subplots_adjust(right = 0.9)
    fig.subplots_adjust(left = 0.2)    
    
    return ax
    
    
def gimmeAxisHalfA4LinePlot(**kwargs):  

    l = 0.5 * 8.27
    fig = gimmeFigureA4(l/11.7, l/8.27, tight_layout=False)        
    ax = fig.add_subplot(111)     

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(15)        
    
#    fig.subplots_adjust(top = 0.9)
    fig.subplots_adjust(bottom = 0.15)
#    fig.subplots_adjust(right = 0.9)
    fig.subplots_adjust(left = 0.2)    
    
    return ax
    
    
def wrapAxisLegendBottomHalfA4(ax, ncol=1):
    wrapAxisLegendBottomA4(ax, ncol=ncol, yanchor=-0.48, xanchor=0)
        
    
def wrapAxisLegendBottomA4(ax, ncol=1, yanchor=-0.5, xanchor=0.0):
    # Shrink current axis by 20%
    
    box = ax.get_position()
    ax.set_position([box.x0*1.2 , box.y0 * 3, box.width , box.height * 0.8])
    
    # Put a legend to the right of the current axis
    ax.legend(loc='lower left', bbox_to_anchor=(xanchor, yanchor), ncol=ncol)
    
    
def AoS_to_SoA(input_data):

    drow = input_data[0]
    dtype = []
    for k in drow.keys():
        if type(drow[k]) == str:
            tt = 'O'
        else:
            tt = type(drow[k])
        dtype.append(( str(k), np.dtype(tt) ) )
    
    
    data = list()
    
    for r in input_data:
        data.append( tuple([ r.get(k) for k in drow.keys() ] ))

    return np.array(data,dtype=dtype)    
    
    
    
    
def setAxLinesBW(ax):
    """
    Take each Line2D in the axes, ax, and convert the line style to be 
    suitable for black and white viewing.
    """
    MARKERSIZE = 7

#    COLORMAP = {
#        'b': {'marker': 'o', 'dash': (None,None), 'ms': MARKERSIZE},
#        'g': {'marker': 's', 'dash': [5,5], 'ms': MARKERSIZE},
#        'r': {'marker': '^', 'dash': [5,3,1,3], 'ms': MARKERSIZE},
#        'c': {'marker': '*', 'dash': [1,3], 'ms': MARKERSIZE},
#        'm': {'marker': 'x', 'dash': [5,2,5,2,5,10], 'ms': MARKERSIZE},
#        'y': {'marker': '<', 'dash': [5,3,1,2,1,10], 'ms': MARKERSIZE},
#        'k': {'marker': '>', 'dash': (None,None), 'ms': MARKERSIZE}
#        }
    COLORMAP = {
        'b': {'marker': 'o',  'ms': MARKERSIZE},
        'g': {'marker': 's',  'ms': MARKERSIZE},
        'r': {'marker': '^',  'ms': MARKERSIZE},
        'c': {'marker': '*',  'ms': MARKERSIZE},
        'm': {'marker': 'x',  'ms': MARKERSIZE},
        'y': {'marker': '<',  'ms': MARKERSIZE},
        'k': {'marker': '>',  'ms': MARKERSIZE}
        }

    lines_to_adjust = ax.get_lines()
    try:
        lines_to_adjust += ax.get_legend().get_lines()
    except AttributeError:
        pass


    [i.set_linewidth(2) for i in ax.spines.itervalues()]

    for line in lines_to_adjust:
        origColor = line.get_color()
        marker = line.get_marker()
        print line.get_linestyle()
        
        

        
        line.set_color('dimgrey')

#        if not line.get_linestyle() == 'None':        
#            line.set_dashes(COLORMAP[origColor]['dash'])
        
        line.set_fillstyle('full')
        line.set_markeredgewidth(1.5)
        line.set_mec('k')
        
        line.set_lw(2)
        if not (marker == 'None'):
            line.set_marker(COLORMAP[origColor]['marker'])

        line.set_markersize(COLORMAP[origColor]['ms'])

def setFigLinesBW(fig):
    """
    Take each axes in the figure, and for each line in the axes, make the
    line viewable in black and white.
    """
    
    for ax in fig.get_axes():
        setNiceGRid(ax)
        setAxLinesBW(ax)

def setNiceGRid(ax):

    
    ax.xaxis.grid(b=True, which='minor', color='lightgrey', lw=0.5, linestyle='-')
    ax.yaxis.grid(b=True, which='minor', color='lightgrey', lw=0.5, linestyle='-')
    ax.yaxis.grid(b=True, which='major', color='k', lw=1, linestyle='-')
    ax.xaxis.grid(b=True, which='major', color='k', lw=1, linestyle='-')    
    ax.set_axisbelow(True)    