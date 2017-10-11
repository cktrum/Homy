import pdb
import numpy as np
from DiscreteD import DiscreteD

class MarkovChain():
	def __init__(self):
		self.initialProb = []
		self.transitionProb = []

	# initialise MarkovChain with given initial probability distribution as well as transition matrix
	def __init__(self, initialProbMatrix, transitionProbMatrix):
		self.initialProb = initialProbMatrix
		self.transitionProb = transitionProbMatrix

	def getNStates(self):
		nS = self.transitionProb.shape[0]
		return nS

	def rand(self, T):
		S = np.zeros((1, T)) #space for resulting row vector
		nS = self.getNStates()
		
		# get initial state distribution
		dp = DiscreteD(self.initialProb.T)

		# generate initial state S_1
		state = dp.rand(1);

		# continue only if it's not the end state
		if state < nS + 1:
			t = 0
			S[0,t] = state
			t = t + 1
			# generate a sequence of states until either t=T or end state is reached
			while t < T and state != nS + 1:
				dp = DiscreteD(self.transitionProb[state-1, :])
				state = dp.rand(1)
				if state < nS + 1:
					S[0,t] = state
					t = t + 1

			S = S[0,0:t+1]
		else: # if the first state is the end state
			S = []

		return S
