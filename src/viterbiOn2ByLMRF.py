from myUtil import myNaturalLog

def viterbiOn2ByLMRF(mrf, getDomain0, getDomain1, p00, p01, p11):
	'''
		mrf:
		[0][0] ---p00--- [1][0] ---p00--- [2][0] ---p00--- [3][0]
		|                |                |                |
		p01              p01              p01              p01
		|                |                |                |
		[0][1] ---p11--- [1][1] ---p11--- [2][1] ---p11--- [3][1]

		Domain of mrf[i][J] is getDomainJ(mrf[i - 1][J])
	'''

	L = len(mrf)
	prevVarDict = [{} for i in range(L)]
	domain00 = {mrf[0][0]} if mrf[0][0] != None else getDomain0(None)
	domain01 = {mrf[0][1]} if mrf[0][1] != None else getDomain1(None)
	thisPDict = {(var0, var1): myNaturalLog(p01(var0, var1)) for var0 in domain00 for var1 in domain01}

	for i in range(1, L):
		prevPDict = thisPDict
		thisPDict = {}
		for prevVar, prevP in prevPDict.items():
			domain0 = {mrf[i][0]} if mrf[i][0] != None else getDomain0(prevVar[0])
			domain1 = {mrf[i][1]} if mrf[i][1] != None else getDomain1(prevVar[1])
			domain = {(var0, var1) for var0 in domain0 for var1 in domain1}
			if len(domain) == 0:
				print('error: empty domain at column', i)
			for thisVar in domain:
				thisP = prevP + myNaturalLog(p00(prevVar[0], thisVar[0])) + myNaturalLog(p01(thisVar[0], thisVar[1])) + myNaturalLog(p11(prevVar[1], thisVar[1]))
				if (thisVar not in thisPDict) or (thisP > thisPDict[thisVar]):
					thisPDict[thisVar] = thisP
					prevVarDict[i][thisVar] = prevVar

	mrf[L - 1] = max(thisPDict.items(), key=lambda x:x[1])[0]
	for i in range(L - 2, -1, -1):
		mrf[i] = prevVarDict[i + 1][mrf[i + 1]]

if __name__ == '__main__':
	mrf = [(None, None), 
		   (None, None), 
		   (   3, None), 
		   (None, None), 
		   (   3, None), 
		   (None, None), 
		   (   3, None)]
	viterbiOn2ByLMRF(mrf, lambda x:{i for i in range(7)}, lambda x:{i for i in range(5)}, lambda x,y:(x+y), lambda x,y:x*y, lambda x,y:1)
	print(mrf)