# File: filtspecs.py
# Module for filter specfifications
# FIR: Determine filter taps
# IIR: Determine numerator (b) and denominator (a)
# polynomial coefficients

from pylab import *
from scipy.signal import butter

def trapfilt_taps(N, phiL, alfa):
    """
    Returns taps for order N FIR LPF with trapezoidal frequency
    response, normalized cutoff frequency phiL = fL/Fs, and rolloff
    parameter alfa.
    >>>>> hLn = trapfilt_taps(N, phiL, alfa) <<<<<
    where
        N: filter order
        phiL: normalized cutoff frequency (-6 dB)
        alfa: frequency rolloff parameter, linear rolloff over range (1-alfa)phiL <= |f| <= (1+alfa)phiL
    """
