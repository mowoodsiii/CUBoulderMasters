# File: ptfun
# Functions for gnuradio-companion PAM p(t) generation
import numpy as np
def pampt(sps, ptype, pparms=[]):
    """
    PAM pulse p(t) = p(n*TB/sps) generation
    >>>>> pt = pampt(sps, ptype, pparms) <<<<<
    where  sps:
        ptype: pulse type ('rect', 'sinc', 'tri')
        pparms not used for 'rect', 'tri'
        pparms = [k, beta] for sinc
        k:     "tail" truncation parameter for (truncates p(t) to -k*sps <= n < k*sps)
        beta:  Kaiser window parameter for 'sinc'
        pt:    pulse p(t) at t=n*TB/sps
    Note: In terms of sampling rate Fs and baud rate FB,sps = Fs/FB
    """
