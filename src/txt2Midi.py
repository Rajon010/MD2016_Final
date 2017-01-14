from sys import argv
from mido import Message, MidiFile, MidiTrack

if len(argv) != 5:
	print('python3 this.py inFileName outFileName hasNote hasChord')
	print('example: python3 this.py in out 1 0')
	exit()
inFileName = argv[1]
outFileName = argv[2]
hasNote = bool(int(argv[3]))
hasChord = bool(int(argv[4]))
if not (hasNote or hasChord):
	print('at least one of hasNote and hasChord needs to be 1')
	exit()

with open(inFileName, 'r') as f:
	lines = f.readlines()
lines = [line.rstrip().split() for line in lines]

midiFile = MidiFile()
track = MidiTrack()
midiFile.tracks.append(track)
track.append(Message('program_change', program=0))

wwhwwwhww = [2, 2, 1, 2, 2, 2, 1, 2, 2]
wwhwwwhwwCumulative = [sum(wwhwwwhww[:i]) for i in range(len(wwhwwwhww) + 1)]
chord2IndexDict = {
	'C': 0,
	'Dm': 1,
	'Em': 2,
	'F': 3,
	'G': 4,
	'Am': 5
}
noteName2IndexDict = {
	'c': 0,
	'd': 1,
	'e': 2,
	'f': 3,
	'g': 4,
	'a': 5,
	'b': 6
}
def baseAndIndex2Key(base, n):
	return base * 12 + wwhwwwhwwCumulative[n]

speed = 112
timeDelta = int(60 / speed * 1000 / 4) # must be int

def appendNoteByKey(_track, n, t):
	if n == -1:
		return t + timeDelta
	track.append(Message('note_on', note=n, time=t))
	return timeDelta

def appendChord(_track, c, t):
	if c == 'X' or not hasChord:
		return t
	chordBaseIndex = chord2IndexDict[c]
	for i in range(0, 5, 2):
		appendNoteByKey(_track, baseAndIndex2Key(4, chordBaseIndex + i), t)
		t = 0
	return 0

def appendNoteByStr(_track, s, t):
	if s in ['-', 'x'] or not hasNote:
		return t + timeDelta
	return appendNoteByKey(_track, baseAndIndex2Key(int(s[1]), noteName2IndexDict[s[0]]), t)

timeInterval = 0
for line in lines:
	if line[0] == '@':
		continue
	if line[0] == '#':
		break
	timeInterval = appendChord(track, line[0], timeInterval)
	for i in range(1, 5):
		timeInterval = appendNoteByStr(track, line[i], timeInterval)
track.append(Message('note_off', note=0, time=timeInterval + timeDelta * 4))

midiFile.save(outFileName + '.mid')
