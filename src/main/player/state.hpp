#ifndef TH03_MAIN_PLAYER_STATE_HPP
#define TH03_MAIN_PLAYER_STATE_HPP
#include "src/main/player/bomb.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "src/main/math/vector_far.hpp"
#include "src/main/math/randring_getters.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

// C248..C2F9 is the near-this lose_render member declared in stuff.hpp.
// It consumes one player word (RET 2); the member body does not read this.
void near pascal player_render(player_stuff_t near *player);
void near pascal player_overlay_render(player_stuff_t near *player);
void near pascal player_knockback_update(player_stuff_t near *player);

#include "src/main/player/move.hpp"
#include "src/main/collision/hitcircle.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/defeat.hpp"
#include "compat/rec98/th03/main/hud/warning.hpp"
extern unsigned char page_back;
extern unsigned char target_formation_marker;
extern unsigned char round_defeated_player;
extern uint16_t combo_points_for_boss_attack;
void near player_shots_add(void);
// Existing root BSS at 1D56:4B9C, verified in the current native MAP.
// The original five-byte reserve is split 1+2+2; no new storage.
extern unsigned char shot_release_frames[2];
// Target C0D8..C1E6 reads BP+4 and returns RET 2; source name inferred.
void near pascal player_lose_anim_update(player_stuff_t near *player);
void near pascal player_state_update(input_t input, player_stuff_t near *player);

#define STATE_FIELD(field, offset, bytes) \
    typedef char state_##field[(offsetof(player_stuff_t, field) == offset && \
        sizeof(((player_stuff_t near *)0)->field) == bytes) ? 1 : -1]
STATE_FIELD(human_movement_last, 0x20, 2);
STATE_FIELD(shot_active, 0x22, 1);
STATE_FIELD(hyper, 0x64, 2);
STATE_FIELD(chargeshot_add, 0x68, 4);
STATE_FIELD(gauge_charged, 0x18, 2);
STATE_FIELD(cpu_frame, 0x74, 2);
STATE_FIELD(patnum_movement, 0x0E, 1);
STATE_FIELD(patnum_glow, 0x0F, 1);
STATE_FIELD(knockback_time, 0x10, 1);
STATE_FIELD(knockback_angle, 0x12, 1);
STATE_FIELD(knockback_length, 0x13, 1);
STATE_FIELD(knockback_active, 0x14, 1);
STATE_FIELD(lose_anim_time, 0x1F, 1);
#undef STATE_FIELD
#endif
