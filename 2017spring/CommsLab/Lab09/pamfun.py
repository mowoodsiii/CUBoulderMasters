# File: pamfun.py
# Functions for pulse amplitude modulation (PAM)
from pylab import *
import ecen4652 as ecen
from quick import *
from math import *
import ptfun

def pam12(sig_an, Fs, ptype, pparms=[], plotparms=[]):
    """
    Pulse amplitude modulation: a_n -> s(t), -TB/2<=t<(N-1/2)*TB,
    V1.1 for 'man', 'rcf', 'rect', 'sinc', and 'tri' pulse types.
    >>>>> sig_st,ixn = pam11(sig_an, Fs, ptype, pparms) <<<<<
    where
        *** INPUTS ***
        sig_an: sequence from class sigSequ
            sig_an.signal():  N-symbol DT input sequence a_n, 0 <= n < N
            sig_an.get_FB():  Baud rate of a_n, TB=1/FB
        Fs:    sampling rate of s(t)
        ptype: pulse type from list ('man','rcf','rect','sinc','tri')
        pparms not used for 'man','rect','tri'
            pparms = [k, alpha] for 'rcf'
            pparms = [k, beta]  for 'sinc'
                k:     "tail" truncation parameter for 'rcf','sinc' (truncates p(t) to -k*TB <= t < k*TB)
                alpha: Rolloff parameter for 'rcf', 0<=alpha<=1
                beta:  Kaiser window parameter for 'sinc'
        plotparms = [window, interval] - Options to fcus/window the plot ouput (see quick.py)
            window: Where to window 'first', 'last', or 'middle'
            interval: Width of window (in datapoints)

        *** OUTPUTS ***
        sig_st: waveform from class sigWave
            sig_st.timeAxis():  time axis for s(t), starts at -TB/2
            sig_st.signal():    CT output signal s(t), -TB/2<=t<(N-1/2)*TB with sampling rate Fs
        ixn
    """

# ***** Set variables and manage data formatting *****
    an = concatenate([[0],sig_an.signal(),[0]])#an = sig_an.signal()
    N = len(an)                # Number of data symbols
    n0 = sig_an.get_n0()       # Starting index
    FB = sig_an.get_FB()       # Baud rate
    TB = 1/float(FB)

    M = int(Fs/FB)               # Interpolation number
    Sb = int(Fs/float(FB))     # Samples per bit

    ptype = ptype.lower()      # Convert ptype to lowercase

    if(ptype=='sinc'):
        k = pparms[0]
        beta = pparms[1]
    elif (ptype=='rcf' or ptype=='rrcf'):
        k = pparms[0]
        alpha = pparms[1]
        if(alpha>1 or alpha<0):
            print('ERROR: pparm[1]=', str(alpha) ,' violates 0<=alpha<=1')
            return
    elif(ptype=='tri'):
        k = 1.0
    else:
        k = 0.5

# ***** Set up time axis *****
    ixL = ceil(-Fs*(n0+0.5)/float(FB))   # Left index for time axis
    ixR = ceil(Fs*(n0+N-0.5)/float(FB))  # Right index for time axis
    tt = arange(ixL,ixR)/float(Fs)  # Time axis for s(t)
    t0 = tt[0]                 # Start time for s(t)
# ***** Conversion from DT a_n to CT a_s(t) *****
    ast = zeros(len(tt))       # Initialize a_s(t)
    ix = array(around(Fs*arange(0,N)/float(FB)),int) # Symbol center indexes
    ast[ix-int(ixL)] = Fs*an   # delta_n -> delta(t) conversion
# ***** Set up PAM pulse p(t) *****
    ast = an.copy()
    for i in range(0,M-1):
        ast = vstack([ast,zeros(len(an))])
    ast = ast.flatten('F')

    # Set left/right limits for p(t)
    kL=-k; kR=-kL
    ixpL = ceil(Fs*kL/float(FB))   # Left index for p(t) time axis
    ixpR = ceil(Fs*kR/float(FB))   # Right index for p(t) time axis
    ttp = arange(ixpL,ixpR)/float(Fs)  # Time axis for p(t)

    ix = where(logical_and(ttp>=kL/float(FB), ttp<kR/float(FB)))[0]
    pt = []
    if (ptype=='rect'):
        pt = zeros(len(ttp))       # Initialize pulse p(t)
        pt[ix] = ones(len(ix))
    elif(ptype=='tri'):
        pt = zeros(len(ttp))       # Initialize pulse p(t)
        triarray = np.arange(0,1,(1/float(len(ix))))[1:]
        pt = np.concatenate([[0],triarray,[1],triarray[::-1]])
        ttp = arange(2*ixpL,2*ixpR)/float(Fs)
    elif(ptype=='man'):
        pt = zeros(len(ttp))       # Initialize pulse p(t)
        pt[ix] = concatenate([-1*ones(int(len(ix)/2)),[0],ones(len(ix)-int(len(ix)/2))])
    elif (ptype=='sinc'):
        pt=np.sinc(FB*ttp)
        pt = pt*kaiser(len(pt),beta) # Pulse p(t), Kaiser windowe
    elif(ptype=='rcf'):
        for t in ttp:
            rcft_num = sin(pi*t/float(TB))*cos(pi*alpha*t/float(TB))
            rcft_den = (pi*t/float(TB))*(1-pow(2*alpha*t/float(TB),2))
            if (rcft_den == 0.0):
                rcft_num = pt[-1]
                rcft_den = 1
            rcft = divide(rcft_num,float(rcft_den))
            pt = concatenate([pt,[rcft]])
    elif(ptype=='rrcf'):
        for t in ttp:
            if(t==0):
                rcft_num = (1-alpha+(4*alpha/pi))
                rcft_den = 1
            elif(t==TB/float(4*alpha)) or (t==-1*TB/float(4*alpha)):
                rcft_num = alpha*((1+2/pi)*sin(pi/float(4*alpha))+(1-2/pi)*cos(pi/float(4*alpha)))
                rcft_den = pow(2,0.5)
            else:
                rcft_num = TB*(sin(pi*t*(1-alpha)/float(TB))+(4*alpha*t/float(TB))*cos(pi*t*(1+alpha)/float(TB)))
                rcft_den = pi*t*(1-pow(4*alpha*t/float(TB),2))
            rcft = divide(rcft_num,float(rcft_den))
            pt = concatenate([pt,[rcft]])
    else:
        print("ptype '%s' is not recognized" % ptype)
        return

    st = convolve(ast,pt,'same')  # s(t) = a_s(t)*p(t)

    # ***** Plot the pulse and hte interpolated sequence *****

    if(ptype=='rect'):
        longptype='Rectangular'
    elif(ptype=='tri'):
        longptype='Tritangular'
    elif(ptype=='sinc'):
        longptype='Sinc'
    elif(ptype=='man'):
        longptype='Manchester'
    elif(ptype=='rcf'):
        longptype='Raised Cosine in Frequency (RCf)'
    elif(ptype=='rrcf'):
        longptype='Root-Raised Cosine in Frequency (RRCf)'

    if(len(ttp)!=len(pt)):
        print('Resetting ttp')
        ttp=quicktt(st,Fs)
    if (plotparms != []) and ((plotparms[0] == 'nopulse') or (plotparms[0] == 'noplot')):
        doNothing=1 # print('%s pulse created but not plotted...' % longptype)
    else:
        quickplot(ttp,pt,'-b',[],[],'',longptype+' Interpolation Pulse','Time','p(t)')

    tts=quicktt(st,Fs)

    ttan = (tts[0::Sb])[1:-1] # discretize time scale for individual points and remove added leading and trailing zeros
    an = (an*(st[0::Sb]))[1:-1] # scale data sequence to fit interpolation s(t) and remove added leading and trailing zeros

    if (plotparms != []) and (plotparms[0] == 'noplot'):
        doNothing=1 # print('Supressing plotting result')
    else:
        quickplot(tts,st,'-b',ttan,an,'or','Interpolated Data using a '+longptype+' pulse','Time','s(t)',plotparms[1:])


    return ecen.sigWave(st, Fs, t0)  # Return waveform from sigWave class



def randompam(t=1,ptype='rect',pparms=[20,0],FB=100,Fs=44100,polarity='bi',L=2):
    """
    Generate a random PAM signal
    """
    N = int(t*FB) # data points
    dn = around(rand(N)) # random unipolar binary signal
    if polarity == 'bi':
        an = (dn*L)-float(L/2) #polar binary
    else:
        an = dn
    seq_an = ecen.sigSequ(an,FB)
    sig_st = pam12(seq_an, Fs, ptype,pparms,['nopulse'])
    return sig_st,seq_an

def whitenoise(t=1,nfL=10000,Fs=44100):
    """
    Generate t seconds of white noise
    """
    nn = randn(round(t*2*nfL)) # Gaussian noise, rate 2*nfL
    sig_nn = ecen.sigSequ(nn, 2*nfL, 0)
    sig_nt = pam11(sig_nn,Fs,'rcf',[20, 0.2],['noplot']) #Bandlimited noise n(t), rate Fs
    return sig_nt

def pamrcvr10(sig_rt, FBparms, ptype, pparms=[], plotparms=[]):
    """
    Pulse amplitude modulation receiver with matched filter:
    r(t) -> b(t) -> bn.
    V1.0 for 'man', 'rcf', 'rect', 'rrcf', 'sinc', and 'tri' pulse types.
    >>>>> bn, bt, ixn = pamrcvr10(tt, rt, FBparms, ptype, pparms) <<<<<
    where
        *** INPUTS ***
        tt: time axis for r(t)
        rt: received (noisy) PAM signal r(t)
        FBparms: = [FB, dly]
        FB: Baud rate of PAM signal, TB=1/FB
        dly: sampling delay for b(t) -> b_n as a fraction of TB sampling times are t=n*TB+t0 where t0 = dly*TB
        ptype: pulse type from list ('man','rcf','rect','rrcf','sinc','tri')
        pparms:
            pparms not used for 'man','rect','tri'
            pparms = [k, alpha] for 'rcf','rrcf'
            pparms = [k, beta] for 'sinc'
            k: "tail" truncation parameter for 'rcf','rrcf','sinc' (truncates p(t) to -k*TB <= t < k*TB)
            alpha: rolloff parameter for ('rcf','rrcf'), 0<=alpha<=1
            beta: Kaiser window parameter for 'sinc'

        *** OUTPUTS ***
        bn: received DT sequence after sampling at t=n*TB+t0
        bt: received PAM signal b(t) at output of matched filter
        ixn: indexes where b(t) is sampled to obtain b_n
    """
    ptype = ptype.lower() # Convert ptype to lowercase

    tt = sig_rt.timeAxis()
    rt = sig_rt.sig

    FB = FBparms[0]
    t0 = FBparms[1]
    Fs = (len(tt)-1)/(tt[-1]-tt[0])
    # ***** Set up matched filter response h_R(t) *****
    TB = 1/float(FB) # Time per symbol
    if(ptype=='sinc'):
      k = pparms[0]
      beta = pparms[1]
    elif (ptype=='rcf' or ptype=='rrcf'):
      k = pparms[0]
      alpha = pparms[1]
      if(alpha>1 or alpha<0):
          print('ERROR: pparm[1]=', str(alpha) ,' violates 0<=alpha<=1')
          return
    else:
      k = 0.5

    if (ptype=='rect'): # Rectangular or Manchester p(t)
        kL = -0.5; kR = -kL
    else:
        kL = -1.0; kR = -kL # Default left/right limits
    ixpL = ceil(Fs*kL*TB) # Left index for p(t) time axis
    ixpR = ceil(Fs*kR*TB) # Right index for p(t) time axis
    ttp = arange(ixpL,ixpR)/float(Fs) # Time axis for p(t)
    pt = zeros(len(ttp)) # Initialize pulse p(t)
    ix = where(logical_and(ttp>=kL*TB, ttp<kR*TB))[0]

    if (ptype=='rect'):
        pt = zeros(len(ttp))       # Initialize pulse p(t)
        pt[ix] = ones(len(ix))
    elif(ptype=='tri'):
        pt = zeros(len(ttp))       # Initialize pulse p(t)
        triarray = np.arange(0,1,(1/float(len(ix))))[1:]
        pt = np.concatenate([[0],triarray,[1],triarray[::-1]])
        ttp = arange(2*ixpL,2*ixpR)/float(Fs)
    elif(ptype=='man'):
        pt = zeros(len(ttp))       # Initialize pulse p(t)
        pt[ix] = concatenate([-1*ones(int(len(ix)/2)),[0],ones(len(ix)-int(len(ix)/2))])
    elif (ptype=='sinc'):
        pt=np.sinc(FB*ttp)
        pt = pt*kaiser(len(pt),beta) # Pulse p(t), Kaiser windowe
    elif(ptype=='rcf'):
        for t in ttp:
            rcft_num = sin(pi*t/float(TB))*cos(pi*alpha*t/float(TB))
            rcft_den = (pi*t/float(TB))*(1-pow(2*alpha*t/float(TB),2))
            if (rcft_den == 0.0):
                rcft_num = pt[-1]
                rcft_den = 1
            rcft = divide(rcft_num,float(rcft_den))
            pt = concatenate([pt,[rcft]])
    elif(ptype=='rrcf'):
        for t in ttp:
            if(t==0):
                rcft_num = (1-alpha+(4*alpha/pi))
                rcft_den = 1
            elif(t==TB/float(4*alpha)) or (t==-1*TB/float(4*alpha)):
                rcft_num = alpha*((1+2/pi)*sin(pi/float(4*alpha))+(1-2/pi)*cos(pi/float(4*alpha)))
                rcft_den = pow(2,0.5)
            else:
                rcft_num = TB*(sin(pi*t*(1-alpha)/float(TB))+(4*alpha*t/float(TB))*cos(pi*t*(1+alpha)/float(TB)))
                rcft_den = pi*t*(1-pow(4*alpha*t/float(TB),2))
            rcft = divide(rcft_num,float(rcft_den))
            pt = concatenate([pt,[rcft]])
    else:
        print("ptype '%s' is not recognized" % ptype)

    hRt = pt[::-1] # h_R(t) = p(-t)
    hRt = Fs/sum(np.power(pt,2.0))*hRt # h_R(t) normalized
    # ***** Filter r(t) with matched filter h_R(t)
    bt = convolve(rt,hRt)/float(Fs) # Matched filter b(t)=r(t)*h_R(t)
    bt = bt[-ixpL:len(tt)-ixpL] # Trim b(t)
    # ***** Sample b(t) at t=n*TB+t0 to obtain b_n *****
    N = ceil(FB*(tt[-1]-tt[0]))+1# Number of symbols
    ixn = array(around((arange(N)+0.5+t0)*Fs/float(FB)),int64) # Sampling indexes
    ix = where(logical_and(ixn>=0,ixn<len(tt)))[0]
    ixn = ixn[ix] # Trim to existing indexes
    bn = bt[ixn] # DT sequence sampled at t=n*TB+t0
    return bn, bt, ixn


def pamrcvr10B(sig_rt, FBparms, ptype, pparms=[] , splot=[]):
	"""
	Pulse amplitude modulation receiver with matched filter: r(t) -> b(t) -> bn.
	V1.0 for 'man', 'rcf', 'rect', 'rrcf', 'sinc', and 'tri' pulse types.
	>>>>> sig_bn, sig_bt, ixn = pamrcvr10(sig_rt, FBparms, ptype, pparms) <<<<<
	where 	sig_rt: 			waveform from class sigWave
			sig_rt.signal():	received (noisy) PAM signal r(t)
			sig_rt.timeAxis(): 	time axis for r(t)
			FBparms: 			= [FB, dly]
			FB:					Baud rate of PAM signal, TB=1/FB
			dly:				sampling delay for b(t) -> b_n as a fraction of TB
								sampling times are t=n*TB+t0 where t0 = dly*TB
			ptype: 				pulse type from list
								('man','rcf','rect','rrcf','sinc','tri')
								pparms not used for 'man','rect','tri'
								pparms = [k, alpha] for 'rcf','rrcf'
								pparms = [k, beta] for 'sinc'
			k:					"tail" truncation parameter for 'rcf','rrcf','sinc'
								(truncates p(t) to -k*TB <= t < k*TB)
			alpha: 				rolloff parameter for ('rcf','rrcf'), 0<=alpha<=1
			beta: 				Kaiser window parameter for 'sinc'
			sig_bn: 			sequence from class sigSequ
			sig_bn.signal(): 	received DT sequence after sampling at t=n*TB+t0
			sig_bt: 			waveform from class sigWave
			sig_bt.signal(): 	received PAM signal b(t) at output of matched filter
			ixn:				indexes where b(t) is sampled to obtain b_n
	"""
	# polarity = 'polar'
	if type(FBparms)==int or type(FBparms)==float:
		FB, t0 = FBparms, 0		# Get FBparms parameters
	else:
		FB, t0 = FBparms[0],0
		if len(FBparms) > 1:
			t0 = FBparms[1]/float(FB)

	Fs = sig_rt.get_Fs()		# Sampling rate
	rt = sig_rt.signal()		# Received signal r(t)
	tt = sig_rt.timeAxis()		# Time axis for r(t)
	nn0 = int(ceil((tt[0]-t0)*FB)) 	# First data index
									# Integer multiple of 1/FB
	ixnn0 = argmin(abs(tt-(nn0/float(FB)+t0)))
	N = int(floor((tt[-1]-tt[ixnn0])*FB)) + 1 	# Number of data symbols

	# ***** Set up matched filter response h_R(t) *****
	ptype = ptype.lower()		# Convert ptype to lowercase
								# Set left/right limits for p(t)
	if (ptype=='rect'):			# Rectangular p(t)
		kL = -0.5; kR = -kL
	elif(ptype == 'tri'):
		kL = -1.0; kR = -kL
	elif(ptype == 'man'):
		kL = -0.5; kR = -kL
	elif (ptype == 'sinc') or (ptype == 'rcf') or (ptype == 'rrcf'):
		kL = -pparms[0]; kR = -kL
	else:
		kL = -1.0; kR = -kL		# Default left/right limits

	ixpL = int(ceil(Fs*kL/float(FB))) # Left index for p(t) time axis
	ixpR = int(ceil(Fs*kR/float(FB))) # Right index for p(t) time axis
	ttp = arange(ixpL,ixpR)/float(Fs) # Time axis for p(t)
	pt = zeros(len(ttp))		# Initialize pulse p(t)

	# ***** Generate Pulse pt *****
	if (ptype=='rect'):			# Rectangular p(t)
		ix = where(logical_and(ttp>=kL/float(FB), ttp<kR/float(FB)))[0]
		pt[ix] = ones(len(ix))
		wave = 'Rectangular'
	elif ptype == 'sinc': 	# Do the same thing for now..
		pt = np.sinc(FB*ttp)
		pt = pt*kaiser(len(pt), pparms[1]) 			# Pulse p(t), Kaiser windowedy
		wave = 'Sinc'
	elif ptype == 'man':
		ix1  = where(logical_and(ttp>=kL/float(FB), ttp<0))[0]
		# if polarity == 'Polar':
			# pt[ix1] = -ones(len(ix1))
		ix2 = where(logical_and(ttp>=0, ttp < kR/float(FB)))[0]
		pt[ix2] = ones(len(ix2))
		wave = 'Manchester'
	elif ptype == 'tri':	# Do nothing because don't need to
		slope = -kL/float(sps)
		# print('slope: ', slope)
		bound = -ixpL
		j = 0
		for i in range(0, bound):
			pt[i] = j*slope
			j += 1
		j = sps
		for i in range(bound, 2*bound):
			pt[i] = j*slope
			j -= 1
		wave = 'Triangular'
	elif ptype == 'rcf':
		[tht, pt] = sinc_ipol.rcf(ttp, FB, pparms[0], pparms[1])	# Generate rcf pulse
		wave = 'RCF'
	elif ptype == 'rrcf':
		TB = 1/float(FB)
		alpha = pparms[1]
		trange = TB/(4.0*alpha)
		# Get middle band between -trange< ixmid < trange and eliminate the
		#	index where ttp = 0
		ixmid = where(logical_and(logical_and(ttp>-trange, ttp<trange),ttp !=0))[0]
		# Get index where ttp = 0
		ix0 = where(ttp == 0)[0]
		# Get outside band s.t. ixout < -trange & ixout > trange
		ixout = where(logical_or(ttp>=trange, ttp<-trange))[0]
		pt[ix0] = 1.0-alpha+(4.0*alpha)/pi
		pt[ixmid] = TB/pi*(sin((1-alpha)*pi*ttp[ixmid]/TB)+(4.0*alpha*ttp[ixmid]/TB)*cos((1+alpha)*pi*ttp[ixmid]/TB))/((1.0-(4.0*alpha*ttp[ixmid]/TB)**2.0)*ttp[ixmid])
		pt[ixout] = TB/pi*(sin((1-alpha)*pi*ttp[ixout]/TB)+(4.0*alpha*ttp[ixout]/TB)*cos((1+alpha)*pi*ttp[ixout]/TB))/((1.0-(4.0*alpha*ttp[ixout]/TB)**2.0)*ttp[ixout])
		wave = 'RRCF'
	else:
		print("ptype '%s' is not recognized" % ptype)

	hRt = pt[::-1]			# h_R(t) = p(-t)
	hRt = Fs/sum(np.power(pt,2.0))*hRt # h_R(t) normalized

	# ***** Filter r(t) with matched filter h_R(t) *****
	bt = convolve(rt,hRt)/float(Fs) # Matched filter b(t)=r(t)*h_R(t)
	bt = bt[-ixpL:len(tt)-ixpL] # Trim b(t)

	# ***** Sample b(t) at t=n*TB+t0 to obtain b_n *****
	ixn = ixnn0 + array(around(Fs*arange(N)/float(FB)),int)	# Sampling indexes
	bn = bt[ixn]				# DT sequence sampled at t=n*TB+t0

	return bn, bt, ixn
