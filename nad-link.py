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

def send(bit):
  pin(False)
  time.sleep(0.00056)
  pin(True)
  time.sleep(0.00169 if bit else 0.00056)

if not carryOn:
  exit(0)

# Send preamble
pin(False)
time.sleep(0.009)
pin(True)
time.sleep(0.0045)

# Send the remote code
for c in "{0:b}".format(cmd):
  if c=='1':
    send(True)
  elif c=='0':
    send(False)

# Terminate the command
pin(False)
time.sleep(0.00056)
pin(True)
time.sleep(0.04202)

# Send repeats until ^C in case of hold commands
if hold:
  while carryOn:
    pin(False)
    time.sleep(0.009)
    pin(True)
    time.sleep(0.00225)
    pin(False)
    time.sleep(0.00056)
    pin(True)
    time.sleep(0.09819)
