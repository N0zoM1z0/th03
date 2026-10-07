#ifndef TH03_MAIN_BOSS_RIKAKO_HPP
#define TH03_MAIN_BOSS_RIKAKO_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal boss_rikako_template_init(int player_id);
void far gba_boss_update_rikako(void);
void far gba_boss_render_rikako(void);
}

#endif
