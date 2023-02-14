#
# picotouch_midislider.py -- Tiny capsense MIDI slider controller using Pico
# 2023 - @todbot / Tod Kurt - github.com/todbot/picotouch
#
# Turns the three key regions into the MIDI CC sliders!
#
#    picotouch board
#   ┌──────────────────────────────────────────────────────────────────────────────────────────┐
#   │     .─.   .─.          .─.   .─.   .─.          .─.   .─.                                │
#   │    ( 1 ) ( 3 )        ( 6 ) ( 8 ) ( 10)        ( 13) ( 15)                               │
#   │     `─'   `─'          `─'   `─'   `─'          `─'   `─'                                │
#   │  .─.   .─.   .─.    .─.   .─.   .─.   .─.    .─.   .─.   .─.                             │
#   │ ( 0 ) ( 2 ) ( 4 )  ( 5 ) ( 7 ) ( 9 ) ( 11)  ( 12) ( 14) ( 16)                            │
#   │  `─'   `─'   `─'    `─'   `─'   `─'   `─'    `─'   `─'   `─'                             │
#   └──────────────────────────────────────────────────────────────────────────────────────────┘
#     [---------------]  [---------------------]  [---------------]
#         slider0              slider1               slider2
#           CC 1                 CC 71                 CC 72
#
# To use:
#
# 1. Install needed libraries:
#   circup install adafruit_midi adafruit_debouncer adafruit_ticks
#
# 2. Copy over this file as code.py:
#   cp code.py /Volumes/CIRCUITPY/code.py
#
# on Pico / RP2040, need 1M pull-down on each input
#

import time
import board
import digitalio
import digitalio
import touchio
import usb_midi
from adafruit_ticks import ticks_ms
import adafruit_midi
from adafruit_midi.control_change  import ControlChange
from adafruit_debouncer import Debouncer

# Whch MIDI CCs for which slider?  Edit to taste
sliders_CCs = (  1, 71, 72, )

# Map of pad ids to slider number & position
sliders_ids = (
    (0, 1, 2, 3, 4),         # slider 0
    (5, 6, 7, 8, 9 ,10, 11), # slider 1
    (12, 13, 14, 15, 16),    # slider 2
)

debug = False

touch_threshold_adjust = 300

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1])

touch_pins = (
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17,
    board.GP18, board.GP19, board.GP20, board.GP21,
    board.GP22,
)

num_sliders = len(sliders_ids) # how many sliders we got
sliders_pos = [ 0 ] * num_sliders  # one entry per slider  # range from 0-1 float
sliders_pos_last = [ 0 ] * num_sliders  # one entry per slider
fade_amount = 0.75  # how much to filter changes
fade_last_millis = ticks_ms()
fade_step = 20  # millisecs between fade steps

led = digitalio.DigitalInOut(board.LED) # defaults to input
led.direction = digitalio.Direction.OUTPUT

touch_ins = []
touchs = []
for pin in touch_pins:
    touchin = touchio.TouchIn(pin)
    touchin.threshold += touch_threshold_adjust
    touch_ins.append(touchin)
    touchs.append( Debouncer(touchin) )

print("\n----------")
print("picotouch_slider hello")
last_msg_millis = ticks_ms()

while True:
    now = ticks_ms()
    # Smoothly fade the sliders to reduce steppiness
    if now - fade_last_millis > fade_step:
        fade_last_millis = now
        for j in range(num_sliders):
            # use averaging filter to slide the slider
            sliders_pos_last[j] = fade_amount * sliders_pos_last[j] + (1-fade_amount)*sliders_pos[j]
            # only send MIDI CC if slider is moving
            if abs(sliders_pos_last[j] - sliders_pos[j]) > 0.01:
                midi.send(ControlChange(sliders_CCs[j], int(sliders_pos_last[j]*127)))
            if debug: print("\t %1.2f / %1.2f" % (sliders_pos_last[j], sliders_pos[j]), end='')
        if debug: print()

    if now - last_msg_millis > 100:  # every 100 msec
        last_msg_millis = now
        print(now,"sliders:",end='')
        for j in range(num_sliders):
            print("  %1.2f  " % sliders_pos_last[j], end='')
        print()


    # Read pads
    for i in range(len(touchs)):
        touch = touchs[i]
        touch.update()
        if touch.rose:
            led.value = True
            for j in range(num_sliders):
                slider_ids = sliders_ids[j]
                if i in slider_ids:
                    # convert pad index to slider position 0..1, sorta
                    slider_pos = (slider_ids.index(i)) / len(slider_ids)
                    sliders_pos[j] = slider_pos
                    print("\t\t\t\tslider #",j, ":", slider_pos)
        if touch.fell:
            led.value = False
