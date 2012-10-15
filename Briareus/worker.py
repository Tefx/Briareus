import Husky
import patches
import sys
import types


class Worker(object):
	def __init__(self, proxy_addr):
		self.map = patches.gen_map(proxy_addr)

	def eval(self, f, *args):
		func = Husky.loads(f)
		func = self.patch(func)
		args = map(Husky.loads, args)
		print func, args
		try:
			res = func(*args)
			return res
		except Exception, e:
			print e
			return str(e)

	def patch(self, f):
		if f is map:
			return self.map
		if isinstance(f, types.FunctionType):
			f.func_globals['map'] = self.map
		return f


