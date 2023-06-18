#
# picotouch_aftertouch.py -- Tiny capsense MIDI slider controller using Pico
# 28 Feb 2023 - @todbot / Tod Kurt - github.com/todbot/picotouch
#
# A touch-sensitive MIDI controller where pressing harder sends MIDI CC
#
# NOTE: This does not work very well.
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

import time
import board, pwmio
import touchio
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on  import NoteOn
from adafruit_midi.pitch_bend  import PitchBend
from adafruit_midi.control_change  import ControlChange
from adafruit_debouncer import Debouncer, Button

debug = False

octave = 4
midi_velocity = 100
midi_channel = 0  # 0-15
midi_cc_num = 1   # standard modwheel

touch_threshold_adjust = 10

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1])

touch_pins = (
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
    board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17,
    board.GP18, board.GP19, board.GP20, board.GP21,
    board.GP22,
)

led = pwmio.PWMOut(board.LED, frequency=25000, duty_cycle=0)

# special keys that aren't notes
pitch_up_key = 22
pitch_dn_key = 21

mod_up_key = 19
mod_mid_key = 18

oct_up_key = 20
oct_dn_key = 17

time.sleep(1)

td_scale_factor = 18

def td_scale(v):
    v = int( v*v ) >> td_scale_factor
    return v

touchs = []  # for debug
touchpads = []
for pin in touch_pins:
    touchin = touchio.TouchIn(pin)
    touchin.threshold += touch_threshold_adjust
    touchs.append(touchin)
    touchpads.append( Debouncer(touchin) )
num_touchs = len(touchs)

notes_on = [0] * num_touchs  # list of notes currently sounding

print("\n----------")
print("picotouch hello")

touchs_smooth = [0] * num_touchs
touchs_delta = [0] * num_touchs
touchs_start  = [0] * num_touchs
sm_amount = 0.95

cc_sending_id = -1
key_down_time = time.monotonic()

while True:
    for i in range(num_touchs):
        touch = touchpads[i]
        touch.update()

        touchs_smooth[i] = touchs_smooth[i] * sm_amount + (1-sm_amount) * touchs[i].raw_value
        touchs_delta[i] =  touchs[i].raw_value - touchs[i].threshold; # + 200

        #print("%+05x" % int(touchs_delta[i]), " ", end='')

        if touch.rose:
            led.duty_cycle = 65535
            if debug: print('key press   %2d' % i)
            noteOn = NoteOn((12*octave) + i, midi_velocity)
            notes_on[i] = noteOn
            midi.send( noteOn, channel=midi_channel )
            cc_sending_id = i
            key_down_time = time.monotonic()
            touchs_start[i] = touchs_smooth[i]

        if touch.fell:
            led.duty_cycle = 0
            if debug: print("key release %2d" % i)
            noteOn = notes_on[i]
            notes_on[i] = 0
            noteOn.velocity = 0  # noteOff == noteOn w/ zero velocity (as well as NoteOff)
            midi.send( noteOn, channel=midi_channel )
            cc_sending_id = -1

    #print()

    for i in range(num_touchs):
        td = int(touchs_smooth[i]) - touchs[i].threshold
        #td = int(touchs_smooth[i] - touchs_start[i])
        if td > 0 and notes_on[i] and i == cc_sending_id and time.monotonic() - key_down_time > 0.4:
            v = td_scale(td)
            v = min(max( v, 0 ), 127 )
            midi.send( ControlChange(midi_cc_num, v), channel=midi_channel)
            led.duty_cycle = v * 512
            print( "*" * (v//2), v,td)
