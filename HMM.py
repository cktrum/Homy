import pdb
import math
import numpy as np
from ProbGenModel import ProbGenModel

class HMM(ProbGenModel):
	def __init__(self, markovChain, outputDist):
		self.stateGen = markovChain
		self.outputDist = outputDist

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
			hmmSize = hmm.shape[1]
		except:
			hmmSize = 1
		T = x.shape[1]
		logP = np.zeros((hmmSize))
		if hmmSize == 1:
			p, logS = hmm.outputDist[0,0].prob(hmm.outputDist, x)
			alphaHat, c = hmm.stateGen.forward(hmm.stateGen, p)
			logP[0] = np.sum(np.log(c)) + np.sum(logS)
		else:
			for i in range(hmmSize):
				p, logS = hmm[0,i].outputDist[0,0].prob(hmm[0,i].outputDist, x)
				alphaHat, c = hmm[0,i].stateGen.forward(hmm[0,i].stateGen, p)
				logP[i] = np.sum(np.log(c)) + np.sum(logS)

		return logP