import sys  
sys.path.append('../../Corellia')
sys.path.append('..')
from Briareus import cloud

import random
total_tests = 5000000

def throw(a):
    x = random.random()
    y = random.random()
    return x*x + y*y < 1.0

@cloud
def monteCarlo(num_test):
  return map(throw, xrange(num_test)).count(True)

def calcPi():
  num_in_circle = monteCarlo(total_tests)
  return (4 * num_in_circle) / float(total_tests)

if __name__ == '__main__':
  print calcPi()
