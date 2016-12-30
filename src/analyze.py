from sys import argv

dataFilenameListFilename = argv[1]
dataPath = argv[2]

def addCount2Dict(d, key, value):
	if key in d:
		d[key] += value
	else:
		d[key] = value
	return

with open(dataFilenameListFilename, 'r') as f:
	dataFilenameList = f.readlines()
dataFilenameList = [dataFilename.rstrip() for dataFilename in dataFilenameList]

chordCountDictAll = {}

for dataFilename in dataFilenameList:
	with open(dataPath + dataFilename, 'r') as f:
		lines = f.readlines()
	lines = [line.rstrip().split() for line in lines]

	chordCountDict = {}
	for line in lines:
		if line[0] == '@':
			time_ = int(line[1][1:])
			continue
		addCount2Dict(chordCountDict, line[0], time_)
	print(dataFilename, chordCountDict)

	for key, value in chordCountDict.items():
		addCount2Dict(chordCountDictAll, key, value)

print('sum', chordCountDictAll)