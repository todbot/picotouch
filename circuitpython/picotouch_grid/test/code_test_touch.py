
import time
import board
import touchio

touch_threshold_adjust = 10

touch_pins = (
    # cols
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5,
    board.GP6, board.GP7, board.GP8, board.GP9,
    # rows
    board.GP10, board.GP11, board.GP12, board.GP13,
)

touchins = []  # for testing
for pin in touch_pins:
    touchin = touchio.TouchIn(pin)
    touchin.threshold += touch_threshold_adjust
    touchins.append(touchin)

print("\n----------")
print("picotouch_grid_test_touch hello")

while True:
    for i in range(len(touchins)):
        print("%d  " % touchins[i].value, end='')
    print()
