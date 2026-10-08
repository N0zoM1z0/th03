#ifndef TH03_MAIN_PLAYER_EXATT_KANA_HPP
#define TH03_MAIN_PLAYER_EXATT_KANA_HPP
#include "compat/rec98/th03/common.h"
extern "C" {
void far pascal exatt_add_kana(int x, int y, unsigned char pid);
void far pascal kana_extra_add(int x, int y, unsigned char angle);
void far pascal exatt_update_kana(void);
void far pascal exatt_render_kana(void);
}
#endif
