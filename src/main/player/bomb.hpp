#ifndef TH03_MAIN_PLAYER_BOMB_HPP
#define TH03_MAIN_PLAYER_BOMB_HPP

#include "src/main/sound/se.hpp"
#include "src/main/player/cpu.hpp"
#include "src/main/player/effects.hpp"
#include "src/main/hud/static.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"

void near story_skill_decrement(void);

#define BOMB_FIELD(field, offset, bytes) \
    typedef char bomb_##field[(offsetof(player_stuff_t, field) == offset && \
        sizeof(((player_stuff_t near *)0)->field) == bytes) ? 1 : -1]
BOMB_FIELD(invincibility_time, 0x06, 1);
BOMB_FIELD(playchar_paletted, 0x08, 1);
BOMB_FIELD(gauge_avail, 0x1A, 2);
BOMB_FIELD(bombs, 0x1D, 1);
BOMB_FIELD(hyper_active, 0x1E, 1);
#undef BOMB_FIELD

typedef char bomb_flag_width[(sizeof(bomb_flag_t) == 1) ? 1 : -1];
typedef char bomb_damage_width[(sizeof(damage_all_on[0]) == 1) ? 1 : -1];
#endif
