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
def safe_ln(x, minval=0.00000000000000001):
    return np.log(x.clip(min=minval))

#display results from multiple error removals
option= 2
name = 'option%sLongestSubSeqRatio' %(option)
a = pickle.load(open(name,'rb'))
ylab = "Ratio of experimental longest valid H/T to max longest valid H/T"
xlab = "m values"

print np.sum(a[0])
print a.shape
xvals = np.arange(0.,len(a[0]))

fig = plt.figure(2)
fig, axes = plt.subplots(nrows=2, ncols=1)
fig.tight_layout()
ax1=fig.add_subplot(211)
for i in xrange(0,a.shape[0]):
	ax1.plot(xvals,a[i],label=("%s mutations" %(i)))

plt.ylabel(ylab)
plt.xlabel(xlab)
plt.title(name + ': relation between m and alternating H/T CS after removing multiple edge')
# plt.legend(loc='upper right', ncol=2, mode="expand")

# Shink current axis by 20%
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# Put a legend to the right of the current axis
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))


option= 3
name = 'option%sLongestSubSeqRatio' %(option)

a = pickle.load(open(name,'rb'))

ax2=fig.add_subplot(212)
for i in xrange(0,a.shape[0]):
	ax2.plot(xvals,a[i],label=("%s mutations" %(i)))

plt.ylabel(ylab)
plt.xlabel(xlab)
plt.title(name + ': relation between m and alternating H/T CS after removing multiple edge')

# Shink current axis by 20%
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# Put a legend to the right of the current axis
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()