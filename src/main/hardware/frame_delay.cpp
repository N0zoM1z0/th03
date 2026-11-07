#pragma option -zCSHARED

#include "src/main/hardware/frame_delay.hpp"

void far pascal frame_delay(int frames)
{
    vsync_Count1 = 0;
    // Poll the original volatile 16-bit VSYNC counter without sleeping.
    for(; vsync_Count1 < frames; ) {
    }
}
