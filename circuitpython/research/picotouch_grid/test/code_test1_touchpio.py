# picotouch_grid test1_touchpio -- initial testing of just touch pads
#                                  using touchio and touchpio
# 21 Feb 2023 - @todbot / Tod Kurt
#
#
import time
import board
import touchio
import touchpio

col_threshold_adjust = -100
row_threshold_adjust = 10

touch_pins_cols = (
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9,
)
touch_pins_rows = (
    board.GP10, board.GP11, board.GP12, board.GP13,
)

touch_cols = []
touch_rows = []

for pin in touch_pins_cols:
    touchin = touchio.TouchIn(pin)
    touchin.threshold += col_threshold_adjust
    touch_cols.append(touchin)

for pin in touch_pins_rows:
    touchin = touchpio.TouchIn(pin)
    touchin.threshold += row_threshold_adjust
    touch_rows.append(touchin)

print("\n----------")
print("picotouch_grid_test_touch hello")

while True:
    for i in range(len(touch_cols)):
        print("%d  " % touch_cols[i].value, end='')
    print('--  ',end='')
    for i in range(len(touch_rows)):
        print("%d  " % touch_rows[i].value, end='')
    print()
