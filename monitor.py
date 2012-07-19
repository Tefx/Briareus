import psutil
from subprocess import PIPE
from multiprocessing import cpu_count
import gevent

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
        for p in self.processes:
            yield self.processes.index(p),
                  p.pid,
                  p.is_running(),
                  str(p.status),
                  p.get_cpu_times(),
                  p.get_cpu_percen(),
                  p.get_cpu_affinity(),
                  p.get_memory_percent(),
                  p.get_connections()

    def keep_alive(self):
        for p in self.processes:
            if not p.is_running():
                del self.processes.index(p)
        


    def isalive(self, num):
        return self.processes[num].is_running()

    def terminate(self, num):
        p = self.processes[num]
        p.terminate()
        try:
            p.wait(5)
        except TimeoutExpired:
            p.kill()
            sleep(2)
        if self.isalive(num):
            return False
        else:
            del self.processes[num]
            return True

    def killall(self):
        for p in self.processes:
            self.terminate(self.processes.index(p))
