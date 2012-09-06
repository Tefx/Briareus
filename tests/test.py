import sys  
sys.path.append('..')
from Briareus import cloud
from math import sin


#@cloud
def f(x):
	for i in xrange(1000000):
		x += sin(x)
	return x

@cloud
def g(x):
	return map(f, xrange(10))

def dot(f, g):
	return lambda x: f(g(x))

def add(a, b):
	return a+b

if __name__ == '__main__':
	print g(1)
	# print Briareus.eval(str, 10)
