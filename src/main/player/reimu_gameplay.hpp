#ifndef TH03_REIMU_GAMEPLAY_CANDIDATE_HPP
#define TH03_REIMU_GAMEPLAY_CANDIDATE_HPP
#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
// Candidate aliases for EXISTING historical storage; no allocation here.
// The two byte fields precede 14 words, so both natural a2 and a1 give 32 bytes.
struct reimu_chargeshot_t {
    unsigned char state;
    unsigned char frame;
    PlayfieldSubpixel x[7];
    PlayfieldSubpixel y[7];
    unsigned char angle;
    unsigned char speed;
};
struct reimu_bomb_particle_t {
    unsigned char active;
    unsigned char unknown_1;
    playfield_subpixel_t x;
    playfield_subpixel_t y;
    playfield_subpixel_t velocity_y;
};
// Shared with other character gauge implementations; field names are provisional.
struct gauge_pattern_timing_t {
    unsigned char total_frames;
    unsigned char byte_1;
    unsigned char byte_2;
    unsigned char byte_3;
};
extern reimu_chargeshot_t reimu_chargeshots[PLAYER_COUNT][12];
extern reimu_chargeshot_t near *reimu_chargeshot_p;
extern unsigned char reimu_chargeshot_alternate_hit_frame;
extern unsigned char reimu_gauge_frame[PLAYER_COUNT];
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];
extern reimu_bomb_particle_t reimu_bomb_particles[PLAYER_COUNT][32];
extern reimu_bomb_particle_t near *reimu_bomb_particle_p;
extern "C" {
void far pascal reimu_chargeshots_reset(void);
void far pascal chargeshot_add_reimu(Subpixel center_x, Subpixel center_y);
void far pascal reimu_hyper_shot_add(Subpixel center_x, Subpixel center_y);
void far pascal chargeshot_update_reimu(void);
void far pascal chargeshot_render_reimu(void);
void far gba_gauge_pattern_pellet_reimu(void);
void far gba_gauge_pattern_bullet_reimu(void);
void far pascal bomb_center_add(int x, int y, int pid);
void far pascal palette_restore_for_pid(pid_t pid);
}
uint8_t far chargeshot_hittest_reimu(void);
void near pascal reimu_chargeshot_sprite_put(int x, int y, int phase);
void near pascal gauge_pattern_reimu(bullet_type_t type);
void far shared_bomb_lifecycle_update(void);
void far reimu_bomb_update(void);
void near reimu_bomb_particles_render(void);
void far reimu_bomb(void);
#endif
