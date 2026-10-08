#ifndef TH03_MAIN_HUD_START_RENDER_HPP
#define TH03_MAIN_HUD_START_RENDER_HPP
#include "compat/rec98/th03/common.h"
// Near Pascal hardware helpers are separate from the normal C++ renderer.
extern "C" {
void near hud_start_anim_render(void);
void near pascal hud_start_sprite_strip_put(
    int x, int y, int pattern, int column
);
void near pascal hud_start_particle_pixel_put(int x, int y);
}
#endif
