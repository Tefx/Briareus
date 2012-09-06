import epickle
import patches
import sys
import types


class Worker(object):
	def __init__(self, proxy_addr):
		self.pickler = epickle.Pickler()
		self.map = patches.gen_map(proxy_addr, self.pickler)

	def eval(self, f, *args):
		print >> sys.stdout, "start.."
		func = self.pickler.loads(f)
		func = self.patch(func)
		args = map(self.pickler.loads, args)
		print func, args
		try:
			res = func(*args)
			print >> sys.stdout, "end..."
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

if __name__ == '__main__':
	def add(a, b):
		return a+b

	p = epickle.Pickler()

	l = map(p.dumps, (add, 1, 2))
	print Worker().eval(l[0], *l[1:])


