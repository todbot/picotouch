#
# picotouch_test.py -- Testing for tiny capsense controller using Pico,
# 2021 - @todbot / Tod Kurt - github.com/todbot/picotouch
#
# To use:
#
# 1. Install needed libraries:
#   circup install adafruit_midi adafruit_debouncer adafruit_ticks
# 2. Copy over this file as code.py:
#   cp picotouch_test.py /Volumes/CIRCUITPY/code.py
#
# on Pico / RP2040, need 1M pull-down on each input
#

import time
import board
import touchio

touch_threshold_adjust = 300

touch_pins = (
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17,
    board.GP18, board.GP19, board.GP20, board.GP21,
    board.GP22,
)

touchins = []  # for testing
touchs = []
for pin in touch_pins:
    touchin = touchio.TouchIn(pin)
    touchin.threshold += touch_threshold_adjust
    touchins.append(touchin)

print("\n----------")
print("picotouch_test hello")
while True:
    for i in range(len(touchs)):
        touch = touchs[i]
        print("%d  " % touch.value[i], end='')
    print()
