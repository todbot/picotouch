/**
 * TouchyTouch - Simple capacitive sense touch library that mimics how CircuitPython touchio works
 *               But also with debounced rose() / fell() events
 *
 * 1 Dec 2022 - @todbot / Tod Kurt
 *
 * See: https://gist.github.com/todbot/27c34c55d36002c601b2c28ae8f1b8a4
 * more really: https://github.com/adafruit/circuitpython/blob/main/shared-module/touchio/TouchIn.c
 *
 */

// Note: this verison has been slightly modified in attempt to make it less twitchy:
// -- increased N_SAMPLES from 10 to 20
// -- included an simple 5-read average on creating initial threshold

#define N_SAMPLES 20
#define TIMEOUT_TICKS 10000

class TouchyTouch
{
 public:
  TouchyTouch() {}

  // set up a particular touch pin, automatically sets threshold and debounce_interval
  // but those can be changed later for tuning
  void begin(int apin = -1) {
    pin = apin;
    recalibrate();
    debounce_interval = 10;
    last_state = false;
    changed = false;
  }

  void recalibrate() {
    const int num_reads = 5;
    for(int i=0; i<num_reads; i++) {
      raw_val_last += rawRead();
    }
    raw_val_last /= num_reads;
    threshold = (raw_val_last * 1.05); 
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
    raw_val_last = rawRead();
    return (raw_val_last > threshold);
  }

  // do the actual touch detection
  int16_t rawRead() {
    uint16_t ticks = 0;
    for (uint16_t i = 0; i < N_SAMPLES; i++) {
      // set pad to digital output high for 10us to charge it
      pinMode(pin, OUTPUT);
      digitalWrite(pin, HIGH);
      delayMicroseconds(10);
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
  uint16_t raw_val_last; // for debugging
};
