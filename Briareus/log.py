import os
import psutil
import time


LOG_PATH = "../log/"

class Logger(object):
	def __init__(self):
		self.proc = psutil.Process(os.getpid())
		self.id = "%s_%d" % (self.proc.name, self.proc.pid)
		self.open_log()

	def open_log(self):
		if not os.path.exists(LOG_PATH):
			os.makedirs(LOG_PATH)
		self.log_file = open(os.path.join(LOG_PATH, self.id+".log"), "w")

	def write(self, data):
		t = time.strftime("%Y-%m-%d %X", time.localtime(time.time()))
		print >> self.log_file, "%s[%s]:\t %s\n" % (t, self.id, data)


if __name__ == '__main__':
	l = Logger()
	l.write("test")
