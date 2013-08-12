# -*- coding: utf-8 -*-
"""
Created on Thu Aug 08 19:38:55 2013

Licensed under GNU GPLv3

@author: Johannes Falke
"""

#!/usr/bin/env python
#import itertools as it
from copy import deepcopy
import numpy as np
#import numexpr as ne
import parts as parts
import plugins as plugins
import matplotlib as mpl
from matplotlib.widgets import Slider, RadioButtons, Button
#from multiprocessing import Pool, freeze_support
mpl.pyplot.rc('text', usetex=True)
mpl.pyplot.rc('font', family='sans-serif')

g0 = 9.81

engineLimitChoices = {
r'$<\infty$': np.inf,            
r'$=1$': 1.,
r'$<3$': 3.,
r"$<5$": 5.,
r'$<10$': 10. }

#calculates number of engines needed to attain a certain TWR,
# with infinitely divisible, 0-dry-mass fuel tanks
def n_e(engine, twr, m_p, deltv, engineCount):
    if (twr==0): return 1
    else:
        #calculate engine count, e[2]=Thrust; e[4]=I_sp; e[1]=Weight, 1/1000
        h = np.ceil(m_p/(engine[2]/(twr*g0*np.exp(deltv/(engine[4]*g0)))-engine[1]))
        
        b = h>engineCount #mask array where engine count is greater than largest allowed
        h[b] = np.inf     #set forbidden
     
        b = h<1 #mask array where engines needed is less than one (forbidden)
        h[b] = np.inf #set forbidden
        return h

#def n_wrap(par):
#    return np.array([n_e(e,*par) for e in parts.engines])


class KerbalPlot:
    def m_ef(self, m_f):
        print 'lol'
    

#TODO resolution & dimension change
# plot(ax, type, twr, vac, dims, res, otherargs)
    #             obj str  float bool int  func
    def plot(self, ax, typ, twr, vac, cnt):
        print "generalised plot! (twr vac cnt)=(",twr,vac,cnt,")"
        
        if self.lastCalc != (twr, vac, cnt):
            self.compute(ax, twr, vac, cnt)
        else: print "No recalculation necessary."
            
        print 'plot',typ
        
        #self.axcb_overlay.cla()
        if not plugins.pldict[typ].isOverlay:
            print "Plot plugin is overlay, not clearing axes"
            self.ax.cla() #clear plot axes
            self.axcb.cla() #clear colourbar axes
        
        
        #FIXME Z,M,N
        #TODO multiprocessing
        
        #main plot config & labels
        ax.set_yscale('log')
        ax.grid(True, which="both")   
        ax.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        ax.set_ylabel(r'Payload mass $m_\mathrm{payload}$ in $\mathrm{t}$')
        ax.set_xlabel(r'Stage $\Delta v$ in $\mathrm{\frac{m}{s}}$')   
        
        #name,pl,func
        
        #plugin_dict[name]==[pl,func]
        #title,cmap,norm,fmt,extend,ticks,labels = ['Optimal engine\n(least total mass $m_\mathrm{total} = m_\mathrm{payload} + m_\mathrm{engine} + m_\mathrm{fuel}$)',
        #          self.cmap,self.norm,None,'neither',np.arange(n_engines)+0.5,enginedict]
        
        plot = plugins.pldict[typ].plotVals
        func = plugins.pldict[typ].pfunc
        z=func(Z=self.Z,M=self.M_cache,N=self.n_cache,X=self.X,Y=self.Y)
        
        ax.set_title(plot[0])
        self.CB = mpl.colorbar.ColorbarBase(self.axcb, cmap=plot[1], norm=plot[2], format=plot[3], extend=plot[4], ticks=plot[5])
        if plot[6]!=None:
            self.CB.ax.set_yticklabels(plot[6])   
        
        print np.shape(z)
        ax.imshow(z,cmap=plot[1], norm=plot[2], extent=(0,10000,0.01,1000), origin='lower')

        #(fake) tabs changed
        if typ != self.currentPlot:
            #update (fake) tab color
            for b in self.buttons:
                if b.label.get_text()==typ:
                    print b.label.get_text(),"active"
                    b.color = self.activeTabColor
                else:
                    print b.label.get_text(),"inactive"
                    b.color = self.inactiveTabColor
            #update plot type var
            self.currentPlot = typ 
       

    def compute(self, ax, twr, vac, cnt):
        #pool = Pool(processes=4)
        print "Computing..."
        #params = self.X,self.Y,twr,cnt
        #n_c2 = pool.map(n_wrap, params)
        self.n_cache = np.array([n_e(e,twr,self.Y,self.X,cnt) for e in self.engines])
        
        self.M_cache = np.array([(n_e(e,twr,self.Y,self.X,cnt)*e[1]+self.Y)*np.exp(self.X/(g0*e[4])) for e in self.engines])
        
        self.Z = np.argmin(self.M_cache,axis=0)
        self.numrows, self.numcols = self.Z.shape        
        
        b = np.sum(np.isinf(self.M_cache), axis=0)==parts.n_engines #mask array where all engines were inf
        self.Z[b] = parts.n_engines

        self.lastCalc = (twr, vac, cnt)  
        

    #TODO: use height slider instead of vac/atm
    # Fraction of full Kerbin atm, unused
    #H_kerbin = 5000
    #atm = lambda h: np.exp(-h/H_kerbin)
    
    

    #outputs status bar info
    def format_coord(self, x, y):
        col = int(x*self.res[0]/self.xmax) #TODO tweak these later
        row = int(self.res[1]/(np.log10(self.ymax)-np.log10(self.ymin))*(np.log10(y)-np.log10(self.ymin))-0.5)
        
        #check if actually in drawing area
        if col>=0 and col<self.numcols and row>=0 and row<self.numrows:
            z = self.Z[self.res[1]*row/self.numrows,self.res[0]*col/self.numcols]
            if z != parts.n_engines: #check if not in forbidden region
                n = self.n_cache[z,row,col]
                m = self.M_cache[z,row,col]
                return u'\u0394v=%1.0fm/s, m\u2093=%1.2ft, \
                        Engine: %1.0f\u2715%s, \
                        fuel mass %1.2ft / %1.1f%% of total %1.2ft'%(x, y, n,\
                        parts.engine_dict[z], m-y, 100*(m-y)/m,m)
            else:
                return u'\u0394v=%1.0fm/s, m\u2093=%1.2ft, Forbidden region'%(x, y)

        else:
            return 'x=%1.4f, y=%1.4f'%(x, y)
    

    #updates graph
    def update(self, ax):
        
        self.plot(ax,self.currentPlot, self.twr, self.isVacuum, self.engineCount)
        mpl.pyplot.draw()

    def atmfunc(self, label):
        print "atmfunc!"
        self.engines = deepcopy(parts.engines) #copy engines list
        print "loc: self.eng=parts.eng?",id(self.engines)==id(parts.engines)
        print "cont: self.eng=parts.eng?",(self.engines)==(parts.engines)
        
        self.isVacuum = True
        print self.engines[0]
        print parts.engines[0]        
        if label=='atm': #swap atm and vac isp in engine array
            self.isVacuum = False
            for i in range(len(self.engines)):
                self.engines[i][3]=parts.engines[i][4]
                self.engines[i][4]=parts.engines[i][3]
            print "Switched to atmosphere"
        else:
            print "Switched to vacuum"
        print self.engines[0]
        print parts.engines[0]
        
        self.update(self.ax)
        #draw()

    #updates engine choice
    def engfunc(self, label):
        self.engineCount = engineLimitChoices[label]

        self.update(self.ax)
        #draw()
        
    def twrchange(self, twr):
        self.twr = twr
        self.update(self.ax)
        
    #def plotchange(self)
    '''#pickEvent
    line, = ax.plot(rand(100), 'o', picker=5)  # 5 points tolerance

    def on_pick(event):
        thisline = event.artist
        xdata, ydata = thisline.get_data()
        ind = event.ind
        print('on pick line:', zip(xdata[ind], ydata[ind]))
    
    cid = fig.canvas.mpl_connect('pick_event', on_pick)
    '''
    
    def __init__(self,xmin=0.,xmax = 10000.,ymin = 0.01,ymax = 1000.,res = (500,500)):
        self.xmin=xmin; self.xmax=xmax
        self.ymin=ymin; self.ymax=ymax
        self.res = res
        print 'KerbalPlot!'
        

        # Create figure and plotting axes
        fig = mpl.pyplot.figure(figsize=(15,10))
        self.ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.15)
        #print self.ax.size                  
        
        # Create colourbar axes
        self.axcb = fig.add_axes([0.90, 0.15, 0.01, 0.75])  
        self.axcb_overlay = fig.add_axes([0.99, 0.15, 0.01, 0.75]) 
        
        # Create colourmaps
        cmap = mpl.pyplot.cm.Accent
        cmaplist = [cmap(i) for i in range(cmap.N)]
        cmaplist[85] = (0.2,0.7,0.9,1.0)
        #cmaplist[42] = (0.2,0.7,0.9,1.0)
        #print size(cmaplist) #==1024
        #self.norm = cols.BoundaryNorm(np.arange(parts.n_engines+1), cmap.N)
        #self.cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N); self.cmap.set_over('white')
        #self.cmap_fmp = get_cmap('jet')
        #self.cmap_cnt = get_cmap('jet');self.cmap_cnt.set_over('black')
        #self.cmap_mss = self.cmap_cnt
        
        # Add sliders and radiobuttons
        axcolor = 'lightgoldenrodyellow'
        self.axtwr  = mpl.pyplot.axes([0.25, 0.04, 0.65, 0.03], axisbg=axcolor)
        self.stwr = Slider(self.axtwr, 'Minimum TWR', 0.0, 5.0, valinit=1.)
        #self.stwr.on_changed(lambda val: self.update(self.ax))
        self.stwr.on_changed(self.twrchange)
        self.atmax = mpl.pyplot.axes([0.08, 0.02, 0.06, 0.1], axisbg=axcolor)
        self.radioatm = RadioButtons(self.atmax, ('vac', 'atm'), active=0)
        self.radioatm.on_clicked(self.atmfunc)
        self.engax = mpl.pyplot.axes([0.02, 0.02, 0.06, 0.1], axisbg=axcolor, title='\# Engines')
        self.radioeng = RadioButtons(self.engax, sorted(engineLimitChoices, key=lambda key: -engineLimitChoices[key]), active=0)    
        self.radioeng.on_clicked(self.engfunc)
        
        # No calculation before
        self.lastCalc = (-1, -1, -1)

        
        # Initialise values
        self.twr = self.stwr.val
        self.isVacuum = True
        self.engineCount = np.inf
        self.engines = parts.engines

        self.allowSRBs = False   #TODO implement SRBs (fixed fuel engines)
        self.fuelTanks = False   #TODO fuel tank discreteness and weight        
        self.mixedEngines= False #TODO mixed engine types
        self.currentPlot = None  #TODO proper (fake) tab support
        #TODO: class for plot functions in plugins.py
        #TODO: plugin entry points
     

        
        # Add iterating arrays
        x = np.arange(self.xmin, self.xmax, self.xmax/self.res[0])
        y = np.logspace(np.log10(self.ymin), np.log10(self.ymax), num=self.res[1])
        self.X, self.Y = np.meshgrid(x, y)
        self.xx,self.yy = np.meshgrid(np.arange(self.res[0]),np.arange(self.res[1]), sparse=True)
        
        #Create buttons for plotting plugins
        self.activeTabColor = axcolor
        self.inactiveTabColor = '#DADAC2'
        #self.types = plugins.pdict.keys()[::-1] #reverse order
        self.types = plugins.pldict.keys()[::-1] #reverse order
        self.buttons = []
        btn_xi= 0.7
        btn_xe= 0.9
        btn_x = np.linspace(btn_xi,btn_xe,len(self.types)+1)        
        for i in np.arange(len(self.types)):
            ax_tmp=mpl.pyplot.axes([btn_x[i],0.9,(btn_xe-btn_xi)/(len(self.types)),0.04])
            self.buttons.append(Button(ax_tmp, self.types[i], hovercolor='0.975'))
            self.buttons[i].on_clicked(lambda event,i=i: self.plot(self.ax,self.types[i],self.twr,self.isVacuum, self.engineCount))
        

        # Initial Plot
        typ_i = "Opt Eng" #try this as initial plot type
        if typ_i in plugins.pldict:
            self.plot(self.ax,typ_i,self.twr,self.isVacuum,self.engineCount)
        elif len(plugins.pldict)==0:
            print "No plugins for plotting found in plugins.py!"
        else:
            self.plot(self.ax, plugins.pldict.keys()[0],\
                      self.twr, self.isVacuum, self.engineCount)
        
        
        # Assign custom status bar formatter
        self.ax.format_coord = self.format_coord


            
        
        
        # Show plot
        mpl.pyplot.show()


if __name__=='__main__':
    #freeze_support()    
    k = KerbalPlot(res=(1000,500))