#ifndef TH03_MAIN_PLAYER_EXATT_REIMU_HPP
#define TH03_MAIN_PLAYER_EXATT_REIMU_HPP

#include "compat/rec98/th03/common.h"
#include "compat/rec98/th03/main/playfld.hpp"

extern "C" {
void far pascal exatt_add_reimu(int x, int y, unsigned char pid);
void far pascal reimu_extra_add(int x, int y, unsigned char angle);
void near pascal exatt_render_state2(screen_x_t left, screen_y_t top, unsigned char frame);
void near pascal exatt_render_state_other(screen_x_t left, screen_y_t top, unsigned char frame);
void near pascal exatt_collmap_set(int x, int y);
void far pascal exatt_update_reimu(void);
void far pascal exatt_render_reimu(void);
}

#endif
