# this module will be imported in the into your flowgraph

# File: ptfun
# Functions for gnuradio-companion PAM p(t) generation
import numpy as np
from pylab import *
def pampt(sps, ptype, pparms=[]):
    """
    PAM pulse p(t) = p(n*TB/sps) generation
    >>>>> pt = pampt(sps, ptype, pparms) <<<<<
    where  sps:
        ptype: pulse type ('rect', 'sinc', 'tri')
        pparms not used for 'rect', 'tri'
        pparms = [k, beta, Fs] for sinc
        k:     "tail" truncation parameter for (truncates p(t) to -k*sps <= n < k*sps)
        beta:  Kaiser window parameter for 'sinc'
        Fs:    Sampling rate
        pt:    pulse p(t) at t=n*TB/sps
    Note: In terms of sampling rate Fs and baud rate FB,sps = Fs/FB
    """
    if ptype is 'rect':
        pt = np.ones(sps)
    elif ptype is 'tri':
        triarray = np.arange(0,1,(1/float(sps)))[1:]
        pt = np.concatenate([triarray,[1],triarray[::-1]])
    elif ptype is 'sinc':
        k = pparms[0]
        beta = pparms[1]
        Fs = pparms[2]

        nn = np.arange(-2*k*sps,2*k*sps)
        pt = sinc((1/float(sps))*nn)
        pt = pt*kaiser(len(pt),beta)
    return(pt)
