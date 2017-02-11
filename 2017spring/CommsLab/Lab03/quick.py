# File: quick.py
# A way to quickly plot a single figure, generate a time axis....

from pylab import *
import numpy as np
import matplotlib.pyplot as plt

def quickplot(plotx1,ploty1,style1="b-",plotx2=[],ploty2=[],style2="ro",plotx3=[],ploty3=[],style3="gx",title="",xname="",yname="",figx=10,figy=4):
    plt.figure(1,figsize=(figx,figy))
    plotx1=np.asarray(plotx1)
    ploty1=np.asarray(ploty1)
    plt.plot(plotx1,ploty1,style1,plotx2,ploty2,style2,plotx3,ploty3,style3)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.title(title)
    plt.xlim([np.amin(plotx1)-(0.05*(np.amax(plotx1)-np.amin(plotx1))),np.amax(plotx1)+(0.05*(np.amax(plotx1)-np.amin(plotx1)))])
    plt.ylim([np.amin(ploty1)-(0.1*(np.amax(ploty1)-np.amin(ploty1))),np.amax(ploty1)+(0.1*(np.amax(ploty1)-np.amin(ploty1)))])
    plt.show()
    return

def quicktt(arrayORtime,Fs,Fb=1,start=0):
    if (isinstance(arrayORtime,float)) or (isinstance(arrayORtime,int)): # arrayORtime is a time value
        tt = arange(start,round(Fs*arrayORtime))/float(Fs)
    else: # arrayORtime is an array of data points
        tt = arange(len(arrayORtime))*Fb/float(Fs)
    return(tt)
