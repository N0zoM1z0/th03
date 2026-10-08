#ifndef TH03_MAIN_PLAYER_EXATT_CHIYURI_HPP
#define TH03_MAIN_PLAYER_EXATT_CHIYURI_HPP
#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal exatt_add_chiyuri(int x, int y, unsigned char pid);
void far pascal exatt_update_chiyuri(void);
void far pascal exatt_render_chiyuri(void);
void far pascal exatt_ellen_slots_init(void);
}

#endif
