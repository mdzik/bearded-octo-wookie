# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:55:33 2015

@author: mdzikowski
"""

import xml.sax
import re

class CLBXMLHandler(xml.sax.ContentHandler):
    
    def __init__(self, config_ref):
        self.config = config_ref
        
    def startElement(self, name, attrs):
        if name == "Params":
            a = dict()
            for (k,v) in attrs.items():
                if k == 'gauge':
                    a['gauge'] = float(re.findall('[-,\.,e,0-9]+', v)[0])
                else:
                    a['name'] = k
                    a['value'] = v
                    a['float'] = float(re.findall('[-,\.,e,0-9]+', v)[0])
                    
                
            self.config[a['name']] = a
        if name == "Geometry":
            
            for (k,v) in attrs.items():
                
                if k in ('nx', 'ny'):
                    a = dict()
                    a['name'] = k
                    a['value'] = v
                    a['float'] = float(re.findall('[-,\.,e,0-9]+', v)[0])                                  
                    self.config[a['name']] = a
            
            
def parseConfig(fconfig):
    CLBc = dict()
    parser = xml.sax.make_parser()
    parser.setContentHandler(CLBXMLHandler(CLBc))
    parser.parse(open(fconfig,"r"))

    
    CLBcf = dict()
    CLBcg = dict()
    for c in  CLBc:
        CLBcf[c] = CLBc[c]['float']
        if 'gauge' in CLBc[c]:
            CLBcg[c] = CLBc[c]['gauge']
       #     print c, "  gauge = ", CLBc[c]['gauge']        
       # print c, " = ", CLBc[c]['float']
        
    return CLBc, CLBcf, CLBcg