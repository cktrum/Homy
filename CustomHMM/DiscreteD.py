import pdb
import numpy as np

from ProbDistr import ProbDistr

class DiscreteD(ProbDistr):
	def __init__(self, pMass):
		self.pD = dict()
		if isinstance(pMass, DiscreteD):
			self.pD['probMass'] = pMass
		else:
			if pMass.shape[0] == 1 or pMass.shape[1] == 1:
				self.pD['probMass'] = pMass
			else:
				self.pD = np.repmat(pD, pMass.shape[0], 1)
				for i in range(pMass.shape[0]):
					self.pD[i, 1]['probMass'] = pMass[i,:].T

	def getPd(self):
		return self.pD

	def init(self, pD, x):
		nObj = size(pD)
		if x.shape[0] > 1:
			print 'DiscreteD object can have only scalar data'

		x = round(x)
		maxObs = max(x)
		fObs = np.zeros((maxObs, 1))
		for m in range(maxObs):
			fObs[m] = 1 + np.sum(x == m)

		if nObj == 1:
			pD['probMass'] = fObs
		else:
			if nObj > maxObs:
				print 'Some DiscreteD objects initialised equal'
			for i in range(nObj):
				m = 1 + mod(i-1, maxObs)
				p = fObs
				p[m] = 2 * p[m]
				pD[i]['probMass'] = p

		return pD

	def rand(self, pD, nData):
		elements = range(1, pD['probMass'].shape[1]+1)
		distr = pD['probMass'].tolist()[0]
		numbers = np.random.choice(elements, nData, p=distr).tolist()
		if len(numbers) == 1:
			return numbers[0]
		else:
			return numbers

	def logprob(self, pD, z):
		lP = log(pD.prob(pD, z))
		return lP