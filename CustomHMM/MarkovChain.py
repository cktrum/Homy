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
		self.transitionProb = np.matrix(transitionProbMatrix)

	def getNStates(self):
		nS = self.transitionProb.shape[0]
		return nS

	def getNextStates(self):
		return self.getNStates()

	def isLeftRight(self):
		lowLeft = np.tril(self.transitionProb, -1)
		lr = np.all(lowLeft[:] == 0)

		return lr
		
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

	def finiteDuration(self, mc):
		fd = mc.transitionProb.shape[1] == mc.transitionProb.shape[0] + 1
		if fd:
			#fd = np.full(np.sum(mc.transitionProb[:,-1])) > 0
			fd = np.sum(mc.transitionProb[:,-1]) > 0
		return fd

	def adaptStart(self, mc):
		aS = {'pI': [], 'pS': []}
		aS['pI'] = np.zeros(mc.initialProb.shape)
		aS['pS'] = np.zeros(mc.transitionProb.shape)

		return aS

	def adaptAccum(self, mc, aState, pX):
		T = pX.shape[1]
		nStates = mc.getNStates()
		A = mc.transitionProb

		alphaHat, c = self.forward(mc, pX)
		betaHat = self.backward(mc, pX, c)

		gamma = np.multiply(alphaHat, np.multiply(betaHat, np.tile(c[0,0:T], (nStates, 1))))
		aState['pI'] = aState['pI'] + gamma[:,1]

		pXbH = np.multiply(pX[:,1:], betaHat[:,1:])
		aHpXbH = alphaHat[:,0:T-1] * pXbH.T
		xi = np.multiply(aHpXbH, A[:,0:nStates])
		aState['pS'][:,0:nStates] = aState['pS'][:,0:nStates] + xi

		if self.finiteDuration(mc):
			aState['pS'][:,nStates] = aState['pS'][:,nStates] + (np.multiply(np.matrix(alphaHat[:,T-1]), betaHat[:,T-1]) * c[0,T-1]).T

		lP = np.sum(np.log(c))

		return (aState, gamma, lP)


	def adaptSet(self, mc, aState):
		mc.initialProb = np.divide(aState['pI'], np.sum(aState['pI']))
		mc.transitionProb = np.divide(aState['pS'], np.tile(np.matrix(np.sum(aState['pS'], axis=1)).T, (1, aState['pS'].shape[1])))

		return mc

	def forward(self, mc, pX):
		pX = np.matrix(pX)
		T = pX.shape[1] # number of observations
		
		# Initialisation
		nS = mc.getNStates()
		c = np.zeros((1, T))
		alphaHat = np.matrix(np.zeros((nS, T)))
		alphaTmp = np.zeros((nS, 1))

		alphaTmp = np.multiply(pX[:,0], mc.initialProb)
		c[0,0] = np.sum(alphaTmp, axis=0)[0,0]
		alphaHat[:,0] = alphaTmp / c[0,0]

		# forward pass
		for t in range(1, T):
			for j in range(	nS):
				sumRes = np.sum(np.multiply(mc.transitionProb[:,j], alphaHat[:,t-1]), axis=0)
				alphaTmp[j,0] = np.multiply(pX[j,t], sumRes.T)
			c[0,t] = np.sum(alphaTmp)
			alphaHat[:,t] = alphaTmp / c[0,t]

		# termination
		if mc.transitionProb.shape[1] > nS:
			cEnd = np.sum(np.multiply(alphaHat[:,T-1], mc.transitionProb[:,nS]))
			c = np.concatenate((c, np.matrix(cEnd)), axis=1)

		return (alphaHat, c)

	def backward(self, mc, pX, c):
		T = pX.shape[1]
		nS = mc.getNStates()
		q = mc.initialProb
		A = mc.transitionProb
		fin = mc.finiteDuration(mc)
		betaHat = np.matrix(np.zeros((nS, T)))
		if not fin:
			betaHat[:, T-1] = np.ones((nS, 1)) / c[0,T-1]
		else:
			betaHat[:, T-1] = np.matrix(A[:, nS]) / (c[0,T-1] * c[0,T])

		for t in range(T-2, -1, -1):
			for i in range(nS):
				betaHat[i,t] = A[i, 0:nS] * (np.multiply(np.matrix(pX[:,t+1]).T, betaHat[:,t+1])) / c[0,t]

		return betaHat