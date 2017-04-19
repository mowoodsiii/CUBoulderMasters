# File: keyfun.py
# Functions for amplitude/frequency/phase shift keying
# ASK, FSK, PSK and hybrid APSK

from pylab import *
import ecen4652 as ecen
import pamfun
import filtfun

def askxmtr(sig_an,Fs,ptype,pparms,xtype,fcparms):
    """
    Amplitude Shift Keying (ASK) Transmitter for
    Coherent ('coh') and Non-coherent ('noncoh') ASK Signals
    >>>>> sig_xt,sig_st = askxmtr(sig_an,Fs,ptype,pparms,xtype,fcparms) <<<<<
    where:
        *** OUTPUTS ***
        sig_xt: waveform from class sigWave
        sig_xt.signal(): transmitted ASK signal, sampling rate Fs
            x(t) = s(t)*cos(2*pi*fc*t+(pi/180)*thetac)
            sig_xt.timeAxis(): time axis for x(t), starts at t=-TB/2
        sig_st: waveform from class sigWave
            sig_st.signal(): baseband PAM signal s(t) for 'coh'
            sig_st.signal(): st = sit + 1j*sqt for 'noncoh'
                sit: PAM signal of an*cos(pi/180*thetacn)
                sqt: PAM signal of an*sin(pi/180*thetacn)

        *** INPUTS ***
        sig_an: sequence from class sigSequ
            sig_an.signal() = [an]                for {'coh'}
            sig_an.signal() = [[an],[thetacn]]    for {'noncoh'}
                an: N-symbol DT input sequence a_n, 0<=n<N
                thetacn: N-symbol DT sequence theta_c[n] in degrees, used instead of thetac for {'noncoh'} ASK
                sig_an.get_FB(): baud rate of a_n (and theta_c[n]), TB=1/FB
        Fs: sampling rate of x(t), s(t)
        ptype: pulse type from list ['man','rcf','rect','rrcf','sinc','tri']
            pparms = [] for {'man','rect','tri'}
            pparms = [k, alpha] for {'rcf','rrcf'}
            pparms = [k, beta] for {'sinc'}
                k: "tail" truncation parameter for {'rcf','rrcf','sinc'} (truncates at -k*TB and k*TB)
                alpha: Rolloff parameter for {'rcf','rrcf'}, 0<=alpha<=1
                beta: Kaiser window parameter for {'sinc'}
        fcparms:
            fcparms = [fc, thetac] for {'coh'}
            fcparms = [fc], for {'noncoh'}
                fc: carrier frequency in Hz
                thetac: carrier phase in deg (0: cos, -90: sin)
        xtype: Transmitter type from list {'coh','noncoh'}
    """
    ptype = ptype.lower()
    xtype = xtype.lower()

    tt=sig_an.timeAxis()
    if xtype=='coh':
        print('Coherent Signal')
        an = sig_an.signal()
        thetacn = 0
        fc = fcparms[0]
        thetac = fcparms[1]
        st = pamfun.pam12(an,Fs,ptype,pparms)
    elif xtype=='noncoh':
        print('Non-Coherent Signal')
        an = sig_an.signal()[0]
        thetacn = sig_an.signal()[1]
        fc = fcparms[0]
        thetac = 0
        sit = pamfun.pam12(multiply(an,cos(thetacn)),Fs,ptype,pparms)
        siq = pamfun.pam12(multiply(an,sin(thetacn)),Fs,ptype,pparms)
        st = sit+1j*sqt
    else:
        print('xtype not supported')
        return

    if (thetac>2*pi) or (thetac<-2*pi) or (max(thetacn)>2*pi):
        print("WARNING: The angle for thetac or thetacn is larger than usual.\n         Be sure that thetac is given in radians")

    xt = st*cos(2*pi*fc*tt+thetac)

    return(ecen.sigWave(xt,Fs,sig_an.get_t0),ecen.sigWave(st,Fs,sig_an.get_t0))



def askrcvr(sig_rt,rtype,fcparms,FBparms,ptype,pparms):
    """
        Amplitude Shift Keying (ASK) Receiver for
        Coherent ('coh') and Non-coherent ('noncoh') ASK Signals
        >>>>> sig_bn,sig_bt,sig_wt,ixn = askrcvr(sig_rt,rtype,fcparms,FBparms,ptype,pparms) <<<<<
        where:
            *** OUTPUTS ***
            sig_bn: sequence from class sigSequ
                sig_bn.signal(): received DT sequence b[n]
                sig_bt: waveform from class sigWave
                sig_bt.signal(): received 'CT' PAM signal b(t)
            sig_wt: waveform from class sigWave
                sig_wt.signal(): wt = wit + 1j*wqt
                wit: in-phase component of b(t)
                wqt: quadrature component of b(t)
            ixn: sampling time indexes for b(t)->b[n], w(t)->w[n]

            *** INPUTS ***
            sig_rt: waveform from class sigWave
                sig_rt.signal(): received (noisy) ASK signal r(t)
                sig_rt.timeAxis(): time axis for r(t)
            rtype: receiver type from list ['coh','noncoh']
            fcparms:
                fcparms = [fc, thetac] for {'coh'}
                fcparms = [fc] for {'noncoh'}
                    fc: carrier frequency in Hz
                    thetac: carrier phase in deg (0: cos, -90: sin)
            FBparms:
                FBparms = [FB, dly]
                    FB: baud rate of PAM signal, TB=1/FB
                    dly: sampling delay for b(t)->b[n], fraction of TB sampling times are t=n*TB+t0 where t0=dly*TB
            ptype: pulse type from list ['man','rcf','rect','rrcf','sinc','tri']
            pparms:
                pparms = [] for 'man','rect','tri'
                pparms = [k, alpha] for {'rcf','rrcf'}
                pparms = [k, beta] for {'sinc'}
                    k: "tail" truncation parameter for {'rcf','rrcf','sinc'} (truncates at -k*TB and k*TB)
                    alpha: Rolloff parameter for {'rcf','rrcf'}, 0<=alpha<=1
                    beta: Kaiser window parameter for {'sinc'}
    """

def fskxmtr(M,sig_dn,Fs,ptype,pparms,xtype,fcparms):
    """
        M-ary Frequency Shift Keying (FSK) Transmitter for
        Choherent ('coh'), Non-coherent ('noncoh'), and
        Continuous Phase ('cpfsk') FSK Signals
        >>>>> sig_xt = fskxmtr(M,sig_dn,Fs,ptype,pparms,xtype,fcparms) <<<<<
        where:
            *** OUTPUTS ***
            sig_xt: waveform from class sigWave
                sig_xt.signal(): transmitted FSK signal, sampling rate Fs
                sig_xt.timeAxis(): time axis for x(t), starts at t=-TB/2

            *** INPUTS ***
            M: number of distinct symbol values in d[n]
            xtype: Transmitter type from set {'coh','noncoh','cpfsk'}
            sig_dn: sequence from class sigSequ
                sig_dn.signal() = [dn] for ['coh','cpfsk']
                sig_dn.signal() = [[dn],[thetacn]] for ['noncoh']
                    dn: M-ary (0,1,..,M-1) N-symbol DT input sequence d_n
                    thetacn: N-symbol DT sequence theta_c[n] in degrees, used instead of thetac0..thetacM-1 for {'noncoh'} FSK
                sig_dn.get_FB(): baud rate of d_n (and theta_c[n]), TB=1/FB
            Fs: sampling rate of x(t)
            ptype: pulse type from set {'man','rcf','rect','rrcf','sinc','tri'}
            pparms:
                pparms = [] for {'man','rect','tri'}
                pparms = [k alpha] for {'rcf','rrcf'}
                pparms = [k beta] for {'sinc'}
                    k: "tail" truncation parameter for {'rcf','rrcf','sinc'} (truncates p(t) to -k*TB <= t < k*TB)
                    alpha: Rolloff parameter for {'rcf','rrcf'}, 0<=alpha<=1
                    beta: Kaiser window parameter for {'sinc'}
            fcparms:
                fcparms = [[fc0,fc1,...,fcM-1],[thetac0,thetac1,...,thetacM-1]] for {'coh'}
                fcparms = [fc0,fc1,...,fcM-1] for {'noncoh'}
                fcparms = [fc, deltaf] for {'cpfsk'}
                    fc0,fc1,...,fcM-1: FSK (carrier) frequencies for {'coh','noncoh'}
                    thetac0,thetac1,...,thetacM-1: FSK (carrier) phases in deg (0: cos, -90: sin) for {'coh'}
                    fc: carrier frequency for {'cpfsk'}
                    deltaf: frequency spacing for {'cpfsk'} for dn=0 -> fc, dn=1 -> fc+deltaf, dn=2 -> fc+2*deltaf, etc
    """

def fskrcvr(M,tt,rt,rtype,fcparms,FBparms,ptype,pparms):
    """
        M-ary Frequency Shift Keying (FSK) Receiver for
        Coherent ('coh'), Non-coherent ('noncoh'), and
        Phase Detector ('phdet') FSK Reception
        >>>>> sig_bn,sig_wt,ixn =
        fskrcvr(M,sig_rt,rtype,fcparms,FBparms,ptype,pparms) <<<<<
        where:
            *** OUTPUTS ***
            sig_bn: sequence from class sigSequ
                sig_bn.signal(): received DT sequence b[n]
                sig_wt: waveform from class sigWave
                sig_wt.signal(): wt = [[w0it+1j*w0qt],[w1it+1j*w1qt],..., [wM-1it+1j*wM-1qt]]
                    wmit: m-th in-phase matched filter output
                    wmqt: m-th quadrature matched filter output
                    ixn: sampling time indexes for b(t)->b[n], w(t)->w[n]

            *** INPUTS ***
            M: number of distinct FSK frequencies
            sig_rt: waveform from class sigwave
                sig_rt.signal(): received (noisy) FSK signal r(t)
                sig_rt.timeAxis(): time axis for r(t)
            rtype: receiver type from list {'coh','noncoh','phdet'}
            fcparms:
                fcparms = [[fc0,fc1,...,fcM-1],[thetac0,thetac1,...,thetacM-1]] for {'coh'}
                fcparms = [fc0,fc1,...,fcM-1] for {'noncoh'}
                fcparms = [fc, deltaf] for {'phdet'}
                    fc0,fc1,...,fcM-1: FSK (carrier) frequencies for {'coh','noncoh'}
                    thetac0,thetac1,...,thetacM-1: FSK (carrier) phases in deg (0: cos, -90: sin) for {'coh'}
                    fc: carrier frequency for {'cpfsk'}
                    deltaf: frequency spacing for {'cpfsk'} for dn=0 -> fc, dn=1 -> fc+deltaf, dn=2 -> fc+2*deltaf, etc
            FBparms = [FB, dly]
                FB: baud rate of PAM signal, TB=1/FB
                dly: sampling delay for wm(t)->wm[n], fraction of TB sampling times are t=n*TB+t0 where t0=dly*TB
            ptype: pulse type from list {'man','rcf','rect','rrcf','sinc','tri'}
            pparms:
                pparms = [] for {'man','rect','tri'}
                pparms = [k, alpha] for {'rcf','rrcf'}
                pparms = [k, beta] for {'sinc'}
                    k: "tail" truncation parameter for {'rcf','rrcf','sinc'} (truncates at -k*TB and k*TB)
                    alpha: Rolloff parameter for {'rcf','rrcf'}, 0<=alpha<=1
                    beta: Kaiser window parameter for {'sinc'}
    """
