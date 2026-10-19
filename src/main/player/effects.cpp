// Complete target-derived CDBD..D031 source proposal; not compiled or accepted.
#pragma codeseg PLAYER_M_TEXT main_01
#include "src/main/player/effects.hpp"
#include "src/main/math/polar.hpp"
#include "src/main/math/randring_getters.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

void far pascal player_effect_circle_expand(
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
    effect->radius = 8;
    effect->radius_delta = 8;
}

void far pascal player_effect_circle_shrink(
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
    effect->radius = 136;
    effect->radius_delta = -8;
}

void far pascal player_effect_quad_shrink(
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
    effect->radius = 162;
    effect->radius_delta = -10;
    effect->angle = randring_far_next16();
}

void far player_effects_update(void)
{
    register player_effect_t near *effect = player_effects;
    int i;
    for(i = 0; i < PLAYER_EFFECT_COUNT; i++, effect++) {
        if(effect->kind != PLAYER_EFFECT_FREE) {
            effect->age++;
            if(effect->age > 16) {
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
        if(effect->kind != PLAYER_EFFECT_FREE) {
            if(effect->x < PLAYFIELD_W_BORDERED) {
                grc_setclip(16, 8, 303, 191);
            } else {
                grc_setclip(336, 8, 623, 191);
            }
            if(effect->kind == PLAYER_EFFECT_CIRCLE) {
                // The circle path floors negative odd y via arithmetic shift.
                grcg_circle(effect->x, effect->y >> 1, effect->radius);
            } else {
                effect->angle += ((i % 2) == 0) ? 8 : -8;
                for(vertex = 0, angle = effect->angle; vertex < 4;
                    vertex++, angle += 64) {
                    x[vertex] = polar(effect->x, effect->radius, CosTable8[angle]);
                    // Unlike the circle path, division truncates toward zero.
                    y[vertex] = polar(effect->y, effect->radius, SinTable8[angle]) / 2;
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
    grc_setclip(0, 0, 639, 199);
}
