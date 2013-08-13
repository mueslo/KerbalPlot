#will not work without a proper function and dependencies!
class PlotPlugin(object):
    #         title,cmap,norm,fmt,extend,ticks,labels
    plotVals=[None,None,None,None,'both',None,None]
    dependency=None
    isOverlay=False
    def __init__(self,plotVals=None,pfunc=None,dependency=None,isOverlay=None):
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
            return self.pfunc(**kwargs)
        else:
            print "Dependencies of plugin not satisfied!"
            
    def pfunc(self,**kwargs):
        pass
    
    def conf(self):
        pass