# File: pcmfun.py
# Functions for conversion between m(t) and PCM representation
from pylab import *
from quantizer import *

def mt2pcm(mt, quant, bits=8):
    qtmt=quantizer(mt,quant,1)
    return(qtmt)

    """
    Message signal m(t) to binary PCM conversion
    >>>>> dn = mt2pcm(mt, bits) <<<<<
    where  mt     normalized (A=1) "analog" message signal
    bits   number of bits used per sample
    dn     binary output sequence in sign-magnitude
    form, MSB (sign) first
    """
    # >>Your code goes here<<

def pcm2mt(dn, bits=8):
    dn=0
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
