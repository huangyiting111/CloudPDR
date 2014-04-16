from Crypto.Util import number 
from Crypto.Hash import HMAC

class CloudPDRObj(object):
	def __init__(self, Nbits):
		
		self.N = number.getRandomInteger(Nbits)
		self.secret = self.generateSecret(Nbits)

	def generateSecret(self,Nbits):
		tmpRand = number.getRandomInteger(Nbits)
		h = HMAC.new(self.N)
		h.update(tmpRand)
		return h.hexdigest()

