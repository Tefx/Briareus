import types
import netable
import epickle
import sys

pickler = epickle.Pickler()

def gen_map(proxy_addr):
	def map(f, l):
		return [netable.call(proxy_addr, "eval", (pickler.dumps(f), pickler.dumps(x))) for x in l]
	return map