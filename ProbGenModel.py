import abc
import pdb
import numpy as np
import math

class ProbGenModel():
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def rand(self, pM, nX):
		return X

	@abc.abstractmethod
	def logprob(self, pM, x):
		return lP

	def prob(self, pD, x):
		logP = pD[0,0].logprob(pD, x)
		logS = np.max(logP, axis=0)
		logP = logP - logS # TODO: match size
		for r in range(logP.shape[0]):
				for c in range(logP.shape[1]):
					if math.isnan(logP[r,c]):
						logP[r,c] = 0

		if logP.shape[0] == 1:
			if np.isinf(logS):
				p = np.zeros((logP.shape))
			else:
				p = np.exp(logP)

		else:
			p = np.exp(logP)
			for r in range(logP.shape[0]):
				for c in range(logP.shape[1]):
					if math.isnan(logP[r,c]):
						logP[r,c] = 0

		return (p, logS)