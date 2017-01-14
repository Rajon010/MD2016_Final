from sys import argv
import myUtil

dataFilenameListFilename = argv[1]
dataPath = argv[2]
inputFilename = argv[3]
outputFilename = argv[4]

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

def replaceDashWithPitch(period):
	prevSolmization = '-'
	for unit in period:
		for i in range(1, 1 + NB_NOTE_PER_UNIT):
			if unit[i] == '-':
				unit[i] = prevSolmization
			else:
				prevSolmization = unit[i]

NB_NOTE_PER_UNIT = 4
for nbTime, period in periodList:
	replaceDashWithPitch(period)
	# prevSolmization = '-'
	# for unit in period:
	# 	for i in range(1, 1 + NB_NOTE_PER_UNIT):
	# 		if unit[i] == '-':
	# 			unit[i] = prevSolmization
	# 		else:
	# 			prevSolmization = unit[i]

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

printProbMelodyGivenChord = False
if printProbMelodyGivenChord:
	for chord, subTable in probTable.items():
		print(chord)
		for i in range(NB_NOTE_PER_UNIT):
			print(i + 1, end='  ')
			for solmization, prob in subTable[i].items():
				print(solmization, ': ', format(prob, '.3f'), sep='', end=', ')
			print()

chordCntDict = {}
for chord, subTable in cntTable.items():
	cnt = 0
	for i in range(NB_NOTE_PER_UNIT):
		cnt = max(cnt, sum(subTable[i].values()))
	chordCntDict[chord] = cnt

sum_ = sum(chordCntDict.values())
chordProbDict = {chord: cnt / sum_ for chord, cnt in chordCntDict.items()}

printProbChord = False
if printProbChord:
	for chord, cnt in chordCntDict.items():
		print(chord, ': ', cnt, sep='', end=', ')
	print()
	for chord, prob in chordProbDict.items():
		print(chord, ': ', format(prob, '.3f'), sep='', end=', ')
	print()

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

printTestJointProbChordMelody = False
if printTestJointProbChordMelody:
	testList = [[s] * 4 for s in SOLMIZATIONS]
	testList += [['c', 'e', 'g', 'e'],
	             ['d', 'f', 'a', 'f'],
	             ['e', 'g', 'b', 'g'],
	             ['f', 'a', 'c', 'a'],
	             ['g', 'b', 'd', 'b'],
	             ['a', 'c', 'e', 'c'],
	             ['b', 'd', 'f', 'd'],
	             ['c', 'd', 'e', 'f'],
	             ['d', 'e', 'f', 'g'],
	             ['g', 'f', 'e', 'd'],
	             ['a', 'f', 'g', 'a'],
	             ['f', 'g', 'a', 'b'],
	             ['g', 'a', 'b', 'c'],
	             ['g', 'a', 'b', 'a'],
	             ['a', 'f', 'e', 'd'],
	             ['b', 'b', 'c', 'd']]
	for test in testList:
		for solmization in test:
			print(solmization, end=' ')
		print(end='  ')
		for chord, prob in calculateChord(test).items():
			print(chord, ': ', format(prob, '.3f'), sep='', end=', ')
		print()

	correctChordCntDict = {chord: 0 for chord in CHORDS}
	for nbTime, period in periodList:
		for unit in period:
			if unit[1][0] == '-':
				continue
			if unit[0] == max(calculateChord([s[0] for s in unit[1: 1 + NB_NOTE_PER_UNIT]]).items(), key=lambda x:x[1])[0]:
				correctChordCntDict[unit[0]] += nbTime
	for chord in CHORDS:
		print(chord, correctChordCntDict[chord], chordCntDict[chord], format(correctChordCntDict[chord] / chordCntDict[chord], '.3f'))
	nbCorrectChord = sum(correctChordCntDict.values())
	nbUnit = sum(chordCntDict.values())
	print('total', nbCorrectChord, nbUnit, format(nbCorrectChord / nbUnit, '.3f'))

printAllJointProbChordMelody = False
if printAllJointProbChordMelody:
	testChordCntDict = {chord: 0 for chord in CHORDS}
	for tuple_ in myUtil.generateAllTupleOrCombination(NB_NOTE_PER_UNIT, len(SOLMIZATIONS), myUtil.TUPLE):
		test = [SOLMIZATIONS[i] for i in tuple_]
		chord = max(calculateChord(test).items(), key=lambda x:x[1])[0]
		# if chord == 'Am':
		# 	print(test)
		testChordCntDict[chord] += 1
	print(testChordCntDict)


chord2ChordCntDict = {c1: {c2: 0 for c2 in CHORDS} for c1 in CHORDS}
for nbTime, period in periodList:
	for i in range(len(period) - 1):
		chord2ChordCntDict[period[i][0]][period[i + 1][0]] += nbTime
nbUnit = sum(chordCntDict.values())
chord2ChordProbDict = {c1: {c2: chord2ChordCntDict[c1][c2] / nbUnit for c2 in CHORDS} for c1 in CHORDS}

printJointProbChordChord = False
if printJointProbChordChord:
	print('x-axis: next chord, y-axis: this chord')
	print(end='\t')
	for chord in CHORDS:
		print(chord, end='\t')
	print()
	for thisChord in CHORDS:
		print(thisChord, end='\t')
		for nextChord in CHORDS:
			print(format(chord2ChordProbDict[thisChord][nextChord], '.3f'), end='\t')
		print()

solmization2ValueDict = {s: i for i, s in enumerate(SOLMIZATIONS)}
pitch2PitchCntDictList = [{s: {j: 0 for j in range(-len(SOLMIZATIONS), len(SOLMIZATIONS) + 1)} for s in SOLMIZATIONS} for i in range(NB_NOTE_PER_UNIT)]
def pitch2Value(pitch):
	return len(SOLMIZATIONS) * int(pitch[1]) + solmization2ValueDict[pitch[0]]
def computeDistanceOf2Pitch(base, target):
	return pitch2Value(target) - pitch2Value(base)
def add2Pitch2PitchCntDict(pitch2PitchCntDict, thisPitch, nextPitch, nbTime):
	if thisPitch == '-':
		return
	distance = computeDistanceOf2Pitch(thisPitch, nextPitch)
	if distance in pitch2PitchCntDict[thisPitch[0]]:
		pitch2PitchCntDict[thisPitch[0]][distance] += nbTime
for nbTime, period in periodList:
	periodLen = len(period)
	for i in range(periodLen - 1):
		for j in range(NB_NOTE_PER_UNIT - 1):
			add2Pitch2PitchCntDict(pitch2PitchCntDictList[j], period[i][j + 1], period[i][j + 2], nbTime)
		add2Pitch2PitchCntDict(pitch2PitchCntDictList[NB_NOTE_PER_UNIT - 1], period[i][NB_NOTE_PER_UNIT - 1 + 1], period[i + 1][1], nbTime)
	for j in range(NB_NOTE_PER_UNIT - 1):
		add2Pitch2PitchCntDict(pitch2PitchCntDictList[j], period[periodLen - 1][j + 1], period[periodLen - 1][j + 2], nbTime)

pitch2PitchProbDictList = [{s: {} for s in SOLMIZATIONS} for i in range(NB_NOTE_PER_UNIT)]
for i, pitch2PitchCntDict in enumerate(pitch2PitchCntDictList):
	sum_ = sum([sum(subDict.values()) for subDict in pitch2PitchCntDict.values()])
	for solmization, subDict in pitch2PitchCntDict.items():
		for distance, cnt in subDict.items():
			pitch2PitchProbDictList[i][solmization][distance] = cnt / sum_

printJointProbMelodyMelody = False
if printJointProbMelodyMelody:
	for i, pitch2PitchProbDict in enumerate(pitch2PitchProbDictList):
		print('y-axis: ', i, '-th note, x-axis: ', (i + 1) % NB_NOTE_PER_UNIT, '-th note', sep='')
		print(end='\t')
		# for i in range(-len(SOLMIZATIONS), len(SOLMIZATIONS) + 1):
		for i in range(-len(SOLMIZATIONS) + 3, len(SOLMIZATIONS) + 1): # terminal is too narrow
			print(i, end='\t')
		print()
		for s in SOLMIZATIONS:
			print(s, end='\t')
			# for distance in range(-len(SOLMIZATIONS), len(SOLMIZATIONS) + 1):
			for distance in range(-len(SOLMIZATIONS) + 3, len(SOLMIZATIONS) + 1): # terminal is too narrow
				print(format(pitch2PitchProbDict[s][distance] * 100, '.2f'), end='\t')
			print()
		print()

EPSILON = 1e-8

def pMM(m1, m2):
	base = m1[NB_NOTE_PER_UNIT - 1][0]
	distance = computeDistanceOf2Pitch(m1[NB_NOTE_PER_UNIT - 1], m2[0])
	if distance not in pitch2PitchProbDictList[NB_NOTE_PER_UNIT - 1][base]:
		return EPSILON
	return pitch2PitchProbDictList[NB_NOTE_PER_UNIT - 1][base][distance]

pMDict = {s: {} for s in SOLMIZATIONS}
def pMC(m, c):
	base = m[0][0]
	distanceTuple = tuple(computeDistanceOf2Pitch(m[i], m[i + 1]) for i in range(NB_NOTE_PER_UNIT - 1))
	if distanceTuple not in pMDict[base]:
		product = 1
		for i in range(NB_NOTE_PER_UNIT - 1):
			if (distanceTuple[i] not in pitch2PitchProbDictList[i][m[i][0]]) or (pitch2PitchProbDictList[i][m[i][0]][distanceTuple[i]] == 0):
				product *= EPSILON
			else:
				product *= pitch2PitchProbDictList[i][m[i][0]][distanceTuple[i]]
		pMDict[base][distanceTuple] = product
	return pMDict[base][distanceTuple] * calculateChord(tuple(pitch[0] for pitch in m))[c]

def pCC(c1, c2):
	return chord2ChordProbDict[c1][c2] if chord2ChordProbDict[c1][c2] != 0 else EPSILON

pitchList = [solmization + str(i) for i in range(8) for solmization in SOLMIZATIONS] + ['c8']
melody2DomainDict = {}
def getDomainM(m):
	highestPitch = max(m, key=lambda p:pitch2Value(p))
	lowestPitch = min(m, key=lambda p:pitch2Value(p))
	upperBound = min(pitch2Value(lowestPitch) + len(SOLMIZATIONS), len(SOLMIZATIONS) * 8 + 1 - 1) # included
	lowerBound = max(pitch2Value(highestPitch) - len(SOLMIZATIONS), len(SOLMIZATIONS) * 5)
	# print(upperBound, lowerBound)
	# print(pitchList[upperBound], pitchList[lowerBound])
	if (lowerBound, upperBound) not in melody2DomainDict:
		melody2DomainDict[(lowerBound, upperBound)] = [tuple(pitchList[index + lowerBound] for index in tuple_) for tuple_ in myUtil.generateAllTupleOrCombination(NB_NOTE_PER_UNIT, upperBound - lowerBound + 1, myUtil.TUPLE) if max(tuple_) - min(tuple_) <= len(SOLMIZATIONS)]
	return melody2DomainDict[(lowerBound, upperBound)]

def getDomainC(c):
	return CHORDS

with open(inputFilename, 'r') as f:
	lines = f.readlines()
lines = [line.rstrip().split() for line in lines]
replaceDashWithPitch(lines)
mrf = [(tuple(line[1: NB_NOTE_PER_UNIT + 1]) if line[1] != 'x' else None, line[0] if line[0] != 'X' else None) for line in lines]
print(mrf)

mrfResult = [(tuple(line[1: NB_NOTE_PER_UNIT + 1]) if line[1] != 'x' else None, line[0] if line[0] != 'X' else None) for line in lines]
from viterbiOn2ByLMRF import viterbiOn2ByLMRF
viterbiOn2ByLMRF(mrfResult, getDomainM, getDomainC, pMM, pMC, pCC)
print(mrfResult)

# for melody, chord in mrfResult:
# 	prevPitch = None
# 	for i in range(NB_NOTE_PER_UNIT):
# 		if melody[i] == prevPitch:
# 			melody[i] = '-'
# 		else:
# 			prevPitch = melody[i]

# for i in range(len(mrf)):
# 	for j in range(2):
# 		if mrf[i][j] != None:
# 			mrfResult[i] = mrfResult[i][:j] + (mrf[i][j],) + mrfResult[i][j + 1:]

with open(inputFilename, 'r') as f:
	inputLines = f.readlines()
inputLines = [line.rstrip().split() for line in inputLines]
with open(outputFilename, 'w') as f:
	for i in range(len(mrfResult)):
		f.write(mrfResult[i][1])
		f.write(' ')
		if inputLines[i][1] != 'x':
			for pitch in inputLines[i][1:]:
				f.write(pitch)
				f.write(' ')
		else:
			prevPitch = None
			for pitch in mrfResult[i][0]:
				if pitch == prevPitch:
					f.write('-')
				else:
					f.write(pitch)
					prevPitch = pitch
				f.write(' ')
		f.write('\n')