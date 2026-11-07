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
    // A single natural active-driver guard emits original TC4 CODE
    // (af869c), including the original unmodified AX return when inactive.
    if(snd_active != 0) {
        _AX = ax;
        // Retain the strict byte-flag ==1 meaning for MIDI. Inverting
        // the PMD/MIDI branch order changed original TC4 CODE (af869a).
        if(snd_midi_active != TH03_KAJA_MIDI_DRIVER_ACTIVE) {
            geninterrupt(TH03_KAJA_PMD_VECTOR);
        } else {
            geninterrupt(TH03_KAJA_MIDI_VECTOR);
        }
    }
    return _AX;
}
