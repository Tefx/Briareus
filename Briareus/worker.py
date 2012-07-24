import epickle
import netable
import uuid
import patches
import sys
import types

class Worker(object):
	def __init__(self, proxy_addr):
		self.pickler = epickle.Pickler()
		self.proxy_addr = proxy_addr
		self.client = netable.Client(proxy_addr)
		self.uuid = uuid.uuid1()
		self.map = patches.gen_map(self.proxy_addr)

	def eval(self, f, *args):
		func = self.pickler.loads(f)
		func = self.patch(func)
		args = map(self.pickler.loads, args)
		try:
			return func(*args)
		except Exception, e:
			return e

	def patch(self, f):
		if f is map:
			return self.map
		if isinstance(f, types.FunctionType):
			f.func_globals['map'] = self.map
		return f


