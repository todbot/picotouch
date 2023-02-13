#
# picotouch_macropad code.py -- Tiny capsense macropad controller using
#                               picotouch board & Raspberry Pi Pico
#
# 2023 - @todbot / Tod Kurt - github.com/todbot/picotouch
#
# To use:
#
# 1. Install needed libraries:
#   circup install adafruit_midi adafruit_debouncer adafruit_ticks
#
# 2. Copy over this file as code.py:
#   cp picotouch/code.py /Volumes/CIRCUITPY/code.py
#
# To change keys, edit 'keymap' as desired
#
# on Pico / RP2040, need 1M pull-down on each input  (picotouch board has this)
#

import time
import board
import touchio
import digitalio

from adafruit_debouncer import Debouncer, Button

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

debug = True

# put your keymap here
keymap = (
    # description  # list of keycodes or string to print out
    ("Capital A",  (Keycode.SHIFT, Keycode.A) ),   # key  0
    ("Hello world", "Hello world"),  # key  1
    (None, None),  # key  2
    (None, None),  # key  3
    (None, None),  # key  4
    (None, None),  # key  5
    (None, None),  # key  6
    (None, None),  # key  7
    (None, None),  # key  8
    (None, None),  # key  9
    (None, None),  # key 10
    (None, None),  # key 11
    (None, None),  # key 12
    (None, None),  # key 13
    (None, None),  # key 14
    (None, None),  # key 15
    (None, None),  # key 16
    (None, None),  # key 17
    (None, None),  # key 18
    (None, None),  # key 19
    (None, None),  # key 20
    (None, None),  # key 21
    (None, None),  # key 22
)

touch_threshold_adjust = 300

touch_pins = (
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17,
    board.GP18, board.GP19, board.GP20, board.GP21,
    board.GP22,
)

kbd = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(kbd)

led = digitalio.DigitalInOut(board.LED) # defaults to input
led.direction = digitalio.Direction.OUTPUT

# special keys that aren't notes
pitch_up_key = 22
pitch_dn_key = 21

mod_up_key = 19
mod_mid_key = 18

oct_up_key = 20
oct_dn_key = 17

touch_ins = []  # for debug
touch_pads = []
for pin in touch_pins:
    touchin = touchio.TouchIn(pin)
    touchin.threshold += touch_threshold_adjust
    touch_pads.append( Button(touchin, value_when_pressed=True))
    touch_ins.append(touchin)  # for debug
num_touch_pads = len(touch_pads)

print("\n----------")
print("picotouch_macropad hello")

while True:
    for i in range(num_touch_pads):
        touch = touch_pads[i]
        touch.update()
        key_desc, key_sequence = keymap[i]
        if touch.rose:
            led.value = True
            if debug: print('key press   %2d' % i, "touchdata:",touch_ins[i].raw_value, touch_ins[i].threshold)
            if key_desc and key_sequence:  # only if keymap entry exists for this key
                print("key_desc:",key_desc,"sequence:",key_sequence)
                if not isinstance(key_sequence,str):
                    kbd.press(*key_sequence)
                else:
                    keyboard_layout.write(key_sequence)

        if touch.fell:
            led.value = False
            if debug: print("key release %2d" % i, "touchdata:",touch_ins[i].raw_value, touch_ins[i].threshold)
            if key_desc and key_sequence:  # only if keymap entry exists for this key
                if not isinstance(key_sequence,str):
                    kbd.release(*key_sequence)
