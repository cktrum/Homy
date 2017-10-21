import pdb
import numpy as np
import math
from ProbDistr import ProbDistr

class GaussD(ProbDistr):
	def __init__(self, mean, stdev=None, cov=None):
		# default values
		self.probDist = dict()
		self.probDist['mean'] = 0
		self.probDist['stdev'] = 1
		self.probDist['covEigen'] = 1

		if mean is not None:
			self.probDist['mean'] = mean
		if stdev is not None:
			self.probDist['stdev'] = stdev
		if cov is not None:
			self.probDist['cov'] = cov
			[v, eigenVectors]=np.linalg.eig(0.5*(cov+cov.T))
			self.probDist['covEigen'] = eigenVectors
			self.probDist['stdev'] = np.sqrt(abs(v))

	def rand(self, pD, nData):
		R = np.random.randn(self.probDist['mean'].shape[0], nData) 	# normalized independent Gaussian random variables
		R = np.dot(np.diag(self.probDist['stdev']), R) 				# scaled to correct standard deviations
		R = self.probDist['covEigen'] * R 							# rotate to proper correlations
		R = R + np.tile(self.probDist['mean'], (1, nData)) 			# translate to desired mean

		return R

	def logprob(self, pD, x):
		if pD.shape[1] < pD.shape[0]:
			pD = pD.T
		nObj = pD.shape[1]
		nx = x.shape[1]
		logP = np.zeros((nObj, nx))
		for i in range(nObj):
			dSize = len(pD[0,i].probDist['mean'])

			if dSize == x.shape[0]:
				if isinstance(pD[0,i].probDist['covEigen'], int):
					covEigen = pD[0,i].probDist['covEigen']
				else:
					covEigen = pD[0,i].probDist['covEigen'].T

				z = covEigen * (x - np.tile(pD[0,i].probDist['mean'], (1, nx)))
				z = np.divide(z, np.tile(pD[0,i].probDist['stdev'], (1, nx)))
				logP[i,:] = - np.sum(np.multiply(z, z), axis=0) / 2
				logP[i,:] = logP[i,:] - np.sum(np.log(pD[0,i].probDist['stdev'])) - dSize * np.log(2*math.pi)/2
			else:
				print 'GaussD:WrongDataSize'
				logP[i,:] = np.tile(-float('inf'), (1, nx))

		return logP


	def init(self, pD, x):
		nObj = len(pD)
		iOK = np.zeros((pD.shape))
		if nObj > x.shape[1]:
			print 'too few data vectors'
		if x.shape[1] == 1:
			print 'GaussD:Init:TooFewData - only one point: default variance = 1'
			varX = np.ones((x.shape))
			iOK[0] = 0
		else:
			varX = var(x, axis=1)
			iOK[0] = 1

		if nObj == 1:
			pD['mean'] = np.mean(x, axis=1)
			if self.allowsCorr(pD):
				pD['cov'] = np.diag(varX)
			else:
				pD['var'] = varX
		else:
			print 'Not implemented yet'
			#TODO VQ methods

		return (pD, iOK)


	def allowsCorr(self, pD):
		pDsize = pD.shape
		nObj = np.prod(pDsize)
		C = np.zeros((pDsize))
		for i in range(nObj):
			C[i] = not np.all(pD[0,i]['covEigen'].shape == 1)

		return C