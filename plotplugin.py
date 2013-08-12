# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 22:19:51 2013

@author: jf
"""



class PlotPlugin(object):
    plotVals=None
    dependency=None
    def __init__(self,plotVals=None,pfunc=None,dependency=None,isOverlay=False):
        if plotVals!=None: self.plotVals = plotVals
        if pfunc!=None: self.pfunc = pfunc  
        if isOverlay!=None: self.isOverlay=isOverlay    
        if dependency!=None: self.dependency=dependency
        self.conf()
        
    def func(self,**kwargs):
        t = True
        for d in self.dependency:
            t = t and kwargs.has_key(d)
        if t:
            relevant_kwargs = {}          
            for d in self.dependency:
                relevant_kwargs[d]=kwargs[d]
            return self.pfunc(**relevant_kwargs)
        else:
            print "Dependencies of plugin not satisfied!"
            
    def pfunc(self,**kwargs):
        pass
    
    def conf(self):
        pass