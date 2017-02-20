import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import triang
import random

def f(x,n):
	return ((n-1.)*x+5)/n

x = [i/100. for i in range(500,1001)]
y2 = [f(v,2) for v in x]
y5 = [f(v,5) for v in x]
y10 = [f(v,10) for v in x]

plt.plot(x,y2, label="n=2")
plt.plot(x,y5, label="n=5")
plt.plot(x,y10, label="n=10")
plt.legend(loc=2)
plt.show()

def tri(n):
	t = triang(1000)
	return np.array([sum(t[:random.randint(0,999)])/sum(t) for i in range(n)])


def Fn1(v, n):
	return (sum(tri(1000)<v)/1000.)**(n-1)


v_list_2 = [Fn1(v/1000., 2) for v in range(0,1001)]
v_list_5 = [Fn1(v/1000., 5) for v in range(0,1001)]
v_list_10 = [Fn1(v/1000., 10) for v in range(0,1001)]

def intFn1(val, n, v_list):
	return sum(v_list[:int(val*1000)]) * 0.001


x = [i/1000. for i in range(1001)]
y2 = [v - intFn1(v, 2, v_list_2)/Fn1(v, 2) for v in x]
y5 = [v - intFn1(v, 5, v_list_5)/Fn1(v, 5) for v in x]
y10 = [v - intFn1(v, 10, v_list_10)/Fn1(v, 10) for v in x]

plt.plot(x,y2, label="n=2")
plt.plot(x,y5, label="n=5")
plt.plot(x,y10, label="n=10")
plt.legend(loc=2)
plt.show()