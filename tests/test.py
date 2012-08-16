import sys  
sys.path.append('..')
import Briareus
import math
from math import sin
from numpy import arange
import pickle
import time
import gevent

@Briareus.cloud
def f(x):
	for i in xrange(10000000):
		x += sin(x)
	return x

@Briareus.cloud
def g(x):
	return map(id, xrange(6))

def dot(f, g):
	return lambda x: f(g(x))

@Briareus.cloud
def test():
	return map(f, xrange(3))

if __name__ == '__main__':
	print g(10)
	# print Briareus.eval(str, 10)
