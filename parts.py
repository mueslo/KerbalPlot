# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 16:29:51 2013

@author: jf
"""

# Not yet implemented
fueltanklist = [['Oscar-B',0.078675,0.015], #19.1% dry weight
                ['Round-8',0.136,0.025], #18.4% dry weight
                ['FL-T100',0.5625,0.0625]] #11.1% dry weight


#these are all the same percentage
#dry weight as FL-T100, also, the
#weight is integer multiples that of FL-T100
#it is therefore redundant to look at these:
'''
                ['FL-T200',1.125,0.125],    #x2
                ['FL-T400',2.25,0.25],      #x4
                ['FL-T800',4.5,0.5],        #x8
                ['X200-8',4.5,0.5],         #x8
                ['X200-16',9,1],            #x16
                ['X200-32',18,2],           #x32
                ['Jumbo-64',36,4]]          #x64 FL-T100
'''

#     units                   t     kN    s        s
#                name         mass thrust isp_atm  isp_vac
engines     =  [['LV-1R',     0.03, 1.5,  220,     290],
                ['R 24-77',   0.09, 20,   250,     300],
                ['Mark 55',   0.9,  120,  290,     320],
                ['LV-1',      0.03, 1.5,  220,     290],
                ['R 48-7S',   0.1,  20,   300,     350],
                ['LV-T30',    1.25, 215,  320,     370],
                ['LV-T45',    1.5,  200,  320,     370],
                ['LV-909',    0.5,  50,   300,     390],
                ['Aerospike', 1.5,  175,  388,     390],
                ['Poodle',    2.5,  220,  270,     390],
                ['Skipper',   4.,   650,  300,     350],
                ['Mainsail',  6.,   1500, 280,     330],
                ['LV-N',      2.25, 60,   220,     800]]
                
n_engines = len(engines)
engine_dict = dict(zip(range(n_engines),[e[0] for e in engines]))