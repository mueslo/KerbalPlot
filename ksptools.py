#!/usr/bin/env python2
import re
import json
from tools import OrderedDefaultDict

import numpy as np
import bisect

from collections import namedtuple
import os

g0 = 9.81

ConfigNode = lambda: OrderedDefaultDict(list)

class KerbalConfig(object):
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.config = ConfigNode()
                    
            def parse(config_node):
                for line in f:
                    
                    #clean line
                    line = line.strip()
                    if "//" in line:
                        line, comment = line.split("//", 1)
                        
                    if "}" in line: #end of namespace, config_node finished
                        yield config_node
                        break #stop reading lines for this node
                    
                    elif "=" in line: #attribute line, add to current config_node
                        attribute, value = line.split("=", 1)
                        attribute = attribute.strip()
                        value = value.strip()
                        config_node[attribute].append(value)
                        
                    elif line and not line.isspace():
                        if "{" in line:
                            name = line.strip("{")
                        else:
                            name = line
                            while "{" not in next(f):
                                pass
                        subnamespace = ConfigNode()
                        config_node[name].append(subnamespace)
                        for c in parse(subnamespace):
                            yield c
            for node in parse(self.config):
                pass
            
    def __getattr__(self, key):
        return self.config[key]
            
    def __repr__(self):
        #for key, val in config_node.items():
        #    if len(val) == 1:
        #        config_node[key] = val.pop()
        return json.dumps(self.config, indent=2)
                

def pc_func_from_params(parameters):
    if any(map(lambda x: len(x) != 2, parameters)):
        raise NotImplementedError()
    
    diff=np.diff(parameters,axis=0)
    slopes = np.divide(diff[:,1], diff[:,0])
    avg_slopes = np.hstack([slopes[0], (slopes[1:] + slopes[:-1]) / 2, slopes[-1]])
    sorted_params = sorted(parameters)
    sorted_x = zip(*sorted_params)[0]
    #print "Generating piecewise-cubic function from parameters", sorted_params
    
    arg_d = {}
    
    for i in range(len(parameters)+1):
        if i == 0:
            arg_d[i] = (sorted_params[i][1],0,0,0)
        elif i == len(parameters):
            arg_d[i] = (sorted_params[i-1][1],0,0,0)
        else:
            x0 = sorted_params[i-1][0]
            x1 = sorted_params[i][0]
            
            y0 = sorted_params[i-1][1]
            y1 = sorted_params[i][1]
            m0 = avg_slopes[i-1]
            m1 = avg_slopes[i]
            
            A = np.array([[1, x0, x0**2, x0**3],
                          [1, x1, x1**2, x1**3],
                          [0, 1, 2*x0, 3*x0**2],
                          [0, 1, 2*x1, 3*x1**2]])
            arg_d[i] = np.linalg.solve(A, np.array([y0, y1, m0, m1]))
        
    
    def func(x, debug=False):
        a,b,c,d = arg_d[bisect.bisect_left(sorted_x, x)]
        return a + b*x + c*x**2 + d*x**3
    
    return np.vectorize(func)

Engine = namedtuple('Engine', ['name', 'mass', 'fvac', 'isp', 'isp_func'])

def get_engines(ksp_dir = "."):
    """ Returns list of type Engine """
    engine_cfgs = []
    for root, dirs, files in os.walk(ksp_dir+'/GameData/Squad/Parts/Engine'):
        #dirs[:] = [d for d in dirs if "liquidEngine" in d]

        for cfg in (f for f in files if ".cfg" in f):
            engine_cfgs.append(KerbalConfig(root+"/"+cfg))

    engines = []
    for e_cfg in engine_cfgs:
        part = e_cfg.PART[-1]
        d = {}
        name = part["title"][-1]

        repls = (('Liquid Fuel Engine', 'LFE'),
                 ('Liquid Engine', 'LE'),
                 ('Atomic Rocket Motor', 'ARM'),
                 ('Solid Fuel Booster', 'SFB'),
                 ('Electric Propulsion System', 'EPS')
        name = reduce(lambda a, kv: a.replace(*kv), repls, name)
        name = name.strip()

        d["name"] = name
        d["mass"] = float(part["mass"][-1])

        for module in part["MODULE"]:       
            atmosphere_curve = module.get("atmosphereCurve")
            if atmosphere_curve:
                try:
                    curvekeys = atmosphere_curve[-1].get("key")
                    d["fvac"] = float(module["maxThrust"][-1])
                    atm_params = [tuple(float(x) for x in k.split()) for k in curvekeys]
                    d["isp"] = atm_params
                    d["isp_func"] = pc_func_from_params(atm_params)
                except (NotImplementedError, KeyError) as e:
                    print "skipping",name,"due to",type(e)
                else:
                    engines.append(Engine(**d))
                finally:
                    break

    engines.sort(key=lambda e: e.mass)
    
    return engines

#calculates number of engines needed to attain a certain TWR,
# with infinitely divisible, 0-dry-mass fuel tanks
def n_e(engine, (Dv, M_p), min_twr=0., pressure=0., max_engine_count=np.inf):
    if (min_twr==0): #if there's no minimum twr, a single engine is the best in terms of mass and therefore fuel efficiency
        return np.ones(np.shape(M_p)) #shape(M_p) *should* == shape(Dv)
    else:
        isp = engine.isp_func(pressure)
        thrust = engine.fvac * isp/engine.isp_func(0)
        u = isp*g0
        
        #calculate engine count
        # via tsiolkovsky rocket eq, see kerbalplot.ipynb
        num = np.ceil(M_p/(thrust/(min_twr*g0*np.exp(Dv/u))-engine.mass))
        
        #using ceiling here isn't actually correct, but only first guess. This is because
        # the fractional engine we rounded up from also only has fraction weight. For large m_p/dv this shouldn't
        # matter too much, but for light crafts this might be very wrong
        
        forbidden = num>max_engine_count #mask array where engine count is greater than largest allowed
        num[forbidden] = np.inf #set forbidden
     
        forbidden = num<1 #mask array where engines needed is less than one (forbidden)
        num[forbidden] = np.inf #set forbidden
        return num

# TODO:
    # max fuel (e.g. SRB)
    # min fuel (e.g. Mammoth, SRB)
    # fuel tank weight
def get_optimal_engine_configuration(engines, dv, mp, pressure=0., min_twr=0., max_engine_count=np.inf):
    pass

    #configuration space: fuel tank type&count, engine type&count


def compute(engines, (Dv, M_p), **kwargs):
    pressure = kwargs['pressure']
    min_twr = kwargs['min_twr']
    max_engine_count = kwargs['max_engine_count']
    #print "Computing..."
    #TODO iterate explicitly so that n is not calculated twice
    #TODO multiprocessing?

    # number of engines needed
    n = np.array([n_e(e, (Dv, M_p), min_twr=min_twr, pressure=pressure, max_engine_count=max_engine_count) for e in engines])
    
    # total mass
    M = [(n[i]*e.mass+M_p)*np.exp(Dv/(g0*e.isp_func(pressure))) for i,e in enumerate(engines)]
    #M = np.array([(n_e(e,M_p,Dv,min_twr=min_twr, pressure=pressure, max_engine_count=max_engine_count)*e.mass+M_p)*np.exp(Dv/(g0*e.isp_func(pressure))) for e in engines])

    # index of engine with configuration of least mass
    I = np.argmin(M,axis=0)     

    b = np.sum(np.isinf(M), axis=0)==len(engines) #mask array where all engines were inf
    I[b] = len(engines) #set the index to len(engines) (out of bounds)

    #print "Done."
    return n, M, I