import pdb
import math
import colorama
from termcolor import cprint,colored
from os import system

colorama.init()
globalTime = 0
mainBlockSize = 0

def is2Power(val):
	tmp = math.log(val,2)
	if(tmp - int(tmp) == 0):
		return True
	return False

class Memory:
	def __init__(self,memoryVal,memoryAddress,memoryTag,dataTag):
		self.memoryVal = memoryVal
		self.memoryAddress = memoryAddress
		self.memoryTag = memoryTag
		self.dataTag = dataTag
		self.timeStamp = globalTime

	def printMemory(self):
		print(str(self.memoryAddress)+" -> "+str(self.memoryVal)+"| ",end=" ")

class Block:
	def __init__(self,blockTag):
		global mainBlockSize

		self.blockSize = mainBlockSize
		self.blockTag = blockTag
		self.crntMemoryCount = 0
		self.memoryArr = []

	def insertInMemoryArray(self,memoryObj):
		self.memoryArr.append(memoryObj)
		self.crntMemoryCount += 1

	def updateInMemoryArray(self,memoryObj):
		for val in self.memoryArr:
			if(val.memoryAddress == memoryObj.memoryAddress):
				self.memoryArr.remove(val)
				self.memoryArr.append(memoryObj)
				break

	def isInBlock(self,memoryObj):
		if(self.crntMemoryCount == 0):
			return False
		for val in self.memoryArr:
			if(val.memoryAddress == memoryObj.memoryAddress):
				return True
		return False

	def getFromBlock(self,memoryObj):
		for val in self.memoryArr:
			if(val.memoryAddress == memoryObj.memoryAddress):
				return val

	def printBlock(self):
		# pdb.set_trace()
		cprint("Block number-> "+str(self.blockTag),"yellow")
		for val in self.memoryArr:
			val.printMemory()
		print()

TimeChecking = []

def updateInTimeCheckingArr(blockTag):
	for val in TimeChecking:
		if(val == blockTag):
			TimeChecking.remove(val)
			break
	TimeChecking.append(blockTag)

def isBlockInTimeChecking(blockTag):
	for val in TimeChecking:
		if(val == TimeChecking):
			return True
	return False



class FullyAssosiative:
	def __init__(self,cacheLine,blockSize):
		self.cacheLine = cacheLine
		self.blockSize = blockSize
		self.cacheSize = self.cacheLine*self.blockSize
		self.crntCacheSize = 0
		self.cache = {}
		global TimeChecking

	def isInCache(self,blockTag):
		if(self.crntCacheSize == 0):
			return False
		for val in self.cache:
			if(val == blockTag):
				return True
		return False


	def writeToCache(self,memoryObj,blockTag):
		# pdb.set_trace()
		if(len(self.cache) == 0):
			cprint("Cache tag miss","yellow")
			self.crntCacheSize += 1
			tmpBlock = Block(blockTag)
			tmpBlock.insertInMemoryArray(memoryObj)
			self.cache[blockTag] = tmpBlock
			TimeChecking.append(blockTag)

		elif(self.isInCache(blockTag) == True):
			cprint("Cache tag Hit","green")
			for val in self.cache:
				if(val == blockTag):
					if(self.cache[val].isInBlock(memoryObj) == True):
						self.cache[val].updateInMemoryArray(memoryObj)
					else:
						self.cache[val].insertInMemoryArray(memoryObj)
					break
			updateInTimeCheckingArr(blockTag)
		else:
			cprint("Cache tag miss","yellow")
			tmpBlock = Block(blockTag)
			tmpBlock.insertInMemoryArray(memoryObj)
			if(self.crntCacheSize < self.cacheLine):
				self.cache[blockTag] = tmpBlock
				self.crntCacheSize += 1
			else:
				# pdb.set_trace()
				cprint("Currently cache is full so using LRU policy to delete the oldest block from cache","yellow")
				cprint("The memory block deleted from the cache is: "+str(TimeChecking[0]),"yellow")
				cprint("contents","yellow")
				self.cache[TimeChecking[0]].printBlock()

				tmpPoppedBlockTag = TimeChecking.pop(0)
				deletedBlock = 0
				for val in self.cache:
					if(val == tmpPoppedBlockTag):
						deletedBlock = self.cache.pop(val)
						break

				self.cache[blockTag] = tmpBlock

			TimeChecking.append(blockTag)

	def readCache(self,memoryObj,blockTag):
		# pdb.set_trace()
		if(len(self.cache) == 0):
			cprint("The cache is empty","yellow")
			return
		found = self.isInCache(blockTag)

		if(found == True):
			cprint("Cache tag Hit","green")
			tmpObj = None

			for val in self.cache:
				if(val == blockTag):
					tmpObj = self.cache[val]

			tmpMemoryObj = None
			for val in tmpObj.memoryArr:
				if(val.memoryAddress == memoryObj.memoryAddress):
					print("The value at the memory address: "+str(memoryObj.memoryAddress)+" is "+str(val.memoryVal))
					tmpMemoryObj = val
					break

			updateInTimeCheckingArr(blockTag)
		else:
			cprint("The value doesn't exists in cache","yellow")


	def printCache(self):
		if(len(self.cache) == 0):
			cprint("The cache is empty","yellow")
			return
		count = 1;
		for val in self.cache:
			tmpStr = "Cache Line: "+str(count)
			cprint(tmpStr,"white","on_blue",attrs=["bold"])
			count += 1
			self.cache[val].printBlock();
		print()


class DirectMapping:

	def __init__(self,cacheLine,blockSize):
		self.cacheLine = cacheLine
		self.blockSize = blockSize
		self.cacheSize = self.cacheLine*self.blockSize
		self.crntCacheSize = 0
		self.cache={}
		global globalTime

	def isInCache(self,blockTagInput,dictIndex):
		if(dictIndex in self.cache.keys()):
			if(self.cache[dictIndex].blockTag == blockTagInput):
				return True
		return False

	def isIndexInCache(self,dictIndex):
		if(dictIndex in self.cache.keys()):
			return True
		return False

	def writeToCache(self,memoryObj,blockTag):
		# pdb.set_trace()
		dictIndex = int(memoryObj.memoryAddress/self.blockSize)
		dictIndex = int(dictIndex%self.cacheLine)

		if(len(self.cache) == 0):
			cprint("Cache tag Miss","yellow")
			self.crntCacheSize += 1
			tmpBlock = Block(blockTag)
			tmpBlock.insertInMemoryArray(memoryObj)
			self.cache[dictIndex] = tmpBlock

		elif(self.isInCache(blockTag,dictIndex) == True):
			# pdb.set_trace()
			cprint("Cache tag hit","green")
			found = self.cache[dictIndex].isInBlock(memoryObj)

			if(found == True):
				self.cache[dictIndex].updateInMemoryArray(memoryObj)
			else:
				self.cache[dictIndex].insertInMemoryArray(memoryObj)

		elif(self.isInCache(blockTag,dictIndex) == False):
			# pdb.set_trace()
			cprint("Cache tag miss","yellow")

			tmpBlock = Block(blockTag)
			tmpBlock.insertInMemoryArray(memoryObj)

			if(self.isIndexInCache(dictIndex) == True):
				cprint("replacing the value of "+str(dictIndex)+" in the cache with new memory block "+str(blockTag),"yellow")
				cprint("Contents that are replaced are: ","yellow")
				self.cache[dictIndex].printBlock()
				self.cache[dictIndex] = tmpBlock

			else:
				self.cache[dictIndex] = tmpBlock

	def readCache(self,memoryObj,blockTag):
		if(len(self.cache) == 0):
			cprint("The cache is empty","yellow")
			return

		dictIndex = int(memoryObj.memoryAddress/self.blockSize)
		dictIndex = int(dictIndex%self.cacheLine)

		if(self.isIndexInCache(dictIndex) == True):
			if(self.cache[dictIndex].blockTag == blockTag):
				
				if(self.cache[dictIndex].isInBlock(memoryObj) == False):
					cprint("The memory block doesn't exist","yellow")
					return

				cprint("Cache Tag hit","green")
				print("The value at the address is "+str(self.cache[dictIndex].getFromBlock(memoryObj).memoryVal))

			else:
				cprint("The memory block doesn't exist","yellow")

		else:
			cprint("The memory block doesn't exist","yellow")

	def printCache(self):
		if(len(self.cache) == 0):
			cprint("The cache is empty","yellow")
			return
		count = 1;
		tmpKeyLst = self.cache.keys()
		tmpKeyLst = list(tmpKeyLst)
		tmpKeyLst.sort()
		for val in tmpKeyLst:
			tmpStr = "Cache Line: "+str(int(int(self.cache[val].blockTag%self.cacheLine)))
			cprint(tmpStr,"white","on_blue",attrs=["bold"])
			count += 1
			self.cache[val].printBlock();
		print()


class SetObject:
	def __init__(self,cacheLines,blockSize):
		self.cacheLines = cacheLines
		self.blockSize = blockSize
		self.setSize = self.cacheLines*self.blockSize
		self.LocalTimeChecking = []
		self.crntCacheSize = 0
		self.setCache ={}
		global globalTime

	def isInCache(self,blockTag):
		if(self.crntCacheSize == 0):
			return False
		for val in self.setCache:
			if(val == blockTag):
				return True
		return False
	
	def updateLocalTimeCheckingArr(self,blockTag):
		for val in self.LocalTimeChecking:
			if(val == blockTag):
				self.LocalTimeChecking.remove(val)
				break
		self.LocalTimeChecking.append(blockTag)

	def writeInSetCache(self,memoryObj,blockTag):
		if(len(self.setCache) == 0):
			cprint("Cache tag miss","yellow")
			self.crntCacheSize += 1
			tmpBlock = Block(blockTag)
			tmpBlock.insertInMemoryArray(memoryObj)
			self.setCache[blockTag] = tmpBlock
			self.LocalTimeChecking.append(blockTag)

		elif(self.isInCache(blockTag) == True):
			cprint("Cache Hit","green")
			for val in self.setCache:
				if(val == blockTag):
					if(self.setCache[val].isInBlock(memoryObj) == True):
						self.setCache[val].updateInMemoryArray(memoryObj)
					else:
						self.setCache[val].insertInMemoryArray(memoryObj)
					break
			self.updateLocalTimeCheckingArr(blockTag)

		else:
			cprint("Cache tag miss","yellow")
			tmpBlock = Block(blockTag)
			tmpBlock.insertInMemoryArray(memoryObj)

			if(self.crntCacheSize < self.cacheLines):
				self.setCache[blockTag] = tmpBlock
				self.crntCacheSize += 1
				self.LocalTimeChecking.append(blockTag)

			else:
				cprint("Currently cache set is full so applying LRU policy in the set to pop element","yellow")
				cprint("The block popped is: "+str(self.LocalTimeChecking[0]),"yellow")
				cprint("contents:","yellow")
				self.setCache[self.LocalTimeChecking[0]].printBlock()
				tmpPoppedBlockTag = self.LocalTimeChecking.pop(0)

				deletedBlock = 0
				for val in self.setCache:
					if(val == tmpPoppedBlockTag):
						deletedBlock = self.setCache.pop(val)
						break
				
				self.setCache[blockTag] = tmpBlock
				self.LocalTimeChecking.append(blockTag)

	def readFromSetCache(self,memoryObj,blockTag):

		found = self.isInCache(blockTag)
		if(found == True):
			cprint("Cache hit","green")
			tmpObj = 0
			
			for val in self.setCache:
				if(val == blockTag):
					tmpObj = self.setCache[val]

			tmpMemoryObj = 0
			for val in tmpObj.memoryArr:
				if(val.memoryAddress == memoryObj.memoryAddress):
					print("The value of the memory address "+str(memoryObj.memoryAddress) +" is "+str(val.memoryVal))
					tmpMemoryObj = val
					break

			self.updateLocalTimeCheckingArr(blockTag)
			

		else:
			cprint("The memory address not found","yellow")

	def printCache(self):
		count = 1
		for val in self.setCache:
			tmpStr = "Cache Line: "+str(count)
			cprint(tmpStr,"white","on_blue",attrs=["bold"])
			count+=1
			self.setCache[val].printBlock()
		print()

class SetAssociative:
	def __init__ (self,cacheLines,blockSize,k):
		self.cacheLines = cacheLines
		self.blockSize = blockSize
		self.k = k
		self.numberOfSets = int(self.cacheLines/self.k)
		self.crntSetCount = 0
		self.cache = {}

	def isSetNumInCache(self,tmpSetNum):
		if(self.crntSetCount == 0):
			return False

		for val in self.cache:
			if(val == tmpSetNum):
				return True
		return False


	def writeToCache(self,memoryObj,blockTag):
		setNum = int(blockTag%self.numberOfSets)

		if(self.isSetNumInCache(setNum) == True):
			self.cache[setNum].writeInSetCache(memoryObj,blockTag)

		elif(self.isSetNumInCache(setNum) == False):
			tmpSetObject = SetObject(self.cacheLines/self.numberOfSets,self.blockSize)
			tmpSetObject.writeInSetCache(memoryObj,blockTag)
			self.cache[setNum] = tmpSetObject
			self.crntSetCount += 1

	def readCache(self,memoryObj,blockTag):
		if(len(self.cache) == 0):
			cprint("The cache is empty","yellow")
			return
		setNum = int(blockTag%self.numberOfSets)

		if(self.isSetNumInCache(setNum) == True):
			self.cache[setNum].readFromSetCache(memoryObj,blockTag)
		else:
			print("The memory block doesn't exists")

	def printCache(self):
		if(len(self.cache) == 0):
			cprint("The cache is empty","yellow")
			return
		for val in self.cache:
			cprint("the set number is: "+str(val),"white","on_magenta",attrs = ["bold"])
			self.cache[val].printCache()
			print()
		print()


def Main():
	cprint("Type of mapping: ","white","on_yellow",attrs=["bold","dark"])
	print("1. Direct Mapping")
	print("2. Fully Associative")
	print("3. Set Associative")
	mapping = input()
	mapping = mapping.lower()
	print()

	while(True):
		print("Enter the number of cache lines:",end=" ")
		cacheLinesInp = int(input())
		if(is2Power(cacheLinesInp) == False):
			cprint("Invalid input of cache line","red")
			cprint("try again","red")
			continue
		print("Enter the block size:",end=" ")
		blockSizeInp = int(input())
		if(is2Power(blockSizeInp) == False):
			cprint("Invalid input of block size","red")
			cprint("try again","red")
			continue
		break


	cprint("CACHE LINES: "+str(cacheLinesInp),"white","on_green",attrs=["bold"])
	cprint("BLOCK SIZE:  "+str(blockSizeInp),"white","on_green",attrs=["bold"])
	cprint("MAPPING:  "+str(mapping.upper()),"white","on_green",attrs=["bold"])

	if(mapping  == "direct mapping"):
		myCache =  DirectMapping(cacheLinesInp,blockSizeInp)
	elif(mapping == "fully associative"):
		myCache = FullyAssosiative(cacheLinesInp,blockSizeInp)
	elif(mapping == "set associative"):
		while(True):
			print("enter the value of k for k way set associative mapping")
			k = int(input())
			if(is2Power(k) == False):
				cprint("Invalid input of k","red")
				cprint("try again","red")
				continue
			myCache = SetAssociative(cacheLinesInp,blockSizeInp,k)
			break

	print()
	while(True):
		cprint("ENTER THE OPERATION","white","on_red",attrs=["bold"])
		print("1. WRITE (ADDRESS) (VALUE)")
		print("2. READ (ADDRESS)")
		print("3. CACHE ")
		print("4. CLEAR")
		print("5. EXIT")
		inp = input()
		print()

		if(inp == "EXIT"):
			break
		elif(inp == "CLEAR"):
			system("cls")
		elif(inp == "CACHE"):
			myCache.printCache()
		else:
			inpLst = []
			inpLst = inp.split(" ")

			if(len(inpLst) == 3):
				x=int(inpLst[1])
				y=int(inpLst[2])
				tmpMemoryObj = Memory(y,x,int(x/blockSizeInp),int(x%blockSizeInp))
				myCache.writeToCache(tmpMemoryObj,int(x/blockSizeInp))
			
			elif(len(inpLst) == 2):
				x = int(inpLst[1])
				tmpMemoryObj = Memory(-1,x,int(x/blockSizeInp),int(x%blockSizeInp))
				myCache.readCache(tmpMemoryObj,int(x/blockSizeInp))
		input()
Main()