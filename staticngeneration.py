import random 
import json


#external to the Graph Object, there is also a function that will generate MC versions of different
#graphs, and will have a param called trials that determines how many to generate

class Graph(object):


	"""docstring for Graph: 
	instantiates a random instantiation of a Head/Tail Chromothripsis Graph
	Is the overarching class container of node and edge lists, takes a few different 
	parameters as constructors: 
	n = number of intervals total (2x number of nodes), 
	m = number of intervals in alternating Chromothripsis graph (2x number of nodes present) 
	k = number of errors in graph

	"""
	def __init__(self,n): 
		
		super(Graph, self).__init__()
		self.n = n #total number of intervals in reference genome
		self.NodeList,self.IntervalList,self.RefList = self.initiateNodes()
		#preprocess NodeDegreeDict w/ Interval Edges
		self.PreProcessedNodeDegreeDict = self.preProcessIntervalList()
		Node.counter = 1
	def resetAdjacencyandMutation(self):
		
		#reset Node counter for next Graph instantiation
		self.m = None
		self.errors = None
		self.adjacencyList = []
		self.optiontype = None
		self.longestSubSeq = 0 #gives information about the longest alternating h/t subseq after perturbing chromosome
		self.mutateStatus = None
		self.mutateChromosome = None
		self.NodeDegreeDict = {}
		self.option, self.t1_orientation, self.shuffledChrom = (None,None,None)
		
	def createAdjacencyandMutation(self,m, optiontype = 2,**kwargs):
		# for key, value in kwargs.iteritems():
		# 	print key, value
		self.resetAdjacencyandMutation()
		self.m = m #total number of intervals in C substring
		self.errors = kwargs#number of errors to introduce stored in kwargs
		
		self.optiontype = optiontype #determines which method the original H/T Chrom is generated w/

		if m > self.n:
			print "Error: m must be smaller then n"
		self.option, self.t1_orientation, self.shuffledChrom = self.genChromosome(optiontype)
		
		#fill in adjacencies List
		self.markadjacencies()
		
		#Record adjacencies in NodeDegreeDict
		self.NodeDegreeDict = self.recordNodeDegrees(self.PreProcessedNodeDegreeDict,self.adjacencyList)
		
		self.Alternating, self.List = self.testHeadTails(self.NodeDegreeDict)
		

	def sortChromosome(self,chromosome):
		#sorts the chromosome in order
		return sorted(chromosome,key=lambda x: x.counter)
	def markadjacencies(self):
		#return adjacencylist of Chromosome
		for i in xrange(len(self.shuffledChrom)):
			if i % 2 == 0:
				self.adjacencyList.append(Edge(self.shuffledChrom[i],self.shuffledChrom[i+1]))
	
	def preProcessIntervalList(self):
		#Input: go through interval edges, for occurence of every node, 
		#store it in a dict of node degrees
		#output a preprocessed nodeDegreeDict
		returndict = {}
		for edge in self.IntervalList:
			node1num= edge.Node1.counter
			node2num= edge.Node2.counter
			returndict[node1num] = returndict.get(node1num,0) + 1
			returndict[node2num] = returndict.get(node2num,0) + 1
		return returndict

	def recordNodeDegrees(self, nodeDegreeDict, adjacencyList):
		#INPUT: takes an adjList + a preprocessed nodeDegreeDict,
		#go through adjacent edges, for occurence of every node, 
		#store it in a dict of node degrees
		#OUTPUT: nodeDegreeDict
		
		returndict = nodeDegreeDict.copy()

		for edge in adjacencyList:
			node1num= edge.Node1.counter
			node2num= edge.Node2.counter
			returndict[node1num] = returndict.get(node1num,0) + 1
			returndict[node2num] = returndict.get(node2num,0) + 1
		return returndict 

	def testHeadTails(self, NodeDegreeDict):
	#INPUT: uses NodeDegreeDict generated by recordnodeDegrees, 
	#OUTPUT: 
		#1) a boolean value, of whether the CChrom in the Graph object is valid alternating
	#head tail or not 
		#2) a string message detailing where the breaks occurred
		#3) a list of lists, of the subsequences of alternating h/t
		#first create a filtered list of nodes with degree = 2 nodes
		FilteredList=[node for node in self.NodeList if NodeDegreeDict[node.counter]==2]

		assert len(FilteredList) != 0
		counter = 0
		#after you remove an edge, the node is gone from the FilteredList, as it has Degree 1
		toreturnlistoflists = []
		templist = []
		returnval = True
		trial = 0
		for i in xrange(len(FilteredList)-1):
			
			if FilteredList[i].orientation != FilteredList[i+1].orientation:
				templist.append(FilteredList[i])

			else: 
				templist.append(FilteredList[i])
				toreturnlistoflists.append(templist)
				templist = []
				returnval = False
			#add last one on to templist 
		# print len(FilteredList)

		templist.append(FilteredList[-1])

		toreturnlistoflists.append(templist)
		return returnval, toreturnlistoflists

	
	def genChromosome(self,num):
		if num == 2:
			t1_orientation, shuffledChrom = self.Option2()
		if num == 3:
			t1_orientation, shuffledChrom = self.Option3()
		self.option = num
		self.t1_orientation = t1_orientation
		self.shuffledChrom = shuffledChrom
		return num,t1_orientation, shuffledChrom

	def printObjlist(self, list1):
		#used for printing either NodeList or Edgelist
		return str(map(lambda x: str(x),list1))

	def printChromosome(self):
		#pretty prints chromosome
		return "Option " + str(self.option) + ", t1_orientation: " +self.t1_orientation + ", List: " + self.printObjlist(self.shuffledChrom)
 	
 	#choose Heads/Tails
 	def chooseOrientation(self,percent_heads):
 		if random.random() < percent_heads:
 			return "heads"
 		else:
 			return "tails"

 	def removeEdges(self,k, adjlist,dictionary):
 		#INPUT: takes an integer k, detailing how many edges to remove, and an adj list, detailing
 		#which list to remove from

 		#OUTPUT: an updated dictionary of node degrees, new adj list, and a list of edges removed
 		print "k = " + str(k)
 		print "len of adjlist = " + str(len(adjlist))
 		if k < len(adjlist): 
 			takeout = random.sample(adjlist, k)
 			keptin = [i for i in adjlist if i not in takeout]
 			
 			return self.recordNodeDegrees(dictionary,keptin), keptin,takeout
 		else:
 			raise Exception("You tried to remove too many edges, has to be less then "+ str(len(self.adjacencyList)))
 	 		 
 	def addEdges(self,k, adjlist,dictionary):
 		#INPUT:  takes an integer k, detailing how many edges to add, an adj list detailing to record the changes
 		#and a dictionary, to choose which nodes to add an edge between, and record the result. 

 		#output: an updated dictionary of node degrees, a new adj list and a list of edges added 
 		#filter the dictionary for edges to add
 		listofonedegreenodes = [nodenum for nodenum,degreecount in dictionary.items() if degreecount == 1]
 		
 		if len(listofonedegreenodes)/2 < k:
 			raise Exception*("You tried to add too many edges, has to be less then " + str(len(listofonedegreenodes)/2))
 		else:
 			return self.recursiveAdd(dictionary,adjlist,listofonedegreenodes,[],k)
 				
 	def recursiveAdd(self,dictionary,adjacencyList,listtoaddfrom,edgesAdded,number):
 		if number == 0:
 			return dictionary,adjacencyList,edgesAdded
 		else:
 			toconnect = random.sample(listtoaddfrom,2)
			node1num = toconnect[0]
			node2num = toconnect[1]
			if (max(node1num,node2num) %2 == 0) and (abs(node1num-node2num) == 1):
				#i.e. if the two nodes are connected by interval edge, try again
				return self.recursiveAdd(dictionary,adjacencyList,listtoaddfrom,edgesAdded,number)
			else: 
				#if not, then 
				#remove them from the listtoaddfrom list, 
				listtoaddfrom = [num for num in listtoaddfrom if num not in toconnect]
				#and get the two nodes that the nodenum's point to:
				node1 = self.NodeList[node1num-1]
				node2 = self.NodeList[node2num-1]
				#2) make an edge
				newEdge = Edge(node1,node2)
				#3) add to adj list and listaddedto
				adjacencyList.append(newEdge)
				edgesAdded.append(newEdge)
				#4)increase counts in dictionary
				dictionary[node1num] +=1
				dictionary[node2num] +=1
				#5) call it again w/ number - 1
				return self.recursiveAdd(dictionary,adjacencyList,listtoaddfrom,edgesAdded,number-1)
				

 	def perturbChromosome(self,perturbation):
 		#INPUT: takes perturbation: a dictionary of perturbationFunctions(remove, add): number of operations
 		#ex. {removeEdges: 4, addEdges: 3} means remove 4 edges, and add 3 edges
 		#OUTPUT: a List of H/T alternating Chromosomes
 		dictionary = self.NodeDegreeDict
 		newAdjlist = [edge for edge in self.adjacencyList]
 		edgesRemoved = []
 		edgesAdded = []
 		for fun, num in perturbation.items():
 			if fun == "remove":
 				dictionary,newAdjlist, edgesRemoved = self.removeEdges(num,newAdjlist,dictionary)
 			if fun == "add":
 				dictionary,newAdjlist,edgesAdded = self.addEdges(num,newAdjlist,dictionary)

 		return self.testHeadTails(dictionary), edgesRemoved, edgesAdded

 	def alterChromosome(self):

		#run calculations as specified by errors dictionary
		#When called, returns a string specifying original chromosome, whether its alternating h/t, 
		#the types of mutations introduced, whether its alternating h/t after mutation, substrings of alternating h/t chromosome
		
		if self.errors:
			((self.mutateStatus, self.mutateChromosome), self.edgesRemoved, self.edgesAdded) = self.perturbChromosome(self.errors)
		self.longestSubSeq = max(map(lambda x: len(x), self.mutateChromosome))

	def printalteredChromosome(self):
		a =  map(lambda x: self.printObjlist(x),self.mutateChromosome)
		toreturn = "Original Chromosome: " + self.printObjlist( self.List[0]) + "\n"
		toreturn += "Generated with OptionType: " + str(self.optiontype) + "\n"
		toreturn +="Alternating H/T: " + str(self.Alternating) + "\n" 
		toreturn += "Mutation type: " + str(self.errors.items()) + "\n" 
		toreturn += "Edges Removed: " + self.printObjlist(self.edgesRemoved) + "\n"
		toreturn += "Edges Added: " + self.printObjlist(self.edgesAdded) + "\n"
		toreturn += "Alternating H/T: " + str(self.mutateStatus) + "\n" 
		toreturn += "Mutated Chromosome: " + str(a) + "\n"
		toreturn += "Longest Mutated H/T: " + str(self.longestSubSeq)
		return toreturn

	def printSavedChromosomeData(self):
		#OUTPUT: Generates a string of the data characterizing the removal of edges from above
		#Template: f.write("Trial N M OptionType edgesRemoved LongestH/T")
		self.alterChromosome()
		return str(self.n) + " " + str(self.m) + " " + str(self.optiontype) + " "+ str(len(self.edgesRemoved)) + " " + str(max(map(lambda x: len(x), self.mutateChromosome))) + "\n"
	
	def emitLongestLength(self):
		#used for doing speedy calculations on if the altered Chromosome is 
		self.alterChromosome()
		return self.longestSubSeq

	def emitMutateStatus(self):
		self.alterChromosome()
		return self.mutateStatus

 	def generateJSONdata(self):
 		fragdict = {}
 		for i in xrange(self.n):
 			self.NodeList[2*i] 
 		pass
	#Circular 
	def Option1():
		pass
	#Telo on ends, selection between Telo
	def Option2(self):
		#choose heads or tails
		t1_orientation = self.chooseOrientation(0.5)
		subsetlength = self.m
		totalintervalnum = self.n
		nodes = self.NodeList
		t1 = None
		t2 = None
		rearrangedC = []
		if t1_orientation == "heads": 
			#choose the range of options that t1 can be - from 2 (heads of first interval) to 2n-1-(2m-4) 
			#operating in intervals, will switch to node number at the end
			start = 1
			end = totalintervalnum - (subsetlength - 1) 
			#choose from [start, end] inclusive for t1 interval
			t1num = random.choice(range(start,end+1))
			t2num = t1num + (subsetlength - 1)
			t1 = nodes[2*t1num-1] #in addition to 2n-1 referring to the head, also have to -1 to get index in array
			t2 = nodes[2*t2num-2]
			#randomly generate the chaining of the m-2 intervals in between, 
			rearrangedC.append(t1)

			permutedintermediate = range(t1num+1,t2num)
			random.shuffle(permutedintermediate) #[t1num+1, t2num-1]

			for intervalnum in permutedintermediate:
				#add tail (2n-1) to rearrangedC, and then head (2n-1)
				#again have to do an additonal -1 on both things to index into the array correctly				
				
				#randomly pick head/tail of the next seq to add
				choice = int(.5 > random.random())
				
				rearrangedC.append(nodes[2*intervalnum-1-(1-choice)]) #tail
				rearrangedC.append(nodes[2*intervalnum-1-choice]) #head


				# rearrangedC.append(nodes[2*intervalnum-2]) #tail
				# rearrangedC.append(nodes[2*intervalnum-1]) #head
			#add last node on
			rearrangedC.append(t2)
			return (t1_orientation, rearrangedC)

		if t1_orientation == "tails":

			start = subsetlength
			end = totalintervalnum 
			#choose from [start, end] inclusive for t1 interval
			t1num = random.choice(range(start,end+1))
			t2num = t1num - (subsetlength - 1)
			#in addition to 2n-1 referring to the head, also have to -1 to get index in array
			t1 = nodes[2*t1num-2] #tail of first telomere choice
			t2 = nodes[2*t2num-1] #head of other telomere
			#randomly generate the chaining of the m-2 intervals in between, 
			rearrangedC.append(t1)

			permutedintermediate = range(t2num+1, t1num)
			random.shuffle(permutedintermediate) #[t1num+1, t2num-1]

			for intervalnum in permutedintermediate:
				#add tail (2n-1) to rearrangedC, and then head (2n-1)
				#again have to do an additonal -1 on both things to index into the array correctly				

				#randomly pick head/tail of the next seq to add
				choice = int(.5 > random.random())
				rearrangedC.append(nodes[2*intervalnum-1-(1-choice)]) #tail
				rearrangedC.append(nodes[2*intervalnum-1-choice]) #head

				# rearrangedC.append(nodes[2*intervalnum-1]) #head
				# rearrangedC.append(nodes[2*intervalnum-2]) #tail

			#add last node on
			rearrangedC.append(t2)
			####### REVERSE! CHANGE THIS LATER
			rearrangedC.reverse()
			return (t1_orientation, rearrangedC)

	#Telo adjacent, selection as complement
	def Option3(self):
		#choose heads or tails
		t1_orientation = self.chooseOrientation(0.5)
		subsetlength = self.m
		totalintervalnum = self.n
		nodes = self.NodeList
		t1 = None
		t2 = None
		rearrangedC = []

		#choose t1
		if t1_orientation == "tails":
			#choose where it is - it can be anywhere except the very end
			t1num = random.choice(range(1,totalintervalnum))

			#anywhere to the right of t1num that leaves enough space in the complement of the interval [t1num, t2num]			t2num =  
			#choose range of tails
			#w is the max length of ranges of values that t2 can assume
			w = totalintervalnum - subsetlength + 1
			#truncate the range to be within n
			w = min(t1num + w, totalintervalnum)
			t2num = random.choice(range(t1num+1,w+1))

			t1 = nodes[2*t1num-2]
			t2 = nodes[2*t2num-1]

			rearrangedC.append(t1)

			#now concantenate a list of all the intergers outside of the [t1num, t2num]
			permutedintermediate = range(1,t1num) + range(t2num+1,totalintervalnum+1)
			
			permutedintermediate = random.sample(permutedintermediate,(subsetlength -2))
			#loop through and generate the rearranged chromosome
			for intervalnum in permutedintermediate:
				#add tail (2n-1) to rearrangedC, and then head (2n-1)
				#again have to do an additonal -1 on both things to index into the array correctly				
				
				#randomly pick head/tail of the next seq to add
				choice = int(.5 > random.random())
				rearrangedC.append(nodes[2*intervalnum-1-(1-choice)]) #tail
				rearrangedC.append(nodes[2*intervalnum-1-choice]) #head

				# rearrangedC.append(nodes[2*intervalnum-1]) #head
				# rearrangedC.append(nodes[2*intervalnum-2]) #tail

			#add last node on
			rearrangedC.append(t2)
			####### REVERSE! CHANGE THIS LATER
			rearrangedC.reverse()
			return (t1_orientation, rearrangedC)

		if t1_orientation == "heads":
			#choose where it is - it can be anywhere except the very beginning
			t1num = random.choice(range(2,totalintervalnum+1))
			#anywhere to the left of t1num that leaves enough space in the complement of the interval [t2num, t1num]			t2num =  
			#choose range of tails
			#w is the max length of ranges of values that t2 can assume
			w = totalintervalnum - subsetlength + 1
			#truncate the range to be within n
			w = max(t1num - w, 1)
			
			t2num = random.choice(range(w, t1num))
			
			t1 = nodes[2*t1num-1] #heads
			t2 = nodes[2*t2num-2] #tail

			rearrangedC.append(t1)

			#now concantenate a list of all the intergers outside of the [t1num, t2num]
			permutedintermediate = range(1,t2num) + range(t1num+1,totalintervalnum+1)
			
			permutedintermediate = random.sample(permutedintermediate,(subsetlength -2))
			#loop through and generate the rearranged chromosome
			for intervalnum in permutedintermediate:
				#add tail (2n-1) to rearrangedC, and then head (2n-1)
				#again have to do an additonal -1 on both things to index into the array correctly				
				
				#randomly pick head/tail of the next seq to add
				choice = int(.5 > random.random())
				rearrangedC.append(nodes[2*intervalnum-1-(1-choice)]) #tail
				rearrangedC.append(nodes[2*intervalnum-1-choice]) #head

				# rearrangedC.append(nodes[2*intervalnum-1]) #head
				# rearrangedC.append(nodes[2*intervalnum-2]) #tail
				
			#add last node on
			rearrangedC.append(t2)

			####### REVERSE! CHANGE THIS LATER
			# rearrangedC.reverse()
			
			return (t1_orientation, rearrangedC)

 
	def initiateNodes(self):
		#INPUT: extracts n and m from self object, 
		#OUTPUT: returns two lists: 
			#node_list - list of 2 * n node objects, in which adjacent nodes of "head"/"tail" link to each other
			#interval list - list of n edges, which reference two nodes 
		n =	2* self.n
		IntervalList= []
		RefList= []
		nodelist = [Node() for i in xrange(n)]
		for i in xrange(1,n-1,2):
			#reference every even node in nodelist, have it point back for Interval, and forward
			#for RefEdge, unless its the last one
			IntervalEdge = Edge(nodelist[i],nodelist[i-1])
			RefEdge = Edge(nodelist[i],nodelist[i+1])
			nodelist[i].interval = IntervalEdge
			nodelist[i-1].interval = IntervalEdge

			nodelist[i].reference = RefEdge
			nodelist[i-1].reference = RefEdge
			RefList.append(RefEdge)
			IntervalList.append(IntervalEdge)
			
		#get last node
		IntervalEdge = Edge(nodelist[n-1],nodelist[n-2])
		nodelist[n-1].interval = IntervalEdge
		nodelist[n-2].interval = IntervalEdge
		IntervalList.append(IntervalEdge)

		return nodelist, IntervalList, RefList
		
class Node(object):
	"""docstring for Node: contains information about different types of edges
	connected: adj list, reference edge, interval edge (internal to same interval)"""
	
	counter = 1
	orientation = "head"
	orientationdict = {"head": "tail", "tail":"head"}
	def __init__(self):
		super(Node, self).__init__()
		self.counter = Node.counter  
		Node.counter += 1

		self.adjlist = []
		self.reference = None
		self.interval = None

		self.orientation = Node.orientation
		Node.orientation = Node.orientationdict[Node.orientation]
	def __str__(self):
		return "Node: " + str(self.counter) + "/" + self.orientation


class Edge(object):
	"""docstring for Edge"""
	def __init__(self, Node1, Node2):
		super(Edge, self).__init__()
		self.Node1 = Node1
		self.Node2 = Node2
	def __str__(self):
		return "(" + str(self.Node1) + "-" + str(self.Node2) + ")"

class DirectedEdge(Edge):
	"""docstring for DirectedEdge: adds a direction of an arc pointing from Node1 (tail) to Node2 (head)"""
	def __init__(self, Node1,Node2):
		super(DirectedEdge, self).__init__(Node1,Node2)
		self.head = Node2
		self.tail = Node1

				
#Test Cases

if __name__ == '__main__':

	a = Node()
	print a.counter
	print a.orientation

	b = Node()
	print b.counter
	print b.orientation


	c = Node()
	print c.counter
	print c.orientation

	Node.counter = 1

	#
	m = 5 #Substring Length
	n = 10 #Overall Str Length

	g = Graph(n)
	g.createAdjacencyandMutation(m,2)
	print map(lambda x: str(x),g.NodeList)

	print map(lambda x: str(x),g.RefList)
	print map(lambda x: str(x),g.IntervalList)

	#print g.printChromosome(*g.genChromosome(2))
	#tests if the length of chromosome is as expected
	print len(g.shuffledChrom) == 2*m -2
	#print g.printChromosome(*g.genChromosome(3))

	#Test Sort
	print "\n"
	print "Testing sorting code:"
	print "------------------------------------------------------"
	p = 100

	print "Option2"
	list1 = []
	g = Graph(n)
	
	for i in xrange(p):
		g.createAdjacencyandMutation(m,2)
		list1.append(g.Alternating)

	# 	print g.printChromosome()
	# 	print g.printObjlist(g.adjacencyList)
	# 	print g.Alternating
	# 	print g.AltMsg
	# 	print("\n")
	print "Run Option 2 " + str(p) + " times and see the percentage of valid H/T Seq"	
	print float(sum(list1))/float(p)

	print "Option3"	
	list1 = []
	for i in xrange(p):
		g.createAdjacencyandMutation(m,2)
		list1.append(g.Alternating)
		# print g.printChromosome()
		# print g.printObjlist(g.adjacencyList)
		# print filter((lambda x: x[1]==2), g.NodeDegreeDict.items())
		# print g.Alternating
		# print g.AltMsg
		# print("\n")
	print "Run Option 3 " + str(p) + " times and see the percentage of valid H/T Seq"	
	print float(sum(list1))/float(p)


	#test ability of testHeadTails to detect breaks in h/t
	n = 15
	m = 9
	g = Graph(n)
	g.createAdjacencyandMutation(m,3)
	#Test 2 valid substring case
	testadjlist = [Edge(g.NodeList[1],g.NodeList[4]),Edge(g.NodeList[2],g.NodeList[5]),
	Edge(g.NodeList[6],g.NodeList[11]),Edge(g.NodeList[7],g.NodeList[8]),Edge(g.NodeList[9],g.NodeList[12])]

	Nodedict = g.recordNodeDegrees(g.preProcessIntervalList(),testadjlist)

	truthvalue, listoflists = g.testHeadTails(Nodedict)
	print truthvalue
	print map(lambda x: g.printObjlist(x), listoflists)

	#Test 1 valid substring case
	testadjlist = [Edge(g.NodeList[1],g.NodeList[4]),Edge(g.NodeList[2],g.NodeList[5]),
	Edge(g.NodeList[6],g.NodeList[9]),Edge(g.NodeList[7],g.NodeList[10]),Edge(g.NodeList[11],g.NodeList[12])]

	Nodedict = g.recordNodeDegrees(g.preProcessIntervalList(),testadjlist)

	truthvalue, listoflists = g.testHeadTails(Nodedict)
	print truthvalue
	print map(lambda x: g.printObjlist(x), listoflists)


	#test edge removal, and seeing if 
	g = Graph(n)
	g.createAdjacencyandMutation(m,3,remove=1)

	print "test longest length"
	print g.emitLongestLength()
	
	"expected longest length = m*2-2-numberRemoved*2"
	print map(lambda x: g.printObjlist(x),g.mutateChromosome)
	print map(lambda x: g.printObjlist(x),g.List)
	
	g.alterChromosome()
	print g.printalteredChromosome()
	
	#test us some adding edges
	g.createAdjacencyandMutation(m,3,add=1)
	g.alterChromosome()
	print g.printalteredChromosome()





#--------------------------------------(work in progress, trying to get the data for d3)

#print "OPT3: t11_orientation: " +g.t11_orientation + ", List: " + str(map(lambda x: str(x),g.shuffledChrom2))

# print json.dumps([2,3,4,5,6])

# class MyEncoder(json.JSONEncoder):
#     def default(self, o):
#         return o.__dict__   

# a = MyEncoder().encode(Node())
# print a
