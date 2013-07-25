import makeData

import pylab
import matplotlib.pyplot as plt
import numpy as np
import pickle

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
# a = pickle.load(open('./storage','rb'))
# print a.shape


# xvals = np.arange(0.,50.)

# plt.figure(1)
# plt.subplot(211)
# plt.plot(xvals,a[10],'r--',xvals,a[20],'b--',xvals,a[30],'g--',xvals,a[40],'y--',xvals,a[49],'m--',xvals,f(xvals))
# plt.axis([0, 50, 0, 1])
# plt.ylabel('prob of getting valid alternating h/t CS')
# plt.xlabel('m values')
# plt.title('OPtion2: relation between m and alternating H/T CS after removing 1 edge')

# c = pickle.load(open('./storage3','rb'))


# xvals = np.arange(0.,50.)
# plt.subplot(212)
# plt.plot(xvals,c[10],'r--',xvals,c[20],'b--',xvals,c[30],'g--',xvals,c[40],'y--',xvals,c[49],'m--',xvals,f(xvals))
# plt.axis([0, 50, 0, 1])
# plt.ylabel('prob of getting valid alternating h/t CS')
# plt.xlabel('m values')
# plt.title('Option 3: relation between m and alternating H/T CS after removing 1 edge')
# plt.show()

#--------------------------------#--------------------------------#--------------------------------#--------------------------------

#PLOT ONE EDGE REMOVAL PLOTS

option= 2
name = "option%sOneRemoval" %(option)
a = pickle.load(open(name,'rb'))


xvals = np.arange(0.,50.)


plt.figure(2)
plt.subplot(211)
plt.plot(xvals,a[10],'r--',xvals,a[20],'b--',xvals,a[30],'g--',xvals,a[40],'y--',xvals,a[49],'m--',xvals,f(xvals))
plt.axis([0, 50, 0, 1])
plt.ylabel('prob of getting valid alternating h/t CS')
plt.xlabel('m values')
plt.title('OPtion2 using Bool: relation between m and alternating H/T CS after removing 1 edge')

option= 3
name = "option%sOneRemoval" %(option)
a = pickle.load(open(name,'rb'))

xvals = np.arange(0.,50.)

plt.figure(2)
plt.subplot(212)
plt.plot(xvals,a[10],'r--',xvals,a[20],'b--',xvals,a[30],'g--',xvals,a[40],'y--',xvals,a[49],'m--',xvals,f(xvals))
plt.axis([0, 50, 0, 1])
plt.ylabel('prob of getting valid alternating h/t CS')
plt.xlabel('m values')
plt.title('OPtion3 using Bool: relation between m and alternating H/T CS after removing 1 edge')
plt.show()

#PLOT LOG PROB #-------------------------------------------------------------------------------------


option= 2
name = "option%sOneRemoval" %(option)
a = pickle.load(open(name,'rb'))
a = safe_ln(a)

xvals = np.arange(0.,50.)


plt.figure(2)
plt.subplot(211)
plt.plot(xvals,a[10],'r--',xvals,a[20],'b--',xvals,a[30],'g--',xvals,a[40],'y--',xvals,a[49],'m--',xvals,safe_ln(f(xvals)))

plt.ylabel('prob of getting valid alternating h/t CS')
plt.xlabel('m values')
plt.title('OPtion2 using Bool: relation between m and alternating H/T CS after removing 1 edge')

option= 3
name = "option%sOneRemoval" %(option)
a = pickle.load(open(name,'rb'))
a = safe_ln(a)
xvals = np.arange(0.,50.)

plt.figure(2)
plt.subplot(212)
plt.plot(xvals,a[10],'r--',xvals,a[20],'b--',xvals,a[30],'g--',xvals,a[40],'y--',xvals,a[49],'m--',xvals,safe_ln(f(xvals)))

plt.ylabel('prob of getting valid alternating h/t CS')
plt.xlabel('m values')
plt.title('OPtion3 using Bool: relation between m and alternating H/T CS after removing 1 edge')
plt.show()

