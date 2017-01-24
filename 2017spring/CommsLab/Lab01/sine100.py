# File: sine100.py
# Asks for sampling frequency Fs and then generates
# and plots 5 periods of a 100 Hz sinewave
from pylab import *
from ast import literal_eval

def sampler(Fs):
    f0 = 100           # Frequency of sine
    tlen = 5e-2        # Signal duration in sec
    tt = arange(0,round(tlen*Fs))/float(Fs)   # Time axis
    st = sin(2*pi*f0*tt)   # Sinewave, frequency f0
    return[Fs,tt,st]
