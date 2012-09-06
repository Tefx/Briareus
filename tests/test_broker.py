import sys  
sys.path.append('..')
from Corellia import Broker

if __name__ == '__main__':
	Broker(8858, 8859).run()