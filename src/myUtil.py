from math import log

def addCount2Dict(d, key, value):
	if key in d:
		d[key] += value
	else:
		d[key] = value
	return

TUPLE = True
COMBINATION = False

def generateAllTupleOrCombinationRecursion(allPossibility, length, tupleElementUpperBound, isTupleOrCombination, tupleOrCombination):
	if len(tupleOrCombination) == length:
		allPossibility.append(tupleOrCombination)
		return

	if isTupleOrCombination:
		# tuple
		elementLowerBound = 0
		elementUpperBound = tupleElementUpperBound
	else:
		# combination
		if len(tupleOrCombination) == 0:
			elementLowerBound = 0
		else:
			elementLowerBound = tupleOrCombination[len(tupleOrCombination) - 1] + 1
		elementUpperBound = tupleElementUpperBound - (length - len(tupleOrCombination)) + 1
		
	for i in range(elementLowerBound, elementUpperBound):
		generateAllTupleOrCombinationRecursion(allPossibility, length, tupleElementUpperBound, isTupleOrCombination, tupleOrCombination + (i,))

def generateAllTupleOrCombination(length, elementUpperBound, isTupleOrCombination):
	allPossibility = []
	generateAllTupleOrCombinationRecursion(allPossibility, length, elementUpperBound, isTupleOrCombination, tuple())
	return allPossibility

NEGATIVE_INFINITY = float('-inf')

def myNaturalLog(x):
	if x <= 0.0:
		return NEGATIVE_INFINITY # log(0) = -infinity
	return log(x)