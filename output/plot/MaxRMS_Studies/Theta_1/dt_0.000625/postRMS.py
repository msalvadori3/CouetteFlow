#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import glob

MinX = []
MinY = []
MaxX = []
MaxY = []

for subdir, dirs, files in os.walk('./'):
    for file in files:

        filepath = subdir + os.sep + file

        if filepath.endswith(".dat"):
            print (filepath)

        # setup for RMS log data
            rmsFile = os.path.join(filepath)
        
            rmsdata = np.genfromtxt(filepath,
                    skip_header=1)

            # Plot for RMS log
            nIter = rmsdata[:,0]
            RMSerrUS = rmsdata[:,1]
            RMSerrSS = rmsdata[:,2]

            MinX = min(nIter)
            MaxX =  max(nIter)
            MinY = min(min(RMSerrUS),min(RMSerrSS))
            #MaxY = max(max(RMSerrUS),max(RMSerrSS))
            MaxY = np.append(MaxY,max(RMSerrSS))

MaxY = sorted(MaxY,reverse=True)
dy = [0.1,0.05,0.025,0.0125,0.00625,0.003125]

p = plt.plot(dy,MaxY, 'ro-', label='RMS$_{Steady}$')
#p = plt.plot(nIter,RMSerrSS, 'b--', label='RMS$_{Steady}$')
plt.title("$\Theta = 1.0$ with dt=0.000625", fontsize=16)
plt.setp(p, linewidth='1.0')
plt.axis([min(dy),max(dy), 10e-5, 10e-3])
plt.xscale('log')
plt.yscale('log')
plt.xlabel('dy', fontsize=22)
plt.ylabel('Peack RMS error', fontsize=22)
plt.grid(True)
ax = plt.gca()
xlabels = plt.getp(ax, 'xticklabels')
ylabels = plt.getp(ax, 'yticklabels')
plt.setp(xlabels, fontsize=18)
plt.setp(ylabels, fontsize=18)
plt.legend(
          loc='upper right',
          borderpad=0.25,
          handletextpad=0.25,
          borderaxespad=0.25,
          labelspacing=0.0,
          handlelength=2.0,
          numpoints=1)
legendText = plt.gca().get_legend().get_texts()
plt.setp(legendText, fontsize=18)
legend = plt.gca().get_legend()
legend.draw_frame(False)

pltFile = 'MaxRMSlog.png'
fig = plt.gcf()
fig.set_size_inches(8,5)
plt.tight_layout()
plt.savefig(pltFile, format='png')
plt.close()

print "%s DONE!!" % (pltFile)
