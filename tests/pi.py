import sys  
sys.path.append('../../Corellia')
sys.path.append('../../Husky')
sys.path.append('..')
from Briareus import cloud

import random
num_pre_tests = 50000
num_test = 100

def monteCarlo(num_test):
    num_in_circle = 0
    for _ in xrange(num_test):
        x = random.random()
        y = random.random()
        if x*x + y*y < 1.0:
            num_in_circle += 1
    return num_in_circle

#@cloud
def calcPi():
    num_in_circle = sum(map(monteCarlo,[num_pre_tests]*num_test))
    pi = (4 * num_in_circle) / float(num_pre_tests*num_test)
    return pi

if __name__ == '__main__':
    pi = calcPi()
    print 'Pi determined to be %s' % pi
