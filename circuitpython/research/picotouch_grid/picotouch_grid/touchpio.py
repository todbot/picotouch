# touchpio.py -- Capacitive Touch Sensing using Pico / RP2040 PIO,
#                   using similar API to CircuitPython's "touchio"
# 24 Feb 2023 - @todbot / Tod Kurt
#
# Part of https://github.com/todbot/picotouch
#
# Uses ideas from "# PIO Capsense experiment / -scottiebabe 2022" from
# https://community.element14.com/products/raspberry-pi/f/forum/51242/want-to-create-a-capacitance-proximity-touch-sensor-with-a-rp2040-pico-board-using-pio/198662
#
#

import array
import rp2pio
import adafruit_pioasm

class TouchIn:
    capsense_pio_code = adafruit_pioasm.assemble(
    """
    pull block           ; trigger a reading, get maxcount value from fifo, OSR contains maxcount
    set pindirs, 1       ; set GPIO as output
    set pins, 1          ; drive pin HIGH to charge capacitance
;    set x,24             ; wait time for pin charge
    set x,30             ; wait time for pin charge
charge:                  ; wait (24+1)*31 = 1085 cycles = 8.6us
    jmp x--, charge [31]
    mov x, osr           ; load maxcount value (10_000 usually)
    set pindirs, 0       ; set GPIO as input
timing:
    jmp x--, test        ; decrement x until timeout
    jmp done             ; we've timed out, so leave
test:
    jmp pin, timing      ; loop while pin is still high
done:
    mov isr, x           ; load ISR with count value in x
    push                 ; push ISR into RX fifo
    """)

    def __init__(self, touch_pin, max_count=10_000):
        self.max_count = max_count
        self.pio = rp2pio.StateMachine( TouchIn.capsense_pio_code,
                                        frequency=125_000_000,
                                        first_set_pin = touch_pin,
                                        jmp_pin = touch_pin )
        self.max_count = 10_000
        self.buf_send = array.array("L", [max_count] )   # 32-bit value
        self.buf_recv = array.array("L", [0] )  # 32-bit value
        self.base_val = self.raw_value
        self.last_val = self.base_val
        self.threshold = self.base_val + 200
        if self.base_val == 0xffffffff:  # -1
            raise ValueError("No pulldown on pin; 1Mohm recommended")

    def raw_read(self):
        self.pio.write( self.buf_send )
        self.pio.readinto( self.buf_recv )
        v = self.buf_recv[0]   # return 32-bit number from PIO
        if v > self.max_count: v = self.last_val
        self.last_val = v
        return v

    @property
    def raw_value(self):
        return self.max_count - self.raw_read()

    @property
    def value(self):
        return self.raw_value > self.threshold
