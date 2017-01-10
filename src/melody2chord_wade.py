import numpy
from myUtil import addCount2Dict

class M2CPotential:
	def __init__(self, _dataFilenameListFilename, _dataPath):
		self.dataFilenameListFilename = _dataFilenameListFilename
		self.dataPath = _dataPath
		# key = ("[C|Dm|Am|G|F]" + "[1|2|3|4|12|23|...|1234]" + "[abcdefg-]+"), value = counts
		self.memoryChordDict = {}
		# key = "[C|Dm|Am|G|F]", value = counts
		self.chordCountDict = {}

	def train(self):
		with open(self.dataFilenameListFilename, "r") as f:
			dataFilenameList = f.readlines()
		dataFilenameList = [dataFilename.rstrip() for dataFilename in dataFilenameList]
		for dataFilename in dataFilenameList:
			with open(self.dataPath + dataFilename, "r") as f:
				lines = f.readlines()
			lines = [line.rstrip().split() for line in lines]
			for line in lines:
				if line[0] == "@":
					continue
				self.chordCountDict[line[0]] = (self.chordCountDict[line[0]] + 1) if line[0] in self.chordCountDict else 1
				for i in range(4):
					if(line[i + 1] == "-"):
						continue
					key = line[0] + str(i + 1) + line[i + 1][0]
					self.memoryChordDict[key] = (self.memoryChordDict[key] + 1) if (key in self.memoryChordDict) else 1
					if(i > 0):
						key = line[0] + str(i) + str(i + 1) + line[i][0] + line[i + 1][0]
						self.memoryChordDict[key] = (self.memoryChordDict[key] + 1) if (key in self.memoryChordDict) else 1
					if(i > 1):
						key = line[0] + str(i - 1) + str(i) + str(i + 1) + line[i - 1][0] + line[i][0] + line[i + 1][0]
						self.memoryChordDict[key] = (self.memoryChordDict[key] + 1) if (key in self.memoryChordDict) else 1
					if(i > 2):
						key = line[0] + "1234" + line[i - 2][0] + line[i - 1][0] + line[i][0] + line[i + 1][0]
						self.memoryChordDict[key] = (self.memoryChordDict[key] + 1) if (key in self.memoryChordDict) else 1
		# print(self.memoryChordDict)
		# print(self.chordCountDict)

	def getProbOfChords(self, _melody):
		count = [0, 0, 0, 0, 0]
		chordList = ["C", "Dm", "F", "G", "Am"]
		for i in range(4):
			for c in range(5):
				key = chordList[c] + str(i + 1) + _melody[i][0]
				count[c] = (count[c] + self.memoryChordDict[key]) if key in self.memoryChordDict else count[c]
				if(i > 0):
					key = chordList[c] + str(i) + str(i + 1) + _melody[i - 1][0] + _melody[i][0]
					count[c] = (count[c] + 2 * self.memoryChordDict[key]) if key in self.memoryChordDict else count[c]
				if(i > 1):
					key = chordList[c] + str(i - 1) + str(i) + str(i + 1) + _melody[i - 2][0] + _melody[i - 1][0] + _melody[i][0]
					count[c] = (count[c] + 4 * self.memoryChordDict[key]) if key in self.memoryChordDict else count[c]
				if(i > 2):
					key = chordList[c] + "1234" + _melody[i - 3][0] + _melody[i - 2][0] + _melody[i - 1][0] + _melody[i][0]
					count[c] = (count[c] + 8 * self.memoryChordDict[key]) if key in self.memoryChordDict else count[c]
		for c in range(5):
			count[c] = count[c] / self.chordCountDict[chordList[c]]
		return list( numpy.exp( numpy.array(count) ) / numpy.sum( numpy.exp( numpy.array(count) ), axis = 0 ) )

