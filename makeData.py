import staticngeneration as gen
import numpy as np
import pickle
# import matplotlib.pyplot as plt


def generateChromosomeData(trials,n,m,option,r):
	toreturn = ""
	for i in xrange(trials):
		toreturn += str(i) + " " + gen.Graph(n,m,option,remove=r).printSavedChromosomeData()
	return toreturn



def buildDataFile(filename, **kwargs):
	f = open("./data/"+filename,'w')
	f.write("Trial N M option edgesRemoved LongestH/T\n")
	n = kwargs["n"]
	m = kwargs["m"]
	trials = kwargs["trials"]
	option = kwargs["option"]
	remove = kwargs["remove"]
	towrite = generateChromosomeData(trials,n,m,option,remove)
	f.write(towrite)
	f.close()

	# for n in xrange(15,101,5):
	# 	for m in xrange(3,n):
	# 		name = "trial%s_%s.txt" %(n/15,m)
	# 		buildDataFile(name,trials=100,n=n,m=m,option=2,remove=1)



 
def genTrials(n_num, m_num, storage, trialnum, filename,option):
	for n_i in xrange(5,n_num):
		g = gen.Graph(n=n_i)
		for m_i in xrange(3,n_i-1):
			#used for numbers
			#trialstorage = np.zeros(trialnum)
			#used for bools
			trialstorage = np.empty(trialnum,bool)
			for trials in xrange(0,trialnum):
				
				# trialstorage[trials]=gen.Graph(n=n_i,m=m_i,option=option,remove=1).emitLongestLength()
				g.createAdjacencyandMutation(m=m_i,option=option,remove=1)
				trialstorage[trials]=g.emitMutateStatus()

			#count number in trials of length m_num-2
			#rows are diff n vals, cols are dif m vals
				#storage[n_i][m_i] = float(len(trialstorage[trialstorage==(m_i-2)]))/float(trialnum)
				
				storage[n_i][m_i] = float(np.sum(trialstorage))/float(trialnum)
	print storage
	pickle.dump(storage,open(filename,'wb'))

if __name__ == '__main__':

	#for fixed n=100, fixed m=50, plot edges removed with longest substring
	 #expect the number of h/t seq of length m-1 after removing one edge is 4/(m-2)

	#for each value of m, run 1000 trials, calculate the probability of h/t seq of length m-1
	
	

	n_num = 50
	m_num = 50
	
	option = 2
	storage  = np.zeros(n_num*n_num).reshape(n_num,n_num)
	trialnum = 5000
	filename = "option%sOneRemoval" %(option)
	genTrials(n_num,m_num,storage,trialnum,filename,option)
	option = 3
	filename = "option%sOneRemoval" %(option)
	genTrials(n_num,m_num,storage,trialnum,filename,option)
