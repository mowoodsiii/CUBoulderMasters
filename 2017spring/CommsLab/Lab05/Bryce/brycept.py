
# File: ptfun
# Functions for gnuradio-companion PAM p(t) generation
from pylab import *
import numpy as np
def testmy_grc():
    return('Package gnuradiopkg imported correctly')

def pampt(sps, ptype, pparms=[]):
	"""
	PAM pulse p(t) = p(n*TB/sps) generation
	>>>>> pt = pampt(sps, ptype, pparms) <<<<<
	where 	sps:    samples/second = discrete time version of FS/FB
			ptype: 	pulse type ('rect', 'sinc', 'tri')
			pparms not used for 'rect', 'tri'
			pparms = [k, beta] for sinc
			k:		"tail" truncation parameter for 'sinc'
					(truncates p(t) to -k*sps <= n < k*sps)
			beta: 	Kaiser window parameter for 'sinc'
			pt:		pulse p(t) at t=n*TB/sps
			Note: 	In terms of sampling rate Fs and baud rate FB,
					sps = Fs/FB
	"""
	k = pparms[0]
	if ptype == 'rect':
		bound = np.floor(sps/float(2))
		pt = np.arange(-bound, bound, 1)
		pt[:] = 1
	elif ptype == 'tri':
		bound = sps
		pt = np.arange(-bound, bound-1, 1, dtype = float)
		j = 1
		for i in range(0, bound):
			pt[i] = j/float(sps)
			j += 1
		j = sps
		for i in range(bound-1, 2*bound-1):
			pt[i] = j/float(sps)
			j -= 1
	elif ptype == 'man':
		bound = np.floor(sps/float(2))
		pt = np.arange(-bound, bound, 1)
		ixn = where(pt<0)[0]
		ixp = where(pt>=0)[0]
		pt[ixn] = -1
		pt[ixp] = 1
	elif ptype == 'sinc':
		pt = np.sinc(np.arange(-k*sps,k*sps)/float(sps))
	elif ptype == 'rcf':
		alpha = pparms[1]
		t = arange(-k*sps, k*sps)/float(sps)
		pt = np.sinc(t)
		pt = pt*cos(alpha*t)/(1-(2*alpha*t)**2)
	else:
		pass

	return pt
