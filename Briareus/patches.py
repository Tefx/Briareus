import types
import netable
import epickle
import sys
from gevent.pool import Pool

pool = Pool(1000)
pickler = epickle.Pickler()

# def gen_map(proxy_addr):
# 	def map(f, l):
# 		return [netable.call(proxy_addr, "eval", (pickler.dumps(f), pickler.dumps(x))) for x in l]
# 	return map

def gen_map(proxy_addr):
	def map(f, l):
		return pool.map(
			lambda x:netable.call(proxy_addr, "eval", (pickler.dumps(f), pickler.dumps(x))),
			l)
	return map