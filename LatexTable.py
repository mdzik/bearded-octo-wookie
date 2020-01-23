#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 11:44:18 2018

@author: mdzik
"""

class LatexTable:
    
    def __init__(self, **kwargs):
        self.columns = dict()
        self.formats = dict()
        pass
    
    #Add column
    def __call__(self, *args):
        if not self.columns.has_key(args[0]):
            self.columns[args[0]] = list()
            if len(args) > 1:
                self.formats[args[0]] = args[1]
            else:
                self.formats[args[0]] = '%s'
        return self.columns[args[0]]
    
    def printme(self):
        
        print '\\begin{tabular}{' + '|c'*len(self.columns)+ '|}'
        keys = self.columns.keys()
        
        print "\hline"
        dline = ''
        for k in keys:
            dline = dline +  str(k)+" & "
        print dline + "\\\\"
        fmt = [self.formats[k] for k in keys ]
        for l in zip( *[self.columns[k] for k in keys] ):
            print "\hline"
            dline = ''
            for f, k in zip(fmt, l):
                dline = dline +  f%k+" & "
            print dline + "\\\\"
        print '\\hline'
        print '\\end{tabular}'
    
#  \begin{tabular}{|r|l|}
#  \hline 
#  w1k1 & w1k2\\
#  \hline
#  w2k1 & w2k2 \\
#  \hline
#  \end{tabular} 
    
        
#lt = LatexTable()
#lt('a', '%.2f').append(1.321321321)
#lt('a').append(2.13213)
#
#lt('b').append('1b')
#lt('b').append('2b')
#
#lt.printme()