import pdb

import numpy as np
from SpeechFeatures import SpeechFeatures
from MarkovChain import MarkovChain
from GaussD import GaussD
from HMM import HMM
import matplotlib.pyplot as plt

def finite_duration():
	initMatrix = np.matrix([[0.75], [0.25]])
	transitionMatrix = np.matrix([[0.4, 0.4, 0.2], [0.1, 0.6, 0.3]])
	markovChain = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([0]), stdev=np.matrix([1]))
	g2 = GaussD(mean=np.matrix([3]), stdev=np.matrix([2]))
	h = HMM(markovChain, np.matrix([[g1], [g2]]))
	[X,S] = h.rand(100)

	return (X,S)

def multi_dim_observation():
	initMatrix = np.matrix([[0.75], [0.25]])
	transitionMatrix = np.matrix([[0.99, 0.01], [0.03, 0.97]])
	markovChain = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([[0], [0]]), cov=np.matrix([[2, 1], [1, 4]]))
	g2 = GaussD(mean=np.matrix([[3], [3]]), cov=np.matrix([[2, 1], [1, 4]]))
	h = HMM(markovChain, np.matrix([[g1], [g2]]))
	[X,S] = h.rand(100)

	return (X,S)

def extract_features(path, title):
	sf = SpeechFeatures()
	signal, fs, enc = sf.wavread(path)
	t = np.array(range(1,signal.shape[0])) / float(fs);
	#plt.plot(signal)

	winlength = 0.03 # 30ms
	
	## get spectram
	output = sf.getFeatures(signal, fs, winlength)
	spectram = output[0]
	log_energy = output[1]
	#plt.imshow(np.log(spectram.T), origin='lower', extent=[0, t[-1], 0, fs])
	#plt.xlabel('time [s]')
	#plt.ylabel('frequency [Hz]')
	#plt.axis('auto')

	## get cepstragram
	ncep = 13
	cepstragram = sf.getFeatures(signal, fs, winlength, ncep)
	plt.figure()
	plt.title(title)
	plt.imshow(cepstragram[0].T, origin='lower')
	plt.axis('auto')


if __name__ == "__main__":
	#(X,S) = finite_duration()
	#(X,S) = multi_dim_observation()
	
	#print 'X =', X
	#print 'S =', S

	extract_features('/home/claudia/Documents/Studium/Master/3.Semester/PatternRecognition/Project/Sounds/female.wav', 'female')
	extract_features('/home/claudia/Documents/Studium/Master/3.Semester/PatternRecognition/Project/Sounds/male.wav', 'male')
	plt.show()