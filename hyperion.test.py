import hyperion
import time
import colorsys
import math
import itertools
from random import random

# create a Array for the colors
colors = bytearray(hyperion.ledCount * (0,0,0))

Speakers = [5,2]
Backwash = [7,0]
Down = [9,8,4]
ScreenTop = [6,3,1]

for set in itertools.cycle([Speakers, Backwash, Down, ScreenTop]):
    if hyperion.abort():
        break

    for sel in itertools.chain(*itertools.repeat(set, 4)):
        for i in xrange(hyperion.ledCount):
            if sel == i:
                colors[i*3] = 255
            else:
                colors[i*3] = 0

        hyperion.setColor(colors)
        time.sleep(0.2)

    for sel in set:
        colors[sel*3] = 255
        hyperion.setColor(colors)

    time.sleep(1)
