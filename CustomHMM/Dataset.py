from os import listdir
from os.path import isfile, join
import numpy as np
import random

from SpeechFeatures import SpeechFeatures

import pdb

class Dataset():
	def __init__(self, pathToDirectory):
		self.commands = dict()
		labels = self.getAllFoldersAsLabels(pathToDirectory)
		for (label, path) in labels:
			files = self.allFilesForLabel(path, label)
			(features, sequences) = self.generateFeatures(files)
			self.commands[label] = {'files': [], 'features': [], 'sequences': []}
			self.commands[label]['files'] = files
			self.commands[label]['features'] = features
			self.commands[label]['sequences'] = np.array(sequences)

	def getAllFoldersAsLabels(self, path):
		folders = [(f, join(path,f)) for f in listdir(path) if not isfile(join(path, f))]

		return folders

	def allFilesForLabel(self, path, label):
		files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

		return files

	def generateFeatures(self, files):
		allFeatures = []
		sizeSequences = []
		sf = SpeechFeatures()
		winlength = 0.03 # 30ms
		ncep = 13

		for file in files:
			signal, fs, enc = sf.wavread(file)
			cepstragram = sf.getFeatures(signal, fs, winlength, ncep)
			features = sf.dynamic_features(cepstragram)
			
			allFeatures.append(features)
			sizeSequences.append(features.shape[1])

		return (allFeatures, sizeSequences)

	def partitionDataset(self, label, training=0.7, validation=0.2, test=0.1):
		files = self.commands[label]['files']
		indices = range(len(files))

		random.shuffle(indices)

		splitBoundary1 = int(round(len(files) * training)) - 1
		splitBoundary2 = splitBoundary1 + int(round(len(files) * validation))
		trainingIndices = indices[:splitBoundary1]
		validationIndices = indices[splitBoundary1:splitBoundary2]
		testIndices = indices[splitBoundary2:]

		trainingSet = self.generateSet(label, trainingIndices)
		validationSet = self.generateSet(label, validationIndices)
		testSet = self.generateSet(label, testIndices)

		return (trainingSet, validationSet, testSet)

	def generateSet(self, label, indices):
		subSet = {'features': None, 'sequences': []}
		for index in indices:
			feature = self.commands[label]['features'][index]
			try:
				subSet['features'] = np.concatenate((subSet['features'], feature), axis=1)
			except:
				subSet['features'] = feature

		subSet['sequences'] = self.commands[label]['sequences'][indices]

		return subSet

	def getLabels(self):
		return self.commands.keys()