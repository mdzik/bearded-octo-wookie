import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np



class SimpleMap:
    def __init__(self, cmap = 'jet'):

        self.cm = plt.get_cmap(cmap) 
        self.cNorm  = colors.Normalize(vmin=0, vmax=1)
        self.scalarMap = cmx.ScalarMappable(norm=self.cNorm, cmap=self.cm)
        print self.scalarMap.get_clim()
        self.l = 1.

    def setLength(self, l):
        self.l = float(l)
        
    def getColor(self, value):
        if value / self.l > 1 or value / self.l < 0:
            raise "Value must be normalized 0-1"
        return self.scalarMap.to_rgba(value / self.l)
        
        
        
        
        
if __name__ == "__main__":    
    cm = SimpleMap('flag')
    
    N = 10       
    x = np.linspace(0,2*np.pi) 
    for i in range(N):
        plt.plot(x,np.sin(x+i/float(N)*np.pi), color=cm.getColor(i/float(N)))
    
    
    
    plt.show()