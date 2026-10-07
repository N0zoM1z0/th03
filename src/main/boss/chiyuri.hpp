#ifndef TH03_MAIN_BOSS_CHIYURI_HPP
#define TH03_MAIN_BOSS_CHIYURI_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal boss_chiyuri_template_init(int player_id);
void far gba_boss_update_chiyuri(void);
void far gba_boss_render_chiyuri(void);
}

#endif
