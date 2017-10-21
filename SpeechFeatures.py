import sidekit.frontend.features as ff
from scikits.audiolab import wavread
import numpy as np
import pdb

class SpeechFeatures():
	def getFeatures(self, signal, fs, winlength, *args):
		if len(args) == 0:
			calcmfccs = False
			ncep = 1
		elif len(args) == 1:
			calcmfccs = True
			ncep = args[0]
		else:
			print 'Incorrect number of inputs.'

		signal = np.real(signal)

		if fs <= 0:
			fs = 44100

		if isinstance(ncep, list):
			ncep = round(np.real(ncep[0]))
		else:
			ncep = round(np.real(ncep))

		if ncep < 1:
			ncep = 1

		if isinstance(winlength, list):
			winlength = np.real(winlength[0])
		else:
			winlength = np.real(winlength)

		if winlength * fs < ncep:
			winlength = ncep / fs

		winshift = 0.5
		minfreq = 20
		maxfreq = 4000
		nbands = 30
		lifterexp = 0
		preemph = 0

		if calcmfccs == True:
			ceps, log_energy, spec, mspec = ff.mfcc(signal, lowfreq=minfreq, maxfreq=maxfreq, nlinfilt=lifterexp, 
				nlogfilt=nbands, nwin=winlength, fs=fs, nceps=int(ncep), shift=winlength*winshift, prefac=preemph)

			output = []
			output.append(ceps)
		else:
			output = []

		if not output:
			spectram, log_energy = ff.power_spectrum(signal, fs=fs, win_time=winlength, shift=winlength*winshift, prefac=1)
			output.append(spectram)
			output.append(log_energy)

		return output

	def dynamic_features(self, ceps):
		ceps = np.matrix(np.array(ceps)[0])
		velocity = np.diff(ceps, n=1, axis=0).T
		acceleration = np.diff(ceps, n=2, axis=0).T
		ceps_transpose = ceps.T
		dynamic = np.concatenate((ceps_transpose[:, 0:-2], velocity[:, 0:-1], acceleration), axis=0)

		return dynamic

	def wavread(self, filename):
		s, fs, enc = wavread(filename)  # s in range -32768 to +32767
		s = np.array(s)
		s = s / max(abs(s)) 

		return (s,fs,enc)