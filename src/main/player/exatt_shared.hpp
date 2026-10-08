#ifndef TH03_MAIN_PLAYER_EXATT_SHARED_HPP
#define TH03_MAIN_PLAYER_EXATT_SHARED_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
unsigned char near cdecl exatt_fly_update(void);
void near pascal exatt_fly_init(
    int x, int y, int target_x, int target_y, unsigned char pid, int speed
);
}

#endif
