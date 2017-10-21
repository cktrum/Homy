import pdb
import numpy as np
from DiscreteD import DiscreteD
from ProbGenModel import ProbGenModel

class MarkovChain(ProbGenModel):
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

	def rand(self, mc, T):
		S = np.zeros((1, T)) #space for resulting row vector
		nS = self.getNStates()
		
		# get initial state distribution
		obj = DiscreteD(mc.initialProb.T)
		dp = obj.getPd()

		# generate initial state S_1
		state = obj.rand(dp, 1);

		# continue only if it's not the end state
		if state < nS + 1:
			t = 0
			S[0,t] = state
			t = t + 1
			# generate a sequence of states until either t=T or end state is reached
			while t < T and state != nS + 1:
				obj = DiscreteD(mc.transitionProb[state-1, :])
				dp = obj.getPd()
				state = obj.rand(dp, 1)
				if state < nS + 1:
					S[0,t] = state
					t = t + 1

			S = S[0,0:t+1]
		else: # if the first state is the end state
			S = []

		return S

	def logprob(self, mc, S):
		if empty(S):
			lP = []
			return

		if np.any(S < 0) or np.any(S != round(S)):
			lP = np.repmat(-Inf, mc.shape)
			return

		lp = np.zeros((mc.shape))
		fromS = S[0:-2]
		toS = S[1:-1]
		for i in range(len(mc)):
			if S[0] > len(mc[i].initialProb):
				lP[i] = -float('inf')
			else:
				lP[i] = np.log(mc[i].initialProb[S[0]])

			if not fromS:
				if max(fromS) > mc[i].getNStates() or S[-1] > mc[i].transitionProb.shape[1]:
					lP[i] = -float('inf')
				else:
					dims = (mc[i].transitionProb.shape, S.shape[0], S.shape[1])
					iTrans = np.ravel_multi_index((mc[i].transitionProb.shape, fromS, toS), dims=dims, order='F')
					lP[i] = lP[i] + np.sum(np.log(mc[i].transitionProb[iTrans]))

		return lP

	def forward(self, mc, pX):
		pX = np.matrix(pX)
		T = pX.shape[1] # number of observations
		
		# Initialisation
		nS = mc.getNStates()
		c = np.zeros((1, T))
		alphaHat = np.matrix(np.zeros((nS, T)))
		alphaTmp = np.zeros((nS, 1))

		alphaTmp = np.multiply(pX[:,0], mc.initialProb)
		c[0,0] = np.sum(alphaTmp)
		alphaHat[:,0] = alphaTmp / c[0,0]

		# forward pass
		for t in range(1, T):
			for j in range(	nS):
				sumRes = np.sum(np.multiply(mc.transitionProb[:,j], alphaHat[:,t-1]), axis=0)
				alphaTmp[j] = np.multiply(pX[j,t], sumRes.T)
			c[0,t] = np.sum(alphaTmp)
			alphaHat[:,t] = alphaTmp / c[0,t]

		# termination
		if mc.transitionProb.shape[1] > nS:
			cEnd = np.sum(np.multiply(alphaHat[:,T-1], mc.transitionProb[:,nS]))
			c = np.concatenate((c, np.matrix(cEnd)), axis=1)

		return (alphaHat, c)