from tools import Client
from worker import Worker

__all__ = ['cloud', 'call', 'Worker']

client = Client(("210.72.68.189", 8858))

def cloud(f):
	return lambda *args: client.eval(f, *args)

def call(f, *args):
	return client.eval(f, *args)
