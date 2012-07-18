import worker
import math
from math import sqrt
from numpy import arange
import pickle
import time

def f(x):
	return sqrt(x)

def g(x):
	return math.pow(x, 2)+f(abs(x))

def dot(f, g):
	return lambda x: f(g(x))

if __name__ == '__main__':
	c = worker.Caller("ipc://clientend")
	print c.eval(f, 10)
	c.shutdown()

