// Source-attested original CDBD..D031 complete player effect compiler unit.
#pragma codeseg PLAYER_M_TEXT main_01
#include "src/main/player/effects.hpp"
#include "src/main/math/polar.hpp"
#include "src/main/math/randring_getters.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

// The physical quad is drawn as four distinct edges rather than a
// generic polygon allocator. Each historical vertex turns 64 byte units.
enum player_effect_native_render_timing_t {
    PLAYER_EFFECT_QUAD_VERTICES = 4,
    PLAYER_EFFECT_EXPLOSION_START_RADIUS = 8,
    PLAYER_EFFECT_EXPLOSION_GROWTH = 8,
    PLAYER_EFFECT_CENTER_START_RADIUS = 136,
    PLAYER_EFFECT_CENTER_SHRINK = -8,
    PLAYER_EFFECT_AXIS_START_RADIUS = 162,
    PLAYER_EFFECT_AXIS_SHRINK = -10,
    PLAYER_EFFECT_EXPIRE_AFTER = 16,
    PLAYER_EFFECT_LEFT_CLIP_X0 = 16,
    PLAYER_EFFECT_LEFT_CLIP_Y0 = 8,
    PLAYER_EFFECT_LEFT_CLIP_X1 = 303,
    PLAYER_EFFECT_LEFT_CLIP_Y1 = 191,
    PLAYER_EFFECT_RIGHT_CLIP_X0 = 336,
    PLAYER_EFFECT_RIGHT_CLIP_Y0 = 8,
    PLAYER_EFFECT_RIGHT_CLIP_X1 = 623,
    PLAYER_EFFECT_RIGHT_CLIP_Y1 = 191,
    PLAYER_EFFECT_FULL_CLIP_X1 = 639,
    PLAYER_EFFECT_FULL_CLIP_Y1 = 199,
};

// The cursor wraps only *after* incrementing, and current-source TC4
// requires that as separate statements; if(++cursor >= COUNT) differs.
extern "C" void far pascal bomb_explosion_add(
    playfield_subpixel_t x, playfield_subpixel_t y, pid2 pid
)
{
    register player_effect_t near *effect;
    player_effect_cursor++;
    if(player_effect_cursor >= PLAYER_EFFECT_COUNT) {
        player_effect_cursor = 0;
    }
    effect = &player_effects[player_effect_cursor];
    effect->kind = PLAYER_EFFECT_CIRCLE;
    effect->age = 0;
    effect->x = playfield_fg_x_to_screen(x, pid);
    effect->y = (y >> 4) + PLAYFIELD_TOP;
    effect->radius = PLAYER_EFFECT_EXPLOSION_START_RADIUS;
    effect->radius_delta = PLAYER_EFFECT_EXPLOSION_GROWTH;
}

extern "C" void far pascal bomb_center_add(
    playfield_subpixel_t x, playfield_subpixel_t y, pid2 pid
)
{
    register player_effect_t near *effect;
    player_effect_cursor++;
    if(player_effect_cursor >= PLAYER_EFFECT_COUNT) {
        player_effect_cursor = 0;
    }
    effect = &player_effects[player_effect_cursor];
    effect->kind = PLAYER_EFFECT_CIRCLE;
    effect->age = 0;
    effect->x = playfield_fg_x_to_screen(x, pid);
    effect->y = (y >> 4) + PLAYFIELD_TOP;
    effect->radius = PLAYER_EFFECT_CENTER_START_RADIUS;
    effect->radius_delta = PLAYER_EFFECT_CENTER_SHRINK;
}

extern "C" void far pascal bomb_axis_add(
    playfield_subpixel_t x, playfield_subpixel_t y, pid2 pid
)
{
    register player_effect_t near *effect;
    player_effect_cursor++;
    if(player_effect_cursor >= PLAYER_EFFECT_COUNT) {
        player_effect_cursor = 0;
    }
    effect = &player_effects[player_effect_cursor];
    effect->kind = PLAYER_EFFECT_QUAD;
    effect->age = 0;
    effect->x = playfield_fg_x_to_screen(x, pid);
    effect->y = (y >> 4) + PLAYFIELD_TOP;
    effect->radius = PLAYER_EFFECT_AXIS_START_RADIUS;
    effect->radius_delta = PLAYER_EFFECT_AXIS_SHRINK;
    effect->angle = randring_far_next16();
}

// Separate increment and expiry check are native-visible: replacing
// them with if(++effect->age > 16) changed genuine original TC4 CODE.
void far player_effects_update(void)
{
    register player_effect_t near *effect = player_effects;
    int i;
    for(i = 0; i < PLAYER_EFFECT_COUNT; i++, effect++) {
        if(effect->kind) {
            effect->age++;
            if(effect->age > PLAYER_EFFECT_EXPIRE_AFTER) {
                effect->kind = PLAYER_EFFECT_FREE;
            }
            effect->radius += effect->radius_delta;
        }
    }
}

void far player_effects_render(void)
{
    register player_effect_t near *effect = player_effects;
    int i;
    screen_x_t x[4];
    vram_y_t y[4];
    uint8_t angle;
    register int vertex;

    grcg_setcolor(GC_RMW, 13);
    for(i = 0; i < PLAYER_EFFECT_COUNT; i++, effect++) {
        if(effect->kind) {
            if(effect->x < PLAYFIELD_W_BORDERED) {
                grc_setclip(
                    PLAYER_EFFECT_LEFT_CLIP_X0, PLAYER_EFFECT_LEFT_CLIP_Y0,
                    PLAYER_EFFECT_LEFT_CLIP_X1, PLAYER_EFFECT_LEFT_CLIP_Y1
                );
            } else {
                grc_setclip(
                    PLAYER_EFFECT_RIGHT_CLIP_X0, PLAYER_EFFECT_RIGHT_CLIP_Y0,
                    PLAYER_EFFECT_RIGHT_CLIP_X1, PLAYER_EFFECT_RIGHT_CLIP_Y1
                );
            }
            if(effect->kind == PLAYER_EFFECT_CIRCLE) {
                // The circle path floors negative odd Y via signed
                // arithmetic shift; /2 rounds differently and changed
                // real original CODE (failed native af857d).
                grcg_circle(effect->x, effect->y >> 1, effect->radius);
            } else {
                effect->angle += ((i % 2) == 0) ? 8 : -8;
                // Exact four-corner polygon traversal: two typed locals
                // and an ordinary while retain the original CODE (af857a).
                // Keep literal byte angle +=64: enum-valued 64 changed
                // TC4 instructions (failed af857b).
                vertex = 0;
                angle = effect->angle;
                while(vertex < PLAYER_EFFECT_QUAD_VERTICES) {
                    x[vertex] = polar(effect->x, effect->radius, CosTable8[angle]);
                    // Unlike the circle path, division truncates toward zero.
                    y[vertex] = polar(effect->y, effect->radius, SinTable8[angle]) / 2;
                    vertex++;
                    angle += 64;
                }
                grcg_line(x[0], y[0], x[1], y[1]);
                grcg_line(x[1], y[1], x[2], y[2]);
                grcg_line(x[2], y[2], x[3], y[3]);
                grcg_line(x[3], y[3], x[0], y[0]);
            }
        }
    }
    // Complete hardware operation: disable GRCG using the observed word write.
    // AX is the I/O accumulator; DX is untouched. No C result is exposed.
    // Original source spelling is unknown; compiler owns surrounding code.
    enum { GRCG_MODE_PORT = 0x7C };
    asm {
        xor ax, ax
        out GRCG_MODE_PORT, ax
    }
    grc_setclip(0, 0, PLAYER_EFFECT_FULL_CLIP_X1, PLAYER_EFFECT_FULL_CLIP_Y1);
}
