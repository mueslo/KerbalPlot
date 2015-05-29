KerbalPlot (new)
==========

test post please ignore

![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/engines_pressure.png)
![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/engines_pressure2.png)
![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/isp_twr.png)

![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Dres_p=0.0_nmax=inf_mintwr=0.15.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Duna_p=0.2_nmax=inf_mintwr=0.4.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Eve_p=5.0_nmax=inf_mintwr=2.0.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Kerbin_p=1.0_nmax=inf_mintwr=1.25.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Laythe_p=0.6_nmax=inf_mintwr=1.0.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Minmus, Bop_p=0.0_nmax=inf_mintwr=0.07.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Moho, Vall_p=0.0_nmax=inf_mintwr=0.35.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Mun, Eeloo, Ike_p=0.0_nmax=inf_mintwr=0.22.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Space_p=0.0_nmax=inf_mintwr=0.05.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Space_p=0.0_nmax=inf_mintwr=0.0.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Space_p=0.0_nmax=inf_mintwr=0.1.png)
![Example plot](http://raw.github.com/mueslo/KerbalPlot/master/optimalengine_Tylo_p=0.0_nmax=inf_mintwr=1.0.png)


KerbalPlot (old)
===

Plots optimal engine for each delta-V/Payload mass configuration, among a few other things.

Windows **Download**: [here](https://github.com/mueslo/KerbalPlot/releases/tag/0.01)
Linux: you know what to do, install the relevant python packages and just start the script

Current Limitations:
 - Cannot mix engine types.
 - Assumes that fuel tanks have zero dry weight and are infinitely divisible (so look for a correspondingly larger payload mass).  
  <sup><sup>(Not sure if this warrants implementing, a good rocket design ditches empty fuel tanks as soon as possible, so the truth lies somewhere between the two approaches anyway)</sup></sup>


Features:
 - Custom plots (see plugins.py for details)
 - Fun times and psychedelic colours
 
Uses:
 - Python 2.7
 - Matplotlib
 - Numpy

Examples:
![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/twr1.48_e10_atm_opteng.png)

![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/twr0.33_e10_vac_opteng.png)

![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/twr1_einf_vac_opteng.png)

![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/twr1_einf_vac_totmss.png)

![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/twr1_einf_vac_%23eng.png)

![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/twr1_einf_vac_fuel%25.png)

![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/twr1_e1_vac_opteng.png)

![Example plot](https://raw.github.com/mueslo/KerbalPlot/master/twr0_vac_opteng.png)
