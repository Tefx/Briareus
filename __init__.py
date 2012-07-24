from netable import Client
from epickle import Pickler

__all__ = ['cloud', 'eval']


client = Client("tcp://192.168.70.101:8858")
pickler = Pickler()

def cloud(f):
	def g(*args):
		args = (f,) + args
		return client.call("eval", map(pickler.dumps, args))
	return g

def eval(*args):
	return client.call("eval", map(pickler.dumps, args))

if __name__ == '__main__':
	@cloud
	def g(x):
		return x+1
	print g(10)