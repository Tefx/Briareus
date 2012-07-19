import psutil
from subprocess import PIPE
from multiprocessing import cpu_count
from time import sleep
import types

class Monitor(object):
    def __init__(self):
        self.processes = []


    def start(self, *cmd):
        for _ in range(cpu_count()-len(self.processes)):
            p = psutil.Popen(cmd, shell=False, stdout=PIPE)
            self.processes.append(p)

    def auto_affinity(self):
        for i in range(len(self.processes)):
            self.processes[i].set_cpu_affinity([i % cpu_count()])

    def list(self):
        if not self.processes:
            print "No process."
        for p in self.processes:
            i = self.processes.index(p)
            if self.isalive(i):
                print "[%d] %s %s" % (i, p.cmdline, str(p.status))
            else:
                print "[%d] dead" % i


    def isalive(self, num):
        num = int(num)
        return self.processes[num].is_running()

    def terminate(self, num):
        num = int(num)
        p = self.processes[num]
        p.terminate()
        try:
            p.wait(5)
        except TimeoutExpired:
            p.kill()
            sleep(2)
        if self.isalive(num):
            print "Fail to terminate [%d]" % num
        else:
            del self.processes[num]
            return True

    def killall(self):
        for p in self.processes:
            self.terminate(self.processes.index(p))

    def call(self, num, attr, *args):
        num = int(num)
        p = self.processes[num]
        try:
            f = getattr(p, attr)
            if isinstance(f, types.MethodType):
                return f(*args)
            else:
                return f
        except AttributeError:
            print "No such method."

class Shell(object):
    def __init__(self, new_monitor=True):
        if new_monitor:
            self.mon = Monitor()

    def run(self):
        while True:
            cmds = raw_input(">>").split()
            if cmds[0] == "quit": 
                self.mon.killall()
                break
            try:
                f = getattr(self.mon, cmds[0])
                ret = f(*cmds[1:])
                if ret is not None:
                    print ret
            except AttributeError:
                print "No such method."


if __name__ == '__main__':
    Shell().run()

