#ifndef TH03_MAIN_PLAYER_STATE_HPP
#define TH03_MAIN_PLAYER_STATE_HPP
#include "src/main/player/bomb.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "src/main/math/vector_far.hpp"
#include "src/main/math/randring_getters.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

// Target C248..C2F9 returns with RET 2; its passed player slot is unused.
// The source name and pointer interpretation are inferred from this caller.
void near pascal player_lose_anim_render(player_stuff_t near *unused_player);
void near pascal player_render(player_stuff_t near *player);
void near pascal player_overlay_render(player_stuff_t near *player);
void near pascal player_knockback_update(player_stuff_t near *player);

#define STATE_FIELD(field, offset, bytes) \
    typedef char state_##field[(offsetof(player_stuff_t, field) == offset && \
        sizeof(((player_stuff_t near *)0)->field) == bytes) ? 1 : -1]
STATE_FIELD(patnum_movement, 0x0E, 1);
STATE_FIELD(patnum_glow, 0x0F, 1);
STATE_FIELD(knockback_time, 0x10, 1);
STATE_FIELD(knockback_angle, 0x12, 1);
STATE_FIELD(knockback_length, 0x13, 1);
STATE_FIELD(knockback_active, 0x14, 1);
STATE_FIELD(lose_anim_time, 0x1F, 1);
#undef STATE_FIELD
#endif
