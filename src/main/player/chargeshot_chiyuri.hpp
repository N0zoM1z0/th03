#ifndef TH03_MAIN_PLAYER_CHARGESHOT_CHIYURI_HPP
#define TH03_MAIN_PLAYER_CHARGESHOT_CHIYURI_HPP

#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"

void far chargeshots_reset_chiyuri(void);

extern "C" {
void far pascal chargeshot_add_chiyuri(Subpixel center_x, Subpixel center_y);
void far pascal chargeshot_update_chiyuri(void);
void far pascal chargeshot_render_chiyuri(void);
void far gba_gauge_pattern_pellet_chiyuri(void);
void far gba_gauge_pattern_bullet_chiyuri(void);
}

uint8_t far chargeshot_hittest_chiyuri(void);

#endif
