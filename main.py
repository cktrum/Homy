import numpy as np
from MarkovChain import MarkovChain
from GaussD import GaussD
from HMM import HMM

def finite_duration():
	initMatrix = np.matrix([[0.75], [0.25]])
	transitionMatrix = np.matrix([[0.4, 0.4, 0.2], [0.1, 0.6, 0.3]])
	markovChain = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([0]), stdev=np.matrix([1]))
	g2 = GaussD(mean=np.matrix([3]), stdev=np.matrix([2]))
	h = HMM(markovChain, np.matrix([[g1], [g2]]))
	[X,S] = h.rand(100)
	print 'X =', X
	print 'S =', S

	return (X,S)

def multi_dim_observation():
	initMatrix = np.matrix([[0.75], [0.25]])
	transitionMatrix = np.matrix([[0.99, 0.01], [0.03, 0.97]])
	markovChain = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([[0], [0]]), cov=np.matrix([[2, 1], [1, 4]]))
	g2 = GaussD(mean=np.matrix([[3], [3]]), cov=np.matrix([[2, 1], [1, 4]]))
	h = HMM(markovChain, np.matrix([[g1], [g2]]))
	[X,S] = h.rand(100)
	print 'X =', X
	print 'S =', S

	return (X,S)

if __name__ == "__main__":
	#(X,S) = finite_duration()
	(X,S) = multi_dim_observation()