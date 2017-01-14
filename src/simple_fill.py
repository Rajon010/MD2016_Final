from sys import argv
import numpy
import random

# setup file path
dataFilenameListFilename = argv[1]
dataPath = argv[2]
inputFile = argv[3]
outputFile = argv[4]

# setup chords
chords = ["C", "Dm", "F", "G", "Am"]

# init dict list
chordDicts = []
for i in range(5):
	chordDicts.append( dict() )

# train
with open(dataFilenameListFilename, "r") as f:
	dataFilenameList = f.readlines()
	dataFilenameList = [dataFilename.rstrip() for dataFilename in dataFilenameList]
	for dataFilename in dataFilenameList:
		with open(dataPath + dataFilename, "r") as f:
			lines = f.readlines()
		lines = [line.rstrip().split() for line in lines]
		for line in lines:
			if line[0] == "@":
				continue
			dict = chordDicts[chords.index(line[0])]
			key = line[1] + " " + line[2] + " " + line[3] + " " + line[4]
			dict[key] = (dict[key] + 1) if key in dict else 1
# print(chordDicts)

# test
with open(inputFile, "r") as f:
	lines = f.readlines()
lines = [line.rstrip().split() for line in lines]

with open(outputFile, "w") as f:
	for line in lines:
		chord = random.choice(chords) if line[0] == "X" else line[0]
		dict = chordDicts[chords.index(chord)]
		maxKey = list( dict.keys() )[0]
		for key in dict:
			maxKey = key if dict[key] > dict[maxKey] else maxKey
		dict[maxKey] = dict[maxKey] - 100
		f.write(chord + " " + maxKey + "\n")

