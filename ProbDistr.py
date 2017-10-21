import abc
from ProbGenModel import ProbGenModel

class ProbDistr(ProbGenModel):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def init(self, pD, x):
		return (pD, iOK)