/**
 * Simple monosynth in Mozzi running on core1 of arduino-pico
 * 
 */
#include <MozziGuts.h>
#include <Oscil.h>
#include <tables/saw_analogue512_int8.h> // oscillator waveform
#include <tables/cos2048_int8.h> // filter modulation waveform
#include <LowPassFilter.h>
#include <ADSR.h>
#include <mozzi_rand.h>  // for rand()
#include <mozzi_midi.h>  // for mtof()

Oscil<SAW_ANALOGUE512_NUM_CELLS, AUDIO_RATE> aOsc1(SAW_ANALOGUE512_DATA);
Oscil<SAW_ANALOGUE512_NUM_CELLS, AUDIO_RATE> aOsc2(SAW_ANALOGUE512_DATA);
Oscil<SAW_ANALOGUE512_NUM_CELLS, AUDIO_RATE> aOsc3(SAW_ANALOGUE512_DATA);
Oscil<SAW_ANALOGUE512_NUM_CELLS, AUDIO_RATE> aOsc4(SAW_ANALOGUE512_DATA);
Oscil<SAW_ANALOGUE512_NUM_CELLS, AUDIO_RATE> aOsc5(SAW_ANALOGUE512_DATA);
Oscil<COS2048_NUM_CELLS, CONTROL_RATE> kFilterMod(COS2048_DATA);
ADSR <CONTROL_RATE, AUDIO_RATE> envelope;
LowPassFilter lpf;

uint8_t resonance = 150; // range 0-255, 255 is most resonant


void setup1() { 
  startMozzi();
  kFilterMod.setFreq(0.8f);
  lpf.setCutoffFreqAndResonance(20, resonance);
  envelope.setADLevels(255, 255);
  envelope.setTimes(15, 200, 2000, 200 );
}

void loop1() {
  audioHook();  // must be only thing in loop for Mozzi
}

void synthNoteOn(int note) {
  float f = mtof(note);
  aOsc2.setFreq( f + (float)rand(100)/100); // orig 1.001, 1.002, 1.004
  aOsc3.setFreq( f + (float)rand(100)/100);
  aOsc4.setFreq( f + (float)rand(100)/100);
  aOsc5.setFreq( (f/2) + (float)rand(100)/1000); 
  //kFilterMod.setPhase(0); // retrigger LFO
  envelope.noteOn(); 
}

void synthNoteOff(int note) {
  envelope.noteOff();
}

// mozzi function, called every CONTROL_RATE
void updateControl() {
  // filter range (0-255) corresponds with 0-8191Hz
  // oscillator & mods run from -128 to 127
  byte cutoff_freq = 100 + kFilterMod.next()/4;
  lpf.setCutoffFreqAndResonance(cutoff_freq, resonance);

  envelope.update();

}

// mozzi function, called every AUDIO_RATE to output sample
AudioOutput_t updateAudio() {
  long asig = lpf.next(aOsc1.next() + 
                       aOsc2.next() + 
                       aOsc3.next() +
                       aOsc4.next() + 
                       aOsc5.next()
                       );
  return MonoOutput::fromAlmostNBit(20,asig*envelope.next());
}
