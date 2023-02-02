#
# picotouch_code.py -- Tiny capsense MIDI controller using Pico
# 2021 - @todbot / Tod Kurt - github.com/todbot/picotouch
#
# To use:
#
# 1. Install needed libraries:
#   circup install adafruit_midi adafruit_debouncer
# 2. Copy over this file as code.py:
#   cp picotouch_code.py /Volumes/CIRCUITPY/code.py#
#
# on Pico / RP2040, need 1M pull-down on each input
#

import time
import board
from digitalio import DigitalInOut, Pull, Direction
import touchio
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on  import NoteOn
from adafruit_midi.pitch_bend  import PitchBend
from adafruit_midi.control_change  import ControlChange
from adafruit_debouncer import Debouncer

midi_base_note = 48   # 48 = C3
midi_velocity = 64    # midpoint
midi_channel = 0
midi_cc_num = 1  # standard modwheel

touch_threshold_adjust = 500

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1])

touch_pins = (
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17,
    board.GP18, board.GP19, board.GP20, board.GP21,
    board.GP22,
)

led = DigitalInOut(board.LED) # defaults to input
led.direction = Direction.OUTPUT

pitch_up_index = 22
pitch_down_index = 21
mod_up_index = 19
mod_down_index = 18
oct_up_index = 20
oct_down_index = 17

touch_ins = []
touchs = []
for pin in touch_pins:
    touchin = touchio.TouchIn(pin)
    touchin.threshold += touch_threshold_adjust
    touch_ins.append(touchin)
    touchs.append( Debouncer(touchin) )

print("\n----------")
print("picotouch hello")
while True:
    for i in range(len(touchs)):
        touch = touchs[i]
        touch.update()
        if touch.rose:
            led.value = True
            if i == oct_up_index:
                print('oct up!')
                midi_base_note = min( midi_base_note + 12, 108)
            elif i == oct_down_index:
                print('oct down!')
                midi_base_note = max( midi_base_note - 12, 0)
            elif i == pitch_up_index:
                print('pitch up!')
                pitchbend_val = 8192 + 4096
                midi.send( PitchBend(pitchbend_val), channel=midi_channel)
            elif i == pitch_down_index:
                print('pitch down!')
                pitchbend_val = 8192 - 4096
                midi.send( PitchBend(pitchbend_val), channel=midi_channel)
            elif i == mod_up_index:
                print('mod up!')
                modwheel_val = 127
                midi.send( ControlChange(midi_cc_num, modwheel_val), channel=midi_channel)
            elif i == mod_down_index:
                print('mod down!')
                modwheel_val = 0
                midi.send( ControlChange(midi_cc_num, modwheel_val), channel=midi_channel)
            else:
                midi.send( PitchBend(8192) , channel=midi_channel)
                midi.send( NoteOn(midi_base_note + i, midi_velocity), channel=midi_channel )
        if touch.fell:
            led.value = False
            print("release",i)
            if i == oct_up_index:
                pass
            elif i == oct_down_index:
                pass
            elif i == pitch_up_index:
                pitchbend_val = 8192
                midi.send( PitchBend(pitchbend_val), channel=midi_channel)
            elif i == pitch_down_index:
                pitchbend_val = 8192
                midi.send( PitchBend(pitchbend_val), channel=midi_channel)
            elif i == mod_up_index:
                modwheel_val = 0
                midi.send( ControlChange(midi_cc_num, modwheel_val), channel=midi_channel)
            elif i == mod_down_index:
                modwheel_val = 0
                midi.send( ControlChange(midi_cc_num, modwheel_val), channel=midi_channel)

            else:
                midi.send( NoteOff(midi_base_note + i, midi_velocity), channel=midi_channel )
