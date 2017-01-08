from sys import argv
import myUtil

dataFilenameListFilename = argv[1]
dataPath = argv[2]

with open(dataFilenameListFilename, 'r') as f:
	dataFilenameList = f.readlines()
dataFilenameList = [dataFilename.rstrip() for dataFilename in dataFilenameList]

periodList = [] # stores unit: (nbTime, period)

for dataFilename in dataFilenameList:
	with open(dataPath + dataFilename, 'r') as f:
		lines = f.readlines()
	lines = [line.rstrip().split() for line in lines]
	nbLine = len(lines)
	lineIndex = 0
	while lineIndex < nbLine:
		nbTime = int(lines[lineIndex][1][1:])
		lineIndex += 1
		periodHeadIndex = lineIndex
		while (lineIndex < nbLine) and (lines[lineIndex][0] != '@'):
			lineIndex += 1
		periodList.append((nbTime, lines[periodHeadIndex: lineIndex]))


NB_NOTE_PER_UNIT = 4
for nbTime, period in periodList:
	lastSolmization = '-'
	for unit in period:
		for i in range(1, 1 + NB_NOTE_PER_UNIT):
			if unit[i] == '-':
				unit[i] = lastSolmization
			else:
				lastSolmization = unit[i]

CHORDS = ['C', 'Dm', 'F', 'G', 'Am']
SOLMIZATIONS = ['c', 'd', 'e', 'f', 'g', 'a', 'b']


def constructTable(initValue):
	table = {}
	for chord in CHORDS:
		table[chord] = [{} for i in range(NB_NOTE_PER_UNIT)]
		for solmizationDict in table[chord]:
			for solmization in SOLMIZATIONS:
				solmizationDict[solmization] = initValue
	return table

cntTable = constructTable(0) # this[chord][i-th note][solmization] = count
for nbTime, period in periodList:
	for unit in period:
		chord = unit[0]
		for i in range(1, 1 + NB_NOTE_PER_UNIT):
			if unit[i] == '-':
				continue
			cntTable[chord][i - 1][unit[i][0]] += nbTime

probTable = constructTable(0) # this[chord][i-th note][solmization] = prob
for chord, subTable in cntTable.items():
	for i in range(NB_NOTE_PER_UNIT):
		sum_ = sum(subTable[i].values())
		for solmization, cnt in subTable[i].items():
			probTable[chord][i][solmization] = cnt / sum_

# for chord, subTable in probTable.items():
# 	print(chord)
# 	for i in range(NB_NOTE_PER_UNIT):
# 		print(i + 1, end='  ')
# 		for solmization, prob in subTable[i].items():
# 			print(solmization, ': ', format(prob, '.3f'), sep='', end=', ')
# 		print()

chordCntDict = {}
for chord, subTable in cntTable.items():
	cnt = 0
	for i in range(NB_NOTE_PER_UNIT):
		cnt = max(cnt, sum(subTable[i].values()))
	chordCntDict[chord] = cnt

sum_ = sum(chordCntDict.values())
chordProbDict = {chord: cnt / sum_ for chord, cnt in chordCntDict.items()}

# for chord, cnt in chordCntDict.items():
# 	print(chord, ': ', cnt, sep='', end=', ')
# print()
# for chord, prob in chordProbDict.items():
# 	print(chord, ': ', format(prob, '.3f'), sep='', end=', ')
# print()

def calculateChord(solmizationList):
	probMelodyGivenChord = {}
	for chord in CHORDS:
		product = 1
		for i in range(NB_NOTE_PER_UNIT):
			product *= probTable[chord][i][solmizationList[i]]
		probMelodyGivenChord[chord] = product
	probMelodyAndChord = {}
	for chord in CHORDS:
		probMelodyAndChord[chord] = probMelodyGivenChord[chord] * chordProbDict[chord]
	probMelody = sum(probMelodyAndChord.values())
	probChordGivenMelody = {}
	for chord in CHORDS:
		probChordGivenMelody[chord] = probMelodyAndChord[chord] / probMelody
	return probChordGivenMelody

# testList = [[s] * 4 for s in SOLMIZATIONS]
# testList += [['c', 'e', 'g', 'e'],
#              ['d', 'f', 'a', 'f'],
#              ['e', 'g', 'b', 'g'],
#              ['f', 'a', 'c', 'a'],
#              ['g', 'b', 'd', 'b'],
#              ['a', 'c', 'e', 'c'],
#              ['b', 'd', 'f', 'd'],
#              ['c', 'd', 'e', 'f'],
#              ['d', 'e', 'f', 'g'],
#              ['g', 'f', 'e', 'd'],
#              ['a', 'f', 'g', 'a'],
#              ['f', 'g', 'a', 'b'],
#              ['g', 'a', 'b', 'c'],
#              ['g', 'a', 'b', 'a'],
#              ['a', 'f', 'e', 'd'],
#              ['b', 'b', 'c', 'd']]
# for test in testList:
# 	for solmization in test:
# 		print(solmization, end=' ')
# 	print(end='  ')
# 	for chord, prob in calculateChord(test).items():
# 		print(chord, ': ', format(prob, '.3f'), sep='', end=', ')
# 	print()

# correctChordCntDict = {chord: 0 for chord in CHORDS}
# for nbTime, period in periodList:
# 	for unit in period:
# 		if unit[1][0] == '-':
# 			continue
# 		if unit[0] == max(calculateChord([s[0] for s in unit[1: 1 + NB_NOTE_PER_UNIT]]).items(), key=lambda x:x[1])[0]:
# 			correctChordCntDict[unit[0]] += nbTime
# for chord in CHORDS:
# 	print(chord, correctChordCntDict[chord], chordCntDict[chord], format(correctChordCntDict[chord] / chordCntDict[chord], '.3f'))
# nbCorrectChord = sum(correctChordCntDict.values())
# nbUnit = sum(chordCntDict.values())
# print('total', nbCorrectChord, nbUnit, format(nbCorrectChord / nbUnit, '.3f'))

# testChordCntDict = {chord: 0 for chord in CHORDS}
# for tuple_ in myUtil.generateAllTupleOrCombination(NB_NOTE_PER_UNIT, len(SOLMIZATIONS), myUtil.TUPLE):
# 	test = [SOLMIZATIONS[i] for i in tuple_]
# 	chord = max(calculateChord(test).items(), key=lambda x:x[1])[0]
# 	# if chord == 'Am':
# 	# 	print(test)
# 	testChordCntDict[chord] += 1
# print(testChordCntDict)


chord2ChordCntDict = {c1: {c2: 0 for c2 in CHORDS} for c1 in CHORDS}
for nbTime, period in periodList:
	for i in range(len(period) - 1):
		chord2ChordCntDict[period[i][0]][period[i + 1][0]] += nbTime
nbUnit = sum(chordCntDict.values())
chord2ChordProbDict = {c1: {c2: chord2ChordCntDict[c1][c2] / nbUnit for c2 in CHORDS} for c1 in CHORDS}
# print('x-axis: next chord, y-axis: this chord')
# print(end='\t')
# for chord in CHORDS:
# 	print(chord, end='\t')
# print()
# for thisChord in CHORDS:
# 	print(thisChord, end='\t')
# 	for nextChord in CHORDS:
# 		print(format(chord2ChordProbDict[thisChord][nextChord], '.3f'), end='\t')
# 	print()

