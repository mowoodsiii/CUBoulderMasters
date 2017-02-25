# File: pamfun.py
# Functions for pulse amplitude modulation (PAM)
from pylab import *
import ecen4652 as ecen
from quick import *
import sinc_ipol
from math import *

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
    ptype = ptype.lower()      # Convert ptype to lowercase
    an = sig_an.signal()       # Sequence a_n
    N = len(an)            # Number of data symbols
    FB = sig_an.get_FB()       # Baud rate
    TB = 1/float(FB)
    M=int(Fs/FB)
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
    ast = zeros(len(tt))       # Initialize a_s(t)
    ix = array(around(Fs*arange(0,N)/float(FB)),int) # Symbol center indexes
    ast[ix-int(ixL)] = Fs*an   # delta_n -> delta(t) conversion
    # ***** Set up PAM pulse p(t) *****
    # Set left/right limits for p(t)
    if (ptype=='rect' or ptype=='tri'):
        kL=-0.5; kR=-kL
    elif (ptype=='sinc'):
        kL=-k; kR=-kL
    else:
        kL = -1.0; kR = -kL    # Default left/right limits
    ixpL = ceil(Fs*kL/float(FB))   # Left index for p(t) time axis
    ixpR = ceil(Fs*kR/float(FB))   # Right index for p(t) time axis
    ttp = arange(ixpL,ixpR)/float(Fs)  # Time axis for p(t)
    pt = zeros(len(ttp))       # Initialize pulse p(t)
    if (ptype=='rect' or ptype=='tri'):        # Rectangular p(t)
        ix = where(logical_and(ttp>=kL/float(FB), ttp<kR/float(FB)))[0]
        pt[ix] = ones(len(ix))
        st = convolve(ast,pt)/float(Fs)  # s(t) = a_s(t)*p(t)
        st = st[int(-ixpL):int(ixR-ixL-ixpL)]  # Trim after convolution
    elif (ptype=='sinc'):
        ast=an
        for i in range(0,M-1):
            ast = vstack([ast,zeros(len(an))])
        ast = ast.flatten('F')
        pt=np.sinc(FB*ttp)
        pt = pt*kaiser(len(pt),beta) # Pulse p(t), Kaiser windowe
        st = convolve(ast,pt,"same") # s(t) = a_s(t)*p(t)
    else:
        print("ptype '%s' is not recognized" % ptype)

    return ecen.sigWave(st, Fs, t0)  # Return waveform from sigWave class

def pam11(sig_an, Fs, ptype, pparms=[], plotparms=[]):
    """
    Pulse amplitude modulation: a_n -> s(t), -TB/2<=t<(N-1/2)*TB,
    V1.1 for ’man’, ’rcf’, ’rect’, ’sinc’, and ’tri’ pulse types.
    >>>>> sig_st = pam11(sig_an, Fs, ptype, pparms) <<<<<
    where  sig_an: sequence from class sigSequ
        sig_an.signal():  N-symbol DT input sequence a_n, 0 <= n < N
        sig_an.get_FB():  Baud rate of a_n, TB=1/FB
        Fs:    sampling rate of s(t)
        ptype: pulse type from list
        (’man’,’rcf’,’rect’,’sinc’,’tri’)
        pparms not used for ’man’,’rect’,’tri’
        pparms = [k, alpha] for ’rcf’
        pparms = [k, beta]  for ’sinc’
        k:     "tail" truncation parameter for ’rcf’,’sinc’
        (truncates p(t) to -k*TB <= t < k*TB)
        alpha: Rolloff parameter for ’rcf’, 0<=alpha<=1
        beta:  Kaiser window parameter for ’sinc’
        sig_st: waveform from class sigWave
        sig_st.timeAxis():  time axis for s(t), starts at -TB/2
        sig_st.signal():    CT output signal s(t), -TB/2<=t<(N-1/2)*TB,
        with sampling rate Fs
    """

# ***** Set variables and manage data formatting *****
    an = sig_an.signal()
    N = len(an)                # Number of data symbols
    n0 = sig_an.get_n0()       # Starting index
    FB = sig_an.get_FB()       # Baud rate
    TB = 1/float(FB)

    Fs=Fs
    M=int(Fs/FB)               # Interpolation number
    Sb = int(Fs/float(FB))     # Samples per bit

    ptype = ptype.lower()      # Convert ptype to lowercase

    if(ptype=='tri'):          # type-specific parameters
        Fs=FB
    elif(ptype=='sinc'):
        k=pparms[0]
        beta=pparms[1]
    elif (ptype=='rcf'):
        k=pparms[0]
        alpha=pparms[1]

# ***** Set up time axis *****
    ixL = ceil(-Fs*(n0+0.5)/float(FB))   # Left index for time axis
    ixR = ceil(Fs*(n0+N-0.5)/float(FB))  # Right index for time axis
    tt = arange(ixL,ixR)/float(Fs)  # Time axis for s(t)
    t0 = tt[0]                 # Start time for s(t)
# ***** Conversion from DT a_n to CT a_s(t) *****
    ast = zeros(len(tt))       # Initialize a_s(t)
    ix = array(around(Fs*arange(0,N)/float(FB)),int) # Symbol center indexes
    ast[ix-int(ixL)] = Fs*an   # delta_n -> delta(t) conversion
# ***** Set up PAM pulse p(t) *****
    # Set left/right limits for p(t)
    if (ptype=='rect' or ptype=='tri' or ptype=='man'):
        kL=-0.5; kR=-kL
    elif (ptype=='sinc' or ptype=='rcf'):
        kL=-k; kR=-kL
    else:
        kL = -1.0; kR = -kL    # Default left/right limits
    ixpL = ceil(Fs*kL/float(FB))   # Left index for p(t) time axis
    ixpR = ceil(Fs*kR/float(FB))   # Right index for p(t) time axis
    ttp = arange(ixpL,ixpR)/float(Fs)  # Time axis for p(t)
    pt = zeros(len(ttp))       # Initialize pulse p(t)
    if (ptype=='rect' or ptype=='tri' or ptype=='man'):        # Rectangular p(t)
        ix = where(logical_and(ttp>=kL/float(FB), ttp<kR/float(FB)))[0]
        if(ptype=='man'):
            pt[ix] = concatenate([-1*ones(int(len(ix)/2)),[0],ones(len(ix)-int(len(ix)/2))])
        else:
            pt[ix] = ones(len(ix))
        st = convolve(ast,pt)/float(Fs)  # s(t) = a_s(t)*p(t)
        st = st[int(-ixpL):int(ixR-ixL-ixpL)]  # Trim after convolution
    elif (ptype=='sinc'):
        ast=an
        for i in range(0,M-1):
            ast = vstack([ast,zeros(len(an))])
        ast = ast.flatten('F')
        pt=np.sinc(FB*ttp)
        pt = pt*kaiser(len(pt),beta) # Pulse p(t), Kaiser windowe
        st = convolve(ast,pt,"same") # s(t) = a_s(t)*p(t)
    elif (ptype=='rcf'):
        ast=an
        for i in range(0,M-1):
            ast = vstack([ast,zeros(len(an))])
        ast = ast.flatten('F')
        pt = []
        for t in ttp:
            rcft_num = sin(pi*t/float(TB))*cos(pi*alpha*t/float(TB))
            rcft_den = (pi*t/float(TB))*(1-pow(2*alpha*t/float(TB),2))
            rcft = divide(rcft_num,float(rcft_den))
            if (rcft_den == 0.0):
                rcft=1
            pt = concatenate([pt,[rcft]])
        st = convolve(ast,pt,"same")#/float(Fs)  # s(t) = a_s(t)*p(t)
    else:
        print("ptype '%s' is not recognized" % ptype)
        return

    if(ptype=='rect'):
        longptype='Rectangular'
    elif(ptype=='tri'):
        longptype='Tritangular'
    elif(ptype=='sinc'):
        longptype='Sinc'
    elif(ptype=='man'):
        longptype='Manchester'
    elif(ptype=='rcf'):
        longptype='RCf'

    if(len(ttp)!=len(pt)):
        ttp=quicktt(st,Fs)
    quickplot(ttp,pt,'-b',[],[],'',longptype+' Interpolation Pulse','Time','Magnitude')

    if(len(ttp)!=len(st)):
        ttp=quicktt(st,Fs)
    if (ptype=='rect' or ptype=='tri' or ptype=='man'):
        ttan = ttp[int(Sb/2)::Sb]
    elif (ptype=='sinc' or ptype=='rcf'):
        ttan = ttp[0::Sb]


    quickplot(ttp,st,'-b',ttan,an,'or','Interpolated Data using a '+longptype+' pulse','Time','p(t)',plotparms)

    return ecen.sigWave(st, Fs, t0)  # Return waveform from sigWave class
