import signal

# Catch ^C (SIGINT) and handle politely
carryOn = True
def sigint_handler(signal, frame):
  global carryOn
  carryOn = False
signal.signal(signal.SIGINT, sigint_handler)

import RPi.GPIO as g
import time
import sys
import os
import atexit
from yaml import load as yaml

from monotonic import monotonic

OutPin = 7

def cleanup():
  g.cleanup(OutPin)
atexit.register(cleanup)

g.setmode(g.BOARD)
g.setup(OutPin, g.OUT, initial=True)

cfg = yaml(file(os.path.join(os.path.dirname(__file__), 'config.yml'),'r'))
mode, cmd = cfg[sys.argv[1]]
hold = mode.lower() == 'hold'

def pin(state):
  g.output(OutPin, state)

def oneBitDelays(bit):
  yield 560
  yield (1690 if bit else 560)

def commandDelays(cmd):
  if not carryOn:
    exit(0)

  # Send preamble
  yield 9000
  yield 4500

  # Send the remote code one bit at a time
  for c in "{0:b}".format(cmd):
    for d in oneBitDelays(c=='1'):
      yield d

  # Terminate the command
  yield 560
  yield 42020

  # Send repeats until ^C in case of hold commands
  if hold:
    while carryOn:
      yield 9000
      yield 2250
      yield 560
      yield 98190

def flippingInstants(cmd, firstInstant):
  last = 0
  for d in commandDelays(cmd):
    if last > 0:
      yield firstInstant + (last * 0.000001)
    last += d


currentState = True

now = monotonic()
currentState = not currentState
pin(currentState)

for i in flippingInstants(cmd, now):
  while monotonic() < i:
    pass
  currentState = not currentState
  pin(currentState)

assert(currentState == True)  # we had an even number of delays and ended up where we started
