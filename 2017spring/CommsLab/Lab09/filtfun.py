# File: filtfun.py
# Module for filter functions

from pylab import *
from scipy.signal import butter, lfilter
import ecen4652 as ecen
import quick

def trapfilt0(sig_xt, fL, k, alfa):
    """
    Delay compensated FIR LPF/BPF filter with trapezoidal frequency response.
    >>>>> sig_yt, n = trapfilt(sig_xt, fL, k, alfa) <<<<<
    where
        sig_yt: waveform from class sigWave
            sig_yt.signal(): filter output y(t), samp rate Fs
            n: filter order
        sig_xt: waveform from class sigWave
            sig_xt.signal(): filter input x(t), samp rate Fs
            sig_xt.get_Fs(): sampling rate for x(t), y(t)
        fL: LPF cutoff frequency (-6 dB) in Hz
        k: h(t) is truncated to |t| <= k/(2*fL)
        alfa: frequency rolloff parameter, linear rolloff over range (1-alfa)fL <= |f| <= (1+alfa)fL
    """
    xt = sig_xt.signal() # Input signal
    Fs = sig_xt.get_Fs() # Sampling rate
    ixk = round(Fs*k/float(2*fL)) # Tail cutoff index
    tth = arange(-ixk,ixk+1)/float(Fs) # Time axis for h(t)
    n = len(tth)-1 # Filter order
    ht_num = (sin(2*pi*fL*tth)*sin(2*pi*alfa*fL*tth))
    ht_den = (pi*tth*2*pi*alfa*fL*tth)
    nans = where(ht_den==0)
    for i in nans:
        ht_den[i]=1 # ht[i-1]
        ht_num[i]=2*fL # ht[i-1]
    ht = ht_num/ht_den
    titlestr = 'Trapezoidal LPF, $h_L(t)$ Truncated to $|t|<k/(2f_L)$, $f_L$ = '+str(fL)+' Hz, k = '+str(k)+', alpha = '+str(alfa)
    quick.quickplot(tth,ht,'-b',[],[],'',titlestr,'Time (s)','h_L(t)')
    yt = lfilter(ht, 1, hstack((xt, zeros(ixk))))/float(Fs) # Compute filter output y(t)
    yt = yt[ixk:] # Filter delay compensation
    return ecen.sigWave(yt*Fs, Fs, sig_xt.get_t0()), n # Return y(t) and filter order

def trapfilt1(sig_xt, fparms, k, alfa, disp=''):
    """
        Delay compensated FIR LPF/BPF filter with trapezoidal
        frequency response.
        >>>>> sig_yt, n = trapfilt(sig_xt, fparms, k, alfa) <<<<<
        where
            sig_yt: waveform from class sigWave
            sig_yt.signal(): filter output y(t), samp rate Fs
            n: filter order
            sig_xt: waveform from class sigWave
            sig_xt.signal(): filter input x(t), samp rate Fs
            sig_xt.get_Fs(): sampling rate for x(t), y(t)
            fparms = fL for LPF
                fL: LPF cutoff frequency (-6 dB) in Hz
            fparms = [fBW, fc] for BPF
                fBW: BPF -6dB bandwidth in Hz
                fc: BPF center frequency in Hz
            k: h(t) is truncated to
                |t| <= k/(2*fL) for LPF
                |t| <= k/fBW for BPF
            alfa: frequency rolloff parameter, linear rolloff over range
                (1-alfa)fL <= |f| <= (1+alfa)fL for LPF
                (1-alfa)fBW/2 <= |f| <= (1+alfa)fBW/2 for LPF
            disp: Indicate whether or not filter should be plotted (to plot, disp="plot")
    """
    if len(fparms)==1:
        fBW=fparms[0] # fL = fBW when fc=0
        fc=0
        print('Low Pass Filter: fL=', fBW, 'Hz')
    elif len(fparms)==2:
        [fBW,fc]=fparms
        print('Band Pass Filter: fBW=',fBW,'Hz, fc=',fc,'Hz')
    else:
        print('Unsupported number of fparms')
        return
    xt = sig_xt.signal() # Input signal
    Fs = sig_xt.get_Fs() # Sampling rate
    ixk = round(Fs*k/float(2*fBW)) # Tail cutoff index
    tth = arange(-ixk,ixk+1)/float(Fs) # Time axis for h(t)
    n = len(tth)-1 # Filter order
    ht_num = (sin(2*pi*fBW*tth)*sin(2*pi*alfa*fBW*tth))
    ht_den = (pi*tth*2*pi*alfa*fBW*tth)
    nans = where(ht_den==0)
    for i in nans:
        ht_den[i]=1 # ht[i-1]
        ht_num[i]=2*fBW # ht[i-1]
    ht = ht_num/ht_den
    ht = 2*ht*cos(2*pi*fc*tth) # Bandpass shift
    titlestr = 'Trapezoidal LPF, $h_L(t)$ Truncated to $|t|<k/(2f_L)$, $f_L$ = '+str(fBW)+' Hz, k = '+str(k)+', alpha = '+str(alfa)
    if disp=='plot':
        quick.quickplot(tth,ht,'-b',[],[],'',titlestr,'Time (s)','h_L(t)')
    yt = lfilter(ht, 1, hstack((xt, zeros(ixk))))/float(Fs) # Compute filter output y(t)
    yt = yt[ixk:] # Filter delay compensation
    return ecen.sigWave(yt/2, Fs, sig_xt.get_t0()), n # Return y(t) and filter order

def trapfilt_cc(sig_xt, fparms, k, alfa, disp=''):
    """
        Delay compensated FIR LPF/BPF filter with trapezoidal
        frequency response, complex-valued input/output and
        complex-valued filter coefficients.
        >>>>> sig_yt, n = trapfilt_cc(sig_xt, fparms, k, alfa) <<<<<
        where
            sig_yt: waveform from class sigWave
            sig_yt.signal():
            complex filter output y(t), samp rate Fs
            n: filter order
            sig_xt: waveform from class sigWave
            sig_xt.signal(): complex filter input x(t), samp rate Fs
            sig_xt.get_Fs(): sampling rate for x(t), y(t)
            fparms = fL for LPF
                fL: LPF cutoff frequency (-6 dB) in Hz
            fparms = [fBW, fBc] for BPF
                fBW: BPF -6dB bandwidth in Hz
                fBc: BPF center frequency (pos/neg) in Hz
            k: h(t) is truncated to
                |t| <= k/(2*fL) for LPF
                |t| <= k/fBW for BPF
            alfa: frequency rolloff parameter, linear rolloff over range
                (1-alfa)*fL <= |f| <= (1+alfa)*fL for LPF
                (1-alfa)*fBW/2 <= |f| <= (1+alfa)*fBW/2 for BPF
    """
    if len(fparms)==1:
        fBW=fparms[0] # fL = fBW when fc=0
        fc=0
        print('Low Pass Filter: fL=', fBW, 'Hz')
    elif len(fparms)==2:
        [fBW,fc]=fparms
        print('Band Pass Filter: fBW=',fBW,'Hz, fc=',fc,'Hz')
    else:
        print('Unsupported number of fparms')
        return
    xt = sig_xt.signal() # Input signal
    Fs = sig_xt.get_Fs() # Sampling rate
    ixk = round(Fs*k/float(2*fBW)) # Tail cutoff index
    tth = arange(-ixk,ixk+1)/float(Fs) # Time axis for h(t)
    n = len(tth)-1 # Filter order
    ht_num = (sin(2*pi*fBW*tth)*sin(2*pi*alfa*fBW*tth))
    ht_den = (pi*tth*2*pi*alfa*fBW*tth)
    nans = where(ht_den==0)
    for i in nans:
        ht_den[i]=1 # ht[i-1]
        ht_num[i]=2*fBW # ht[i-1]
    ht = ht_num/ht_den
    htbp = 2*ht*exp(2j*pi*fc*tth) # Bandpass shift
    # htbp = 2*ht*cos(2*pi*fc*tth) # Bandpass shift
    titlestr = 'Complex Trapezoidal LPF, $h_L(t)$ Truncated to $|t|<k/(2f_L)$, $f_L$ = '+str(fBW)+' Hz, k = '+str(k)+', alpha = '+str(alfa)
    if disp=='plot':
        quick.quickplot(tth,htbp,'-b',[],[],'',titlestr,'Time (s)','h_L(t)')
    yt = lfilter(htbp, 1, hstack((xt, zeros(ixk)))) # Compute filter output y(t)
    yt = yt[ixk:] # Filter delay compensation
    return ecen.sigWave(yt/2, Fs, sig_xt.get_t0()), n
