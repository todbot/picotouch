# TouchMatrix for PicoTouch_Grid
# 16 Feb 2023 - @todbot / Tod Kurt
#
# Part of https://github.com/todbot/picotouch
#

from micropython import const

import touchio
import touchpio

class TouchMatrix:
    num_rows = const(4)
    num_cols = const(10)
    num_keys = const(num_rows * num_cols)
    smooth_amt = 0.25

    def __init__(self, col_pins, row_pins, col_threshold_adjust=10, row_threshold_adjust=10):
        self.cols = []
        self.rows = []
        for pin in col_pins:
            touchin = touchio.TouchIn(pin)
            touchin.threshold += col_threshold_adjust
            self.cols.append(touchin)
        for pin in row_pins:
            touchin = touchpio.TouchIn(pin)
            touchin.threshold += col_threshold_adjust
            self.rows.append(touchin)
        self.last_keys_pressed = [False] * self.num_keys
        self.smooth_rows = [0] * self.num_rows
        self.smooth_cols = [0] * self.num_cols

    # return key events in form [ (keynum,is_pressed), ...]
    def update(self):
        keys_pressed = [False] * self.num_keys
        rows_pressed = []

        # get all row touchpad states,
        # smooth (filter) the reads, since rows are more noisy
        # then, if pressed, add to list
        for r in range(self.num_rows):
            t = self.rows[r]
            val = t.raw_value - t.threshold
            self.smooth_rows[r] = (self.smooth_rows[r]*self.smooth_amt) + (1-self.smooth_amt)*val
            if self.smooth_rows[r] > 0: # pressed
                rows_pressed.append(r)

        # get all col touchpad states
        # set a keynum keypress for each row/col intersect press
        for c in range(self.num_cols):
            if self.cols[c].value:
                for r in rows_pressed:
                    key_num = (r*self.num_cols) + c  # convert col,row -> key num 0-39
                    keys_pressed[ key_num ] = True

        # debounce and construct key events
        # inspect all keys, compare to state last check
        key_events = []
        for i in range(self.num_keys):
            if keys_pressed[i]:
                if not self.last_keys_pressed[i]:  # pressed!
                    self.last_keys_pressed[i] = True
                    key_events.append( (i,True) )  # pressed event
            else:
                if self.last_keys_pressed[i]:  # released
                    self.last_keys_pressed[i] = False
                    key_events.append( (i,False) )

        return key_events
