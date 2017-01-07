def addCount2Dict(d, key, value):
	if key in d:
		d[key] += value
	else:
		d[key] = value
	return