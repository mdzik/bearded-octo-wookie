# -*- coding: utf-8 -*-

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['lines.linewidth'] = 1.5
mpl.rcParams['lines.markersize'] = 7
mpl.rcParams['lines.markeredgewidth'] = 1.
mpl.rcParams['lines.color'] = 'w'
font = {
        'size'   : 10}

mpl.rc('font', **font)

legend = {
    'fontsize' : 'medium'
}

mpl.rc('legend', **legend)

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
        return plt.figure(figsize=(ratioX*8.27, ratioY*11.7),tight_layout=tight_layout)
def gimmeFigureA4LinePlot(**kwargs):
    return gimmeFigureA4(0.25,**kwargs)
   
def gimmeAxisA4LinePlotLegendBottom():
    fig = gimmeFigureA4LinePlot(tight_layout=False)
    return fig.add_subplot(111)    
 
    
def wrapAxisLegendBottomA4(ax):
    # Shrink current axis by 20%
    
    box = ax.get_position()
    ax.set_position([box.x0 , box.y0 * 3, box.width , box.height * 0.8])
    
    # Put a legend to the right of the current axis
    ax.legend(loc='lower left', bbox_to_anchor=(0.0, -0.5))