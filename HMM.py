import pdb
import numpy as np

class HMM():
	def __init__(self, markovChain, outputDist):
		self.stateGen = markovChain
		self.outputDist = outputDist

	def rand(self, nSamples):
		# TODO: find a better way to determine size of output
		nOutput = self.outputDist[0][0,0].rand(1).shape[0]
		X = np.matrix(np.zeros((nOutput, nSamples)))
		S = self.stateGen.rand(nSamples)
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
			X[:,i] = self.outputDist[idx][0,0].rand(1)

		return (X,S)