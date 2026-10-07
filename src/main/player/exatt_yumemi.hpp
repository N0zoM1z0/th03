#ifndef TH03_MAIN_PLAYER_EXATT_YUMEMI_HPP
#define TH03_MAIN_PLAYER_EXATT_YUMEMI_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal exatt_add_yumemi(int x, int y, unsigned char pid);
void far pascal yumemi_extra_add(int x, int y);
void far pascal exatt_update_yumemi(void);
void far pascal exatt_render_yumemi(void);
}

#endif
