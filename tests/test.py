import sys  
sys.path.append('..')
from Briareus import cloud
from math import sin

#@cloud
def f(x):
	for i in xrange(1000000):
		x += sin(x)
	return x

def g(x):
	return map(f, xrange(6))

def dot(f, g):
	return lambda x: f(g(x))

if __name__ == '__main__':
	print f(7)
	# print Briareus.eval(str, 10)
