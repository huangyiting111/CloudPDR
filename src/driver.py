import argparse
import sys
from BlockUtil import *
from Ibf import *
#from CloudPDRObj import *
import CloudPdrFuncs
import BlockEngine as BE
from CloudPDRKey import CloudPDRKey
from TagGenerator import TagGenerator
from Crypto.Hash import SHA256
from datetime import datetime
import MessageUtil as MU
import CloudPdrMessages_pb2
from client import RpcPdrClient
from PdrSession import PdrSession
from math import floor
from math import log
from CryptoUtil import pickPseudoRandomTheta
from Crypto.Util import number
from ExpTimer import ExpTimer
import multiprocessing as mp
from TagGenerator import singleTag
from TagGenerator import singleW
import struct
from PdrManager import IbfManager, QSetManager
import copy



LOST_BLOCKS = 6

W = {}
Tags = {}

def produceClientId():
    h = SHA256.new()
    h.update(str(datetime.now()))
    return h.hexdigest()




def subsetAndLessThanDelta(clientMaxBlockId, serverLost, delta):
    
    lossLen = len(serverLost)
    if lossLen >= clientMaxBlockId:
        return (False, "Fail#1: LostSet from the server is not subset of the client blocks ")
    
    for i in serverLost:
        if i>= 0 and i <= clientMaxBlockId:
            continue
    if lossLen > delta:
        return (False, "FAIL#2: Server has lost more than DELTA blocks")
    return (True, "")


def workerTask(inputQueue,W,T,ibf,blockProtoBufSz,blockDataSz,secret,public, TT):
    
    pName = mp.current_process().name
    x = ExpTimer()
    x.registerSession(pName)
    x.registerTimer(pName, "tag")
    x.registerTimer(pName, "ibf")
    
    while True:
        item = inputQueue.get()
        if item == "END":
            TT[pName+str("_tag")] = x.getTotalTimer(pName, "tag")
            TT[pName+str("_ibf")] = x.getTotalTimer(pName, "ibf")
            return
        
        for blockPBItem in BE.chunks(item, blockProtoBufSz):
            block = BE.BlockDisk2Block(blockPBItem, blockDataSz)
            bIndex = block.getDecimalIndex()
#            print mp.current_process(), "Processing block", bIndex
            x.startTimer(pName, "tag")
            w = singleW(block, secret["u"])
            tag = singleTag(w, block, public["g"], secret["d"], public["n"])
            x.endTimer(pName, "tag")
            W[bIndex] = w
            T[bIndex] = tag
            
            x.startTimer(pName, "ibf")
            ibf.insert(block, None, public["n"], public["g"], True)
            x.endTimer(pName, "ibf")
            del block




def clientWorkerProof(inputQueue, blockProtoBufSz, blockDataSz, lost, chlng, W, N, comb, lock, qSets, ibf, manager, TT):
    
    pName = mp.current_process().name
    x = ExpTimer()
    x.registerSession(pName)
    x.registerTimer(pName, "cmbW")
    x.registerTimer(pName, "qSet")
    
    while True:
        item = inputQueue.get()
        if item == "END":
            TT[pName+str("_cmbW")] = x.getTotalTimer(pName, "cmbW")
            TT[pName+str("_qSet")] = x.getTotalTimer(pName, "qSet")
            return
        
        for blockPBItem in BE.chunks(item, blockProtoBufSz):
            block = BE.BlockDisk2Block(blockPBItem, blockDataSz)
            bIndex = block.getDecimalIndex()
            if bIndex in lost:
                x.startTimer(pName, "qSet")
                binBlockIndex = block.getStringIndex()
                indices = ibf.getIndices(binBlockIndex, True)
                for i in indices:
                    with lock:
                        qSets.addValue(i, bIndex)
                        
                x.endTimer(pName, "qSet")
                del block
                continue
            
            x.startTimer(pName, "cmbW")
            aI = pickPseudoRandomTheta(chlng, block.getStringIndex())
            aI = number.bytes_to_long(aI)
            h = SHA256.new()
            wI = W[bIndex]
            h.update(wI)
            wI = number.bytes_to_long(h.digest())
            wI = pow(wI, aI, N)
            with lock:
                comb["w"] *= wI
                comb["w"] = pow(comb["w"], 1, N)
            x.endTimer(pName, "cmbW")
            del block

    

def processServerProof(cpdrProofMsg, session):
    et = ExpTimer()
    pName = mp.current_process().name
    et.registerSession(pName)
    
    
    et.registerTimer(pName, "subset-check")
    et.startTimer(pName, "subset-check")
    if len(cpdrProofMsg.proof.lostIndeces) > 0:
        res, reason = subsetAndLessThanDelta(session.fsInfo["blockNum"],
                                             cpdrProofMsg.proof.lostIndeces,
                                             session.delta)
        if res == False:
            print reason
            return False
     
    et.endTimer(pName, "subset-check")
    
    et.registerTimer(pName, "cmbW-start")
    et.startTimer(pName, "cmbW-start")
   
    servLost = cpdrProofMsg.proof.lostIndeces
    serCombinedSum = long(cpdrProofMsg.proof.combinedSum)
    gS = pow(session.g, serCombinedSum, session.sesKey.key.n)
    serCombinedTag = long(cpdrProofMsg.proof.combinedTag)
    sesSecret = session.sesKey.getSecretKeyFields() 
    Te =pow(serCombinedTag, sesSecret["e"], session.sesKey.key.n)
    et.endTimer(pName, "cmbW-start")
    
#     inputQueue, blockProtoBufSz, blockDataSz, lost, chlng, W, N, combW, lock
    
    gManager = mp.Manager()
    combRes = gManager.dict()
    TT = gManager.dict()
    combRes["w"] = 1
    
    
    qSetManager = QSetManager()
    qSetManager.start()
    qSets = qSetManager.QSet()
    
    combLock = mp.Lock()
    bytesPerWorker = mp.Queue(session.fsInfo["workers"])
    
    workerPool = []
    for i in xrange(session.fsInfo["workers"]):
        p = mp.Process(target=clientWorkerProof,
                       args=(bytesPerWorker, session.fsInfo["pbSize"],
                             session.fsInfo["blkSz"], servLost, 
                             session.challenge, session.W, session.sesKey.key.n,
                             combRes, combLock, qSets, session.ibf, gManager, TT))
        p.start()
        workerPool.append(p)
    
    fp = open(session.fsInfo["fsName"], "rb")
    fp.read(4)
    fp.read(session.fsInfo["skip"])
    
    while True:
        chunk = fp.read(session.fsInfo["bytesPerWorker"])
        if chunk:
            bytesPerWorker.put(chunk)
        else:
            for j in xrange(session.fsInfo["workers"]):
                bytesPerWorker.put("END")
            break
    
    for p in workerPool:
        p.join()
    
   
    et.registerTimer(pName, "cmbW-last")
    et.startTimer(pName, "cmbW-last")
    combinedWInv = number.inverse(combRes["w"], session.sesKey.key.n)  #TODO: Not sure this is true
    RatioCheck1=Te*combinedWInv
    RatioCheck1 = pow(RatioCheck1, 1, session.sesKey.key.n)
    
         
    if RatioCheck1 != gS:
        print "FAIL#3: The Proof did not pass the first check to go to recover"
        return False

    et.endTimer(pName, "cmbW-last")

    print "# # # # # # # ##  # # # # # # # # # # # # # ##"
    
   
    qS = qSets.qSets()
    
    et.registerTimer(pName, "lostSum")
    et.startTimer(pName, "lostSum")
    lostSum = {}
    for p in cpdrProofMsg.proof.lostTags.pairs:
        lostCombinedTag = long(p.v)
        Lre =pow(lostCombinedTag, sesSecret["e"], session.sesKey.key.n)
        
        Qi = qS[p.k]
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
    et.endTimer(pName, "lostSum")
    
    
    serverStateIbf = session.ibf.generateIbfFromProtobuf(cpdrProofMsg.proof.serverState,
                                                 session.fsInfo["blkSz"])
    
    
    localIbf = Ibf(session.fsInfo["k"], session.fsInfo["ibfLength"])
    
    lc = copy.deepcopy(session.ibf.cells())
    localIbf.setCells(lc)
    
    et.registerTimer(pName, "subIbf")
    et.startTimer(pName,"subIbf")
    diffIbf = localIbf.subtractIbf(serverStateIbf, session.challenge,
                                    session.sesKey.key.n, session.fsInfo["blkSz"], True)
    et.endTimer(pName,"subIbf")
    
    for k in lostSum.keys():
        val=lostSum[k]
        diffIbf.cells[k].setHashProd(val)
   
    
    et.registerTimer(pName, "recover")
    et.startTimer(pName, "recover")
    L=CloudPdrFuncs.recover(diffIbf, servLost, session.challenge, session.sesKey.key.n, session.g)
    et.endTimer(pName, "recover")
    
    
    for k in lostSum.keys():
        print diffIbf.cells[k].hashProd
        
    if L==None:
        print "fail to recover"
        sys.exit(1)
        
    for blk in L:
        print blk.getDecimalIndex()
      
    return "Exiting Recovery..."

def processClientMessages(incoming, session, lostNum=None):
    
    cpdrMsg = MU.constructCloudPdrMessageNet(incoming)
    
    if cpdrMsg.type == CloudPdrMessages_pb2.CloudPdrMsg.INIT_ACK:
        print "Processing INIT-ACK"
        lostMsg = MU.constructLossMessage(lostNum, session.cltId)
        return lostMsg
        
    elif cpdrMsg.type == CloudPdrMessages_pb2.CloudPdrMsg.LOSS_ACK:
        print "Processing LOSS_ACK"
        
        session.challenge = session.sesKey.generateChallenge()
        challengeMsg = MU.constructChallengeMessage(session.challenge, session.cltId)
        return challengeMsg    
    
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
    
    p.add_argument('--task', dest='task', action='store', type=int, default=100,
                   help='Number of blocks per worker for the W,Tag calculation')
   
    p.add_argument('-w', dest="workers", action='store', type=int, default=4,
                  help='Number of worker processes ')

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
    
    
    
    
    #Read the generator from File
    fp = open(args.genFile, "r")
    g = fp.read()
    g = long(g)
    fp.close() 
    pdrSes.addG(g)
    
    #Generate key class
    pdrSes.sesKey = CloudPDRKey(args.n, g)
    secret = pdrSes.sesKey.getSecretKeyFields()
    public = pdrSes.sesKey.getPublicKeyFields()
    pdrSes.addSecret(secret)
    pubPB = pdrSes.sesKey.getProtoBufPubKey()
    
    
    fp=open(args.blkFp,"rb")
    fsSize = fp.read(4)
    fsSize, = struct.unpack("i", fsSize)
    fs = CloudPdrMessages_pb2.Filesystem()
    fs.ParseFromString(fp.read(int(fsSize)))
    
    ibfLength =  floor(log(fs.numBlk,2)) 
    ibfLength *= (args.hashNum+1)
    ibfLength = int(ibfLength)
    pdrSes.addibfLength (ibfLength)
    
    
    
    #fs, fsFp = BlockEngine.getFsDetailsStream(args.blkFp)
    totalBlockBytes = fs.pbSize*fs.numBlk
    bytesPerWorker = (args.task*totalBlockBytes)/ fs.numBlk
    
    pdrSes.addFsInfo(fs.numBlk, fs.pbSize, fs.datSize, int(fsSize), 
                     bytesPerWorker, args.workers, args.blkFp, ibfLength, args.hashNum)
    
    genericManager = mp.Manager()
    pdrManager = IbfManager()
    
    blockByteChunks = genericManager.Queue(args.workers)
    W = genericManager.dict()
    T = genericManager.dict()
    TT = genericManager.dict()
    
    pdrManager.start()
    ibf = pdrManager.Ibf(args.hashNum, ibfLength)
    ibf.zero(fs.datSize)
    
    
    pool = []
    for i in xrange(args.workers):
        p = mp.Process(target=workerTask, args=(blockByteChunks,W,T,ibf,fs.pbSize,fs.datSize,secret,public, TT))
        p.start()
        pool.append(p)
    
    while True:
        chunk = fp.read(bytesPerWorker)
        if chunk:
            blockByteChunks.put(chunk)
        else:
            for j in xrange(args.workers):
                blockByteChunks.put("END")
            break
    
    for p in pool:
        p.join()
    
    
    
    pdrSes.addState(ibf)
    pdrSes.W = W
    log2Blocks = log(fs.numBlk, 2)
    log2Blocks = floor(log2Blocks)
    delta = int(log2Blocks)
    pdrSes.addDelta(delta)



    initMsg = MU.constructInitMessage(pubPB, args.blkFp,
                                               T, cltId, args.hashNum, delta, fs.numBlk)

    clt = RpcPdrClient()    
    print "Sending Initialization message"
    initAck = clt.rpc("127.0.0.1", 9090, initMsg) 
    print "Received Initialization ACK"
    
    
    lostMsg = processClientMessages(initAck, pdrSes, args.lostNum)
    print "Sending Lost message"
    lostAck = clt.rpc("127.0.0.1", 9090, lostMsg)
    print "Received Lost-Ack message"
    
    
    challengeMsg = processClientMessages(lostAck, pdrSes)
    print "Sending Challenge message"
    proofMsg = clt.rpc("127.0.0.1", 9090, challengeMsg)
    print "Received Proof message"
    processClientMessages(proofMsg, pdrSes)
    


if __name__ == "__main__":
    main()