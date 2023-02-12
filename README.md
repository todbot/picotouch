# picotouch

Tiny capsense touch MIDI keyboard from a Raspberry Pi Pico

<img width=700 src="./docs/picotouch_smd_top1.png"/>
<img width=700 src="./docs/picotouch_top2.png"/>

[For sale on Tindie!](https://www.tindie.com/products/todbot/picotouch-capsense-midi-keyboard-for-raspi-pico/)


## Demos


https://user-images.githubusercontent.com/274093/216477797-90a1e4ca-b68f-4eb2-be46-de1d6d81551e.mp4


https://user-images.githubusercontent.com/274093/115614719-dfea2d80-a2a2-11eb-9ef7-c71edfc8e3df.mp4

Also see videos in this Twitter thread : https://twitter.com/todbot/status/1382469033061093377

## Materials needed
- 1 - picotouch PCB ([order from OSHpark](https://oshpark.com/shared_projects/5MnI1jPf))
- 1 - Raspberry Pi Pico
- 23 - 1M ohm 0805 SMD resistors  ([Digikey cart with this & Pico](https://www.digikey.com/short/w381rn4w))


## How to solder

It's not too bad!  A pretty easy first-time SMD soldering project.  Here's how to solder the Pico down.
The technique is: line up the Pico solder one corner, solder the other, then finish all the rest.
In the video you see I don't get it aligned perfectly straight (hard to see around the camera), but it still works great!

https://user-images.githubusercontent.com/274093/217670870-b04d55ed-e37d-4be2-bea7-4985d2b3f8c4.mp4



## Installation

* Install CircuitPython
  - Hold down BOOT button while plugging in Pico to get RPI-RP2 drive
  - Download CircuitPython UF2 from https://circuitpython.org/board/raspberry_pi_pico/
  - Drag UF2 to RPI-RP2 drive. CircuitPython is now installed!

* Install CircuitPython libraries onto Pico
  - If you have Python on your computer you can do:
    ```
    pip3 install circup
    circup install adafruit_midi adafruit_debouncer adafruit_ticks
    ```
  - Otherwise, download the CircuitPython Libraries Bundle at https://circuitpython.org/libraries
    and copy over the `adafruit_midi`, `adafruit_debouncer`, & `adafruit_ticks` libraries

* Install picotouch `code.py`
  - Via commandline:
    ```
    cp picotouch/circuitpython/picotouch/code.py /Volumes/CIRCUITPY/code.py
    ```
  - Or you can drag-n-drop using your computer's GUI
  - Note: this will delete the previous `code.py` on your Pico.
      Normally this is fine, but if it's not, be sure to save it if you want to keep it!
