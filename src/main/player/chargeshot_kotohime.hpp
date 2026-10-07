#ifndef TH03_MAIN_PLAYER_CHARGESHOT_KOTOHIME_HPP
#define TH03_MAIN_PLAYER_CHARGESHOT_KOTOHIME_HPP

#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"

void far chargeshots_reset_kotohime(void);

extern "C" {
void far pascal chargeshot_add_kotohime(Subpixel center_x, Subpixel center_y);
void far pascal chargeshot_update_kotohime(void);
void far pascal chargeshot_render_kotohime(void);
void far gba_gauge_pattern_pellet_kotohime(void);
void far gba_gauge_pattern_bullet_kotohime(void);
}

uint8_t far chargeshot_hittest_kotohime(void);

#endif
