# picotouch_grid -- Grid-based MIDI controller
# 16 Feb 2023 - @todbot / Tod Kurt
#
# Part of https://github.com/todbot/picotouch
#

# keys
import time
import board
import neopixel
import rainbowio

# midi
import usb_midi
import busio

# display
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import bitmap_label as label

from touchmatrix import TouchMatrix

playdebug = True
do_usb_midi = True
do_serial_midi = True

touch_col_pins = (
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9
)
touch_row_pins = ( board.GP10, board.GP11, board.GP12, board.GP13, )
neopixel_pin = board.GP28
oled_sda_pin = board.GP14
oled_scl_pin = board.GP15
midi_tx_pin  = board.GP20

dw,dh = 128,32

midi_usb_out = usb_midi.ports[1]
midi_uart = busio.UART(tx=midi_tx_pin, baudrate=31250) # timeout=midi_timeout)


print("\n----------")
time.sleep(2)  # get capsense time to stabilize
print("picotouch_grid hello")

touch_matrix = TouchMatrix( col_pins=touch_col_pins, row_pins=touch_row_pins,
                            col_threshold_adjust = -20,
                           # row_threshold_adjust = -100
                           )

leds = neopixel.NeoPixel(neopixel_pin, 40, brightness=0.1, auto_write=False)
leds.fill(0x666666)

displayio.release_displays()
oled_i2c = busio.I2C( scl=oled_scl_pin, sda=oled_sda_pin, frequency=400_000 )
display_bus = displayio.I2CDisplay(oled_i2c, device_address=0x3C)  # or 0x3D depending on disp
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=dw, height=dh, rotation=180)
maingroup = displayio.Group()
display.show(maingroup)

maingroup.append( label.Label(terminalio.FONT, text="picotouch_grid", x=0, y=10, scale=1))
note_label = label.Label(terminalio.FONT, text="note:", x=80, y=23)
noteval_label = label.Label(terminalio.FONT, text="xx", x=110, y=23)
maingroup.append(note_label)
maingroup.append(noteval_label)

dim_by = 5
octave = 3
mode = 0


def keynum_to_note(keynum):
    r,c = keynum // 10, keynum % 10  # fixme hardcoded vals
    r = 3 - r  # go from bottom to top
    note = r * 10 + c
    return note + (octave*12)
    #return (40 - keynum) + (octave*12)  # this is wrong

def play_note_on(note, vel):  #
    """Callback for sequencer when note should be tured on"""
    if playdebug: print("on : n:%3d v:%3d" % (note,vel), end="\n" )
    midi_msg = bytearray([0x90, note, vel])  # FIXME
    if do_usb_midi:
        midi_usb_out.write( midi_msg )
    if do_serial_midi:
        midi_uart.write( midi_msg )

def play_note_off(note, vel):  #
    #if on: # FIXME: always do note off to since race condition of note muted right after playing
    if playdebug: print("off: n:%3d v:%3d" % (note,vel), end="\n" )
    midi_msg = bytearray([0x80, note, vel])  # FIXME
    if do_usb_midi:
        midi_usb_out.write( midi_msg )
    if do_serial_midi:
        midi_uart.write( midi_msg )

while True:
    if mode==0:
        leds[:] = [[max(i-dim_by,0) for i in l] for l in leds] # dim all by (dim_by,dim_by,dim_by)
        leds[30] = 0x111111
    else:
        pass
    leds.show()

    t = time.monotonic()
    key_events = touch_matrix.update()
    #print("dt:%3d" % ((time.monotonic() - t) * 1000) )

    if len(key_events): print("key events!", time.monotonic())
    for (keynum,is_pressed) in key_events:
        print("\tkey:", keynum, is_pressed)
        noteval_label.text = str(keynum)
        if is_pressed:
            if keynum == 30:  # lower-left
                leds.fill(0x1111111)
                mode = (mode + 1) % 2
            else:
                h = int(keynum * (256/40))  # map to 0-255
                leds[keynum] = rainbowio.colorwheel( time.monotonic() * 50 )
                play_note_on(keynum_to_note(keynum), 100)
                #noteOn = NoteOn(keynum_to_note(keynum), 100 )
                #midi.send( noteOn )

        else:  # released
            if keynum != 30:  # special mod key
                play_note_off(keynum_to_note(keynum), 0)
                #noteOn = NoteOn(keynum_to_note(keynum), 0)
                #midi.send( noteOn )
