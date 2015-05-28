#!/usr/bin/env python2
import re
import json
from tools import OrderedDefaultDict

import numpy as np
import bisect

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