import gevent
import signal
from sys import argv, exit
from subprocess import Popen
from multiprocessing import cpu_count


running = True

def stop():
    global running
    running = False

def launch_worker(address):
    return Popen(["python2", "worker.py", address], shell=False, stdout=False)

def run_and_monitor(no):
    global running
    print "Launching Worker[%d]..." % no
    p = launch_worker(argv[1])
    while running:
        gevent.sleep(5)
        if p.poll():
            print "Launch Worker[%d] terminated, relaunching..." % no
            p = launch_worker(argv[1])
    p.terminate()

def main():
    gevent.signal(signal.SIGTERM, stop)
    gevent.signal(signal.SIGQUIT, stop)
    gevent.signal(signal.SIGINT, stop)
    workers = [gevent.spawn(run_and_monitor, no) for no in range(cpu_count())]
    gevent.joinall(workers)

if __name__ == '__main__':
    if len(argv) != 2:
        exit('Usage: %s address' % __file__)
    main()


