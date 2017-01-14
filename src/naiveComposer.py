from sys import argv
from random import choice

dataFilenameListFilename = argv[1]
dataPath = argv[2]
inputFilename = argv[3]
outputFilename = argv[4]

with open(dataFilenameListFilename, 'r') as f:
	dataFilenameList = f.readlines()
dataFilenameList = [dataFilename.rstrip() for dataFilename in dataFilenameList]

chordCntDict = {}
melocyCntDict = {}

for dataFilename in dataFilenameList:
	with open(dataPath + dataFilename, 'r') as f:
		lines = f.readlines()
	lines = [line.rstrip().split() for line in lines]
	for line in lines:
		if line[0] == '@':
			nbTime = int(line[1][1:])
			continue
		chord = line[0]
		melody = ' '.join(line[1: 1 + 4])
		if chord in chordCntDict:
			chordCntDict[chord] += nbTime
		else:
			chordCntDict[chord] = nbTime
		if melody in melocyCntDict:
			melocyCntDict[melody] += nbTime
		else:
			melocyCntDict[melody] = nbTime

sortedMelodyList = list(sorted(melocyCntDict.items(), key=lambda x:x[1], reverse=True))
sortedChordList = list(sorted(chordCntDict.items(), key=lambda x:x[1], reverse=True))
chordSampleList = []
for key, value in sortedChordList:
	chordSampleList += [key] * value

with open(inputFilename, 'r') as f:
	inputLines = f.readlines()
inputLines = [line.rstrip().split() for line in inputLines]

with open(outputFilename + '_naive', 'w') as f:
	# chordIndex = 0
	melocyIndex = 0
	for line in inputLines:
		if line[0] == 'X':
			# f.write(sortedChordList[chordIndex % len(sortedChordList)][0])
			# chordIndex += 1
			f.write(choice(chordSampleList))
		else:
			f.write(line[0])
		f.write(' ')
		if line[1] == 'x':
			f.write(sortedMelodyList[melocyIndex % len(sortedMelodyList)][0])
			melocyIndex += 1
		else:
			for i in range(1, 5):
				f.write(line[i])
				f.write(' ')
		f.write('\n')
