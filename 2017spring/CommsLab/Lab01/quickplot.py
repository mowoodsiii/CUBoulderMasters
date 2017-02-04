# File: quickplot.py
# A way to quickly plot a single figure

import numpy as np
import matplotlib.pyplot as plt

def quickplot(plotx1,ploty1,style1="b-",plotx2=[],ploty2=[],style2="or",xname="",yname="",title="",figx=10,figy=4):
    plt.figure(1,figsize=(figx,figy))
    plotx1=np.asarray(plotx1)
    ploty1=np.asarray(ploty1)
    plt.plot(plotx1,ploty1,style1,plotx2,ploty2,style2)
    plt.xlabel(xname)
    plt.ylabel(yname)
    plt.title(title)
    plt.xlim([np.amin(plotx1)-(0.05*(np.amax(plotx1)-np.amin(plotx1))),np.amax(plotx1)+(0.05*(np.amax(plotx1)-np.amin(plotx1)))])
    plt.ylim([np.amin(ploty1)-(0.1*(np.amax(ploty1)-np.amin(ploty1))),np.amax(ploty1)+(0.1*(np.amax(ploty1)-np.amin(ploty1)))])
    plt.show()
    return
