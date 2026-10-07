#ifndef TH03_MAIN_PLAYER_EXATT_RIKAKO_HPP
#define TH03_MAIN_PLAYER_EXATT_RIKAKO_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal exatt_add_rikako(int x, int y, unsigned char pid);
void far pascal rikako_extra_add(int x, int y, unsigned char angle);
void far pascal exatt_update_rikako(void);
void far pascal exatt_render_rikako(void);
}

#endif
