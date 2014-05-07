import argparse
import sys
from BlockUtil import *
from Ibf import *
#from CloudPDRObj import *
import CloudPdrFuncs
import BlockEngine
from CloudPDRKey import CloudPDRKey
from TagGenerator import TagGenerator
from Crypto.Hash import SHA256
from datetime import datetime
import MessageUtil
import CloudPdrMessages_pb2
from client import RpcPdrClient
from PdrSession import PdrSession
from math import floor
from math import log
from CryptoUtil import pickPseudoRandomTheta
from Crypto.Util import number
from bitarray import bitarray
from Block import *

LOST_BLOCKS = 6

def produceClientId():
    h = SHA256.new()
    h.update(str(datetime.now()))
    return h.hexdigest()


def processServerProof(cpdrProofMsg, session):
    serverLost =  set()
    
    if len(cpdrProofMsg.proof.lostIndeces) > 0:
        for lost in cpdrProofMsg.proof.lostIndeces:
            serverLost.add(lost)
        
        blockSet = set(range(len(session.blocks)))
        if serverLost.issubset(blockSet) == False:
            del blockSet
            print "FAIL#1: LostSet from the server is not subset of the blocks in the Client"
            return False
        
        
        if len(serverLost) > session.delta:
            print "FAIL#2: Server has lost more than DELTA blocks"
            return False
    
    serCombinedSum = long(cpdrProofMsg.proof.combinedSum)
    gS = pow(session.g, serCombinedSum, session.sesKey.key.n)
    serCombinedTag = long(cpdrProofMsg.proof.combinedTag)
    sesSecret = session.sesKey.getSecretKeyFields() 
        
    Te =pow(serCombinedTag, sesSecret["e"], session.sesKey.key.n)
        
    index = 0
    combinedW=1
    for blk in session.blocks:
        if index in cpdrProofMsg.proof.lostIndeces:
            index+=1
            continue
        
        h = SHA256.new()
        aBlk = pickPseudoRandomTheta(session.challenge, blk.getStringIndex())
        aI = number.bytes_to_long(aBlk)
        
        w = session.W[index]
        h.update(str(w))
        wHash = number.bytes_to_long(h.digest())
        wa= pow(wHash, aI, session.sesKey.key.n)
        combinedW = pow((combinedW*wa), 1, session.sesKey.key.n)
        index+=1
            

    combinedWInv = number.inverse(combinedW, session.sesKey.key.n)  #TODO: Not sure this is true
    RatioCheck1=Te*combinedWInv
    RatioCheck1 = pow(RatioCheck1, 1, session.sesKey.key.n)
        
    if RatioCheck1 != gS:
        print "FAIL#3: The Proof did not pass the first check to go to recover"
        return False

    print "# # # # # # # ##  # # # # # # # # # # # # # ##"
    
    qSets = {}
    for lIndex in serverLost:
        binLostIndex = session.ibf.binPadLostIndex(lIndex)
        indeces = session.ibf.getIndices(binLostIndex, True)
            
        for i in indeces:
            if i not in qSets.keys():
                qSets[i] = []
            qSets[i].append(lIndex)
    
    
    lostSum = {}
    for p in cpdrProofMsg.proof.lostTags.pairs:
        lostCombinedTag = long(p.v)
        Lre =pow(lostCombinedTag, sesSecret["e"], session.sesKey.key.n)
        
        Qi = qSets[p.k]
        combinedWL = 1
        for vQi in Qi:
            h = SHA256.new()
            aLBlk = pickPseudoRandomTheta(session.challenge, session.ibf.binPadLostIndex(vQi))
            aLI = number.bytes_to_long(aLBlk)
            wL = session.W[vQi]
            h.update(str(wL))
            wLHash = number.bytes_to_long(h.digest())
            waL = pow(wLHash, aLI, session.sesKey.key.n)
            combinedWL = pow((combinedWL*waL), 1, session.sesKey.key.n)
        
        combinedWLInv = number.inverse(combinedWL, session.sesKey.key.n)
        lostSum[p.k] = Lre*combinedWLInv
        lostSum[p.k] = pow(lostSum[p.k], 1, session.sesKey.key.n)
        
    serverStateIbf = session.ibf.generateIbfFromProtobuf(cpdrProofMsg.proof.serverState,
                                                 session.dataBitSize)
    

    diffIbf = session.ibf.subtractIbf(serverStateIbf, session.challenge,
                                      session.sesKey.key.n, session.dataBitSize, True)    
    
    
    for k in lostSum.keys():
        val=lostSum[k]
        diffIbf.cells[k].setHashProd(val)
    
    L=CloudPdrFuncs.recover(diffIbf, serverLost, session.challenge, session.sesKey.key.n, session.g)
    
    for k in lostSum.keys():
        print diffIbf.cells[k].hashProd
        
    if L==None:
        print "fail to recover"
    
        
    for blk in L:
        print blk.getDecimalIndex()
      
    return "Exiting Recovery..."

def processClientMessages(incoming, session, lostNum=None):
    
    cpdrMsg = MessageUtil.constructCloudPdrMessageNet(incoming)
    
    if cpdrMsg.type == CloudPdrMessages_pb2.CloudPdrMsg.INIT_ACK:
        print "Processing INIT_ACK"
        outgoingMsg = MessageUtil.constructLossMessage(lostNum, session.cltId)
        return outgoingMsg
        
    elif cpdrMsg.type == CloudPdrMessages_pb2.CloudPdrMsg.LOSS_ACK:
        print "Processing LOSS_ACK"
        session.challenge = session.sesKey.generateChallenge()
        #print session.challenge
        outgoingMsg = MessageUtil.constructChallengeMessage(session.challenge, session.cltId)
        return outgoingMsg    
    
    elif cpdrMsg.type == CloudPdrMessages_pb2.CloudPdrMsg.PROOF:
        print "Received Proof"
        res = processServerProof(cpdrMsg, session)
        print res

def main():
    
    p = argparse.ArgumentParser(description='Driver for IBF')

    
    p.add_argument('-b', dest='blkFp', action='store', default=None,
                   help='Serialized block filename as generated from BlockEngine')
    
    p.add_argument('-k', dest='hashNum', action='store', type=int,
                   default=5, help='Number of hash arguments')
    
    p.add_argument('-g', dest="genFile", action="store", default=None,
                 help="static generator file")

    
    p.add_argument('-n', dest='n', action='store', type=int,
                   default=1024, help='RSA modulus size')
    
    p.add_argument('-s', dest='size', action='store', type=int, default=512,
                   help='Data Bit Size')
    
    p.add_argument('-l', dest='lostNum', action='store', type=int, default=5,
                   help='Number of Lost Packets')
   

    args = p.parse_args()
    if args.hashNum > 10: 
        print "Number of hashFunctions should be less than 10"
        sys.exit(1)
        
    if args.blkFp == None:
        print 'Please specify a file that stores the block collection'
        sys.exit(1)
    
    if args.genFile == None:
        print 'Please specify a generator file'
        sys.exit(1)
        
    #Generate client id
    cltId = produceClientId()
       
    
    #Create current session
    pdrSes = PdrSession(cltId)
    pdrSes.addDataBitSize(args.size)
    
    # Read blocks from Serialized file
    blocks = BlockEngine.readBlockCollectionFromFile(args.blkFp)
    pdrSes.blocks = BlockEngine.blockCollection2BlockObject(blocks)
    
    
    #Get Ibf len based on delta, k and number of blocks
    
    ibfLength =  floor(log(len(pdrSes.blocks),2)) 
    ibfLength *= (args.hashNum+1)
    ibfLength = int(ibfLength)
    pdrSes.addibfLength (ibfLength)
    
    
    #Read the generator from File
    fp = open(args.genFile, "r")
    g = fp.read()
    g = long(g)
    fp.close() 
    pdrSes.addG(g)
    
   
    #Generate key class
    pdrSes.sesKey = CloudPDRKey(args.n, g)
    secret = pdrSes.sesKey.getSecretKeyFields()
    pdrSes.addSecret(secret)
    pubPB = pdrSes.sesKey.getProtoBufPubKey()
    
    
    #Create a tag generator
    tGen = TagGenerator()
    wStartTime = datetime.now()
    
    #Create Wi
    pdrSes.W = tGen.getW(pdrSes.blocks, secret["u"])
    wEndTime = datetime.now()
    
    #Create Tags
    tagStartTime = datetime.now()
    T = tGen.getTags(pdrSes.W, g, pdrSes.blocks, secret["d"], pdrSes.sesKey.key.n)
    tagEndTime = datetime.now()
    tagCollection = tGen.createTagProtoBuf(T)
    print "W creation:" , wEndTime-wStartTime
    print "Tag creation:" , tagEndTime-tagStartTime
    
 
 
    #Create the local state
    clientIbf = Ibf(args.hashNum, ibfLength)
    clientIbf.zero(blocks.blockBitSize)
    for blk in pdrSes.blocks:
        clientIbf.insert(blk, None, pdrSes.sesKey.key.n, g, True)
 
    pdrSes.addState(clientIbf)
    
 
    #Construct InitMsg
    log2Blocks = log(len(pdrSes.blocks), 2)
    log2Blocks = floor(log2Blocks)
    delta = int(log2Blocks)
    pdrSes.addDelta(delta)
    
    
    initMessage = MessageUtil.constructInitMessage(pubPB, 
                                                   blocks, 
                                                   tagCollection,
                                                   cltId,
                                                   args.hashNum,
                                                   delta)

    clt = RpcPdrClient()    
    
    print "Sending Init..."
    inComing = clt.rpc("127.0.0.1", 9090, initMessage)
    outgoing = processClientMessages(inComing, pdrSes, args.lostNum)
    
    
    print "Sending Lost message"
    incoming = clt.rpc("127.0.0.1", 9090, outgoing)
    outgoing = processClientMessages(incoming, pdrSes)
    
    print "Sending Challenge ...."
    incoming = clt.rpc("127.0.0.1", 9090, outgoing)
    processClientMessages(incoming, pdrSes)
    
    
    
    
    
 
   
#    commonBlocks = pickCommonBlocks(args.numBlocks, args.numCommon)
#    diff_a, diff_b = pickDiffBlocks(args.numBlocks, commonBlocks, args.totalBlocks)
#   
#
#     ibfA = Ibf(args.hashNum, args.ibfLen)
#     ibfA.zero(args.dataSize)
#     ibfB = Ibf(args.hashNum, args.ibfLen)
#     ibfB.zero(args.dataSize)
# 
#     for cBlock in commonBlocks:
#         ibfA.insert(blocks[cBlock], cObj.secret, cObj.N, cObj.g, args.dataSize)
#         ibfB.insert(blocks[cBlock], cObj.secret, cObj.N, cObj.g, args.dataSize)
# 
#     for diffBlock in diff_a:
#         ibfA.insert(blocks[diffBlock], cObj.secret, cObj.N, cObj.g, args.dataSize)
# 
#     lostindices=[]
#     #lostindices=diff_a
#     for i in diff_a:
#         lostindices.append(i)
# 
#     for diffBlock in diff_b:
#         ibfB.insert(blocks[diffBlock], cObj.secret, cObj.N, cObj.g,  args.dataSize)
# 
# 
#     for diffBlock in diff_b:
#         ibfB.delete(blocks[diffBlock], cObj.secret, cObj.N, cObj.g)
#         
#     
#     diffIbf = ibfA.subtractIbf(ibfB,  cObj.secret, cObj.N, args.dataSize)
#     for cellIndex in xrange(args.ibfLen):
#         diffIbf.cells[cellIndex].printSelf()
#     
#     #lostindices=diff_a
#     L=CloudPdrFuncs.recover(diffIbf, diff_a, args.dataSize, cObj.secret, cObj.N, cObj.g)
# 
#     if L==None:
#         print "fail to recover"
# 
#     for block in L:
#         print block
# 
#     
#     print len(L)
#     print len(lostindices)
# 
#     recovered=0
#     if(len(L)==len(lostindices)):
#         for i in lostindices:
#             if i in L:
#                 recovered+=1
#                 #print "SUCCESS"
# 
#     print recovered
    
    


if __name__ == "__main__":
    main()