#ifndef TH03_MAIN_PLAYER_EFFECTS_HPP
#define TH03_MAIN_PLAYER_EFFECTS_HPP

#include <stddef.h>
#include "src/main/playfield/playfld.hpp"

enum { PLAYER_EFFECT_COUNT = 12 };
enum player_effect_kind_t {
    PLAYER_EFFECT_FREE = 0,
    PLAYER_EFFECT_CIRCLE = 1,
    PLAYER_EFFECT_QUAD = 2
};

// Existing DGROUP storage, not an allocation or claim of physical ownership.
// The last byte is unclassified storage, not source/code alignment padding.
struct player_effect_t {
    uint8_t kind;
    uint8_t age;
    screen_x_t x;
    screen_y_t y;
    uint8_t radius;
    int8_t radius_delta;
    uint8_t angle;
    uint8_t unclassified_09;
};
extern player_effect_t player_effects[PLAYER_EFFECT_COUNT];
extern uint8_t player_effect_cursor;

extern "C" void far pascal bomb_explosion_add(
    playfield_subpixel_t x, playfield_subpixel_t y, pid2 pid
);
extern "C" void far pascal bomb_center_add(
    playfield_subpixel_t x, playfield_subpixel_t y, pid2 pid
);
extern "C" void far pascal bomb_axis_add(
    playfield_subpixel_t x, playfield_subpixel_t y, pid2 pid
);
void far player_effects_update(void);
void far player_effects_render(void);

#define EFFECT_FIELD(field, offset, bytes) \
    typedef char effect_field_##field[(offsetof(player_effect_t, field) == offset \
        && sizeof(((player_effect_t near *)0)->field) == bytes) ? 1 : -1]
EFFECT_FIELD(kind, 0, 1);
EFFECT_FIELD(age, 1, 1);
EFFECT_FIELD(x, 2, 2);
EFFECT_FIELD(y, 4, 2);
EFFECT_FIELD(radius, 6, 1);
EFFECT_FIELD(radius_delta, 7, 1);
EFFECT_FIELD(angle, 8, 1);
EFFECT_FIELD(unclassified_09, 9, 1);
#undef EFFECT_FIELD

typedef char effect_size[(sizeof(player_effect_t) == 10) ? 1 : -1];
typedef char effect_words[(sizeof(int) == 2 && sizeof(pid2) == 2 &&
    sizeof(playfield_subpixel_t) == 2) ? 1 : -1];
typedef char effect_signed_pixels[(screen_x_t(-1) < 0 &&
    screen_y_t(-1) < 0 && int8_t(-1) < 0) ? 1 : -1];
#endif
