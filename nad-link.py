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

import ctypes
libc = ctypes.CDLL('libc.so.6')
def usleep(us):
  libc.usleep(int(us))

def pin(state):
  g.output(OutPin, state)

def send(bit):
  pin(False)
  usleep(560)
  pin(True)
  usleep(1690 if bit else 560)

if not carryOn:
  exit(0)

# Send preamble
pin(False)
usleep(9000)
pin(True)
usleep(4500)

# Send the remote code
for c in "{0:b}".format(cmd):
  if c=='1':
    send(True)
  elif c=='0':
    send(False)

# Terminate the command
pin(False)
usleep(560)
pin(True)
usleep(42020)

# Send repeats until ^C in case of hold commands
if hold:
  while carryOn:
    pin(False)
    usleep(9000)
    pin(True)
    usleep(2250)
    pin(False)
    usleep(560)
    pin(True)
    usleep(98190)
