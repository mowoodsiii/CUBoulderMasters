# this module will be imported in the into your flowgraph

# File: ptfun
# Functions for gnuradio-companion PAM p(t) generation
import numpy as np
from pylab import *
import quick
def pampt(sps, ptype, pparms=[], plot='', duty=1):
    """
    PAM pulse p(t) = p(n*TB/sps) generation
    >>>>> pt = pampt(sps, ptype, pparms) <<<<<
    where  sps: samples per symbol
        ptype: pulse type ('rect', 'sinc', 'tri')
        pparms not used for 'rect', 'tri'
        pparms = [k, beta] for sinc
            k:     "tail" truncation parameter for (truncates p(t) to -k*sps <= n < k*sps)
            beta:  Kaiser window parameter for 'sinc'
        pt: pulse p(t) at t=n*TB/sps
    Note: In terms of sampling rate Fs and baud rate FB, sps = Fs/FB
    """
    if ptype is 'rect':
        pt = np.ones(sps)
    elif ptype is 'tri':
        triarray = np.arange(0,1,(1/float(sps)))[1:]
        pt = np.concatenate([triarray,[1],triarray[::-1]])
    elif ptype is 'sinc':
        k = pparms[0]
        beta = pparms[1]
        nn = np.arange(-k*sps,k*sps) # was (-2*k*sps,2*k*sps)
        pt = sinc((1/float(sps))*nn)
        pt = pt*kaiser(len(pt),beta)
    elif ptype is 'man':
        if(sps % 2 == 0): # is even....
            pt = concatenate([-1*ones(int(sps/2)),ones(int(sps/2))])
        else: # is odd....
            pt = concatenate([-1*ones(int(floor(sps/2))),[0],ones(int(floor(sps/2)))])
    elif ptype is 'rcf':
        k = pparms[0]
        alpha = pparms[1]
        nn = np.arange(-k*sps,k*sps)
        tt = nn/float(sps)
        pt=[]
        for t in tt:
            rcft_num = sin(pi*t)*cos(pi*alpha*t)
            rcft_den = (pi*t)*(1-pow(2*alpha*t,2))
            rcft = divide(rcft_num,float(rcft_den))
            if (rcft_den == 0.0):
                rcft=pt[-1]
            pt = concatenate([pt,[rcft]])
        #pt=np.sinc(tt)
        #pt=pt*cos(alpha*tt)/(1-(2*alpha*tt)**2)
    else:
        print("ERROR: ptype '",ptype,"' not recognized")
        return 0

    if(duty!=1):
        if(ptype=='tri'):
            sps = sps*2
        elif(ptype=='rcf' or ptype=='sinc'):
            sps = sps/duty
        widthbuff = zeros(int(((sps/float(duty))-len(pt))/float(2)))
        pt = concatenate([widthbuff,pt,widthbuff])

    if plot == 'plotpulse':
        tt=quick.quicktt(pt,sps/duty)
        quick.quickplot(tt,pt,'-b',[],[],'',ptype+' Pulse (sps='+str(sps)+' samp/symbol, duty='+str(duty*100)+'%)','Time (s)','Magnitude')
    return(pt)
