#ifndef TH03_MAIN_SOUND_KAJA_HPP
#define TH03_MAIN_SOUND_KAJA_HPP

#include <dos.h>

extern "C" {
extern unsigned char snd_active;
extern unsigned char snd_midi_active;

short far pascal snd_kaja_interrupt(short ax);
}

#endif
