#ifndef TH03_MAIN_PLAYER_EXATT_MIMA_HPP
#define TH03_MAIN_PLAYER_EXATT_MIMA_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal exatt_add_mima(int x, int y, unsigned char pid);
void far pascal exatt_update_mima(void);
void far pascal exatt_render_mima(void);
}

#endif
