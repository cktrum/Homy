import pdb
import numpy as np
import math
from ProbDistr import ProbDistr

class GaussD(ProbDistr):
	def __init__(self, mean=None, stdev=None, cov=None):
		# default values
		self.probDist = dict()
		self.probDist['mean'] = 0.0
		self.probDist['stdev'] = 1.0
		self.probDist['covEigen'] = 1.0

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
				if isinstance(pD[0,i].probDist['covEigen'], float):
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
		try:
			nObj = len(pD)
			iOK = np.zeros((pD.shape))
		except:
			nObj = 1
			iOK = [0]
		
		if nObj > x.shape[1]:
			print 'too few data vectors'
		if x.shape[1] == 1:
			print 'GaussD:Init:TooFewData - only one point: default variance = 1'
			varX = np.ones((x.shape))
			iOK[0] = 0
		else:
			varX = np.var(x, axis=1)
			iOK[0] = 1

		if nObj == 1:
			pD.probDist['mean'] = np.mean(x, axis=1)
			if self.allowsCorr(pD):
				pD.probDist['cov'] = np.diag(varX)
			else:
				pD.probDist['var'] = varX
				pD.probDist['stdev'] = np.sqrt(np.abs(varX))
				if type(pD.probDist['covEigen']) != float:
					transpose = pD.probDist['covEigen'].T
				else:
					transpose = pD.probDist['covEigen']
				pD.probDist['cov'] = pD.probDist['covEigen'] * np.diagflat(np.square(pD.probDist['stdev'])) * transpose
		else:
			print 'Not implemented yet'
			#TODO VQ methods

		return (pD, iOK)

	def setCov(self, c):
		if c.shape[0] != c.shape[1]:
			print 'Covariance must be square'

		if not np.isreal(c):
			print 'Covariance must be real-valued'

		if np.maximum(np.maximum(np.abs(c - c.T))) < 0.0001 * np.maximum(np.maximum(np.abs(c + c.T))):
			(v, pD.probDist['covEigen']) = np.linalg.eig(0.5 * (c+c.T))
			maxImag = np.maximum(np.abs(np.imag(pD.probDist['covEigen'][:])))
			if not np.isreal(pD.probDist['covEigen']):
				print 'GaussD:setCov - Covariance eigenvectors forced to real. Max error:', maxImag
				pD.probDist['covEigen'] = np.real(pD.probDist['covEigen'])

			pD.probDist['stdev'] = np.sqrt(np.abs(np.diagflat(v)))

		else:
			print 'Covariance must be symmetric'

	def allowsCorr(self, pD):
		try:
			pDsize = pD.shape
		except:
			pDsize = (1,1)
		nObj = np.prod(pDsize)
		C = np.zeros((pDsize))

		for i in range(nObj):
			if pDsize == (1,1):
				if type(pD.probDist['covEigen']) != float:
					covEigenShape = pD.probDist['covEigen'].shape
				else:
					covEigenShape = (1,1)
			else:
				if type(pD[i,0].probDist['covEigen']) != float:
					covEigenShape = pD[i,0].probDist['covEigen'].shape
				else:
					covEigenShape = (1,1)

			C[i] = not np.all(np.array(covEigenShape) == 1)
		return C

	def adaptStart(self, pD):
		try:
			nObj = len(pD)
		except:
			nObj = 1

		aState = np.tile({'sumDev': 0, 'sumSqDev': 0, 'sumWeight': 0}, (nObj, 1))
		if nObj == 1:
			if type(pD.probDist['mean']) == float:
				dSize = 1
			else:
				dSize = len(pD.probDist['mean'])
			aState[i,0]['sumDev'] = np.zeros((dSize, 1))
			aState[i,0]['sumSqDev'] = np.zeros((dSize, dSize))
			aState[i,0]['sumWeight'] = 0
		else:
			for i in range(nObj):
				if type(pD[i,0].probDist['mean']) == float:
					dSize = 1
				else:
					dSize = len(pD[i,0].probDist['mean'])
				aState[i,0]['sumDev'] = np.zeros((dSize, 1))
				aState[i,0]['sumSqDev'] = np.zeros((dSize, dSize))
				aState[i,0]['sumWeight'] = 0

		return aState

	def adaptAccum(self, pD, aState, obsData, obsWeight=None):
		[dSize, nData] = obsData.shape
		try:
			nObj = len(pD)
		except:
			nObj = 1

		if obsWeight is None:
			if nObj == 1:
				obsWeight = np.ones((nObj, nData))
			else:
				obsWeight = pD[0,0].prob(pD, obsData)
				obsWeight = np.divide(obsWeight, np.tile(np.sum(obsWeight), (nObj, 1)))

		for i in range(nObj):
			if nObj == 1:
				dev = obsData - np.tile(pD.probDist['mean'], (1, nData))
			else:
				dev = obsData - np.tile(pD[i,0].probDist['mean'], (1, nData))
			wDev = np.multiply(dev, np.tile(obsWeight[i,:], (dSize, 1)))
			aState[i,0]['sumDev'] = aState[i,0]['sumDev'] + np.sum(wDev, axis=1)
			aState[i,0]['sumSqDev'] = aState[i,0]['sumSqDev'] + dev * wDev.T
			aState[i,0]['sumWeight'] = aState[i,0]['sumWeight'] + np.sum(obsWeight[i,:])

		return aState

	def adaptSet(self, pD, aState):
		try:
			nObj = len(pD)
		except:
			nObj = 1
			tmp = pD
			pD = np.matrix((1,1))
			pD[0,1] = tmp

		for i in range(nObj):
			if aState[i,0]['sumWeight'] > np.amax(np.spacing(np.array(pD[i,0].probDist['mean']))):
				pD[i,0].probDist['mean'] = pD[i,0].probDist['mean'] + aState[i,0]['sumDev'] / aState[i,0]['sumWeight']

				S2 = aState[i,0]['sumSqDev'] - np.divide((aState[i,0]['sumDev'] * aState[i,0]['sumDev'].T), aState[i,0]['sumWeight'])
				covEstim = np.divide(S2, aState[i,0]['sumWeight'])
				if np.any(np.diag(covEstim) < np.spacing(np.array(pD[i,0].probDist['mean']))):
					print 'GaussD: ZeroVar', 'Not enough data for GaussD #', i, '. StDev forced to inf'
					if type(pD[i,0].probDist['mean']) == float:
						covEstim = np.diagflat(np.tile(sys.float_info.max, (1,1)))
					else:
						covEstim = np.diagflat(np.tile(sys.float_info.max, pD[i,0].probDist['mean'].shape))

				if self.allowsCorr(pD[i,0]):
					pD[i,0] = self.setCov(covEstim)
				else:
					pD[i,0].probDist['stdev'] = np.matrix(np.sqrt(np.diag(covEstim))).T

		if nObj == 1:
			return pD[i,0]
		else:
			return pD