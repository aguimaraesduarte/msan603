import numpy as np

def trucksim(n, d):
	return list(np.random.choice(d.keys(), size = n, replace = True, p = d.values()))

def truck1CI(keyname, simlist, n, alpha):
	samples = []
	percents_keyname = []
	for i in range(n):
		sample = list(np.random.choice(simlist, len(simlist)))
		percent_keyname = float(sample.count(keyname))/len(sample)
		samples.append(sample)
		percents_keyname.append(percent_keyname)
	return (np.mean(percents_keyname),
			np.percentile(percents_keyname, (alpha/2.0)*100),
			np.percentile(percents_keyname, (1-alpha/2.0)*100),
			np.std(percents_keyname))

d = {"<10": .08,
	 "10-15": .27,
	 "15-20": .10,
	 "20-25": .11,
	 "25-30": .15,
	 "30-35": .20,
	 "35-37": .07,
	 "37+": .02}
n = 1000
alpha = 0.1

simlist = trucksim(n, d)

print "2-a)"
m, l, u, s = truck1CI("30-35", simlist, 100, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
m, l, u, s = truck1CI("30-35", simlist, 1000, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
m, l, u, s = truck1CI("30-35", simlist, 2500, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
m, l, u, s = truck1CI("30-35", simlist, 5000, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
m, l, u, s = truck1CI("<10", simlist, 100, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
m, l, u, s = truck1CI("<10", simlist, 1000, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
m, l, u, s = truck1CI("<10", simlist, 2500, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
m, l, u, s = truck1CI("<10", simlist, 5000, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)

print
print "3"
alpha = 0.05
m, l, u, s = truck1CI("35-37", simlist, 200, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
m, l, u, s = truck1CI("37+", simlist, 200, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
alpha = 0.1
m, l, u, s = truck1CI("35-37", simlist, 200, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)
m, l, u, s = truck1CI("37+", simlist, 200, alpha)
print "m={}, l={}, u={}, s={}".format(m, l, u, s)

print
print "4"
total = 0
for i in range(1000):
	trucks = trucksim(4989, d)
	cnt = trucks.count("35-37")
	if cnt >= 368:
		total += 1
l = total/1000.0
print "p(35-37): {}".format(l)

total = 0
for i in range(1000):
	trucks = trucksim(4989, d)
	cnt = trucks.count("37+")
	if cnt >= 108:
		total += 1
l = total/1000.0
print "p(37+): {}".format(l)

print
print "5"
inter = 0
a = 0
b = 0
union = 0
for i in range(1000):
	trucks = trucksim(4989, d)
	cnt1 = trucks.count("35-37")
	cnt2 = trucks.count("37+")
	if cnt1 >= 368 and cnt2 >= 108:
		inter += 1
	if cnt1 >= 368:
		a += 1
	if cnt2 >= 108:
		b += 1
	if cnt1 >= 368 or cnt2 >= 108:
		union += 1
print "p(35-37 and 37+): {}".format(inter/1000.0)
print "p(35-37): {}".format(a/1000.0)
print "p(37+): {}".format(b/1000.0)
print "p(35-37 or 37+): {}".format(union/1000.0)
print "Do we have p(35-37 and 37+) = p(35-37) + p(37+) - p(35-37 or 37+)?"
print "{}+{}-{}={}".format(a/1000.0, b/1000.0, union/1000.0, (a/1000.0) + (b/1000.0) - (union/1000.0))
print "yes!"