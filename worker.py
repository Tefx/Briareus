import epickle
import netable
import uuid

class Worker(object):
	def __init__(self):
		self.pickler = epickle.Pickler()
		self.uuid = uuid.uuid1()

	def eval(self, f, *args):
		print "%s got job." % str(self.uuid)
		f = self.pickler.loads(f)
		args = map(self.pickler.loads, args)
		try:
			return f(*args)
		except Exception, e:
			return e
		


class Caller(object):
	def __init__(self, address):
		self.client = netable.Client(address)
		self.pickler = epickle.Pickler()

	def eval(self, *args):
		return self.client.call("eval", map(self.pickler.dumps, args))

	def shutdown(self):
		self.client.shutdown()

if __name__ == '__main__':
	from sys import argv, exit
	if len(argv) != 2:
		exit('Usage: %s address\nYou should ALWAYS use a script to launch workers.' % __file__)
	netable.Netable(Worker).run(argv[1], False)