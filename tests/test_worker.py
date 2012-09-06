import sys  
sys.path.append('..')

from Corellia import Worker as CWorker
from Briareus import Worker as BWorker

WORKER_ADDR = ("localhost", 8859)
CLIENT_ADDR = ("localhost", 8858)

if __name__ == '__main__':
	CWorker(BWorker, CLIENT_ADDR).run(WORKER_ADDR)