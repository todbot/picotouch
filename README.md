# picotouch

Tiny capsense touch MIDI keyboard from a Raspberry Pi Pico

<img width=700 src="./docs/picotouch_top1.png"/>
<img width=700 src="./docs/picotouch_top2.png"/>

## Demo
https://user-images.githubusercontent.com/274093/115614719-dfea2d80-a2a2-11eb-9ef7-c71edfc8e3df.mp4

Also see videos in this Twitter thread : https://twitter.com/todbot/status/1382469033061093377

## Materials needed
- 1 - picotouch PCB ([order from OSHpark](https://oshpark.com/shared_projects/5MnI1jPf))
- 1 - Raspberry Pi Pico
- 22 - 1M ohm 0805 SMD resistors  ([Digikey cart with this & Pico](https://www.digikey.com/short/w381rn4w))


## Installation

- Install CircuitPython
  - Hold down BOOT button while plugging in Pico to get RPI-RP2 drive 
  - Download CircuitPython UF2 from https://circuitpython.org/board/raspberry_pi_pico/
  - Drag UF2 to RPI-RP2 drive. CircuitPython is now installed!

- Install Needed CircuitPython libraries onto Pico
  - If you have Python on your computer you can do:   
  ```
  pip3 install circup
  circup install adafruit_midi adafruit_debouncer
  ```
  - Otherwise, download the CircuitPython Libraries Bundle at https://circuitpython.org/libraries
    and copy over the `adafruit_midi` and `adafruit_debouncer` libraries

- Copy over `code.py`
  - Via commandline:
  ```
  cp picotouch/firmare/picotouch_code.py /Volumes/CIRCUITPY/code.py
  ```
  - Or you can drag-n-drop using your computer's GUI, then rename to `code.py`
