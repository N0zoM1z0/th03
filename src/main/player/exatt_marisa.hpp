#ifndef TH03_MAIN_PLAYER_EXATT_MARISA_HPP
#define TH03_MAIN_PLAYER_EXATT_MARISA_HPP
#include "compat/rec98/th03/common.h"
extern "C" {
void far pascal exatt_add_marisa(int x, int y, unsigned char pid);
void far pascal marisa_exatt_add(int x, int y, unsigned char pid);
void far pascal exatt_update_marisa(void);
void far pascal exatt_render_marisa(void);
}
#endif
