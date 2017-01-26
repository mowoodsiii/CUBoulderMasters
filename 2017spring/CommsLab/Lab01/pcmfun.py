# File: pcmfun.py
# Functions for conversion between m(t) and PCM representation
from pylab import *
from quantizer import *
from ftpam01 import *

def mt2pcm(mt, tt, Fs, quant=8):
    pwmt=quantizer(mt,quant,1)

    plt.figure(1,figsize=(12,5))
    plt.plot(tt,pwmt,'b-',tt,pwmt,'ro')
    plt.title("100Hz DT Sinusoidal Wave, sampled at Fs=%d Hz with an %d bit quantizer" % (Fs,quant))
    plt.xlabel('Time (s)')
    plt.grid()
    plt.show()

    if quant > 0:      # Neg powers of 2, LSB
        p2 = np.power(2.0,arange(0,-quant,-1)) # power: np.power(base,exp)     array range: arange(start,stop,step)
    else:             # Neg powers of 2, MSB
        p2 = np.power(2.0,1+arange(quant,0,1))
    B = array(mod(array(floor(outer(pwmt,p2)),int),2),int8) # outer product: outer(vec1,vec2)
                # Rows of B are bits of chars
    dn = reshape(B,B.size)
    st,tt,ctt,Fs = bitstream(dn,quant,Fs)

    plt.figure(1,figsize=(10,8))
    div=8
    for i in range(0,div):
        plt.subplot((div*100)+11+i)
        plt.subplots_adjust(hspace=0.75)
        plt.plot(tt[(i*len(tt)/div):((i+1)*len(tt)/div)-1],st[(i*len(st)/div):((i+1)*len(tt)/div)-1],'b-')
        ylim([-0.25,1.25])
    plt.show()

    return(pwmt,quant)

    """
    Message signal m(t) to binary PCM conversion
    >>>>> dn = mt2pcm(mt, bits) <<<<<
    where  mt     normalized (A=1) "analog" message signal
    bits   number of bits used per sample
    dn     binary output sequence in sign-magnitude
    form, MSB (sign) first
    """
    # >>Your code goes here<<

def pcm2mt(pwmt, quant=8):
    Tb = 1/float(Fb)              # Time per bit
    N = floor(len(rt)/float(Fs)/Tb)  # Number of received bits
    rt = around(rt)

    ixL = round(-0.5*Fs*Tb)     # Left index for time axis
    ixR = round((N-0.5)*Fs*Tb)  # Right index for time axis

    ixR=ixR+(len(rt)-(ixR-ixL))
    tthat = arange(ixL,ixR)/float(Fs)

    dnhat = rt[round((Fs*Tb)/2)::int(Fs*Tb)]
    dnhat = dnhat.astype(int)
    ctthat = arange(0,len(dnhat))*Tb

    return
    """
    Binary PCM to message signal m(t) conversion
    >>>>> mt = pcm2mt(dn, bits) <<<<<
    where  dn     binary output sequence in sign-magnitude
    form, MSB (sign) first
    bits   number of bits used per sample
    mt     normalized (A=1) "analog" message signal
    """
    # >>Your code goes here <<
