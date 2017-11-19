import pdb
import math
import sys
import numpy as np
from ProbGenModel import ProbGenModel

class HMM(ProbGenModel):
	def __init__(self, markovChain, outputDist):
		self.stateGen = markovChain
		self.outputDist = outputDist

	def init(self, hmm, xT, lxT=None):
		try:
			outputDistSize = hmm.outputDist.shape[0]
		except:
			outputDistSize = 1

		if lxT is None:
			lxT = xT.shape[1]

		if outputDistSize != hmm.stateGen.getNextStates():
			if outputDistSize == 1:
				hmm.outputDist = np.tile(hmm.outputDist, (hmm.stateGen.getNextStates(), 1))
			else:
				hmm.outputDist = np.tile(hmm.outputDist[0], (hmm.stateGen.getNextStates(), 1))

		if hmm.stateGen.isLeftRight():
			hmm = self.initLeftRight(hmm, xT, lxT)
		else:
			hmm = self.initByCluster(hmm, xT, lxT)

		return hmm

	def rand(self, h, nSamples):
		# TODO: find a better way to determine size of output
		nOutput = h.outputDist[0][0,0].rand(h.outputDist[0][0,0], 1).shape[0]
		X = np.matrix(np.zeros((nOutput, nSamples)))
		S = h.stateGen.rand(h.stateGen, nSamples)
		if len(S) == 0:
			print('Your state sequence begins with an end state')
			return ([], [])

		for i in range(nSamples):
			if S[i] == 0:
				if i > 0:
					S = S[0:i]
					X = X[:,0:i]
				else:
					print('Your state sequence begins with an end state')
				break

			idx = int(S[i]) - 1
			X[:,i] = h.outputDist[idx][0,0].rand(h.outputDist[idx][0,0], 1)

		return (X,S)

	def logprob(self, hmm, x):
		try:
			hmm.shape
			isMatrix = True
			hmmSize = hmm.shape[1]
		except:
			isMatrix = False
			hmmSize = 1

		T = x.shape[1]
		logP = np.zeros((hmmSize))
		if not isMatrix:
			p, logS = hmm.outputDist[0,0].prob(hmm.outputDist, x)
			alphaHat, c = hmm.stateGen.forward(hmm.stateGen, p)
			logP[0] = np.sum(np.log(c)) + np.sum(logS)
		else:
			for i in range(hmmSize):
				p, logS = hmm[0,i].outputDist[0,0].prob(hmm[0,i].outputDist, x)
				alphaHat, c = hmm[0,i].stateGen.forward(hmm[0,i].stateGen, p)
				logP[i] = np.sum(np.log(c)) + np.sum(logS)

		return logP

	def initLeftRight(self, hmm, obsData, lData):
		dSize = obsData.shape[0]
		nTrainingSeq = len(lData)
		startIndex = np.cumsum(np.concatenate(([0], lData), axis=0))
		nStates = hmm.stateGen.getNextStates()
		pD = hmm.outputDist

		for i in range(nStates):
			xT = np.zeros((dSize, 0))
			for r in range(nTrainingSeq):
				dStart = startIndex[r] + int(round(np.multiply(i, lData[r]) / nStates))
				dEnd = startIndex[r] + int(round((i+1) * lData[r] / nStates) - 1)
				xT = np.concatenate((xT, obsData[:, dStart:dEnd]), axis=1)
			(pD[i], iOK) = pD[i,0].init(pD[i,0], xT)

		hmm.outputDist = pD

		return hmm

	def initByCluster(self, hmm, obsData, lData):
		hmm.outputDist = hmm.outputDist.init(hmm.outputDist, obsData)
		for i in range(5):
			hTemp = hmm.train(hmm, obsData, lData, 1)
			hmm.outputDist = hTemp.outputDist

		return hmm

	def train(self, hmm, xT, lxT, nIterations=10, minStep=None):
		if minStep is None:
			minStep = sys.float_info.max
		else:
			minStep = minStep * xT.shape[1]

		ixT = np.cumsum(np.concatenate(([0], lxT), axis=0))
		logprobs = np.zeros((1, nIterations))
		logPold = -sys.float_info.max
		logPdelta = sys.float_info.max

		for nTraining in range(nIterations):
			aS = hmm.adaptStart(hmm)
			for r in range(len(lxT)):
				aS, logP = hmm.adaptAccum(hmm, aS, xT[:, ixT[r]:ixT[r+1]-1])
			logprobs[0,nTraining] = logprobs[0,nTraining] + logP
			logPdelta = logprobs[0,nTraining] - logPold
			logPold = logprobs[0,nTraining]
			hmm = hmm.adaptSet(hmm, aS)

		if not nTraining:
			nTraining = 0

		while logPdelta > minStep:
			nTraining = nTraining + 1
			logprobs[0,nTraining] = 0
			aS = hmm.adaptStart(hmm)
			for r in range(len(lxT)):
				aS, logP = hmm.adaptAccum(hmm, aS, xT[:, ixT[r]:ixT[r+1]-1])
			logprobs[0,nTraining] = logprobs[0,nTraining] + logP
			logPdelta = logprobs[0,nTraining] - logPold
			logPold = logprobs[0,nTraining]
			hmm = hmm.adaptSet(hmm, aS)

		return (hmm, logprobs)

	def adaptStart(self, hmm):
		aState = {'MC': [], 'Out': [], 'LogProb': 0}
		if type(hmm) != HMM:
			print 'Method works only for a single object'
		aState['MC'] = hmm.stateGen.adaptStart(hmm.stateGen)
		aState['Out'] = hmm.outputDist[0,0].adaptStart(hmm.outputDist)

		return aState

	def adaptAccum(self, hmm, aState, obsData):
		try:
			hmm.outputDist.shape
			isArray = True
		except:
			isArray = False

		if isArray is True:
			pX, lScale = hmm.outputDist[0,0].prob(hmm.outputDist, obsData)
		else:
			pX, lScale = hmm.outputDist.prob(hmm.outputDist, obsData)

		aState['MC'], gamma, logP = hmm.stateGen.adaptAccum(hmm.stateGen, aState['MC'], pX)
		
		if isArray is True:
			aState['Out'] = hmm.outputDist[0,0].adaptAccum(hmm.outputDist, aState['Out'], obsData, gamma)
		else:
			aState['Out'] = hmm.outputDist.adaptAccum(hmm.outputDist, aState['Out'], obsData, gamma)

		if len(lScale) == 1:
			aState['LogProb'] = aState['LogProb'] + logP + obsData.shape[1] * lScale
		else:
			aState['LogProb'] = aState['LogProb'] + logP + np.sum(lScale)

		logP = aState['LogProb']

		return (aState, logP)

	def adaptSet(self, hmm, aState):
		hmm.stateGen = hmm.stateGen.adaptSet(hmm.stateGen, aState['MC'])
		try:
			hmm.outputDist.shape
			hmm.outputDist = hmm.outputDist[0,0].adaptSet(hmm.outputDist, aState['Out'])
		except:
			hmm.outputDist = hmm.outputDist.adaptSet(hmm.outputDist, aState['Out'])

		return hmm