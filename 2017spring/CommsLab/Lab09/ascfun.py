# File: ascfun.py
# Functions for conversion between ASCII and bits
from pylab import *

def asc2bin(txt, bits=8):
   """
   ASCII text to serial binary conversion
   >>>>> dn = asc2bin(txt, bits) <<<<<
   where  txt        input text string
      abs(bits)  bits per char, default=8
      bits > 0   LSB first parallel to serial
      bits < 0   MSB first parallel to serial
      dn         binary output sequence
   """

   txtnum = array([ord(c) for c in txt])   # convert the string into an ASCII (decimal representation) list
   if bits > 0:      # Neg powers of 2, LSB
      p2 = np.power(2.0,arange(0,-bits,-1)) # power: np.power(base,exp)     array range: arange(start,stop,step)
   else:             # Neg powers of 2, MSB
      p2 = np.power(2.0,1+arange(bits,0,1))
   B = array(mod(array(floor(outer(txtnum,p2)),int),2),int8) # outer product: outer(vec1,vec2)

                # Rows of B are bits of chars
   dn = reshape(B,B.size)
   return dn         # Serial binary output

def bin2asc(dn, bits, threshold=0):
   n = int(len(dn)) # number of bits
   N = int(floor(n/float(abs(bits)))) # number of letters


   if threshold!=0:
       ihigh = (dn > threshold)
       ilow  = (dn <= threshold)
       dn[ihigh] = 1
       dn[ilow]  = 0

   bitString = []
   for i in range(N):
      bitString.append(dn[(i*abs(bits)):((i+1)*abs(bits))])
   if bits < 0:
      for i in range(N):
          bitString[i] = bitString[i][::-1]
   ASCIIString = []
   for i in range(N):
       value=0
       for j in range(abs(bits)):
           value = value + (int(bitString[i][j])<<j)
       ASCIIString.append(value)
   textString=""
   for i in range(N):
       textString=textString+chr(ASCIIString[i])

   return(textString,ASCIIString)

   """
   Serial binary to ASCII text conversion
   >>>>> txt = bin2asc(dn, bits, flg) <<<<<
   where  dn         binary input sequence
      abs(bits)  bits per char, default=8
      bits > 0   LSB first parallel to serial
      bits < 0   MSB first parallel to serial
      flg != 0   limit range to [0...127]
      txt        output text string
   """
   # >>Function to be completed in part (b)<<
