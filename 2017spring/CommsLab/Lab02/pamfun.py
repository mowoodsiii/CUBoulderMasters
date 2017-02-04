# File: pamfun.py
# Functions for pulse amplitude modulation (PAM)
from pylab import *
import ecen4652 as ecen

def pam10(sig_an, Fs, ptype, pparms=[]):
    """
    Pulse amplitude modulation: a_n -> s(t), -TB/2<=t<(N-1/2)*TB,
    V1.0 for ’rect’, ’sinc’, and ’tri’ pulse types.
    >>>>> sig_st = pam10(sig_an, Fs, ptype, pparms) <<<<<
    where  sig_an: sequence from class sigSequ
        sig_an.signal():  N-symbol DT input sequence a_n, 0 <= n < N
        sig_an.get_FB():  Baud rate of a_n, TB=1/FB
        Fs:    sampling rate of s(t)
        ptype: pulse type (’rect’,’sinc’,’tri’)
        pparms not used for ’rect’,’tri’
        pparms = [k, beta]  for ’sinc’
        k:     "tail" truncation parameter for ’sinc’
        (truncates p(t) to -k*TB <= t < k*TB)
        beta:  Kaiser window parameter for ’sinc’
        sig_st: waveform from class sigWave
        sig_st.timeAxis():  time axis for s(t), starts at -TB/2
        sig_st.signal():    CT output signal s(t), -TB/2<=t<(N-1/2)*TB,
        with sampling rate Fs
    """
    N = len(sig_an)            # Number of data symbols
    FB = sig_an.get_FB()       # Baud rate
    if(ptype=='tri'):
        Fs=FB
    elif(ptype=='sinc'):
        k=pparms[0]
        beta=pparms[1]
    n0 = sig_an.get_n0()       # Starting index
    ixL = ceil(-Fs*(n0+0.5)/float(FB))   # Left index for time axis
    ixR = ceil(Fs*(n0+N-0.5)/float(FB))  # Right index for time axis
    tt = arange(ixL,ixR)/float(Fs)  # Time axis for s(t)
    t0 = tt[0]                 # Start time for s(t)
    # ***** Conversion from DT a_n to CT a_s(t) *****
    an = sig_an.signal()       # Sequence a_n
    ast = zeros(len(tt))       # Initialize a_s(t)
    ix = array(around(Fs*arange(0,N)/float(FB)),int) # Symbol center indexes
    ast[ix-int(ixL)] = Fs*an   # delta_n -> delta(t) conversion
    # ***** Set up PAM pulse p(t) *****
    ptype = ptype.lower()      # Convert ptype to lowercase
    # Set left/right limits for p(t)
    if (ptype=='rect' or ptype=='tri'):
        kL = -0.5; kR = -kL
    else:
        kL = -1.0; kR = -kL    # Default left/right limits
    ixpL = ceil(Fs*kL/float(FB))   # Left index for p(t) time axis
    ixpR = ceil(Fs*kR/float(FB))   # Right index for p(t) time axis
    ttp = arange(ixpL,ixpR)/float(Fs)  # Time axis for p(t)
    pt = zeros(len(ttp))       # Initialize pulse p(t)
    if (ptype=='rect' or ptype=='tri'):        # Rectangular p(t)
        ix = where(logical_and(ttp>=kL/float(FB), ttp<kR/float(FB)))[0]
        pt[ix] = ones(len(ix))
    elif (ptype=='sinc'):
        pwt = sig_pt.sig*kaiser(len(sig_pt.sig),beta)    # Pulse p(t), Kaiser windowed
    else:
        print("ptype '%s' is not recognized" % ptype)
    # ***** Filter with h(t) = p(t) *****
    st = convolve(ast,pt)/float(Fs)  # s(t) = a_s(t)*p(t)
    st = st[int(-ixpL):int(ixR-ixL-ixpL)]  # Trim after convolution
    return ecen.sigWave(st, Fs, t0)  # Return waveform from sigWave class
