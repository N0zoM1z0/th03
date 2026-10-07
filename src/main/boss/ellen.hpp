#ifndef TH03_MAIN_BOSS_ELLEN_HPP
#define TH03_MAIN_BOSS_ELLEN_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
void far pascal boss_ellen_template_init(int player_id);
void far gba_boss_update_ellen(void);
void far gba_boss_render_ellen(void);
}

#endif
