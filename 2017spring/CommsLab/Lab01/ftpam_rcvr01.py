# File: ftpam_rcvr01.py
# Script file that accepts a binary unipolar flat-top PAM
# signal r(t) with bitrate Fb and sampling rate Fs as
# input and decodes it into a received text string.
# The PAM signal r(t) is received from a wav-file with
# sampling rate Fs. First r(t) is sampled at the right
# DT sequence sampling times, spaced Tb = 1/Fb apart. The
# result is then quantized to binary (0 or 1) to form the
# estimated received sequence dnhat which is subsequently
# converted to 8-bit ASCII text.
from pylab import *
import ascfun as af
import wavfun as wf

def wav2ascii(filename,bits=8,Fb=100,pfilter="none",thresh=1):
    rt, Fs = wf.wavread(filename)
    Tb = 1/float(Fb)              # Time per bit
    N = floor(len(rt)/float(Fs)/Tb)  # Number of received bits

    if pfilter is "lp":
        prevval=0
        for i in range(len(rt)):
            if (rt[i]>thresh) or (rt[i]<(thresh*-0.1)):
                rt[i]=prevval
            prevval=rt[i]
        rt=rt*(1/float(thresh))

    rt = around(rt)


    ixL = round(-0.5*Fs*Tb)     # Left index for time axis
    ixR = round((N-0.5)*Fs*Tb)  # Right index for time axis

    ixR=ixR+(len(rt)-(ixR-ixL))
    tthat = arange(ixL,ixR)/float(Fs)

    dnhat = rt[round((Fs*Tb)/2)::int(Fs*Tb)]
    dnhat = dnhat.astype(int)
    ctthat = arange(0,len(dnhat))*Tb

    plt.figure(1,figsize=(10,2.5))
    plt.plot(tthat,rt,'b-')
    lettercolor=''
    colors=['b','g','r','c','m','y','k']
    for c in range(0,len(colors)):
       for b in range(bits):
           lettercolor=lettercolor + colors[c]
    plt.scatter(ctthat,dnhat,color=lettercolor)
    title = "Unipolar Binary Flat-Top PAM for file '" + filename + "' (Fb=" + str(Fb) + "bit/sec)"

    if pfilter is not "none":
        title = title + " (filter threshhold = " + str(thresh) + ")"
    plt.title(title)
    #ylim([amin(rt)-0.1,amax(rt)+0.1])
    plt.show()

    print('The file "%s" reads: ' % (filename))
    print(dnhat)

    txthat =  af.bin2asc(dnhat,bits)

    print('\n...which translates to: "%s"' % (txthat))
