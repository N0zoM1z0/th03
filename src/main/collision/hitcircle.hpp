#ifndef TH03_MAIN_HITCIRCLES_HPP
#define TH03_MAIN_HITCIRCLES_HPP

// Circle animation that indicates that an entity was hit. Unlike TH05's
// hitshots which are only shown for enemies, these hit circles are separated
// into flashing yellow enemy circles and a single consistently white player
// circle.

#include "compat/rec98/th03/common.h"
#include "compat/rec98/th01/math/subpixel.hpp"

extern bool hitcircles_enemy_add_do_not_randomly_center_within_hitbox;

void pascal hitcircles_enemy_add(
	subpixel_t center_x, subpixel_t center_y, pid2 pid
);
void pascal hitcircles_player_add(
	subpixel_t center_x, subpixel_t center_y, pid2 pid
);
void near hitcircles_update(void);

void near hitcircles_render(void);

#endif
