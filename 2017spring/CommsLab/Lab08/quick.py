# File: quick.py
# A way to quickly plot a single figure, generate a time axis....

from pylab import *
import numpy as np
import matplotlib.pyplot as plt

def quickplot(plotx1,ploty1,style1="b-",plotx2=[],ploty2=[],style2="or",title="",xname="",yname="",interval=[],figdim=[14,4]):
    """
    Plot a data series,
    V2.1 Includes zoom/window option
    >>>>> void = quickplot(plotx1,ploty1,style1,plotx2,ploty2,style2,title,xname,yname,interval,figdim) <<<<<
    where   plotx1: independent variable of sequence 1
            ploty1: dependent variable of sequence 1
            style1: line style of sequence 1                                (default: blue line, 'b-')
            plotx2: independent variable of sequence 2                      (default: empty [])
            ploty2: dependent variable of sequence 2                        (default: empty [])
            style2: line style of sequence 2                                (default: red circles, 'or')
            title:  plot title                                              (default: blank '')
            xname:  x-axis label                                            (default: blank '')
            yname:  y-axis label                                            (default: blank '')
            plotparms = [direction, interval]:  Zoom/window options         (default: empty)
                direction: where to window 'first', 'last', or 'middle'
                interval:  width of window (in datapoints)
            figdim = [figx,figy]: figure print dimensions                   (default: [14,4])
                figx:      figure width
                figy:      figure height
    """
    figx=figdim[0]
    figy=figdim[1]
    plt.figure(figsize=(figx,figy))
    plotx1=np.asarray(plotx1)
    ploty1=np.asarray(ploty1)
    title_interval=""
    if(len(interval)==2):
        direction = interval[0]
        interval = interval[1]
        title_interval = str(direction).title()+" "+str(interval)+" samples of "
        if(plotx2!=[]):
            dataratio=round(len(plotx1)/float(len(plotx2)))
        else:
            dataratio=1
        if(direction=='first'):
            plotx1 = plotx1[0:interval*dataratio]
            ploty1 = ploty1[0:interval*dataratio]
            if(plotx2!=[]):
                plotx2 = plotx2[0:interval]
                ploty2 = ploty2[0:interval]
        elif(direction=='last'):
            plotx1 = plotx1[len(plotx1)-interval*dataratio:]
            ploty1 = ploty1[len(ploty1)-interval*dataratio:]
            if(plotx2!=[]):
                plotx2 = plotx2[len(plotx2)-interval:]
                ploty2 = ploty2[len(ploty2)-interval:]
        elif(direction=='middle'):
            plotx1 = plotx1[int((len(plotx1)/float(2))-((interval*dataratio)/float(2))):int((len(plotx1)/float(2))+((interval*dataratio)/float(2)))]
            ploty1 = ploty1[int((len(ploty1)/float(2))-((interval*dataratio)/float(2))):int((len(ploty1)/float(2))+((interval*dataratio)/float(2)))]
            if(plotx2!=[]):
                plotx2 = plotx2[int((len(plotx2)/float(2))-(interval/float(2))):int((len(plotx2)/float(2))+(interval/float(2)))]
                ploty2 = ploty2[int((len(ploty2)/float(2))-(interval/float(2))):int((len(ploty2)/float(2))+(interval/float(2)))]
    plt.plot(plotx1,ploty1,style1,plotx2,ploty2,style2)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.title(title_interval+title)

    try:
        plotx1[plotx1==inf]=0
        plotx1[plotx1==-inf]=0
        ploty1[ploty1==inf]=0
        ploty1[ploty1==-inf]=0
        plotx2[plotx2==inf]=0
        plotx2[plotx2==-inf]=0
        ploty2[ploty2==inf]=0
        ploty2[ploty2==-inf]=0
    except IndexError:
        pass

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
