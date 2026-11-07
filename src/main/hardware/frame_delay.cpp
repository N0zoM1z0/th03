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
    vsync_Count1 = 0;
    // Natural while loop emits the original polling instructions.
    // Swapping comparison operands changed TC4 CODE (af864b), as did
    // forcing the volatile unsigned counter to signed int (af864c).
    // Keep the original mixed signed/unsigned source expression and
    // its real hardware polling order, without timeout or sleeps.
    while(vsync_Count1 < frames) {
    }
}
