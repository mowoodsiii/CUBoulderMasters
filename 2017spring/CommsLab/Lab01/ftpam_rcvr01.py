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

def wav2ascii(filename,bits=8):
    rt, Fs = wf.wavread(filename)
    rt = around(rt)
    Fb = 100                      # Data bit rate
    Tb = 1/float(Fb)              # Time per bit
    N = floor(len(rt)/float(Fs)/Tb)  # Number of received bits

    ixL = round(-0.5*Fs*Tb)     # Left index for time axis
    ixR = round((N-0.5)*Fs*Tb)  # Right index for time axis
    tthat = arange(ixL,ixR)/float(Fs)

    dnhat = rt[round((Fs*Tb)/2)::int(Fs*Tb)]
    ctthat = arange(0,len(dnhat))*Tb

    plt.figure(1,figsize=(10,4))
    plt.plot(tthat,rt,'b-')
    lettercolor=''
    colors=['b','g','r','c','m','y','k']
    for c in range(0,len(colors)):
       for b in range(bits):
           lettercolor=lettercolor + colors[c]
    plt.scatter(ctthat,dnhat,color=lettercolor)
    ylim([-0.25,1.25])
    plt.show()

    print('%s reads: ' % (filename))
    print(dnhat)

    txthat =  af.bin2asc(dnhat,bits)

    print(txthat)                 # Print result
