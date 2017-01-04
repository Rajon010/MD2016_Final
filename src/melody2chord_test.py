from sys import argv
import melody2chord

dataFilenameListFilename = argv[1]
dataPath = argv[2]

potential = melody2chord.M2CPotential(dataFilenameListFilename, dataPath)
potential.train()

probs = potential.getProbOfChords( ["a6", "f6", "a6", "f6"] )
print("P([C,Dm,F,G,Am]|[a6,f6,a6,f6]) =", probs)

probs = potential.getProbOfChords( ["f5", "a5", "f5", "d5"] )
print("P([C,Dm,F,G,Am]|[f5,a5,f5,d5]) =", probs)

probs = potential.getProbOfChords( ["e6", "g6", "e6", "c6"] )
print("P([C,Dm,F,G,Am]|[e6,g6,e6,c6]) =", probs)

probs = potential.getProbOfChords( ["f5", "-", "-", "d5"] )
print("P([C,Dm,F,G,Am]|[f5,-,-,d5]) =", probs)

