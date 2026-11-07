#pragma option -zCSHARED

#include "src/main/hardware/frame_delay.hpp"

// Original TH02 shared `frmdely1` physical owner consumed by TH03 MAIN:
// the interrupt-driven counter is volatile and unsigned 16-bit, while
// the far-Pascal duration parameter is an original signed 16-bit int.
// This old Turbo C++ version supports a typedef-based compile-time guard.
typedef char frame_delay_original_native_word_abi[
    (sizeof(int) == 2 && sizeof(vsync_Count1) == 2) ? 1 : -1
];

void far pascal frame_delay(int frames)
{
    // The original volatile, unsigned 16-bit VSYNC counter is reset
    // exactly once, then genuinely reread on every iteration. A natural
    // for-init spelling remains original TC4 CODE (af914a), WITHOUT
    // introducing a timeout or replacing hardware polling with a sleep.
    // Reversing the comparison operands changed CODE (af914b), and
    // forcing signed counter interpretation also changed CODE (af914c).
    // Keep the original mixed signed/unsigned 16-bit expression.
    for(vsync_Count1 = 0; vsync_Count1 < frames; ) {
    }
}
