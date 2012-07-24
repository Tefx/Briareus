import sys  
sys.path.append('..')
import Briareus


import math
from math import sin
from numpy import arange
import pickle
import time
import gevent

def f(x):
	for i in xrange(1000000):
		x += sin(x)
	return x

@Briareus.cloud
def g(x):
	return math.pow(x, 2)+f(abs(x))

def dot(f, g):
	return lambda x: f(g(x))

if __name__ == '__main__':
	print g(10)