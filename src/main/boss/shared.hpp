#ifndef TH03_MAIN_BOSS_SHARED_HPP
#define TH03_MAIN_BOSS_SHARED_HPP

#include "compat/rec98/th03/common.h"

extern "C" {
unsigned char near boss_update_start(void);
void near boss_move_sine(void);
void near boss_fall(void);
void far boss_hittest_end(void);
void near boss_target_update(void);
void near boss_pattern_next(void);
void near boss_explosion_render(void);
}

#endif
