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
    // Reset the volatile 16-bit VSYNC counter exactly once. The loop
    // rereads the live counter on every pass, without sleeping or timing out.
    // Keep the original mixed signed/unsigned comparison order.
    vsync_Count1 = 0;
    while(vsync_Count1 < frames) {
    }
}
