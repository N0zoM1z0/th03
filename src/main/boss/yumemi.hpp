#ifndef TH03_MAIN_BOSS_YUMEMI_HPP
#define TH03_MAIN_BOSS_YUMEMI_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal boss_yumemi_template_init(int player_id);
void far gba_boss_update_yumemi(void);
void far gba_boss_render_yumemi(void);
}

#endif
