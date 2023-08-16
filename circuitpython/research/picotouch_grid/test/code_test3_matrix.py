# picotouch_grid test3_matrix -- test TouchMatrix class (touch pads & LEDs)
# 23 Feb 2023 - @todbot / Tod Kurt
#
#

import time
import board
import neopixel
import rainbowio
import touchmatrix

touch_col_pins = ( board.GP0, board.GP1, board.GP2, board.GP3, board.GP4,
                   board.GP5, board.GP6, board.GP7, board.GP8, board.GP9 )
touch_row_pins = ( board.GP10, board.GP11, board.GP12, board.GP13, )
neopixel_pin  = board.GP28
oled_sda_pin  = board.GP14
oled_scl_pin  = board.GP15
midi_uart_pin = board.GP20

print("\n----------")
print("picotouch_grid test3_matrix hello")

touch_matrix = touchmatrix.TouchMatrix( col_pins=touch_col_pins, row_pins=touch_row_pins)

leds = neopixel.NeoPixel(neopixel_pin, 40, brightness=0.1, auto_write=False)
leds.fill(0x666666)

dim_by = 3


while True:
    leds[:] = [[max(i-dim_by,0) for i in l] for l in leds] # dim all by (dim_by,dim_by,dim_by)
    leds.show()

    t = time.monotonic()
    key_events = touch_matrix.update()
    #print("dt:%3d" % ((time.monotonic() - t) * 1000) ) # test timing

    if len(key_events): print("key events!")
    for (keynum, is_pressed) in key_events:
        print("\tkey:", keynum, is_pressed)
        if is_pressed:
            leds[keynum] = rainbowio.colorwheel( time.monotonic() * 50 )
