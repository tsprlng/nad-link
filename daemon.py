#!/usr/bin/python

# Daemon to listen to keyboard-style events from my Bluetooth remote and trigger things (including NAD-link).

import struct
import sys
from subprocess import Popen as popen
import os.path
import itertools

import fcntl
def eviocgrab(file_descriptor):  # linux call for super annoying exclusive access to input device
    EVIOCGRAB = 1074021776
    return fcntl.ioctl(file_descriptor, EVIOCGRAB, 1)

CommandScript = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nad-link.py')
def cmd(cmd):
    return popen(['python', CommandScript, cmd])

EventFilePath = "/dev/input/event1"  # n.b. this is probably not always the right one

EventStructFormat = 'llHHI'  # long, long, unsigned short, unsigned short, unsigned int
EventStructSize = struct.calcsize(EventStructFormat)

HyperionSeqs = {
    400: ['--color 222211', '--color 886633', '--color ffcc77', '--color 88ffcc'],
    401: ['--color 000000', '--clearall']
}
hyperionLastKey = None
hyperionSeq = None
def hyperion(keycode):
    global hyperionLastKey, hyperionSeq  # why must statics be so annoying?
    if keycode != hyperionLastKey:
        hyperionSeq = itertools.cycle(HyperionSeqs[keycode])
        hyperionLastKey = keycode
    popen(itertools.chain(['hyperion-remote'], hyperionSeq.next().split(' '))).wait()

thing = None  # holds the current invocation of the nad-link script (while there is one) for holdy commands like volume

def handle(type, code, value):
    global thing

    if (code < 113 or code > 115) and (code < 398 or code > 401):  # disregard bizarre noise events
        return

    if thing:
        # Pressing something else while already holding a volume key at once is unacceptable silliness.
        # Therefore, this will quit the control script when that happens!
        # As a happy accident it also covers the normal deliberate 'key up' (value = 0) events.
        thing.send_signal(2)  # SIGINT
        thing.wait()
        thing = None
    elif value != 1:
        return
    elif code == 114:  # volume down
        thing = cmd('-')
    elif code == 115:  # volume up
        thing = cmd('+')
    elif code == 113:  # mute
        cmd('monitor').wait()
    elif code == 398:  # red button
        cmd('off').wait()
    elif code == 399:  # green button
        cmd('pi').wait()  # switch source if on
        cmd('on').wait()  # or switch on if not
    elif code >= 400 and code <= 401:  # yellow and blue!
        hyperion(code)


if len(sys.argv) >= 2 and sys.argv[1] == 'print':  # i miss 'rescue nil'
    def handle(*things): print(', '.join(str(thing) for thing in things))

# open the keyboard event file in binary mode (whatever the hell that is)
with open(EventFilePath, "rb") as in_file:
    eviocgrab(in_file)
      # exclusively grab the keyboard... so that XBMC can't exclusively grab the keyboard
      # (thanks for that, XBMC.)
      # remember to make sure this daemon starts before XBMC does!

    while True:
        event = in_file.read(EventStructSize)
        if not event:
            break

        (tv_sec, tv_usec, type, code, value) = struct.unpack(EventStructFormat, event)
        handle(type, code, value)
