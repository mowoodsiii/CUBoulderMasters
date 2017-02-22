def showeye(sig_rt, FB, NTd=50, dispparms=[]):
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
    rt = sig_rt.signal()       # Get r(t)
    Fs = sig_rt.get_Fs()       # Sampling rate
    t0 = dispparms[0]/float(FB)  # Delay in sec
    tw = dispparms[1]/float(FB)  # Display width in sec
    dws = floor(Fs*tw)         # Display width in samples
    tteye = arange(dws)/float(Fs)  # Time axis for eye
    trix = around(Fs*(t0+arange(NTd)/float(FB)))
    ix = where(logical_and(trix>=0, trix<=len(rt)-dws))[0]
    trix = trix[ix]            # Trigger indexes within r(t)
    TM = rt[trix[0]:trix[0]+dws]   # First trace
    TM = vstack((TM, rt[trix[1]:trix[1]+dws]))
    # Second trace
    plot(FB*tteye, TM.T, ’-b’) # Plot transpose of TM
    grid()
    show()
