#
# picotouch boot.py -- Tiny capsense MIDI controller using Raspberry Pi Pico
# 2021-2024 - @todbot / Tod Kurt - github.com/todbot/picotouch
#

#import usb_hid
#import storage
import usb_midi
import supervisor

supervisor.set_usb_identification(manufacturer="todbot",
                                  product="picotouch",
                                  vid=0x27B8,  # ThingM, todbot's company
                                  pid=0xb1c0 ) # "pico"

usb_midi.set_names(streaming_interface_name="picotouch",
                   in_jack_name="midi_in",
                   out_jack_name="midi_out")

print("set usb and midi ident to 'picotouch'")

#usb_hid.disable()
#print("disabled usb_hid")

#storage.remount("/", readonly=False)
#print("remounted read-write")

