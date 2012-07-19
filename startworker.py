import gevent
import signal
from sys import argv, exit
import psutil
from subprocess import PIPE
from multiprocessing import cpu_count
from os import system


if len(argv) != 2:
    exit('Usage: %s address' % __file__)
address = argv[1]

is_running = True
processes = []
cmds = ["python2", "worker.py", address]

for i in range(cpu_count()):
    p = psutil.Popen(cmds, shell=False, stdout=PIPE)
    p.set_cpu_affinity([i])
    processes.append(p)

def keep_alive():
    global is_running
    while is_running:
        for i in range(len(processes)):
            if not processes[i].is_running():
                processes[i] = psutil.Popen(cmds, shell=False, stdout=PIPE)
        gevent.sleep(1)

def print_info():
    global is_running
    while is_running:
        s = ["NUM\tCPU\tMEM\tAFFINITY\tSTATUS\t\tUSERTIME\tSYSTEMTIME"]
        for p in processes:
            s.append("[%d]\t%.2f\t%.2f\t%s\t\t%8s\t%s\t\t%s" % \
                     (processes.index(p),
                      p.get_cpu_percent(),
                      p.get_memory_percent(),
                      ",".join(map(str, p.get_cpu_affinity())),
                      p.status,
                      p.get_cpu_times().user,
                      p.get_cpu_times().system,))
        system("clear")
        print "\n".join(s)
        gevent.sleep(1)

def killall():
    for p in processes:
        p.terminate()
        try:
            p.wait(5)
        except TimeoutExpired:
            p.kill()
            sleep(2)
        if self.isalive(num):
            print "Fail to terminate process: [%d]" % p.pid

def stop():
    global is_running
    is_running = False

gevent.signal(signal.SIGTERM, stop)
gevent.signal(signal.SIGQUIT, stop)
gevent.signal(signal.SIGINT, stop)
ka = gevent.spawn(keep_alive)
pi = gevent.spawn(print_info)
pi.join()
ka.join()
killall()
