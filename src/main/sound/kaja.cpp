#pragma option -zCSHARED

#include "src/main/sound/kaja.hpp"

// Hardware PMD and MIDI service dispatch, not a runtime-selectable port:
// geninterrupt() receives one of the original constant software vectors.
enum {
    TH03_KAJA_PMD_VECTOR = 0x60,
    TH03_KAJA_MIDI_VECTOR = 0x61,
};

short far pascal snd_kaja_interrupt(short ax)
{
    if(!snd_active) {
        return _AX;
    }

    _AX = ax;
    if(snd_midi_active != 1) {
        geninterrupt(TH03_KAJA_PMD_VECTOR);
    } else {
        geninterrupt(TH03_KAJA_MIDI_VECTOR);
    }
    return _AX;
}
