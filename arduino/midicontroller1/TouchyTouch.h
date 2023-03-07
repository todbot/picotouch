/**
 * TouchyTouch - Simple capacitive sense touch library that mimics how CircuitPython touchio works
 *               But also with debounced rose() / fell() events
 *
 * 7 Mar 2023 - @todbot / Tod Kurt
 *
 * See: https://gist.github.com/todbot/27c34c55d36002c601b2c28ae8f1b8a4
 * more really: https://github.com/adafruit/circuitpython/blob/main/shared-module/touchio/TouchIn.c
 *
 */

// Note: this verison has been slightly modified in attempt to make it less twitchy:
// -- increased N_SAMPLES from 10 to 20
// -- included an simple 5-read average on creating initial threshold

#define N_SAMPLES 20         // default is 10 in touchio, 15-20 works better on picotouch
#define CHARGE_MICROS 10     // default is 10 in touchio
#define TIMEOUT_TICKS 10000
#define OUTPUT_STYLE OUTPUT_8MA

class TouchyTouch
{
 public:
  TouchyTouch() {}

  // set up a particular touch pin, automatically sets threshold and debounce_interval
  // but those can be changed later for tuning
  void begin(int apin = -1, uint16_t debounce_millis=20) {
    pin = apin;
    recalibrate();
    debounce_interval = debounce_millis;
    last_state = false;
    changed = false;
  }

  void recalibrate() {
    const int num_reads = 5;
    for(int i=0; i<num_reads; i++) {
      raw_value += rawRead();
    }
    raw_value /= num_reads;
    threshold = (raw_value * 1.05); 
  }

  // call update() as fast as possible
  void update() {
    changed = false;
    uint32_t now = millis();
    if( now - last_debounce_millis > debounce_interval ) {
      last_debounce_millis = now;
      bool touch_state = isTouched();
      changed = touch_state != last_state;
      last_state = touch_state;
    }
  }

  // signal changed to true since last update
  bool rose() {
    return changed && last_state==true;
  }

  // signal changed to false since last update
  bool fell() {
    return changed && last_state==false;
  }

  // cause a read to happen, return true if above threshold
  bool isTouched() {
    raw_value = rawRead();
    return (raw_value > threshold);
  }

  // do the actual touch detection
  int16_t rawRead() {
    uint16_t ticks = 0;
    for (uint16_t i = 0; i < N_SAMPLES; i++) {
      // set pad to digital output high for 10us to charge it
      pinMode(pin, OUTPUT_STYLE);
      digitalWrite(pin, HIGH);
      delayMicroseconds(CHARGE_MICROS);
      // set pad back to an input and take some samples
      pinMode(pin, INPUT);
      while ( digitalRead(pin) ) {
        if (ticks >= TIMEOUT_TICKS) {
          return TIMEOUT_TICKS;
        }
        ticks++;
      }
    }
    return ticks;
  }

  uint32_t last_debounce_millis;
  uint16_t debounce_interval;
  bool last_state;
  bool changed;
  uint16_t threshold;
  int pin;
  uint16_t raw_value;
};
