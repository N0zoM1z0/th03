#ifndef TH03_MAIN_PLAYER_EXATT_ELLEN_HPP
#define TH03_MAIN_PLAYER_EXATT_ELLEN_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal exatt_add_ellen(int x, int y, unsigned char pid);
void far pascal ellen_extra_add(int x, int y, unsigned char angle, unsigned char mode);
void far pascal exatt_update_ellen(void);
void far pascal exatt_render_ellen(void);
}

#endif
