# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:38:16 2015

@author: mdzikowski
"""


from matplotlib.backends.backend_pdf import PdfPages
class plotToPng:
    pdf_nb_plots_per_page = 2
    def __init__(self,fname, plt):
        self.i = 0
        self.plt = plt
        
        self.pltF = plt.figure
        self.fname = fname
        self.plt.figure = self.masker
        
        self.plt.show = self.newFile

        self.idx = 0
        self.isOpened = False
        self.page = 0
        
        #self.newFile(f=fname)
        self.begin()
        
    def begin(self):
      #if self.i % self.pdf_nb_plots_per_page == 0:
      self.fig = self.pltF(figsize=(11.69, 8.27), dpi=100)
     
      # Plot stuffs !
      #self.plt.subplot2grid((self.pdf_nb_plots_per_page, 1), (self.i % self.pdf_nb_plots_per_page, 0))

      
    def end(self, force=False):
      #if (self.i + 1) % self.pdf_nb_plots_per_page == 0 or force:
        #self.plt.tight_layout()
        #self.pdf_pages.savefig(self.fig)        
        
      self.fig.savefig(self.fname+str(self.idx)+str(self.page)+".png")
      self.page = self.page+1
      self.plt.close(self.fig)
      print "Closing page"
      
      
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
        
        #self.i = 0
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
            
            

class plotToPdf:
    pdf_nb_plots_per_page = 2
    
    def __init__(self,fname, plt):
        self.i = 0
        self.plt = plt
        
        self.pltF = plt.figure
        self.fname = fname
        self.plt.figure = self.masker
        
        self.plt.show = self.newFile

        self.idx = 0
        self.isOpened = False
        self.page = 0
        
        self.newFile(f=fname)
        self.begin()
        
    def begin(self):
      if self.i % self.pdf_nb_plots_per_page == 0:
          self.fig = self.pltF(figsize=(8.27, 11.69), dpi=100)
     
      # Plot stuffs !
      self.plt.subplot2grid((self.pdf_nb_plots_per_page, 1), (self.i % self.pdf_nb_plots_per_page, 0))

      
    def end(self, force=False):
      if (self.i + 1) % self.pdf_nb_plots_per_page == 0 or force:
        self.plt.tight_layout()
        self.pdf_pages.savefig(self.fig)        
        
        #self.fig.savefig(self.fname+str(self.idx)+str(self.page)+".png")
        self.page = self.page+1
        self.plt.close(self.fig)
        print "Closing page"
      
      
    def newFile(self,**kargs):
        
        self.end(self.i > 0)
        
        if self.isOpened:
          self.pdf_pages.close()

        
        if 'f' in kargs:
            self.pdf_pages = PdfPages(kargs['f']+".pdf")
        else:
            self.pdf_pages = PdfPages(self.fname+str(self.idx)+".pdf")            
        self.idx = self.idx  + 1
        self.isOpened = True
        
        self.i = 0
        self.page = 0
        self.begin()

    def close(self):
        if self.isOpened:
            self.pdf_pages.close()
        self.isOpened = False
        
    def masker(self,**kargs):
        if len(kargs) == 0:
            self.end()
            self.i = self.i + 1
            self.begin()            
        else:
            raise "Masker to much"                    