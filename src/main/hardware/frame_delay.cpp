#pragma option -zCSHARED

#include "src/main/hardware/frame_delay.hpp"

void far pascal frame_delay(int frames)
{
    vsync_Count1 = 0;
    while(vsync_Count1 < frames) {
    }
}
