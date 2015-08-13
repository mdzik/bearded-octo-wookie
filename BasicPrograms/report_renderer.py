# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:42:05 2015

@author: mdzikowski
"""

import matplotlib as mpl

mpl.rcParams['lines.linewidth'] = 4
mpl.rcParams['lines.markersize'] = 12
mpl.rcParams['lines.markeredgewidth'] = 2.
mpl.rcParams['lines.color'] = 'w'
font = {
        'size'   : 5}

mpl.rc('font', **font)


from bearded_octo_wookie.RaportRenderer import *

def remove_kwargs(plot):
    if plot['kwargs'].has_key('ms'):
        plot['kwargs'].pop('ms')


class PidH:
    pid = 0

pidh = PidH()

@generic_figure_processor
def pf(*args, **kwargs):
    plt.grid(which='both')
    plt.savefig('/tmp/test'+str(pidh.pid)+'.png', dpi=300)
    pidh.pid = pidh.pid + 1



@decorate_with_call( plt.xlabel, 'XxX', for_fig=('1',) )
@decorate_with_call( plt.ylabel, r'$Y$')
@decorate_with_alter( remove_kwargs )
@generic_plot_processor
def pp(*args, **kwargs):
    pass


render('/tmp/raport.npz', pp, pf)
    

