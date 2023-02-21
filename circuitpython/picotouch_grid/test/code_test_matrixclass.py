
import time
import board
import touchio

touch_threshold_adjust_row = 10
touch_threshold_adjust_col = 10

touch_row_pins = (
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9
)
touch_col_pins = ( board.GP10, board.GP11, board.GP12, board.GP13, )

class TouchMatrix:
    def __init__(self, col_pins, row_pins, threshold_adjust_col=100, threshold_adjust_row=100):
        self.touch_cols = []
        self.touch_rows = []
        for pin in col_pins:
            touchin = touchio.TouchIn(pin)
            touchin.threshold += touch_threshold_adjust_col
            self.touch_cols.append(touchin)
        for pin in row_pins:
            touchin = touchio.TouchIn(pin)
            touchin.threshold += touch_threshold_adjust_row
            self.touch_rows.append(touchin)
        self.num_touch_cols = len(self.touch_cols)
        self.num_touch_rows = len(self.touch_rows)

    # fixme: better name for this
    def check(self):
        col_pressed = None
        row_pressed = None
        for i in range(len(self.touch_cols)):
            if self.touch_cols[i].value:
                col_pressed = i
        for i in range(len(self.touch_rows)):
            if self.touch_rows[i].value:
                row_pressed = i
        return (col_pressed,row_pressed)



print("\n----------")
print("picotouch_grid test hello")

touch_matrix = TouchMatrix( col_pins=touch_col_pins, row_pins=touch_row_pins )

while True:
    (col,row) = touch_matrix.check()
    if col is not None and row is not None:
        print(col,row)
