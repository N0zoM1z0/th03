#ifndef TH03_MAIN_BOSS_KOTOHIME_HPP
#define TH03_MAIN_BOSS_KOTOHIME_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal boss_kotohime_template_init(int player_id);
void far gba_boss_update_kotohime(void);
void far gba_boss_render_kotohime(void);
}

#endif
