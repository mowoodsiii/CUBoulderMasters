# File: showfun.py
# "show" functions like showft, showpsd, etc
from pylab import *
from math import exp, expm1
import quick

def showft(sig_xt, ff_lim, description=""):
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
    [f_low,f_high,llim]=ff_lim
    # Swap pos/neg time axis parts
    # ***** Compute X(f), make frequency axis *****
    Xf = fft(xt)/float(Fs)    # DFT/FFT of x(t),
    # scaled for X(f) approximation
    ff = (Fs*array(arange(N),int64)/float(N)) # Frequency axis
    # ***** Compute |X(f)|, arg[X(f)] *****
    absXf = abs(Xf)           # Magnitude |X(f)|
    argXf = angle(Xf)         # Phase arg[X(f)]
    # ***** Mirror |X(f)| about 0 (if ff_lim[0]<0) *****
    if f_low<0:
        absXf = concatenate([absXf[::-1],absXf])
        neg = [-1*i for i in argXf]
        argXf = concatenate([neg[::-1],argXf])
        neg = [-1*i for i in ff]
        ff = concatenate([neg[::-1],ff])
    # ***** Floor values of argXf for points where absXf<llim *****
    if llim>0:
        for i in range(0,len(absXf)):
            if absXf[i] < llim:
                argXf[i] = 0
    # ***** Convert absXt to dB and floor argXf for points where absXf<llim(dB) *****
    if llim<0:
        absXfmax=amax(absXf)
        for i in range(0,len(absXf)):
            absXf[i] = 20*math.log10(absXf[i]/absXfmax)
            if absXf[i]<llim:
                absXf[i]=llim
                argXf[i]=0
    # ***** Plot magnitude/phase *****
    f1 = figure(figsize=[14,6])
    af11 = f1.add_subplot(211)
    af11.plot(ff,absXf)         # Plot magnitude
    af11.grid()
    str_ylabel='|X(f)|'
    if(llim<0):
        str_ylabel=str_ylabel+' (in dB)'
    af11.set_ylabel(str_ylabel)
    strgt = 'FT Approximation'+description+', $F_s=$' + str(Fs) + ' Hz'
    strgt = strgt + ', N=' + str(N)
    strgt = strgt + ', $\Delta_f$={0:3.2f}'.format(Fs/float(N)) + ' Hz'
    af11.set_title(strgt)
    xlim([ff_lim[0],ff_lim[1]])
    af12 = f1.add_subplot(212)
    af12.plot(ff,(180/pi)*argXf)  # Plot phase in degrees
    af12.grid()
    af12.set_ylabel('arg[X(f)] [deg]')
    af12.set_xlabel('f [Hz]')
    xlim([f_low,f_high])
    show()

def showeye(sig_rt, FB, NTd=50, dispparms=[], plotsize='large'):
    """
    Display eye diagram of digital PAM signal r(t)
    >>>>> showeye(sig_rt, FB, NTd, dispparms) <<<<<
    where  sig_rt: waveform from class sigWave
        sig_rt.signal():  received PAM signal
        r(t)=sum_n a_n*q(t-nTB)
        sig_rt.get_Fs():  sampling rate for r(t)
        FB:  Baud rate of DT sequence a_n, TB = 1/FB
        NTd: Number of traces displayed
        dispparms = [delay, width, ylim1, ylim2]
            delay:  trigger delay (in TB units, e.g., 0.5)
            width:  display width (in TB units, e.g., 3)
            ylim1:  lower display limit, vertical axis
            ylim2:  upper display limit, vertical axis
    """
    if (type(FB)==int) or (type(FB)==float):
        FB=[FB]
    if plotsize=='small':
        plotx=10
        ploty=4
    elif plotsize=='large':
        plotx=15
        ploty=8
    elif type(plotsize)==list:
        plotx=plotsize[0]
        ploty=plotsize[1]

    nplots=len(FB)

    for fb in FB:
        rt = sig_rt.sig       # Get r(t)
        Fs = sig_rt.get_Fs()       # Sampling rate
        t0 = dispparms[0]/float(fb)  # Delay in sec
        tw = dispparms[1]/float(fb)  # Display width in sec
        dws = floor(Fs*tw)         # Display width in samples
        tteye = arange(dws)/float(Fs)  # Time axis for eye
        trix = (around(Fs*(t0+arange(NTd)/float(fb)))).astype(int)
        ix = where(logical_and(trix>=0, trix<=len(rt)-dws))[0]
        trix = trix[ix]            # Trigger indexes within r(t)

        TM = rt[trix[0]:int(trix[0]+dws)]   # First trace
        for i in range(1,NTd):
            TM = vstack((TM, rt[trix[i]:int(trix[i]+dws)]))# Second trace
        title = 'Eye Diagram for '+ sig_rt.signame +' (FB='+str(fb)+'bits/s)'
        quick.quickplot(fb*tteye,TM.T,'-b',[],[],'',title,'t/TB','Data Levels',[],[plotx,ploty])

def showpsd0(sig_xt, ff_lim, N):
    """
    Plot (DFT/FFT approximation to) power spectral density (PSD) of x(t).
    Displays S_x(f) either linear and absolute or normalized in dB.
    >>>>> showpsd(sig_xt, ff_lim, N) <<<<<
    where sig_xt: waveform from class sigWave
        sig_xt.signal(): sampled CT signal x(t)
        sig_xt.get_Fs(): sampling rate of x(t)
        ff_lim = [f1,f2,llim]
        f1: lower frequency limit for display
        f2: upper frequency limit for display
        llim = 0: display S_x(f) linear and absolute
        llim < 0: display 10*log_{10}(S_x(f))/max(S_x(f)) in dB with lower display limit llim dB
        N: blocklength
    """

    # ***** Determine number of blocks, prepare x(t) *****
    xt = sig_xt.signal() # Get x(t)
    Fs = sig_xt.get_Fs() # Sampling rate of x(t)
    N = int(min(N, len(xt))) # N <= length(xt) needed
    NN = int(floor(len(xt)/float(N))) # Number of blocks of length N
    f1 = ff_lim[0]
    f2 = ff_lim[1]
    if(f1 > f2):
        print("ERROR: f1 > f2")
        return
    xt = xt[0:N*NN] # Truncate x(t) to NN blocks
    xNN = reshape(xt,(NN,N)) # NN row vectors of length N
    # ***** Compute DFTs/FFTs, average over NN blocks *****
    Sxf = np.power(abs(fft(xNN)),2.0) # NN FFTs, mag squared
    if NN > 1:
        Sxf = sum(Sxf, axis=0)/float(NN)
    Sxf = Sxf/float(N*Fs) # Correction factor DFT -> PSD
    Sxf = reshape(Sxf,size(Sxf))
    ff = Fs*array(arange(N),int64)/float(N) # Frequency axis
    if f1 < 0: # Negative f1 case
        ixp = where(ff<0.5*Fs)[0] # Indexes of pos frequencies
        ixn = where(ff>=0.5*Fs)[0] # Indexes of neg frequencies
        ff = hstack((ff[ixn]-Fs,ff[ixp])) # New freq axis
        Sxf = hstack((Sxf[ixn],Sxf[ixp])) # Corresponding S_x(f)
    df = Fs/float(N) # Delta_f, freq sample spacing
    # ***** Determine maximum, trim to ff_lim *****
    maxSxf = max(Sxf) # Maximum of S_x(f)
    ixf = where(logical_and(ff>=f1, ff<f2))[0]
    ff = ff[ixf] # Trim to ff_lim specs
    Sxf = Sxf[ixf]
    # ***** Plot PSD *****
    strgt = 'PSD Approximation, $F_s=${:d} Hz'.format(Fs)
    strgt = strgt + ', $\\Delta_f=${:.3g} Hz'.format(df)
    strgt = strgt + ', $NN=${:d}, $N=${:d}'.format(NN, N)
    quick.quickplot(ff,Sxf,'-b',[],[],'',strgt,'f [Hz]','Y AXIS')
    show()

def showpsd1(sig_xt, ff_lim, N, subject=''):
    """
    Plot (DFT/FFT approximation to) power spectral density (PSD) of x(t).
    Displays S_x(f) either linear and absolute or normalized in dB.
    >>>>> showpsd(sig_xt, ff_lim, N) <<<<<
    where sig_xt: waveform from class sigWave
        sig_xt.signal(): sampled CT signal x(t)
        sig_xt.get_Fs(): sampling rate of x(t)
        ff_lim = [f1,f2,llim]
            f1: lower frequency limit for display
            f2: upper frequency limit for display
            llim = 0: display S_x(f) linear and absolute
            llim < 0: display 10*log_{10}(S_x(f))/max(S_x(f)) in dB with lower display limit llim dB
        N: blocklength
    """

    # ***** Determine number of blocks, prepare x(t) *****
    xt = sig_xt.signal() # Get x(t)
    Fs = sig_xt.get_Fs() # Sampling rate of x(t)
    N = int(min(N, len(xt))) # blocklength; N <= length(xt) needed
    NN = int(floor(len(xt)/float(N))) # Number of blocks of length N

    f1 = ff_lim[0]
    f2 = ff_lim[1]
    llim = ff_lim[2]
    if(f1 > f2):
        print("ERROR: f1 > f2")
        return
    xt = xt[0:N*NN] # Truncate x(t) to NN blocks
    xNN = reshape(xt,(NN,N)) # NN row vectors of length N

    # ***** Compute DFTs/FFTs, average over NN blocks *****
    Sxf = np.power(abs(fft(xNN)),2.0) # NN FFTs, mag squared
    if NN > 1:
        Sxf = sum(Sxf, axis=0)/float(NN)
    Sxf = Sxf/float(N*Fs) # Correction factor DFT -> PSD
    Sxf = reshape(Sxf,size(Sxf))
    ff = Fs*array(arange(N),int64)/float(N) # Frequency axis
    if f1 < 0: # Negative f1 case
        ixp = where(ff<0.5*Fs)[0] # Indexes of pos frequencies
        ixn = where(ff>=0.5*Fs)[0] # Indexes of neg frequencies
        ff = hstack((ff[ixn]-Fs,ff[ixp])) # New freq axis
        Sxf = hstack((Sxf[ixn],Sxf[ixp])) # Corresponding S_x(f)
    df = Fs/float(N) # Delta_f, freq sample spacing

    # ***** Determine the total power *****
    P_total = sum(Sxf)*df

    # ***** Determine maximum, trim to ff_lim *****
    maxSxf = max(Sxf) # Maximum of S_x(f)
    if ((f1!=inf) and (f1!=-inf) and (f2!=inf) and (f1!=-inf)):
        ixf = where(logical_and(ff>=f1, ff<f2))[0]
        ff = ff[ixf] # Trim to ff_lim specs
        Sxf = Sxf[ixf]

    # ***** Determine the power over the ff_lim interval *****
    P_ff_lim = sum(Sxf)*df

    # ***** Convert to normalized dB based on llim
    if(llim<0):
        Sxf = 10*log10(Sxf/float(maxSxf))
        strgy = "$S_x(f)/|S_x(f)| [dB]$"
        Sxf[Sxf<llim]=llim
    else:
        Sxf = abs(Sxf)
        strgy = "$S_x(f)$"

    # ***** Plot PSD *****
    strgt = 'PSD Approximation'
    if(subject!=''):
        strgt = strgt + ' of '+subject
    strgt = strgt + ':\n$F_s=${:d} Hz'.format(Fs)
    strgt = strgt + ',    $\\Delta_f=${:.3g} Hz'.format(df)
    strgt = strgt + ',    $NN=${:d},    $N=${:d}'.format(NN, N)
    strgt = strgt + '\n' + '$P(-\infty,\infty)$={:.3g}W'.format(P_total)

    strgt = strgt + ',          $P({:.1g}Hz,{:.1g}Hz)$ = {:.3g}W = {:.3g}% of $P(-\infty,\infty)$'.format(f1,f2,P_ff_lim,100*P_ff_lim/float(P_total))
    quick.quickplot(ff,Sxf,'-b',[],[],'',strgt,'f [Hz]','$S_x(f)$')
    show()
