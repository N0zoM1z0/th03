#pragma option -zCSHARED

#include "src/main/sound/kaja.hpp"

// Hardware PMD and MIDI service dispatch, not a runtime-selectable port:
// geninterrupt() receives one of the original constant software vectors.
enum {
    TH03_KAJA_PMD_VECTOR = 0x60,
    TH03_KAJA_MIDI_VECTOR = 0x61,
    TH03_KAJA_MIDI_DRIVER_ACTIVE = 1,
};

// Keep original two-byte register/argument width and byte driver flags.
// These are source-only compile-time contracts, not added runtime DATA.
typedef char kaja_original_register_word[(sizeof(short) == 2) ? 1 : -1];
typedef char kaja_original_driver_flags[
    (sizeof(snd_active) == 1 && sizeof(snd_midi_active) == 1) ? 1 : -1
];

short far pascal snd_kaja_interrupt(short ax)
{
    // Only an active driver consumes AX and sends a software interrupt.
    // Otherwise the original caller's AX is returned without modification.
    if(snd_active) {
        _AX = ax;
        // Only the byte value 1 selects MIDI; every other flag selects PMD.
        if(snd_midi_active != TH03_KAJA_MIDI_DRIVER_ACTIVE) {
            geninterrupt(TH03_KAJA_PMD_VECTOR);
        } else {
            geninterrupt(TH03_KAJA_MIDI_VECTOR);
        }
    }
    return _AX;
}
