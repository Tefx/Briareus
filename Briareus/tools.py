from gevent import monkey; monkey.patch_all()

import sys  
sys.path.append('..')

import Corellia
import epickle 

class Client(Corellia.Client):
	def __init__(self, *args):
		super(Client, self).__init__(*args)
		self.picker = epickle.Pickler()

	def __getattr__(self, func):
		f = super(Client, self).__getattr__(func)
		def fun(*args):
			l = map(self.picker.dumps, args)
			return f(*l)
		return fun


pickler = epickle.Pickler()

def call(addr, func, args):
	return Corellia.call(addr, func, map(pickler.dumps, args))

