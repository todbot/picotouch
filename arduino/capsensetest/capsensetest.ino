// capsensetest.ino -- implement a fakey capsense touch sensor using same technique as in CircuitPython
// 2 Aug 2022 - @todbot / Tod Kurt

///////////////

class FakeyTouch 
{
  #define FT_TIMEOUT_TICKS 10000
  #define FT_NUM_SAMPLES 5
  public:
  FakeyTouch() { }
  FakeyTouch( int apin, int athreshold = 500 ) {
    pin = apin;
    thold = athreshold;
  }  
  void begin(int apin, int athreshold = 500 ) {
    pin = apin;
    thold = athreshold;
    baseline = readTouchRaw();
    if( baseline == FT_TIMEOUT_TICKS ) { 
      Serial.println("No pulldown on pin, 1Mohm recommended");
    }
  }
  void begin() {
    baseline = readTouchRaw();
  }
  int readTouchRaw() {
    int raw = 0;
    for( int i = 0; i < FT_NUM_SAMPLES; i++ ) {
      pinMode(pin, OUTPUT);
      digitalWrite(pin,HIGH);
      delayMicroseconds(10);  // wait for capacitance to charge
      pinMode(pin,INPUT);
      while( digitalRead(pin) && raw < FT_TIMEOUT_TICKS ) { raw++; }
    }
    return raw;
  }
  bool isTouched() {
    return (readTouchRaw() > baseline + thold);
  }
  int baseline;
  int thold;
  int num_samples;
  int pin; 
};

///////////////////


const int touchpin_F = 16; // GP16
const int touch_pins[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22};
const int touch_count = sizeof(touch_pins) / sizeof(int);
const int touch_threhshold = 500;

//FakeyTouch touchF = FakeyTouch( touchpin_F );
FakeyTouch touches[touch_count];

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);
  Serial.println("hello world\n");
  for( int i=0; i< touch_count; i++ ) {
    touches[i].begin( touch_pins[i] );
  }
}

void loop() {

  for( int i=0; i< touch_count; i++ ) {
    if( touches[i].isTouched() ) { Serial.println(i); }
  }
  
//  uint32_t st = millis();
//  for( int i=0; i< touch_count; i++ ) {
//    Serial.print( touches[i].isTouched() ? "!" : "_");
//  }
//  uint32_t elapsed = millis() - st;
//  Serial.print(" --- "); Serial.println(elapsed);
//  delay(20);
}
