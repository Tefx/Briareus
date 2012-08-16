from netable import Client
from epickle import Pickler

__all__ = ['cloud', 'eval']

client = Client("tcp://210.72.68.189:8858")
pickler = Pickler()

def cloud(f):
	def g(*args):
		args = (f,) + args
		return client.call("eval", map(pickler.dumps, args))
	return g

def eval(*args):
	return client.call("eval", map(pickler.dumps, args))
