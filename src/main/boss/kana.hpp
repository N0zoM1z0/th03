#ifndef TH03_MAIN_BOSS_KANA_HPP
#define TH03_MAIN_BOSS_KANA_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal boss_kana_template_init(int player_id);
void far gba_boss_update_kana(void);
void far gba_boss_render_kana(void);
}

#endif
