# File: showfun.py
# "show" functions like showft, showpsd, etc
from pylab import *
def showft(sig_xt, ff_lim):
    """
    Plot (DFT/FFT approximation to) Fourier transform of
    waveform x(t). Displays magnitude |X(f)| either linear
    and absolute or normalized (wrt to maximum value) in dB.
    Phase of X(f) is shown in degrees.
    >>>>> showft(sig_xt, ff_lim) <<<<<
    where  sig_xt: waveform from class sigWave
        sig_xt.timeAxis(): time axis for x(t)
        sig_xt.signal():   sampled CT signal x(t)
        ff_lim = [f1,f2,llim]
        f1:       lower frequency limit for display
        f2:       upper frequency limit for display
        llim = 0: display |X(f)| linear and absolute
        llim > 0: same as llim = 0 but phase is masked
        (set to zero) for |X(f)| < llim
        llim < 0: display 20*log_{10}(|X(f)|/max(|X(f)|))
        in dB with lower display limit llim dB,
        phase is masked (set to zero) for f
        with magnitude (dB, normalized) < llim
    """
    # ***** Prepare x(t), swap pos/neg parts of time axis *****
    N = sig_xt.Nsamp           # Blocklength of DFT/FFT
    Fs = sig_xt.get_Fs()      # Sampling rate
    tt = sig_xt.timeAxis()    # Get time axis for x(t)
    ixp = where(tt>=0)[0]     # Indexes for t>=0
    ixn = where(tt<0)[0]      # Indexes for t<0
    xt = sig_xt.signal()      # Get x(t)
    xt = hstack((xt[ixp],xt[ixn]))
    # Swap pos/neg time axis parts
    # ***** Compute X(f), make frequency axis *****
    Xf = fft(xt)/float(Fs)    # DFT/FFT of x(t),
    # scaled for X(f) approximation
    ff = Fs*array(arange(N),int64)/float(N)  # Frequency axis
    # ***** Compute |X(f)|, arg[X(f)] *****
    absXf = abs(Xf)           # Magnitude |X(f)|
    argXf = angle(Xf)         # Phase arg[X(f)]
    # ***** Plot magnitude/phase *****
    f1 = figure()
    af11 = f1.add_subplot(211)
    af11.plot(ff,absXf)         # Plot magnitude
    af11.grid()
    af11.set_ylabel('|X(f)|')
    strgt = 'FT Approximation, $F_s=$' + str(Fs) + ' Hz'
    strgt = strgt + ', N=' + str(N)
    strgt = strgt + ', $\Delta_f$={0:3.2f}'.format(Fs/float(N)) + ' Hz'
    af11.set_title(strgt)
    af12 = f1.add_subplot(212)
    af12.plot(ff,180/pi*argXf)  # Plot phase in degrees
    af12.grid()
    af12.set_ylabel('arg[X(f)] [deg]')
    af12.set_xlabel('f [Hz]')
    show()

def showft_plus(sig_xt, ff_lim):
    """
    Plot (DFT/FFT approximation to) Fourier transform of
    waveform x(t). Displays magnitude |X(f)| either linear
    and absolute or normalized (wrt to maximum value) in dB.
    Phase of X(f) is shown in degrees.
    >>>>> showft(sig_xt, ff_lim) <<<<<
    where  sig_xt: waveform from class sigWave
        sig_xt.timeAxis(): time axis for x(t)
        sig_xt.signal():   sampled CT signal x(t)
        ff_lim = [f1,f2,llim]
        f1:       lower frequency limit for display
        f2:       upper frequency limit for display
        llim = 0: display |X(f)| linear and absolute
        llim > 0: same as llim = 0 but phase is masked
        (set to zero) for |X(f)| < llim
        llim < 0: display 20*log_{10}(|X(f)|/max(|X(f)|))
        in dB with lower display limit llim dB,
        phase is masked (set to zero) for f
        with magnitude (dB, normalized) < llim
    """
    # ***** Prepare x(t), swap pos/neg parts of time axis *****
    N = sig_xt.Nsamp           # Blocklength of DFT/FFT
    Fs = sig_xt.get_Fs()      # Sampling rate
    tt = sig_xt.timeAxis()    # Get time axis for x(t)
    ixp = where(tt>=0)[0]     # Indexes for t>=0
    ixn = where(tt<0)[0]      # Indexes for t<0
    xt = sig_xt.signal()      # Get x(t)
    xt = hstack((xt[ixp],xt[ixn]))
    # Swap pos/neg time axis parts
    # ***** Compute X(f), make frequency axis *****
    Xf = fft(xt)/float(Fs)    # DFT/FFT of x(t),
    # scaled for X(f) approximation
    ff = (Fs*array(arange(N),int64)/float(N)) # Frequency axis
    # ***** Compute |X(f)|, arg[X(f)] *****
    absXf = abs(Xf)           # Magnitude |X(f)|
    argXf = angle(Xf)         # Phase arg[X(f)]
    # ***** Mirror |X(f)| about 0 (if ff_lim[0]<0) *****
    if ff_lim[0]<0:
        absXf = concatenate([absXf[::-1],absXf])
        argXf = concatenate([argXf[::-1],argXf])
        neg = [-1*i for i in ff]
        ff = concatenate([neg[::-1],ff])
    # ***** Floor values of argXf for points where absXf<llim *****
    if ff_lim[2]>0:
        for i in range(0,len(absXf)):
            if absXf[i] < ff_lim[2]:
                argXf[i] = 0
    # ***** Plot magnitude/phase *****
    f1 = figure()
    af11 = f1.add_subplot(211)
    af11.plot(ff,absXf)         # Plot magnitude
    af11.grid()
    af11.set_ylabel('|X(f)|')
    strgt = 'FT Approximation, $F_s=$' + str(Fs) + ' Hz'
    strgt = strgt + ', N=' + str(N)
    strgt = strgt + ', $\Delta_f$={0:3.2f}'.format(Fs/float(N)) + ' Hz'
    af11.set_title(strgt)
    xlim([ff_lim[0],ff_lim[1]])
    af12 = f1.add_subplot(212)
    af12.plot(ff,(180/pi)*argXf)  # Plot phase in degrees
    af12.grid()
    af12.set_ylabel('arg[X(f)] [deg]')
    af12.set_xlabel('f [Hz]')
    xlim([ff_lim[0],ff_lim[1]])
    show()
