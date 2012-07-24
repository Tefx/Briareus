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