import zmq


LRU_READY = "\x01"
context = zmq.Context()


class Broker(object):
	def __init__(self, front_addr, back_addr):
		self.frontend = context.socket(zmq.ROUTER)
		self.frontend.bind(front_addr)
		self.backend = context.socket(zmq.ROUTER)
		self.backend.bind(back_addr)
		self.workers = []
		self.poll_workers = zmq.Poller()
		self.poll_workers.register(self.backend, zmq.POLLIN)
		self.poll_both = zmq.Poller()
		self.poll_both.register(self.frontend, zmq.POLLIN)
		self.poll_both.register(self.backend, zmq.POLLIN)

	def run(self):
		while True:
			if self.workers:
				socks = dict(self.poll_both.poll())
			else:
				socks = dict(self.poll_workers.poll())

			if socks.get(self.backend) == zmq.POLLIN:
				msg = self.backend.recv_multipart()
				if not msg:
					break
				worker_id = msg[0]
				print "Worker[%s] added."  % repr(worker_id)
				self.workers.append(worker_id)
				if msg[2] != LRU_READY:
					self.frontend.send_multipart(msg[2:])


			if socks.get(self.frontend) == zmq.POLLIN:
				msg = self.frontend.recv_multipart()
				request = [self.workers.pop(0), ''] + msg
				self.backend.send_multipart(request)


if __name__ == '__main__':
	Broker("ipc://clientend", "ipc://serverend").run()