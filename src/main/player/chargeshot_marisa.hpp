#ifndef TH03_MARISA_GAMEPLAY_CANDIDATE_HPP
#define TH03_MARISA_GAMEPLAY_CANDIDATE_HPP
#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
extern "C" {
void far pascal marisa_chargeshot_state_reset(void);
void far pascal chargeshot_add_marisa(Subpixel center_x, Subpixel center_y);
void far pascal marisa_hyper_14340(void);
void far pascal chargeshot_update_marisa(void);
void far pascal chargeshot_render_marisa(void);
void far gba_gauge_pattern_pellet_marisa(void);
void far gba_gauge_pattern_bullet_marisa(void);
}
uint8_t far chargeshot_hittest_marisa(void);
void near pascal gauge_pattern_marisa(bullet_type_t type);
void far marisa_bomb(void);
#endif
