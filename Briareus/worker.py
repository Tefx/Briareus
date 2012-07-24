import epickle
import netable
import uuid
import patches

class Worker(object):
	def __init__(self, proxy_addr):
		self.pickler = epickle.Pickler()
		self.proxy_addr = proxy_addr
		self.client = netable.Client(proxy_addr)
		self.uuid = uuid.uuid1()

	def eval(self, f, *args):
		print "%s got job." % str(self.uuid)
		f = self.pickler.loads(f)
		self.patch(f)
		args = map(self.pickler.loads, args)
		try:
			return f(*args)
		except Exception, e:
			return e

	def patch(self, f):
		f.func_globals["Briareus_proxy_addr"] = self.proxy_addr
		if 'map' in f.func_globals:
			f.func_globals['map'] = patches.map


