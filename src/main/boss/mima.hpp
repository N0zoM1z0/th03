#ifndef TH03_MAIN_BOSS_MIMA_HPP
#define TH03_MAIN_BOSS_MIMA_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal boss_mima_template_init(int player_id);
void far gba_boss_update_mima(void);
void far gba_boss_render_mima(void);
}

#endif
