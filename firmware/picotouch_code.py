#
# picotouch.py -- Tiny capsense MIDI controller using Pico
# 2021 - @todbot / Tod Kurt - github.com/todbot/picotouch
#
# on Pico / RP2040, need 1M pull-down on each input
#

import time
import board
import touchio

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on  import NoteOn
from adafruit_debouncer import Debouncer


midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

touch_pins = (
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17,
    board.GP18, board.GP19, board.GP20, board.GP21,
    #board.GP22,
)

midi_base_note = 48   # C3
midi_velocity = 64    # midpoint

touch_keys = [] # don't need this
touchs = []
for pin in touch_pins:
    #print(pin,",",end='')
    touchin = touchio.TouchIn(pin)
    touch_keys.append(touchin)
    touchs.append( Debouncer(touchin) )

print("\n----------")
print("picotouch hello")

while True:
    for i in range(len(touchs)):
        touch = touchs[i]
        touch.update()
        if touch.rose:
            print("touch press ",i)
            midi.send( NoteOn(midi_base_note + i, midi_velocity) )
        if touch.fell:
            print("touch release ",i)
            midi.send( NoteOff(midi_base_note + i, midi_velocity) )

