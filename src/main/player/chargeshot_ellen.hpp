#ifndef TH03_MAIN_PLAYER_CHARGESHOT_ELLEN_HPP
#define TH03_MAIN_PLAYER_CHARGESHOT_ELLEN_HPP

#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"

void far chargeshots_reset_ellen(void);

extern "C" {
void far pascal chargeshot_add_ellen(Subpixel center_x, Subpixel center_y);
void far pascal chargeshot_update_ellen(void);
void far pascal chargeshot_render_ellen(void);
void far gba_gauge_pattern_pellet_ellen(void);
void far gba_gauge_pattern_bullet_ellen(void);
}

void far pascal ellen_hyper(Subpixel center_x, Subpixel center_y);
uint8_t far chargeshot_hittest_ellen(void);

#endif
