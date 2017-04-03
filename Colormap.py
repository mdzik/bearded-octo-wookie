import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np



class SimpleMap:
    def __init__(self, cmap = 'jet', data=False, discreate=False):
        
        
        if discreate:    
            self.cm = plt.get_cmap(cmap, len(np.unique(data)))
        else:
            self.cm = plt.get_cmap(cmap)            
        if np.iterable(data):
                self.cNorm  = colors.Normalize(vmin=np.min(data), vmax=np.max(data))
        else:
                self.cNorm  = colors.Normalize(vmin=0, vmax=1)
            

        self.scalarMap = cmx.ScalarMappable(norm=self.cNorm, cmap=self.cm)
        self.scalarMap.set_array([])
        print self.scalarMap.get_clim()
        self.l = 1.
    def setLength(self, l):
        self.l = float(l)
    def getColor(self, value):
        return self.scalarMap.to_rgba(value / self.l)
    def getMap(self):
        return self.cm
    def getSM(self):
        return self.scalarMap
class SimpleMarkerMap:

    markers = {#'+': 'plus', 
               #0: 'tickleft', 
               #'4': 'tri_right', 
               #3: 'tickdown', 
               #4: 'caretleft', 
               'H': 'hexagon2', 
               'v': 'triangle_down', 
               #'3': 'tri_left', 
               'p': 'pentagon', 
               'h': 'hexagon1', 
               '*': 'star', 
               'x': 'x', 
               'o': 'circle',
               #7: 'caretdown', 
               #5: 'caretright',
               #'2': 'tri_up', 
               #1: 'tickright',
               #6: 'caretup', 
               's': 'square', 
               '^': 'triangle_up', 
               'd': 'thin_diamond', 
               '<': 'triangle_left', 
               #'1': 'tri_down', 
               #'|': 'vline', 
               #'_': 'hline', 
               #'>': 'triangle_right', 
               #2: 'tickup', 
               '8': 'octagon', 
               'D': 'diamond'
               }       


    def __init__(self, cmap = 'jet'):
        self.syms = self.markers.keys()
        self.l = 1.

    def setLength(self, l):
        self.l = float(l)
        
    def getColor(self, value):
        if value / self.l > 1 or value / self.l < 0:
            raise "Value must be normalized 0-1"
        value = value / self.l
        return self.syms[ int( value * ( len( self.syms ) - 1 ) )   ]

        
if __name__ == "__main__":    
    cm = SimpleMap('flag')
    
    N = 10       
    x = np.linspace(0,2*np.pi) 
    for i in range(N):
        plt.plot(x,np.sin(x+i/float(N)*np.pi), color=cm.getColor(i/float(N)))
    
    
    
    plt.show()