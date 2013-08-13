import plotplugin as pl
import numpy as np
import matplotlib as mpl
import parts as parts
mpl.pyplot.rc('text', usetex=True)
mpl.pyplot.rc('font', family='sans-serif')

print "Importing plugins..."
n_engines = np.size(parts.engines,axis=0)

# dictionary of all plugins (this will be used by kerbalplot)
pldict = {}

#to make plugin loadable by kerbalplot:
#plugin_dict['short name'] = [plot_options,plot_function]
# where plot_options = [plt_title,plt_cmap,plt_norm,plt_cbar_format,
#                      plt_cbar_extend,plt_cbar_tick_locations,plt_cbar_labels]
# see examples below


#sample plotting function
#def pfunc():
    #import any of the following (Z,M,N,X,Y) (all numpy arrays) via e.g.
    # X=kwargs["X"]
    # and add it to the dependencies

    #"Z" contains the optimal engine type for each resolved pixel
    #Z.shape==(x_resolution,y_resolution)    

    #"M" contains the minimal total mass satisfying
    # given conditions (TWR, max num engines, atm/vac)
    # for each type of engine
    #M.shape==(number_of_engines,x_resolution,y_resolution)

    #"N" contains the minimal total number of engines satisfying
    # given conditions (TWR, max num engines, atm/vac)
    # for each type of engine. Note that argmin(N, axis=0) != argmin(M, axis=0)
    #N.shape==(number_of_engines,x_resolution,y_resolution)
    
    #"X","Y" contain the meshgrid indexing of the plotted grid
    #X.shape==Y.shape== (x_resolution,y_resolution)

#try plugin to show where smallest number of engines isn't the best solution!
        
class FuelMassPercentage(pl.PlotPlugin):
    dependency=("M","Y")
    plotVals=[r'Fuel mass percentage\n\
                $1 - \frac{m_\mathrm{total}}{m_\mathrm{payload}}$',
                mpl.cm.get_cmap('jet'),mpl.colors.Normalize(0,100),None,
                'neither',np.linspace(0,100,11), None]
    def pfunc(self,**kwargs):
        M=kwargs["M"]
        Y=kwargs["Y"]
        
        m = np.min(M,axis=0)

        return 100*(m-Y)/m
    
class EngineCountOverlay(pl.PlotPlugin):
    dependency = ["Z","N"]
    isOverlay = True
    plotVals = ['Optimal number of engines\n'+
                r'$ n_\mathrm{engines}^{\mathrm{opt}} $',
                None,None,
                "%1.0f",'max',np.concatenate\
                ([2**(np.arange(0.,10.,1)),[1000]]),None]
    def pfunc(self,**kwargs):
        Z=kwargs["Z"]
        N=kwargs["N"]
        n_opt = np.zeros(Z.shape)
        zero = np.zeros(Z.shape)
        for i in np.ndindex(Z.shape):
            if Z[i]==n_engines:
                n_opt[i] = -np.inf
            else:
                n_opt[i] = N[Z[i]][i]
        return np.dstack([zero,zero,zero,np.log2(n_opt)/10.])
        
class EngineCount(pl.PlotPlugin):
    dependency = ["Z","N"]
    plotVals = ['Optimal number of engines\n'+
                r'$ n_\mathrm{engines}^{\mathrm{opt}} $',
                None,mpl.colors.LogNorm(1,1000),
                "%1.0f",'max',np.concatenate\
                ([2**(np.arange(0.,10.,1)),[1000]]),None]
    def conf(self):
        cmap_cnt = mpl.cm.get_cmap('jet')
        cmap_cnt.set_over('black')
        self.plotVals[1] = cmap_cnt
        
    def pfunc(self,**kwargs):
        Z=kwargs["Z"]
        N=kwargs["N"]
        n_opt = np.zeros(Z.shape)
        #sloooooow
        for i in np.ndindex(Z.shape):
            if Z[i]==n_engines:
                n_opt[i] = -np.inf
            else:
                n_opt[i] = N[Z[i]][i]
        return n_opt
        
class TotalMass(pl.PlotPlugin):
    dependency = ["M"]
    plotVals = ['Total mass of craft\n'+
                r'$ m_\mathrm{total} $',
                  None,mpl.colors.LogNorm(0.01,1000),
                  "%1.2ft", 'both', np.concatenate\
                  ([2**(np.arange(-6.,10.,2)),[1000]]),None]
    def conf(self):
        cmap_mss = mpl.cm.get_cmap('jet')
        cmap_mss.set_over('black')
        self.plotVals[1] = cmap_mss
        
    def pfunc(self,**kwargs):
        M = kwargs["M"]
        return np.min(M,axis=0)
        
class OptimalEngine(pl.PlotPlugin):
    dependency = ["Z"]
    plotVals = ['Optimal engine type \n'+
                  r'least $ m_\mathrm{total} = m_\mathrm{payload} + m_\mathrm{engine} + m_\mathrm{fuel} $',
                  None,None,None,'neither',
                  np.arange(n_engines)+0.5,
                  parts.engine_dict]
    def conf(self):
        cmap_tmp = mpl.pyplot.cm.Accent
        cmaplist_tmp = [cmap_tmp(i) for i in range(cmap_tmp.N)]
        cmaplist_tmp[85] = (0.2,0.7,0.9,1.0)
        norm_eng = mpl.colors.BoundaryNorm(np.arange(n_engines+1), cmap_tmp.N)
        cmap_eng = cmap_tmp.from_list('Custom cmap', cmaplist_tmp, cmap_tmp.N)
        cmap_eng.set_over('white')
        self.plotVals[1] = cmap_eng
        self.plotVals[2] = norm_eng
        
    def pfunc(self,**kwargs):
        return kwargs["Z"]


pldict["Fuel\%"]   = FuelMassPercentage()
pldict["\# Eng O"] = EngineCountOverlay()
pldict["\# Eng"]   = EngineCount()
pldict["Tot Mass"] = TotalMass()
pldict["Opt Eng"]  = OptimalEngine()
                            
print "Plugin import completed."