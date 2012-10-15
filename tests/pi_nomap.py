from Briareus import cloud

import random
total_tests = 10000000

def monteCarlo(num_test):
  num_in_circle = 0
  for _ in xrange(num_test):
    x = random.random()
    y = random.random()
    if x*x + y*y < 1.0:
      num_in_circle += 1
  return num_in_circle

def calcPi():
  num_in_circle = monteCarlo(total_tests)
  return (4 * num_in_circle) / float(total_tests)

if __name__ == '__main__':
  print calcPi()