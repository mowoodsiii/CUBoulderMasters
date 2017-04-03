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
        fmparms = [fm, km, alfam] LPF at fm parameters no LPF at fm if fmparms = []
        fm: highest message frequency
        km: LPF h(t) truncation to |t| <= km/(2*fm)
        alfam: LPF at fm frequency rolloff parameter, linear rolloff over range 2*alfam*fm
        fBparms = [fBW, fcB, kB, alfaB] BPF at fcB parameters no BPF if fBparms = []
        fBW: -6 dB BW of BPF
        fcB: center freq of BPF
        kB: BPF h(t) truncation to |t| <= kB/fBW
        alfaB: BPF frequency rolloff parameter, linear rolloff over range alfaB*fBW
"""

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
            'abs' (absolute value envelope detector),
            'coh' (coherent),
            'iqangle' (I-Q rcvr, angle or phase),
            'iqabs' (I-Q rcvr, absolute value or envelope),
            'sqr' (squaring envelope detector)
        fcparms = [fc, thetac]
        fc: carrier frequency
        thetac: carrier phase in deg (0: cos, -90: sin)
        fmparms = [fm, km, alfam] LPF at fm parameters no LPF at fm if fmparms = []
        fm: highest message frequency
        km: LPF h(t) truncation to |t| <= km/(2*fm)
        alfam: LPF at fm frequency rolloff parameter, linear rolloff over range 2*alfam*fm
        fBparms = [fBW, fcB, kB, alfaB] BPF at fcB parameters no BPF if fBparms = []
        fBW: -6 dB BW of BPF
        fcB: center freq of BPF
        kB: BPF h(t) truncation to |t| <= kB/fBW
        alfaB: BPF frequency rolloff parameter, linear rolloff over range alfaB*fBW
        dcblock: remove dc component from mthat if true
"""

def qamxmtr(sig_mt, fcparms, fmparms=[]):
"""
    Quadrature Amplitude Modulation (QAM) Transmitter with
    complex-valued input/output signals
    >>>>> sig_xt = qamxmtr(sig_mt, fcparms, fmparms) <<<<<
    where
        sig_xt: waveform from class sigWave
        sig_xt.signal(): complex-valued QAM signal
        sig_xt.timeAxis(): time axis for x(t)
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
