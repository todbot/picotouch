#
# picotouch code.py -- Tiny capsense MIDI controller using Raspberry Pi Pico
# 2021-2023 - @todbot / Tod Kurt - github.com/todbot/picotouch
#
# To use:
#
# 1. Install needed libraries:
#   circup install adafruit_midi adafruit_debouncer adafruit_ticks
#
# 2. Copy over this file as code.py:
#   cp picotouch/code.py /Volumes/CIRCUITPY/code.py
#
# on Pico / RP2040, need 1M pull-down on each input  (picotouch board has this)
#

import time
import board
import touchio
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on  import NoteOn
from adafruit_midi.pitch_bend  import PitchBend
from adafruit_midi.control_change  import ControlChange
from adafruit_debouncer import Debouncer, Button

debug = True

octave = 4

midi_velocity = 64  # midpoint
midi_channel = 0  # 0-15
midi_cc_num = 1   # standard modwheel

touch_threshold_adjust = 300

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
print("picotouch hello")

while True:
    for i in range(num_touch_pads):
        touch = touch_pads[i]
        touch.update()
        if touch.rose:
            led.value = True
            if debug: print('key press   %2d' % i, "touch:",touch_ins[i].raw_value, touch_ins[i].threshold)
            if i == pitch_up_key:
                print('pitch up!')
                pitchbend_val = 8192 + 4096
                midi.send( PitchBend(pitchbend_val), channel=midi_channel)
            elif i == pitch_dn_key:
                print('pitch middle!')
                pitchbend_val = 8192 - 4096
                midi.send( PitchBend(pitchbend_val), channel=midi_channel)
            elif i == mod_up_key:
                print('mod up!')
                modwheel_val = 127
                midi.send( ControlChange(midi_cc_num, modwheel_val), channel=midi_channel)
            elif i == mod_mid_key:
                print('mod middle!')
                modwheel_val = 64
                midi.send( ControlChange(midi_cc_num, modwheel_val), channel=midi_channel)
            elif i == oct_up_key:
                if octave < 9: octave = octave + 1
                print('oct up!', octave)
            elif i == oct_dn_key:
                if octave > 0: octave = octave - 1
                print('oct down!', octave)
            else:
                midi.send( PitchBend(8192) , channel=midi_channel)
                midi.send( NoteOn((12*octave) + i, midi_velocity), channel=midi_channel )

        if touch.fell:
            led.value = False
            if debug: print("key release %2d" % i, "touch:",touch_ins[i].raw_value, touch_ins[i].threshold)
            if i == pitch_up_key:
                pitchbend_val = 8192  # reset to midpoint
                midi.send( PitchBend(pitchbend_val), channel=midi_channel)
            elif i == pitch_dn_key:
                pitchbend_val = 8192  # reset to midpoint
                midi.send( PitchBend(pitchbend_val), channel=midi_channel)
            elif i == mod_up_key:
                modwheel_val = 0  # reset to normal
                midi.send( ControlChange(midi_cc_num, modwheel_val), channel=midi_channel)
            elif i == mod_mid_key:
                modwheel_val = 0
                midi.send( ControlChange(midi_cc_num, modwheel_val), channel=midi_channel)
            elif i == oct_up_key:
                pass
            elif i == oct_dn_key:
                pass
            else:
                midi.send( NoteOff((12*octave) + i, midi_velocity), channel=midi_channel )
