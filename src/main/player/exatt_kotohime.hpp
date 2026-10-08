#ifndef TH03_MAIN_PLAYER_EXATT_KOTOHIME_HPP
#define TH03_MAIN_PLAYER_EXATT_KOTOHIME_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal exatt_add_kotohime(int x, int y, unsigned char pid);
void far pascal kotohime_extra_add(int target_x, int target_y);
void far pascal exatt_update_kotohime(void);
void far pascal exatt_render_kotohime(void);
}

#endif
