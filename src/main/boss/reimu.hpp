#ifndef TH03_MAIN_BOSS_REIMU_HPP
#define TH03_MAIN_BOSS_REIMU_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal boss_reimu_template_init(int player_id);
void far gba_boss_update_reimu(void);
void far gba_boss_render_reimu(void);
}

#endif
