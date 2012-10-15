from gevent import monkey; monkey.patch_all()

import sys  
sys.path.append('..')

import Corellia
import Husky 

class Client(Corellia.Client):
	def __getattr__(self, func):
		f = super(Client, self).__getattr__(func)
		def fun(*args):
			l = map(Husky.dumps, args)
			return f(*l)
		return fun


def call(addr, func, args):
	return Corellia.call(addr, func, map(Husky.dumps, args))

