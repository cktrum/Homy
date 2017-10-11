import pdb
import numpy as np

class DiscreteD():
	def __init__(self, pMass):
		self.pD = dict()
		if isinstance(pMass, DiscreteD):
			self.pD['probMass'] = pMass
		else:
			if pMass.shape[0] == 1 or pMass.shape[1] == 1:
				self.pD['probMass'] = pMass
			else:
				self.pD = np.repmat(self.pD, pMass.shape[0], 1)
				for i in range(pMass.shape[0]):
					self.pD[i, 1]['probMass'] = pMass[i,:].T

	def rand(self, nData):
		elements = range(1, self.pD['probMass'].shape[1]+1)
		distr = self.pD['probMass'].tolist()[0]
		numbers = np.random.choice(elements, nData, p=distr).tolist()
		if len(numbers) == 1:
			return numbers[0]
		else:
			return numbers