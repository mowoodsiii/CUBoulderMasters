from pylab import *
import ecen4652 as ecen
import quick
import filtfun

def amxmtr(sig_mt, xtype, fcparms, fmparms=[], fBparms=[]):
    """
    Amplitude Modulation Transmitter for suppressed ('sc')
    and transmitted ('tc') carrier AM signals
    >>>>> sig_xt = amxmtr(sig_mt, xtype, fcparms, fmparms, fBparms) <<<<<
    where
        sig_xt: waveform from class sigWave
            sig_xt.signal(): transmitted AM signal
            sig_xt.timeAxis(): time axis for x(t)
        sig_mt: waveform from class sigWave
            sig_mt.signal(): modulating (wideband) message signal
            sig_mt.timeAxis(): time axis for m(t)
        xtype: 'sc' or 'tc' (suppressed or transmitted carrier)
        fcparms = [fc, thetac] for 'sc'
        fcparms = [fc, thetac, alfa] for 'tc'
            fc: carrier frequency
            thetac: carrier phase in deg (0: cos, -90: sin)
            alfa: modulation index 0 <= alfa <= 1
        fmparms = [fm, km, alfam] LPF at fm parameters, no LPF at fm if fmparms = []
            fm: highest message frequency
            km: LPF h(t) truncation to |t| <= km/(2*fm)
            alfam: LPF at fm frequency rolloff parameter, linear rolloff over range 2*alfam*fm
        fBparms = [fBW, fcB, kB, alfaB] BPF at fcB parameters no BPF if fBparms = []
            fBW: -6 dB BW of BPF
            fcB: center freq of BPF
            kB: BPF h(t) truncation to |t| <= kB/fBW
            alfaB: BPF frequency rolloff parameter, linear rolloff over range alfaB*fBW
    """
    if xtype=='sc':
        if len(fcparms)==3:
            [fc,thetac,Ac] = fcparms
        elif len(fcparms)==2:
            [fc,thetac] = fcparms
            Ac=1
        else:
            print('Inapprorpriate fcparms for SC type')
            return
    elif xtype=='tc':
        if len(fcparms)==4:
            [fc,thetac,alfa,Ac] = fcparms
        elif len(fcparms)==3:
            [fc,thetac,alfa] = fcparms
            Ac=1;
        else:
            print('Inapprorpriate fcparms for TC type')
            return
    else:
        print('xtype "',xtype,'" not supported!' )
        return

    if len(fmparms)==3: # Perform LPF
        [fm,km,alfam] = fmparms
        [sig_mt,order] = filtfun.trapfilt1( sig_mt, [fm], km, alfam)
    elif len(fmparms)!=0:
        print('Improper LPF fparms!')

    # Generate AM signal
    tt = sig_mt.timeAxis()
    sig_xt = sig_mt.copy()
    if xtype=='sc': # section 1.1
        sig_xt.sig = Ac * sig_mt.signal() * cos(2*pi*fc*tt+thetac)
    elif xtype=='tc': # section 1.5
        sig_xt.sig = (Ac * cos(2*pi*fc*tt+thetac)) + (Ac * sig_mt.signal() * alfa * cos(2*pi*fc*tt+thetac))

    if len(fBparms)==4: # Perform BPF
        [fBW,fcB,kB,alfaB] = fBparms
        [sig_xt,order] = filtfun.trapfilt1( sig_xt, [fBW,fcB], kB, alfaB)
    elif len(fBparms)!=0:
        print('Improper BPF fparms!')

    return sig_xt

def amrcvr(sig_rt, rtype, fcparms, fmparms=[], fBparms=[], dcblock=False):
    """
    Amplitude Modulation Receiver for coherent ('coh') reception,
    or absolute value ('abs'), or squaring ('sqr') demodulation,
    or I-Q envelope ('iqabs') detection, or I-Q phase ('iqangle')
    detection.
    >>>>> sig_mthat = amrcvr(sig_rt, rtype, fcparms, fmparms,
    fBparms, dcblock) <<<<<
    where
        sig_mthat: waveform from class sigWave
            sig_mthat.signal(): demodulated message signal
            sig_mthat.timeAxis(): time axis mhat(t)
        sig_rt: waveform from class sigWave
            sig_rt.signal(): received AM signal
            sig_rt.timeAxis(): time axis for r(t)
        rtype: Receiver type from list
            'abs' (absolute value envelope detector; pg12 of Lab08),
            'coh' (coherent; pg6 of Lab08),
            'iqangle' (I-Q rcvr, angle or phase),
            'iqabs' (I-Q rcvr, absolute value or envelope),
            'sqr' (squaring envelope detector; pg11 of Lab08)
        fcparms = [fc, thetac]
            fc: carrier frequency
            thetac: carrier phase in deg (0: cos, -90: sin)
        fmparms = [fm, km, alfam] LPF at fm parameters; no LPF at fm if fmparms = []
            fm: highest message frequency
            km: LPF h(t) truncation to |t| <= km/(2*fm)
            alfam: LPF at fm frequency rolloff parameter, linear rolloff over range 2*alfam*fm
        fBparms = [fBW, fcB, kB, alfaB] BPF at fcB parameters; no BPF if fBparms = []
            fBW: -6 dB BW of BPF
            fcB: center freq of BPF
            kB: BPF h(t) truncation to |t| <= kB/fBW
            alfaB: BPF frequency rolloff parameter, linear rolloff over range alfaB*fBW
        dcblock: remove dc component from mthat if true
    """
    tt = sig_rt.timeAxis()

    if len(fcparms)==3:
        [fc,thetac,Ac] = fcparms
    elif len(fcparms)==2:
        [fc,thetac] = fcparms
        Ac=1
    else:
        print('Inapprorpriate number of fcparms')
        return
    if (thetac>2*pi) or (thetac<-2*pi):
        print("WARNING: The angle for thetac is larger than usual (",thetac,").\n         Be sure that thetac is given in radians")

    rtype = rtype.lower()
    if rtype=='abs':
        print('Absolute Value Envelope Detector')
    elif rtype=='coh':
        print('Coherent')
    elif rtype=='iqangle':
        print('I-Q Angle')
    elif rtype=='iqabs':
        print('I-Q Absolute Value')
    elif rtype=='sqr':
        print('Squaring Envelope Detector')
    else:
        print('Unsupported rtype: ', rtype)
        return

    if len(fBparms)==4:
        [fBW,fcB,kB,alfaB] = fBparms
        [sig_rt,order] = filtfun.trapfilt1( sig_rt, [fBW,fcB], kB, alfaB)
    elif len(fBparms)!=0:
        print('Inappropriate number of arguments for fBparms')
        return


    sig_vt=sig_rt.copy()
    if rtype=='abs':
        sig_vt.sig = abs(sig_rt.signal())
    elif rtype=='sqr':
        sig_vt.sig = sig_rt.signal()**2
    elif rtype=='coh':
        sig_vt.sig = sig_rt.signal()*2*Ac*cos(2*pi*fc*tt+thetac)
    elif rtype=='iqangle':
        sig_vit=sig_vt
        sig_vqt=sig_vt.copy()
        sig_vit.sig=sig_rt.signal()*(2*cos(2*pi*fc*tt))
        sig_vqt.sig=sig_rt.signal()*(-2*sin(2*pi*fc*tt))
    elif rtype=='iqabs':
        sig_vit=sig_vt
        sig_vqt=sig_vt.copy()
        sig_vit.sig=sig_rt.signal()*(2*cos(2*pi*fc*tt))
        sig_vqt.sig=sig_rt.signal()*(-2*sin(2*pi*fc*tt))

    if len(fmparms)==3:
        [fm,km,alfam] = fmparms
        if rtype=='abs' or rtype=='coh' or rtype=='sqr':
            [sig_wt,order] = filtfun.trapfilt1( sig_vt, [fm], km, alfam)
        else:
            [sig_wqt,order] = filtfun.trapfilt1( sig_vit, [fm], km, alfam)
            [sig_wit,order] = filtfun.trapfilt1( sig_vqt, [fm], km, alfam)
    elif len(fmparms)!=0:
        print('Inappropriate number of arguments for fmparms')
        return
    else:
        sig_wt=sig_vt.copy()

    # Reconstruction (if anything)
    if rtype=='abs':
        sig_mhat = sig_wt.copy()
    elif rtype=='sqr':
        sig_mhat = sig_wt.copy()
        sig_mhat.sig = sqrt(sig_wt.signal())
    elif rtype=='coh':
        sig_mhat = sig_wt.copy()
    elif rtype=='iqangle':
        sig_mhat = atan2(sig_wqt.signal(),sig_wit.signal())
    elif rtype=='iqabs':
        sig_mhat = sqrt(sig_wqt.signal()**2+sig_wit.signal()**2)

    if dcblock==True:
        sig_mhat.sig = sig_mhat.signal() - mean(sig_mhat.signal()) # Block DC

    return(sig_mhat)


def qamxmtr(sig_mt, fcparms, fmparms=[]):
    """
    Quadrature Amplitude Modulation (QAM) Transmitter with
    complex-valued input/output signals
    >>>>> sig_xt = qamxmtr(sig_mt, fcparms, fmparms) <<<<<
    where
        sig_xt: waveform from class sigWave
            sig_xt.signal(): complex-valued QAM signal
            sig_xt.timeAxis(): time axis for x(t)
        sig_mt: waveform from class sigWave
            sig_mt.signal(): complex-valued (wideband) message signal
            sig_mt.timeAxis(): time axis for m(t)
        fcparms = [fc, thetaci, thetacq]
            fc: carrier frequency
            thetaci: in-phase (cos) carrier phase in deg
            thetacq: quadrature (sin) carrier phase in deg
        fmparms = [fm, km, alfam] for LPF at fm parameters no LPF/BPF at fm if fmparms = []
            fm: highest message frequency (-6dB)
            km: h(t) is truncated to |t| <= km/(2*fm)
            alfam: frequency rolloff parameter, linear rolloff over range (1-alfam)*fm <= |f| <= (1+alfam)*fm
    """


def qamrcvr(sig_rt, fcparms, fmparms=[]):
    """
    Quadrature Amplitude Modulation (QAM) Receiver with
    complex-valued input/output signals
    >>>>> sig_mthat = qamrcvr(sig_rt, fcparms, fmparms) <<<<<
    where
        sig_mthat: waveform from class sigWave
            sig_mthat.signal(): complex-valued demodulated message signal
            sig_mthat.timeAxis(): time axis for mhat(t)
        sig_rt: waveform from class sigWave
            sig_rt.signal(): received QAM signal (real- or complex-valued)
            sig_rt.timeAxis(): time axis for r(t)
        fcparms = [fc, thetaci, thetacq]
            fc: carrier frequency
            thetaci: in-phase (cos) carrier phase in deg
            thetacq: quadrature (sin) carrier phase in deg
        fmparms = [fm, km, alfam] for LPF at fm parameters no LPF at fm if fmparms = []
            fm: highest message frequency (-6 dB)
            km: h(t) is truncated to |t| <= km/(2*fm)
            alfam: frequency rolloff parameter, linear rolloff over range (1-alfam)*fm <= |f| <= (1+alfam)*fm
    """
