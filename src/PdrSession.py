


class PdrSession(object):
    
    INIT=0
    INIT_ACK=1
    CHALLENGE=2
    PROOF=3

    def __init__(self, cltId,key=None, W=None, blocks=None, challenge=None):
        self.sesKey = key
        self.W = W
        self.blocks = blocks
        self.challenge = challenge
        self.state = self.INIT
        self.cltId = cltId
        
    def addSecret(self, secret):
        self.secret = secret
    
    def addState(self, ibf):
        self.ibf = ibf
    
    def addDelta(self, delta):
        self.delta = delta
        
    def addG(self, g):
        self.g = g
        
    def addh(self, h):
        self.h=h
        
        