# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:38:16 2015

@author: mdzikowski
"""


#from matplotlib.backends.backend_pdf import PdfPages
class plotToPdf:
    pdf_nb_plots_per_page = 2
    
    def __init__(self,fname):
        self.i = 0
        
        self.pltF = plt.figure
        self.fname = fname
        plt.figure = self.masker
        
        plt.show = self.newFile

        self.idx = 0
        self.isOpened = False
        self.page = 0
        
        self.newFile(f=fname)
        self.begin()
        
    def begin(self):
      if self.i % self.pdf_nb_plots_per_page == 0:
          self.fig = self.pltF(figsize=(8.27, 11.69), dpi=100)
     
      # Plot stuffs !
      plt.subplot2grid((self.pdf_nb_plots_per_page, 1), (self.i % self.pdf_nb_plots_per_page, 0))

      
    def end(self):
      if (self.i + 1) % self.pdf_nb_plots_per_page == 0:
        plt.tight_layout()
    #    self.pdf_pages.savefig(self.fig)        
        
        self.fig.savefig(self.fname+str(self.idx)+str(self.page)+".png")
        self.page = self.page+1
        plt.close(self.fig)
      self.i = self.i + 1
      
    def newFile(self,**kargs):
        
        self.end()
        
#        if self.isOpened:
#          self.pdf_pages.close()

        
#        if 'f' in kargs:
#            self.pdf_pages = PdfPages(kargs['f']+".pdf")
#        else:
#            self.pdf_pages = PdfPages(self.fname+str(self.idx)+".pdf")            
        self.idx = self.idx  + 1
        self.isOpened = True
        
        self.i = 0
        self.page = 0
        self.begin()

    def close(self):
#        if self.isOpened:
#            self.pdf_pages.close()
        self.isOpened = False
        
    def masker(self,**kargs):
        if len(kargs) == 0:
            self.end()
            self.begin()
        else:
            raise "Masker to much"        