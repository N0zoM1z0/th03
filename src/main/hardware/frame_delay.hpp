#ifndef TH03_FRAME_DELAY_HPP
#define TH03_FRAME_DELAY_HPP

extern "C" {
extern volatile unsigned int __cdecl vsync_Count1;
}

void far pascal frame_delay(int frames);

#endif
