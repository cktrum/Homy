import pdb

import sys
import numpy as np
from SpeechFeatures import SpeechFeatures
from MarkovChain import MarkovChain
from GaussD import GaussD
from HMM import HMM
from Dataset import Dataset
from HMMTraining import HMMTraining

import matplotlib.pyplot as plt

def finite_duration():
	initMatrix = np.matrix([[0.75], [0.25]])
	transitionMatrix = np.matrix([[0.4, 0.4, 0.2], [0.1, 0.6, 0.3]])
	markovChain = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([0]), stdev=np.matrix([1]))
	g2 = GaussD(mean=np.matrix([3]), stdev=np.matrix([2]))
	h = HMM(markovChain, np.matrix([[g1], [g2]]))
	[X,S] = h.rand(h, 100)

	return (X,S)

def multi_dim_observation():
	initMatrix = np.matrix([[0.75], [0.25]])
	transitionMatrix = np.matrix([[0.99, 0.01], [0.03, 0.97]])
	markovChain = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([[0], [0]]), cov=np.matrix([[2, 1], [1, 4]]))
	g2 = GaussD(mean=np.matrix([[3], [3]]), cov=np.matrix([[2, 1], [1, 4]]))
	h = HMM(markovChain, np.matrix([[g1], [g2]]))
	[X,S] = h.rand(h, 100)

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
	#plt.figure()
	#plt.title(title)
	#plt.imshow(cepstragram[0].T, origin='lower')
	#plt.axis('auto')
	features = sf.dynamic_features(cepstragram)

def test_forward():
	
	initMatrix = np.matrix([[1.0], [0]])
	transitionMatrix = np.matrix([[0.9, 0.1, 0], [0, 0.9, 0.1]])
	mc = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([0]), stdev=np.matrix([1]))
	g2 = GaussD(mean=np.matrix([3]), stdev=np.matrix([2]))

	# output sequence
	x = np.matrix([-0.2, 2.6, 1.3])
	pX, logS = g1.prob(np.matrix([g1, g2]), x)
	alphaHat, c = mc.forward(mc, pX)
	print 'alphaHat:', alphaHat, 'expected: [1 0.3847 0.4189; 0 0.6153 0.5811]'
	print 'c:', c, 'expected: [1 0.1625 0.8266 0.0581]'

	h = HMM(mc, np.matrix([[g1], [g2]]))
	# logP = P(X|h)
	logP = h.logprob(h, x)
	print 'logP: ', logP, 'expected: -9.1877'
	
	initMatrix = np.matrix([[1.0], [0]])
	transitionMatrix = np.matrix([[0.0, 1.0, 0.0], [0.0, 0.7, 0.3]])
	x = np.matrix([-0.2, 2.6, 1.3])
	mc = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([0]), stdev=np.matrix([1]))
	g2 = GaussD(mean=np.matrix([3]), stdev=np.matrix([1]))
	h1 = HMM(mc, np.matrix([[g1], [g2]]))

	transitionMatrix = np.matrix([[0.5, 0.5, 0.0], [0.0, 0.5, 0.5]])
	mc2 = MarkovChain(initMatrix, transitionMatrix)
	g3 = GaussD(mean=np.matrix([0]), stdev=np.matrix([1]))
	g4 = GaussD(mean=np.matrix([3]), stdev=np.matrix([1]))
	h2 = HMM(mc2, np.matrix([[g3], [g4]]))

	logP = h1.logprob(np.matrix([h1, h2]), x)
	print 'logP:', logP, 'expected: [-5.562463348 -6.345037882]'

def test_backward():
	initMatrix = np.matrix([[1.0], [0]])
	transitionMatrix = np.matrix([[0.9, 0.1, 0], [0, 0.9, 0.1]])
	x = np.matrix([-0.2, 2.6, 1.3])
	c = np.matrix([1.0, 0.1625, 0.8266, 0.0581])

	mc = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([0]), stdev=np.matrix([1]))
	g2 = GaussD(mean=np.matrix([3]), stdev=np.matrix([2]))

	pX, logS = g1.prob(np.matrix([[g1], [g2]]), x)
	betaHat = mc.backward(mc, pX, c)
	print 'betaHat:', betaHat
	print 'expected: [1.0003 1.0393 0; 8.4182 9.3536 2.0822]'

	initMatrix = np.matrix([[1.0], [0]])
	transitionMatrix = np.matrix([[0.9, 0.1], [0.1, 0.9]])
	x = np.matrix([-0.2, 2.6, 1.3])
	
	mc = MarkovChain(initMatrix, transitionMatrix)
	g1 = GaussD(mean=np.matrix([0]), stdev=np.matrix([1]))
	g2 = GaussD(mean=np.matrix([3]), stdev=np.matrix([2]))

	pX, logS = g1.prob(np.matrix([g1, g2]), x)
	alphaHat, c = mc.forward(mc, pX)
	betaHat = mc.backward(mc, pX, c)
	print 'betaHat:', betaHat
	print 'expected: [1.0 6.798238264 1.125986646; 5.223087455 5.75095566 1.125986646]'

def trainHMMs():
	hmmTraining = HMMTraining()
	defaultGaussD = GaussD()
	data = Dataset('./Recordings/Commands/')
	labels = data.getLabels()
	states = [3]
	hmms = []
	testSet_features = None
	testSet_sequences = None
	testLabels = []
	
	for i in range(len(labels)):
		(training, validation, test) = data.partitionDataset(labels[i])
		trainingFeatures = training['features']
		trainingSeq = training['sequences']
		hmm = hmmTraining.makeLeftRightHMM(states[i], defaultGaussD, trainingFeatures, trainingSeq)
		hmms.append(hmm)
		
		if testSet_features is None:
			testSet_features = test['features']
			testSet_sequences = test['sequences']
		else:
			testSet_features = np.concatenate((testSet_features, test['features']), axis=1)
			testSet_sequences = np.concatenate((testSet_sequences, test['sequences']), axis=1)
		testLabels.append([labels[i]] * len(test['sequences']))

	hmms = np.matrix(hmms)
	confusionMatrix = hmmTraining.validateModels(hmms, testSet_features, testSet_sequences, testLabels)
	
	print "confusionMatrix", confusionMatrix
	plt.imshow(confusionMatrix)
	plt.show()

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		mode = 1
	else:
		mode = sys.argv[1]

	if mode == '1':
		(X,S) = finite_duration()
		print 'X =', X
		print 'S =', S
		
		(X,S) = multi_dim_observation()
		print 'X =', X
		print 'S =', S
	elif mode == '2':	
		extract_features('./Recordings/Commands/play/play1.wav', 'play1')
		#plt.show()
	elif mode == '3':
		test_forward()
	elif mode == '4':
		test_backward()
	elif mode == '5':
		trainHMMs()