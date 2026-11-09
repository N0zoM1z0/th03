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
    PLAYER_EFFECT_QUAD_ANGLE_STEP = 64,
    PLAYER_EFFECT_QUAD_ROTATE_DELTA = 8,
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
    // Original ring cursor postfix, not prefix. Changing all three
    // changed real TC4 CODE (af924d).
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
    // Full physical effect-pool lifetime update: native while preserves
    // the original signed index, near pointer and post-write updates.
    for(i = 0; i < PLAYER_EFFECT_COUNT; ++i, ++effect) {
        if(effect->kind != PLAYER_EFFECT_FREE) {
            // Preserve byte-memory postfix: prefix changes TC4 CODE
            // (fresh native negative af924f).
            effect->age++;
            if(effect->age > PLAYER_EFFECT_EXPIRE_AFTER) {
                effect->kind = PLAYER_EFFECT_FREE;
            }
            // This signed radius compound update is CODE-sensitive;
            // explicit radius=radius+delta changed real TC4 output
            // in independent negative af924i.
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
    // Draw the entire actual effect pool, selecting the true left/
    // right playfield clipping per effect before GRCG rasterization.
    // Source `kind != FREE` and native while are byte-exact (af924b/c).
    for(i = 0; i < PLAYER_EFFECT_COUNT; ++i, ++effect) {
        if(effect->kind != PLAYER_EFFECT_FREE) {
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
                // Keep the signed shift for negative Y; switching
                // to /2 changed native CODE (fresh af924h).
                grcg_circle(effect->x, effect->y >> 1, effect->radius);
            } else {
                // Alternate real four-corner rotation direction by
                // physical slot parity. Explicit byte assignment with
                // named +/-8 is native exact (fresh af924g).
                effect->angle = effect->angle + (((i % 2) == 0) ? PLAYER_EFFECT_QUAD_ROTATE_DELTA : -PLAYER_EFFECT_QUAD_ROTATE_DELTA);
                // Exact four-corner polygon traversal: two typed locals
                // and an ordinary while retain the original CODE (af857a).
                // Compound `angle += enum_64` failed old native
                // TC4 (af857b), but explicit byte assignment with
                // named step *does* reproduce original CODE (af924e).
                vertex = 0;
                angle = effect->angle;
                while(vertex < PLAYER_EFFECT_QUAD_VERTICES) {
                    x[vertex] = polar(effect->x, effect->radius, CosTable8[angle]);
                    // Unlike the circle path, division truncates toward zero.
                    y[vertex] = polar(effect->y, effect->radius, SinTable8[angle]) / 2;
                    vertex++;
                    // Original 90-degree step after both polar calls.
                    angle = angle + PLAYER_EFFECT_QUAD_ANGLE_STEP;
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
