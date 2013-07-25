import staticngeneration as gen
import numpy as np
import pickle
# import matplotlib.pyplot as plt

 
def genTrials(n_num, m_num, r_num,storage, trialnum, filename,option):
	
	g = gen.Graph(n=n_num)
	for m_i in xrange(3,m_num):
		for r_i in xrange(0,min(n_num-m_i,r_num)): #can only remove up to m_i - 2 edges b/c there are only m_i - 1 edges total
			trialstorage = np.empty(trialnum,bool)
			for trials in xrange(0,trialnum):
				
				# trialstorage[trials]=gen.Graph(n=n_i,m=m_i,option=option,remove=1).emitLongestLength()
				g.createAdjacencyandMutation(m_i,option,add=r_i)
				
				trialstorage[trials]=g.emitMutateStatus()
				#Data is now stored as  r_i,m_i
				storage[r_i][m_i] = float(np.sum(trialstorage))/float(trialnum)
	#print storage
	pickle.dump(storage,open(filename,'wb'))

if __name__ == '__main__':

	#for fixed n=100, fixed m=50, plot edges removed with longest substring
	 #expect the number of h/t seq of length m-1 after removing one edge is 4/(m-2)

	#for each value of m, run 1000 trials, calculate the probability of h/t seq of length m-1
	
	n_num = 100
	m_num = 50
	r_num = 10
	option = 2
	storage  = np.zeros(r_num*m_num).reshape(r_num,m_num)
	trialnum = 5000
	filename = "option%sDifErrorsAdd" %(option)
	genTrials(n_num,m_num,r_num,storage,trialnum,filename,option)
	option = 3
	filename = "option%sDifErrorsAdd" %(option)
	genTrials(n_num,m_num,r_num,storage,trialnum,filename,option)