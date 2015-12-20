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
    allFigs = list()

pidh = PidH()

f_fig_tpl = '/tmp/figure.tex'
#fig_tpl = 'figure.tex'
#fig_tpl = ''.join(file(f_fig_tpl).readlines())

odname = '/tmp/'
file_format = 'eps'

@decorate_with_call( plt.xlabel, 'XxX', for_fig=('1',) )
@decorate_with_call( plt.ylabel, r'$Y$')
@generic_figure_processor
def pf(*args, **kwargs):
    plt.grid(which='both')

    
#    ofname = 'test'+str(pidh.pid)
#    plt.savefig(odname+ofname+'.'+file_format, dpi=300)
#
#    tpl_data = {
#        'FILE_NAME':ofname+'.'+file_format,
#        'LABEL': 'label',
#        'DESC':'desc'
#    }
#    file(odname+ofname+'.tex','w').writelines( fig_tpl%tpl_data )
#    pidh.pid = pidh.pid + 1
#    pidh.allFigs.append(ofname+'.tex')




@decorate_with_alter( remove_kwargs )
@generic_plot_processor
def pp(*args, **kwargs):
    pass


render('/tmp/raport.npz', pp, pf, show=True)
    

final = file(odname+'final.tex','w')


final.writelines('\
\\pdfminorversion=4\n\
\\documentclass{article}\n\
\\usepackage{graphicx}\n\
\\begin{document}\n\
')

for fig in pidh.allFigs:
    final.writelines('\
    \\input{'+fig+'}\n\
    ')    
final.writelines('\
\\end{document}\
')

final.close()