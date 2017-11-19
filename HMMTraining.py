import numpy as np

from MarkovChain import MarkovChain
from HMM import HMM

import pdb

class HMMTraining():
	def makeLeftRightHMM(self, nStates, pD, obsData, lData=None):
		if nStates <= 0:
			print 'Number of states must be > 0'
		if lData is None:
			lData = obsData.shape[1]

		D = np.mean(lData)
		D = D / nStates
		mc = self.initLeftRightMC(nStates, D)
		hmm = HMM(mc, pD)
		hmm = hmm.init(hmm, obsData, lData)

		hmm, logprobs = hmm.train(hmm, obsData, lData, 5, np.log(1.01))
		
		return hmm


	def initLeftRightMC(self, nStates, stateDuration=None):
		defaultDuration = 10.0
		if nStates <= 1:
			print 'Number of states must be > 1'
		if stateDuration is None:
			stateDuration = defaultDuration
		if type(stateDuration) == float or type(stateDuration) == np.float64 or len(stateDuration) == 1:
			stateDuration = np.tile(stateDuration, (nStates, 1))
		elif len(stateDuration) != nStates:
			print 'Incompatible length of state durations'

		minDiagProb = 0.1
		D = np.maximum(np.ones((stateDuration.shape)), stateDuration)
		aii = np.maximum(np.ones((D.shape)) * minDiagProb, np.divide((D-1), D))
		aij = (1-aii)
		aij = np.diagflat(aij, 1)
		aij = aij[0:nStates, :]
		A = np.concatenate((np.diagflat(aii), np.zeros((nStates, 1))), axis=1) + aij
		p0 = np.concatenate((np.matrix([1]), np.zeros((nStates-1,1))), axis=0)

		mc = MarkovChain(p0, A)

		return mc

	def validateModels(self, hmms, testSet, testSequences, testLabels, labelIndices):
		numClasses = hmms.shape[1]
		confusionMatrix = np.zeros((numClasses, numClasses))

		for i in range(len(testLabels)):
			sample = self.extractSample(testSet, testSequences, i)
			prob, c = self.classify(hmms, sample)
			idx = labelIndices[testLabels[i]]
			confusionMatrix[idx,c] = confusionMatrix[idx,c] + 1

		return confusionMatrix

	def extractSample(self, data, subSequences, index):
		if index == 0:
			first = 0
		else:
			first = np.sum(subSequences[0:index])

		last = first + subSequences[index]
		sample = data[:, first:last]

		return sample

	def classify(self, hmms, sample):
		logprobs = hmms[0,0].logprob(hmms, sample)
		prob = np.amax(logprobs)
		label = logprobs.argmax()

		return (prob, label)