#ifndef TH03_MAIN_HFLIPLUT_HPP
#define TH03_MAIN_HFLIPLUT_HPP

#include "compat/rec98/planar.h"

extern "C" {
extern dots8_t hflip_lut[256];
void far hflip_lut_generate(void);
}

#endif
