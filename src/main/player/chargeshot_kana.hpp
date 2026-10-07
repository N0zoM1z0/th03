#ifndef TH03_MAIN_PLAYER_CHARGESHOT_KANA_HPP
#define TH03_MAIN_PLAYER_CHARGESHOT_KANA_HPP

#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"

extern "C" {
void far pascal chargeshots_reset_kana(void);
void far pascal chargeshot_add_kana(Subpixel center_x, Subpixel center_y);
void far pascal chargeshot_update_kana(void);
void far pascal chargeshot_render_kana(void);
void far gba_gauge_pattern_pellet_kana(void);
void far gba_gauge_pattern_bullet_kana(void);
}

uint8_t far chargeshot_hittest_kana(void);

#endif
