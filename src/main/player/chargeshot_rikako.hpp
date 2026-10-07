#ifndef TH03_MAIN_PLAYER_CHARGESHOT_RIKAKO_HPP
#define TH03_MAIN_PLAYER_CHARGESHOT_RIKAKO_HPP

#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"

void far chargeshots_reset_rikako(void);

extern "C" {
void far pascal chargeshot_add_rikako(Subpixel center_x, Subpixel center_y);
void far pascal rikako_charge_add_private(Subpixel center_x, Subpixel center_y);
void far rikako_chargeshot_cancel(void);
void far pascal chargeshot_update_rikako(void);
void far pascal chargeshot_render_rikako(void);
void far gba_gauge_pattern_pellet_rikako(void);
void far gba_gauge_pattern_bullet_rikako(void);
}

uint8_t far chargeshot_hittest_rikako(void);

#endif
