import numpy as np

def firstPrice(size, n):
	samples = [sorted(np.random.uniform(0, 1, n)) for i in range(size)]
	maxes = [s[-1] for s in samples]

	return (np.mean(maxes)*(n-1.)/n)

def secondPrice(size, n):
	samples = [sorted(np.random.uniform(0, 1, n)) for i in range(size)]
	second_maxes = [s[-2] for s in samples]

	return (np.mean(second_maxes))

size = 100000
for n in [2, 10]:
	print "{} bidders, first price".format(n)
	print "{}".format(firstPrice(size, n))
	print
	print "{} bidders, second price".format(n)
	print "{}".format(secondPrice(size, n))
	print
