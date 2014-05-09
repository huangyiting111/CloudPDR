import sys
import CloudPdrMessages_pb2
import BlockUtil
import argparse
import datetime
from Block import Block
from bitarray import bitarray
import struct
from ExpTimer import ExpTimer
import copy
import numpy as np

TEST = False

def createBlocks(blocksNum, blockSize):
    blocks = BlockUtil.blockCreatorMemory(blocksNum, blockSize)
    return blocks

def createBlockProtoBufs(blocks, blockSize):
    print "Creating protocol buffers...."
    blockCollection = CloudPdrMessages_pb2.BlockCollection()
    blockCollection.blockBitSize = blockSize*8
    for b in blocks:
        pbufBlock = blockCollection.blocks.add()
        pbufBlock.index = b.getStringIndex()
        pbufBlock.data = b.getData().to01()

    return blockCollection


def createBlockProtoBufsDisk(blocks, blockSize):
    blockCollection = CloudPdrMessages_pb2.BlockCollectionDisk()
    blockCollection.blockBitSize = blockSize*8
    for b in blocks:
        pbfBlk = blockCollection.collection.add()
        pbfBlk.blk = b.data.tobytes()
        
    return blockCollection


def readBlockCollectionFromDisk(filename):
    print "Reading block collection from disk (", filename, ")"
    bc = CloudPdrMessages_pb2.BlockCollectionDisk()
    fp = open(filename,"rb")
    bc.ParseFromString(fp.read())
    fp.close()
    return bc

def writeBlockCollectionToFile(filename, blkCollection):
    print "Writing Block Collection to File"
    fp = open(filename, "wb")
    fp.write(blkCollection.SerializeToString())
    fp.close()

def readBlockCollectionFromFile(filename):
    print "Reading Block collection from File"
    blockCollection = CloudPdrMessages_pb2.BlockCollection()
    fp = open(filename, "rb")
    blockCollection.ParseFromString(fp.read())
    fp.close()
    return blockCollection

def listBlocksInCollection(blocks):
    for blk in blocks:
        print blk.getDecimalIndex()

def blockCollectionDisk2BlockObject(blockCollection):
    b = []
    bSize = blockCollection.blockBitSize
    for i in blockCollection.collection:
        bObj = Block(0,bSize, True)
        bObj.buildBlockFromProtoBufDisk(i.blk)
        b.append(bObj)
    return b

def blockCollection2BlockObject(blockCollection):
    b = []
    bSize = blockCollection.blockBitSize
    for blk in blockCollection.blocks:
        bObj = Block(0,0)
        bObj.buildBlockFromProtoBuf(blk.index, blk.data, bSize) 
        b.append(bObj)
    return b


### # # # # # Filesystem functions  ## # # # # # # # # ##  ## 

def createWriteFilesystem2Disk(blkNum, blkSz, indexSize, filename):
    fs = CloudPdrMessages_pb2.Filesystem()
    fs.numBlk = blkNum
    fs.index = indexSize
    fs.datSize = blkSz*8
    
    fp = open(filename, "wb")
    xrangeObj = None
    for i in xrange(blkNum):
        if i == 0:
            blk = BlockUtil.createSingleBlock(i, blkSz)
            pseudoData = copy.deepcopy(blk.data2)
            xrangeObj = xrange(len(pseudoData))
        else:
            BlockUtil.createSingleBlock(i, blkSz, pseudoData, xrangeObj, 8)
            
        blkPbf = CloudPdrMessages_pb2.BlockDisk()
        #reshaped = np.reshape(blk.data2, (8,len(blk.data2)/8))
        
        blkPbf.blk = (BlockUtil.npArray2bitArray(blk.data2)).tobytes()
        blkPbf = blkPbf.SerializeToString()
        if i == 0:
            fs.pbSize=len(blkPbf)
            fs = fs.SerializeToString()
            fsLen = len(fs)
            fsLen = struct.pack("i",fsLen)
            fp.write(fsLen)
            fp.write(fs)
            
        fp.write(blkPbf)
        
    fp.close()
    
    
def readFileSystem(fsFilename):
    #DEBUG function
    fp = open(fsFilename, "rb")
    fsSize = fp.read(4)
    fsSize, = struct.unpack("i", fsSize)
    
    fs = CloudPdrMessages_pb2.Filesystem()
    fs.ParseFromString(fp.read(int(fsSize)))
    
    print "pbSize", fs.pbSize
    print "numBlk", fs.numBlk
    print "index", fs.index
    print "dataSize", fs.datSize
    
    for i in range(fs.numBlk):
        c = CloudPdrMessages_pb2.BlockDisk()
        
        c.ParseFromString(fp.read(fs.pbSize))
        bb = bitarray()
        bb.frombytes(c.blk)
        print bb[0:32]
        
    fp.close()
    
    
    
    



def main():

    p = argparse.ArgumentParser(description='BlockEngine Driver')

    p.add_argument('-n', dest='numBlocks', action='store', type=int,
                   default=2, help='Number of blocks to create')
    
    p.add_argument('-s', dest='dataSize', action='store', type=int,
                   default=64, help='Block data size')
    
    p.add_argument('-w', dest='fpW', action='store', default=None,
                   help='File to write Block collection')

    p.add_argument('-r', dest='fpR', action='store', default=None,
                   help='File to read Block collection')


    args = p.parse_args()
    
            
    if args.fpW == None and args.fpR == None:
        print "Please specfiy a read or write operation"
        sys.exit(1)
    
    if args.fpW != None:
        
        if args.numBlocks <= 0:
            print "Please specify a number of blocks > 0"
            sys.exit(1)

        if args.dataSize <= 0:
            print "Please specify data blocks size > 0"
            sys.exit(1)

        et = ExpTimer()
        et.registerSession("writing")
        et.registerTimer("writing", "write")
        et.startTimer("writing", "write")
        createWriteFilesystem2Disk(args.numBlocks, args.dataSize, 32, args.fpW)
        et.endTimer("writing", "write")
        et.printSessionTimers("writing")
                    
    if args.fpR:
        start = datetime.datetime.now()
        blkCol = readBlockCollectionFromFile(args.fpR)
        listBlocksInCollection(blkCol)
        end = datetime.datetime.now()
        

if __name__ == "__main__":
    main()
        