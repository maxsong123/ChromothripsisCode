import makeData

import pylab
import matplotlib.pyplot as plt
import numpy as np
import pickle
# -----------------------------------------------------------------------
# PLOT makeDiff Plots
def f(a):
	#calculates values for 4/(m-1)
	return np.array(map(b, a))
def b(x):
	if x != 2: 
		return 1./(x-2) 
	else: 
		return 0
def safe_ln(x,logoption=False,minval=0.00000000000000001):
    if logoption:
    	return np.log(x.clip(min=minval))
    else: 
    	return x
def setaxis(logoption=False):
	if logoption: 
		return [0,50,-0.01,0]
	else:
		return [0.,50.,0.,1.0]

    

#display results from multiple error removals
logoption = False
option= 2
name = 'option%sDifErrorsAdd' %(option)
ab = pickle.load(open(name,'rb'))

a = safe_ln(ab,logoption)

xvals = np.arange(0.,len(a[0]))

fig = plt.figure(1)

ax1=fig.add_subplot(211)
ax1.plot(xvals,a[2],label=("%s mutations-Option2" %(2)))
ax1.plot(xvals,a[3],label=("%s mutations-Option2" %(3)))
ax1.plot(xvals,a[4],label=("%s mutations-Option2" %(4)))

option= 3
name = 'option%sDifErrorsAdd' %(option)
ab = pickle.load(open(name,'rb'))
a = safe_ln(ab,logoption)

ax1.plot(xvals,a[1],label=("%s mutations-Option3" %(1)))
ax1.plot(xvals,a[2],label=("%s mutations-Option3" %(2)))
ax1.plot(xvals,a[3],label=("%s mutations-Option3" %(3)))

plt.ylabel('log prob of getting valid alternating h/t CS')
plt.xlabel('m values')
plt.title(name + ': relation between m and alternating H/T CS after adding multiple edge')
# plt.legend(loc='upper right', ncol=2, mode="expand")

# Shink current axis by 20%
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# Put a legend to the right of the current axis
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))


plt.show()