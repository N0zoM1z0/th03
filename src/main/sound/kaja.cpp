#pragma option -zCSHARED

#include "src/main/sound/kaja.hpp"

short far pascal snd_kaja_interrupt(short ax)
{
    if(!snd_active) {
        return _AX;
    }

    _AX = ax;
    if(snd_midi_active != 1) {
        geninterrupt(0x60);
    } else {
        geninterrupt(0x61);
    }
    return _AX;
}
