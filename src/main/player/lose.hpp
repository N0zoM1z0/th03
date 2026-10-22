#ifndef TH03_MAIN_PLAYER_LOSE_HPP
#define TH03_MAIN_PLAYER_LOSE_HPP
#include "src/main/player/state.hpp"
#pragma option -a1
#include "compat/rec98/th03/resident.hpp"
#pragma option -a2
#include "compat/rec98/libs/master.lib/master.hpp"
#include "src/main/math/polar.hpp"
// Views of existing DGROUP words; no storage allocation.
extern int player_lose_left, player_lose_top, player_lose_radius;
extern unsigned char round_reset_flag;
void near pascal player_lose_particle_put(unsigned char angle_x, unsigned char angle_y);
void near round_defeat_banners_render(void);
#endif
