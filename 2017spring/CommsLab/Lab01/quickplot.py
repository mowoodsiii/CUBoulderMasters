# File: quickplot.py
# A way to quickly plot a single figure

import numpy as np
import matplotlib.pyplot as plt

def quickplot(plotx,ploty,xaxis,yaxis,title):
  plt.figure(1,figsize=(10,4))
  plt.plot(plotx,ploty)
  plt.xlabel(xaxis)
  plt.ylabel(yaxis)
  plt.title(title)
  plt.show()
  return
