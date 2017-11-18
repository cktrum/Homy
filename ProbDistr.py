import abc
from ProbGenModel import ProbGenModel

class ProbDistr(ProbGenModel):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def init(self, pD, x):
		return (pD, iOK)

	@abc.abstractmethod
	def adaptStart(self, pD):
		return aState

	@abc.abstractmethod
	def adaptAccum(self, pD, aState, obsData):
		return aState

	@abc.abstractmethod
	def adaptSet(self, pD, aState):
		return pD