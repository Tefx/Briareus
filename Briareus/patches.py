from gevent.pool import Pool
import tools

pool = Pool(1000)

def gen_map(proxy_addr, pickler):
	def map(f, l):
		return pool.map(
			lambda x:tools.call(proxy_addr, "eval", (f, x)),
			l)
	return map