#ifndef TH03_MAIN_HUD_INTRO_HPP
#define TH03_MAIN_HUD_INTRO_HPP
#pragma option -a1
#include "src/main/hud/start_anim.hpp"
#include "src/main/hud/start_render.hpp"
#include "compat/rec98/th03/resident.hpp"
#include "src/main/math/randring_getters.hpp"
#include "src/main/math/polar.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#pragma option -a2

struct hud_start_particle_t {
    int x, y, velocity;
    unsigned char angle, active, turn_early, turn_late;
};
typedef char hud_start_particle_size10[(sizeof(hud_start_particle_t) == 10) ? 1 : -1];

extern hud_start_particle_t hud_start_particles[128];
extern hud_start_particle_t near *hud_start_particle_p;
extern unsigned char hud_start_flag, hud_intro_phase, round_id;
extern int hud_intro_frame, hud_intro_sprite, hud_intro_x, hud_intro_destination_x;
extern int CosTable8[256], SinTable8[256];
extern "C" int far pascal IRand(void);
extern "C" unsigned int super_patdata[];
#endif
