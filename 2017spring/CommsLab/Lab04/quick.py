# File: quick.py
# A way to quickly plot a single figure, generate a time axis....

from pylab import *
import numpy as np
import matplotlib.pyplot as plt

def quickplot(plotx1,ploty1,style1="b-",plotx2=[],ploty2=[],style2="or",title="",xname="",yname="",figx=10,figy=4):
    plt.figure(figsize=(figx,figy))
    plotx1=np.asarray(plotx1)
    ploty1=np.asarray(ploty1)
    plt.plot(plotx1,ploty1,style1,plotx2,ploty2,style2)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.title(title)
    try:
        maxx=np.amax(concatenate([[np.amax(plotx1)],[np.amax(plotx2)]]))
    except ValueError:
        maxx=np.amax(plotx1)
    try:
        maxy=np.amax(concatenate([[np.amax(ploty1)],[np.amax(ploty2)]]))
    except ValueError:
        maxy=np.amax(ploty1)
    try:
        minx=np.amin(concatenate([[np.amin(plotx1)],[np.amin(plotx2)]]))
    except ValueError:
        minx=np.amin(plotx1)
    try:
        miny=np.amin(concatenate([[np.amin(ploty1)],[np.amin(ploty2)]]))
    except ValueError:
        miny=np.amin(ploty1)

    plt.xlim([minx-(0.05*(maxx-minx)),maxx+(0.05*(maxx-minx))])
    plt.ylim([miny-(0.1*(maxy-miny)),maxy+(0.1*(maxy-miny))])
    grid()
    plt.show()
    return

def quicktt(array,rate,length=0,start=0):
    if(length==0):
        tt=arange(len(array))/float(rate)
    else:
        tt = arange(start,round(rate*length))/float(rate)
    return(tt)
