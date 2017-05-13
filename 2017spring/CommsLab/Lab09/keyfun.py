# File: keyfun.py
# Functions for amplitude/frequency/phase shift keying
# ASK, FSK, PSK and hybrid APSK

from pylab import *
import ecen4652 as ecen
import pamfun
import filtfun
import quick

def askxmtr(seq_an,Fs,ptype,pparms,xtype,fcparms,plotparms=['noplot']):
    """
    Amplitude Shift Keying (ASK) Transmitter for
    Coherent ('coh') and Non-coherent ('noncoh') ASK Signals
    >>>>> sig_xt,sig_st = askxmtr(seq_an,Fs,ptype,pparms,xtype,fcparms) <<<<<
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
        seq_an: sequence from class sigSequ
            seq_an.signal() = [an]                for {'coh'}
            seq_an.signal() = [[an],[thetacn]]    for {'noncoh'}
                an: N-symbol DT input sequence a_n, 0<=n<N
                thetacn: N-symbol DT sequence theta_c[n] in degrees, used instead of thetac for {'noncoh'} ASK
                seq_an.get_FB(): baud rate of a_n (and theta_c[n]), TB=1/FB
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

    Ac=1
    if xtype=='coh':
        print('XMTR: Coherent Signal')
        an = seq_an.signal()
        thetacn = zeros(len(an))
        [fc,thetac] = fcparms
        st = pamfun.pam12(seq_an,Fs,ptype,pparms,plotparms)
        tt=quick.quicktt(st.signal(),Fs)
        xt = Ac*st.signal()*cos(2*pi*fc*tt+thetac)
    elif xtype=='noncoh':
        print('XMTR: Non-Coherent Signal')
        an = seq_an[0].signal()
        thetacn = seq_an[1]
        if thetacn=='rand':
            thetacn=(pi/2.0)*rand(len(an))
        seq_an_sit = seq_an[0].copy()
        seq_an_sqt = seq_an[0].copy()
        seq_an_sit.sig = multiply(an,cos(thetacn))
        seq_an_sqt.sig = multiply(an,sin(thetacn))
        fc = fcparms[0]
        thetac = 0
        sit = pamfun.pam12(seq_an_sit,Fs,ptype,pparms,plotparms)
        sqt = pamfun.pam12(seq_an_sqt,Fs,ptype,pparms,plotparms)
        st = sit.copy()
        st.sig = sit.signal() + 1j*(sqt.signal())
        tt=quick.quicktt(sit.signal(),Fs)
        xt=multiply(sit.signal(),cos(2*pi*fc*tt))+multiply(sqt.signal(),-sin(2*pi*fc*tt))
    else:
        print('xtype not supported')
        return

    return(ecen.sigWave(xt,Fs,0),ecen.sigWave(st.signal(),Fs,0))



def askrcvr(sig_rt,rtype,fcparms,FBparms,ptype,pparms):
    """
        Amplitude Shift Keying (ASK) Receiver for
        Coherent ('coh') and Non-coherent ('noncoh') ASK Signals
        >>>>> seq_bn,sig_bt,sig_wt,ixn = askrcvr(sig_rt,rtype,fcparms,FBparms,ptype,pparms) <<<<<
        where:
            *** OUTPUTS ***
            seq_bn: sequence from class sigSequ
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
    rt = sig_rt.signal() # pg5 of lab09.pdf
    tt = sig_rt.timeAxis()

    ptype = ptype.lower()
    rtype = rtype.lower()

    if rtype=='coh':
        print('RCVR: Coherent Signal')
        [fc,thetac] = fcparms
    elif rtype=='noncoh':
        print('RCVR: Non-Coherent Signal')
        fc = fcparms
        thetac=0

    [FB,dly] = FBparms

    if (ptype=='rcf') or (ptype=='rrcf'):
        [k,alpha] = pparms
    elif (ptype=='sinc'):
        [k,beta] = pparms

    sig_vmit = sig_rt.copy()
    sig_vmqt = sig_rt.copy()
    sig_vmit.sig = multiply(2*cos(2*pi*fc*tt+thetac),rt)
    sig_vmqt.sig = multiply(-2*sin(2*pi*fc*tt+thetac),rt)

    [win,wit,ixn] = pamfun.pamrcvr10(sig_vmit, FBparms, ptype, pparms)
    [wqn,wqt,ixn] = pamfun.pamrcvr10(sig_vmqt, FBparms, ptype, pparms)

    sig_bt = sig_rt.copy()
    sig_bt.sig = sqrt((wit**2)+(wqt**2))
    seq_bn = ecen.sigSequ(sig_bt.signal()[ixn],FB)

    sig_wt = sig_rt.copy()
    sig_wt.sig = wit + (1j*wqt)

    return(seq_bn , sig_bt , sig_wt , ixn)

def fskxmtr(M,seq_dn,Fs,ptype,pparms,xtype,fcparms):
    """
        M-ary Frequency Shift Keying (FSK) Transmitter for
        Coherent ('coh'), Non-coherent ('noncoh'), and
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
            seq_dn: sequence from class sigSequ
                seq_dn.signal() = [dn] for ['coh','cpfsk']
                seq_dn.signal() = [[dn],[thetacn]] for ['noncoh']
                    dn: M-ary (0,1,..,M-1) N-symbol DT input sequence d_n
                    thetacn: N-symbol DT sequence theta_c[n] in degrees, used instead of thetac0..thetacM-1 for {'noncoh'} FSK
                seq_dn.get_FB(): baud rate of d_n (and theta_c[n]), TB=1/FB
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
    FB = seq_dn.get_FB()
    Ac = 1
    if xtype=='noncoh':
        [dn,thetacn] = seq_dn.signal()
        fcm = fcparms
        if thetacn == '' or thetacn == 'rand':
            thetacm = (pi/2.0)*rand(M)
        else:
            thetacm = thetacn
    elif xtype=='coh':
        dn = seq_dn.signal()
        thetacn = zeros(len(dn))
        [fcm,thetacm] = fcparms
    elif xtype=='cpfsk':
        dn = seq_dn.signal()
        [fc,deltaf] = fcparms
    else:
        print('Not a valid xtype')
        return

    # If the signal is bipolar, shift it up to be unipolar
    if min(dn)<0.0:
        dn = dn + ((M/2.0)-0.5)
        if max(dn)!=float(M-1):
            print('WARNING: The received signal may not contain logic that is interger-spaced (required for current working version)')
    print(dn)
    for m in arange(0,M):
        deln = ones(len(dn))
        deln[where(dn!=m)] = 0
        smt = pamfun.pam12(ecen.sigSequ(deln,FB),Fs,ptype,pparms,['nopulse'])
        tt = smt.timeAxis()
        try:
            xmt = add(xmt , smt.signal()*Ac*cos(2*pi*fcm[m]*tt+thetacm[m]))
        except NameError:
            Ac*cos(2*pi*fcm[m]*tt+thetacm[m])
            xmt = smt.signal()*Ac*cos(2*pi*fcm[m]*tt+thetacm[m])

    sig_xt = ecen.sigWave(xmt,Fs)
    titlestr = 'Transmitted FSK Signal :: M=' + str(int(M))
    if len(fcm)<=3:
        titlestr = titlestr + '\n'
        for m in arange(0,len(fcm)):
            titlestr = titlestr + '$f_{c' + str(m) + '}=' + str(fcm[m]) + 'Hz$, '
    quick.quickplot(sig_xt.timeAxis(),sig_xt.signal(),'-r',[],[],'',titlestr,'Time [s]','x(t)')
    return(sig_xt)


def fskrcvr(M,sig_rt,rtype,fcparms,FBparms,ptype,pparms):
    """
        M-ary Frequency Shift Keying (FSK) Receiver for
        Coherent ('coh'), Non-coherent ('noncoh'), and
        Phase Detector ('phdet') FSK Reception
        >>>>> sig_bn,sig_wt,ixn = fskrcvr(M,sig_rt,rtype,fcparms,FBparms,ptype,pparms) <<<<<
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
    rt = sig_rt.signal()
    tt = sig_rt.timeAxis()
    Fs = sig_rt.get_Fs()

    if rtype=='coh':
        [fcm,thetacm] = fcparms
        for m in arange(0,M):
            vmt = rt * 2*cos(2*pi*fcm[m]*tt+thetacm[m])
            [wmn,wmt,ixn] = pamfun.pamrcvr10(ecen.sigWave(vmt,Fs), FBparms, ptype, pparms,'noplot')
            # quick.quickplot(quick.quicktt(wmt,Fs),wmt)
            try:
                wt = concatenate(([wt],[wmt]),0)
            except NameError:
                wt = wmt
        wn = wt
    elif rtype=='noncoh':
        fcm = fcparms
        for m in arange(0,M):
            vmit = rt * 2*cos(2*pi*fcm[m]*tt)
            vmqt = rt * -2*sin(2*pi*fcm[m]*tt)
            [wmin,wmit,ixn] = pamfun.pamrcvr10(ecen.sigWave(vmit,Fs), FBparms, ptype, pparms,'noplot')
            [wmqn,wmqt,ixn] = pamfun.pamrcvr10(ecen.sigWave(vmqt,Fs), FBparms, ptype, pparms,'noplot')
            wmt = wmit + 1j*wmqt
            wmn = sqrt(square(wmit)+square(wmqt))
            try:
                wt = concatenate(([wt],[wmt]),0)
                wn = concatenate(([wn],[wmn]),0)
            except NameError:
                wt = wmt
                wn = wmn
    elif rtype=='phdet':
        [fc,deltaf] = fcparms
        print('phdet not implamented yet')

    sig_wt = ecen.sigWave(wt,Fs)
    bn = wn.argmax(axis=0)
    sig_bn = ecen.sigWave(bn[ixn],Fs)

    return sig_bn,sig_wt,ixn
