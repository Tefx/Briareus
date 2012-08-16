import epickle
import netable
import uuid
import patches
import sys
import types
import log

Logger = log.Logger("worker")

class Worker(object):
	def __init__(self, proxy_addr):
		self.pickler = epickle.Pickler()
		self.proxy_addr = proxy_addr
		self.client = netable.Client(proxy_addr)
		self.uuid = uuid.uuid1()
		self.map = patches.gen_map(self.proxy_addr)

	def eval(self, f, *args):
		Logger.write("Task received.\tloading...")
		func = self.pickler.loads(f)
		Logger.write("Task loaded.\tpatch...")
		func = self.patch(func)
		args = map(self.pickler.loads, args)
		try:
			Logger.write("Patched.\tRuning....")
			res =  func(*args)
			Logger.write("Task finished.")
			return res
		except Exception, e:
			return e

	def patch(self, f):
		if f is map:
			return self.map
		if isinstance(f, types.FunctionType):
			f.func_globals['map'] = self.map
		return f


