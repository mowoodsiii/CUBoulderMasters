# File: wavSampler.py
#
from pylab import *
from ast import literal_eval
from wavfun import wavread
import sinc_ipol

def wavSampler(Fs,wavfile,fL,k):
    wave,framerate = wavread(wavfile)
    if Fs < framerate:
        print('Insufficient sampling frequency')
        return
    tlen = len(wave)/framerate  # Signal duration in sec
    tt = arange(0,round(tlen*framerate))/float(framerate)   # Time axis
    plt.figure(1,figsize=(10,4))
    stem(tt,wave)
    plt.title("%s (Fs=%d Hz)" % (wavfile,Fs))
    plt.xlabel("time(sec)")
    plt.ylabel("xt")
    show()

    multiplier = round(Fs/float(framerate))
    print('Multiplier:%d' % (multiplier))
    filledwave=wave
    for i in range(1,multiplier+1):
        filledwave = vstack([filledwave,zeros(len(wave))])
    filledwave = reshape(filledwave,filledwave.size,order='F')
    newtt = arange(0,len(filledwave))/float(Fs*multiplier)
    plt.figure(1,figsize=(10,4))
    stem(newtt,filledwave)
    plt.title("%s %dx Expanded (Fs%d=%d Hz)" % (wavfile,multiplier,multiplier,Fs))
    plt.xlabel("time(sec)")
    plt.ylabel("xt")
    show()

    tth,ht = sinc_ipol.sinc(Fs*multiplier,fL,k)
    plt.figure(1,figsize=(10,4))
    plt.title("sinc Pulse for Interpolation (Fs%d=%dHz, fL=%dHz, k=%d)" % (multiplier,Fs,fL,k))
    plt.xlabel("time(sec)")
    plt.ylabel("xt")
    plot(tth,ht,'m')
    show()

    convolvedwave = convolve(filledwave,ht,'same')

    plt.figure(1,figsize=(10,4))
    #stem(newtt[0:(multiplier*48)],convolvedwave[0:(multiplier*48)])
    stem(newtt[0:300],convolvedwave[0:300])
    plt.title("%s %dx Expanded and Interpolated (Fs%d=%d Hz)" % (wavfile,multiplier,multiplier,Fs))
    plt.xlabel("time(sec)")
    plt.ylabel("y%dt" % multiplier)
    show()
    return
