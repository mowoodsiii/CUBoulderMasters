# File: wavSampler.py
#
from pylab import *
from ast import literal_eval
from wavfun import wavread
import sinc_ipol

def wavSampler(Fs,wavfile):
    wave,framerate = wavread(wavfile)
    if Fs < framerate:
        print('Insufficient sampling frequency')
        return
    tlen = len(wave)/framerate  # Signal duration in sec
    tt = arange(0,round(tlen*framerate))/float(framerate)   # Time axis
    plt.figure(1,figsize=(10,4))
    stem(tt,wave)
    show()

    multiplier = round(Fs/float(framerate))
    print('Multiplier:%d' % (multiplier))
    filledwave=wave
    for i in range(1,multiplier):
        filledwave = vstack([filledwave,zeros(len(wave))])
    filledwave = reshape(filledwave,filledwave.size,order='F')
    newtt = arange(0,len(filledwave))/float(Fs*multiplier)
    plt.figure(1,figsize=(10,4))
    stem(newtt,filledwave)
    show()

    fL = 3000
    k = 10
    tth,ht = sinc_ipol.sinc(Fs*multiplier,fL,k)
    plt.figure(1,figsize=(10,4))
    plot(tth,ht,'m')
    show()

    convolvedwave = convolve(filledwave,ht,'same')
    plt.figure(1,figsize=(10,4))
    stem(newtt,convolvedwave)
    show()
    return
