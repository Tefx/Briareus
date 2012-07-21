import worker
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

def g(x):
	return math.pow(x, 2)+f(abs(x))

def dot(f, g):
	return lambda x: f(g(x))

def test(i):
<<<<<<< HEAD
	c = worker.Caller("tcp://localhost:8858")
=======
	c = worker.Caller("tcp://192.168.70.101:8858")
>>>>>>> aabe1df4895ba25f0ee3d9602c85b349696e2ecb
	h = dot(f,g)
	print c.eval(h, i)
	c.shutdown()

if __name__ == '__main__':
	jobs = [gevent.spawn(test, i) for i in xrange(2)]
	gevent.joinall(jobs)

	# for i in xrange(100):
	# 	h = dot(f,g)
	# 	print h(i)

	# c = worker.Caller("tcp://192.168.70.101:8858")
	# print c.eval(g, 10)
	# c.shutdown()
