/**
   midicontroller1.ino -- Arduino version of picotouch MIDI controller
   2 Aug 2022 - @todbot / Tod Kurt

   Libraries needed:
   - "arduino-pico" core for Pico - https://arduino-pico.readthedocs.io/en/latest/
   - Adafruit_TinyUSB - also select in IDE "Tools / USB Stack: Adafruit TinyUSB"

 **/


#include <Adafruit_TinyUSB.h>
#include <MIDI.h>

#include "TouchyTouch.h"


int midi_base_note = 48; // 48 = C3
int midi_velocity = 64;  // midpoint
int midi_channel = 1;    // 1-16
int midi_cc_num = 1;     // 1 = standard modwheel

const int touch_threshold_adjust = 300;

const int touch_pins[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22};
const int touch_count = sizeof(touch_pins) / sizeof(int);

const int pitch_up_index = 22;
const int pitch_down_index = 21;
const int mod_up_index = 19;
const int mod_down_index = 18;
const int oct_up_index = 20;
const int oct_down_index = 17;

Adafruit_USBD_MIDI usb_midi;
MIDI_CREATE_INSTANCE(Adafruit_USBD_MIDI, usb_midi, MIDIusb);

TouchyTouch touches[touch_count];

void setup() {
  Serial.begin(115200);
  Serial.println("picotouch midicontroller1");

  pinMode(PIN_LED, OUTPUT);

  MIDIusb.begin(MIDI_CHANNEL_OMNI);   // Initiate MIDI communications, listen to all channels
  MIDIusb.turnThruOff();    // turn off echo

  // delay to let power stabilize a little so touch calibration read goes okay
  delay(1000);

  // Touch buttons
  for (int i = 0; i < touch_count; i++) {
    touches[i].begin( touch_pins[i] );
    touches[i].threshold += touch_threshold_adjust; // make a bit more noise-proof
  }
}

int pitchbend_val = 0; // midpoint
int modwheel_val = 0;

void loop() {
  // key handling
  for ( int i = 0; i < touch_count; i++) {
    touches[i].update();

    if ( touches[i].rose() ) {
      Serial.printf("press       %d %d %d\n", i, touches[i].raw_value, touches[i].threshold);
      digitalWrite(PIN_LED, HIGH);

      if ( i == oct_up_index ) {
        Serial.println("oct up!");
        midi_base_note = min( midi_base_note + 12, 108);
      }
      else if ( i == oct_down_index ) {
        Serial.println("oct down!");
        midi_base_note = max( midi_base_note - 12, 0);
      }
      else if ( i == pitch_up_index) {
        Serial.println("pitch up!");
        pitchbend_val = 4096; // full up
        MIDIusb.sendPitchBend(pitchbend_val, midi_channel);
      }
      else if ( i == pitch_down_index ) {
        Serial.println("pitch down!");
        pitchbend_val = - 4096; // full down
        MIDIusb.sendPitchBend(pitchbend_val, midi_channel);
      }
      else if ( i == mod_up_index ) {
        Serial.println("mod up!");
        modwheel_val = 127;
        MIDIusb.sendControlChange(midi_cc_num, modwheel_val, midi_channel);
      }
      else if ( i == mod_down_index ) {
        Serial.println("mod down!");
        modwheel_val = 0;
        MIDIusb.sendControlChange(midi_cc_num, modwheel_val, midi_channel);
      }
      else {
        MIDIusb.sendPitchBend(0, midi_channel);
        MIDIusb.sendNoteOn(midi_base_note + i, midi_velocity, midi_channel);
      }
    }

    if ( touches[i].fell() ) {
      Serial.printf("    release %d %d %d\n", i, touches[i].raw_value, touches[i].threshold);
      digitalWrite(PIN_LED, LOW);
      if ( i == oct_up_index ) {
      }
      else if ( i == oct_down_index ) {
      }
      else if ( i == pitch_up_index) {
      }
      else if ( i == pitch_down_index ) {
      }
      else if ( i == mod_up_index ) {
      }
      else if ( i == mod_down_index ) {
      }
      else {  // notes!
        MIDIusb.sendNoteOff(midi_base_note + i, midi_velocity, midi_channel);
      }
    }
  }

}
