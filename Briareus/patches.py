import types
import netable
import epickle

pickler = epickle.Pickler()
Briareus_proxy_addr = "tcp://192.168.70.101:8858"

def map(f, l):
	return [netable.call(Briareus_proxy_addr, "eval", [pickler.dumps(f), pickler.dumps(x)]) for x in l]

if __name__ == '__main__':
	print map(str, range(10))