import pdb
import numpy as np

class GaussD():
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

	def rand(self, nData):
		R = np.random.randn(self.probDist['mean'].shape[0], nData) 	# normalized independent Gaussian random variables
		R = np.dot(np.diag(self.probDist['stdev']), R) 				# scaled to correct standard deviations
		R = self.probDist['covEigen'] * R 							# rotate to proper correlations
		R = R + np.tile(self.probDist['mean'], (1, nData)) 			# translate to desired mean

		return R
