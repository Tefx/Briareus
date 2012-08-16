import os
import psutil
import time


LOG_PATH = "../log/"

class Logger(object):
	def __init__(self, module_name):
		self.proc = psutil.Process(os.getpid())
		self.id = "%s_%d" % (module_name, self.proc.pid)
		self.filename = os.path.join(LOG_PATH, self.id+".log")
		self.opened = False

	def open_log(self):
		if not os.path.exists(LOG_PATH):
			os.makedirs(LOG_PATH)
		self.log_file = open(self.filename, "w")
		self.opened = True

	def write(self, data):
		if not self.opened:
			self.open_log()
		t = time.strftime("%Y-%m-%d %X", time.localtime(time.time()))
		self.log_file.writelines("%s[%s]:\t %s\n" % (t, self.id, data))
		self.log_file.flush()


if __name__ == '__main__':
	l = Logger("name")
	l.write("test")
