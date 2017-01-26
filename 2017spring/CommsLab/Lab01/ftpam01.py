# File: ftpam01.py
# Script file that accepts an ASCII text string as input and
# produces a corresponding binary unipolar flat-top PAM signal
# s(t) with bit rate Fb and sampling rate Fs.
# The ASCII text string uses 8-bit encoding and LSB-first
# conversion to a bitstream dn. At every index value
# n=0,1,2,..., dn is either 0 or 1. To convert dn to a
# flat-top PAM CT signal approximation s(t), the formula
#   s(t) = dn,  (n-1/2)*Tb <= t < (n+1/2)*Tb,
# is used.

from pylab import *
import ascfun as af
import wavfun as wf

def ascii2ftpam(string="Test",bits=8,export="",Fs=44100,Fb=100):
    dn =  af.asc2bin(string,bits)
    print('"%s" = ' % (string))
    st,tt,ctt,Fs = bitstream(dn,bits,Fs,Fb,export)
    if export is "export":
        wavexport(string,st,Fs)
    return

def bitstream(dn,bits=8,Fs=44100,Fb=100,export=""):
   #print(dn)
   N = len(dn)       # Total number of bits

   Tb = 1/float(Fb)            # Time per bit
   ixL = round(-0.5*Fs*Tb)     # Left index for time axis
   ixR = round((N-0.5)*Fs*Tb)  # Right index for time axis

   st = dn
   for i in range(1,int(Fs*Tb)):
       st = vstack([st,dn])#zeros(len(dn))])
   st = reshape(st,st.size,order='F')

   tt = arange(ixL,ixR)/float(Fs)  # Time axis for s(t)
   ctt = arange(0,len(dn))*Tb # Time axis for individule bit center points of dn

   if export is "export":
       bitstream_plot(tt,st,bits,ctt,dn)
   return(st,tt,ctt,Fs)

def wavexport(string,st,Fs):
    if (len(string)>10) or (string.isalnum() is False):
        print("NOTE: String is not alphanumeric...\n")
        string="ascii2wav"
    print('Outputting file as "%s.wav"\n\n' % (string))
    wf.wavwrite(0.999*st/float(max(abs(st))),Fs,string+'.wav') # Write .wav file

def bitstream_plot(tt,st,bits,ctt,dn):
    plt.figure(1,figsize=(10,4))
    plt.plot(tt,st,'b-')
    lettercolor=''
    colors=['b','g','r','c','m','y','k']
    for c in range(0,len(colors)):
       for b in range(bits):
           lettercolor=lettercolor + colors[c]
    plt.scatter(ctt,dn,color=lettercolor)
    ylim([-0.25,1.25])
    grid()
    plt.show()
