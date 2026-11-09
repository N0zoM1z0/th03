// Complete current source-native Reimu Chargeshot/Gauge physical owner.
// Native original TC4/TLINK evidence remains separate from canonical
// packed-game Factory acceptance and historical raw OMF packet identity.
#pragma codeseg HITBOX_TEXT main_04
#pragma option -a1
#include <stddef.h>
#include "src/main/player/reimu_gameplay.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#pragma option -a2
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/libs/sprite16/sprite16.h"
// MAIN_04 frame relationship observed in the neighboring maintained owner.
// Revalidate native fixups; this does not change bullets_add's far ABI.
#pragma samecodeseg bullets_add

// The physical 32-byte charged-shot entity holds seven X and seven Y
// historical positions. The original hitbox only scans SIX entries,
// although update/render scan TWELVE per player.
enum reimu_charge_limits_t {
    REIMU_CHARGE_SLOTS_PER_PLAYER = 12,
    REIMU_CHARGE_TOTAL_SLOTS = 24,
    REIMU_CHARGE_HITTEST_SLOTS = 6,
    REIMU_CHARGE_HISTORY_SAMPLES = 7,
    REIMU_CHARGE_LAST_SAMPLE = 6,
    REIMU_CHARGE_STANDARD_LAUNCH = 4,
    REIMU_CHARGE_FIRST_PAIR = 2,
    REIMU_CHARGE_STOP_FRAME = 64,
    REIMU_CHARGE_SPRITE_PHASE_MASK = 3,
    REIMU_GAUGE_FINISH_AFTER = 64,
    REIMU_GAUGE_RING_PERIOD = 32,
    REIMU_GAUGE_RING_PHASE = 16,
    REIMU_GAUGE_INIT_TICKS = 32,
    REIMU_CHARGE_LAUNCH_ANGLE = 0x90,
    REIMU_CHARGE_LAUNCH_SPEED = 0x60,
    REIMU_CHARGE_LAUNCH_ANGLE_STEP = 0x20,
    REIMU_CHARGE_CLIP_RADIUS = TO_SP(24),
    REIMU_CHARGE_HIT_MARGIN = TO_SP(20),
    REIMU_CHARGE_RENDER_SPRITE_WIDTH = 48,
    REIMU_CHARGE_RENDER_SPRITE_HEIGHT = 48,
    REIMU_CHARGE_RENDER_LEFT_OFFSET = 24,
    REIMU_CHARGE_RENDER_TOP_OFFSET = 8,
};

// Stored in one original byte per 32-byte projectile, shared by ordinary
// Chargeshot trails and Hyper spawns. Inactive slots remain allocated.
enum reimu_chargeshot_state_t {
    REIMU_SHOT_INACTIVE = 0,
    REIMU_SHOT_SLOWING = 1,
    REIMU_SHOT_HOMING = 2,
};

typedef char reimu_charge_stride_is_32[
    (sizeof(reimu_chargeshot_t) == 32) ? 1 : -1
];
typedef char reimu_charge_x_at_02[
    (offsetof(reimu_chargeshot_t, x) == 2) ? 1 : -1
];
typedef char reimu_charge_y_at_10[
    (offsetof(reimu_chargeshot_t, y) == 0x10) ? 1 : -1
];
typedef char reimu_charge_angle_at_1e[
    (offsetof(reimu_chargeshot_t, angle) == 0x1E) ? 1 : -1
];

void far pascal reimu_chargeshots_reset(void)
{
    reimu_chargeshot_p = &reimu_chargeshots[0][0];
    // Clear all 24 actual 32-byte projectile slots, both players.
    // Signed-index and near-pointer increments happen after each store.
    for(int i = 0; i < REIMU_CHARGE_TOTAL_SLOTS; ++i, ++reimu_chargeshot_p) {
        reimu_chargeshot_p->state = REIMU_SHOT_INACTIVE;
    }
}
void far pascal chargeshot_add_reimu(Subpixel center_x, Subpixel center_y)
{
    int i;
    int j;
    unsigned char angle;
    reimu_chargeshot_p = &reimu_chargeshots[pid.current][0];
    angle = REIMU_CHARGE_LAUNCH_ANGLE;
    // Four independently seeded spiral projectiles, with seven real
    // X/Y history samples per shot and mutable byte-angle step after
    // each full initialization (native source test af911a).
    for(i = 0; i < REIMU_CHARGE_STANDARD_LAUNCH; ++i, ++reimu_chargeshot_p) {
        reimu_chargeshot_p->state = REIMU_SHOT_SLOWING;
        reimu_chargeshot_p->frame = 0;
        for(j = 0; j < REIMU_CHARGE_HISTORY_SAMPLES; ++j) {
            reimu_chargeshot_p->x[j].v = center_x.v;
            reimu_chargeshot_p->y[j].v = center_y.v;
        }
        reimu_chargeshot_p->angle = angle;
        // Direct `angle += enum_step` changed CODE (af826c), but
        // explicit byte `angle = angle + named_step` is native-exact
        // in the new original TC4 experiment af911f.
        angle = angle + REIMU_CHARGE_LAUNCH_ANGLE_STEP;
        reimu_chargeshot_p->speed = REIMU_CHARGE_LAUNCH_SPEED;
    }
    reimu_chargeshot_alternate_hit_frame = 1;
}
void far pascal reimu_hyper_shot_add(Subpixel center_x, Subpixel center_y)
{
    reimu_chargeshot_p = &reimu_chargeshots[pid.current][0];
    // The first-free Hyper allocator cannot use a natural while with
    // explicit post-skip increments: it changed original CODE (af911b).
    // Keep original for/continue/break exactly, without dummy padding.
    for(int i = 0; i < REIMU_CHARGE_SLOTS_PER_PLAYER; ++i, ++reimu_chargeshot_p) {
        if(reimu_chargeshot_p->state != REIMU_SHOT_INACTIVE) {
            continue;
        }
        reimu_chargeshot_p->state = REIMU_SHOT_HOMING;
        reimu_chargeshot_p->frame = 0;
        for(int j = 0; j < REIMU_CHARGE_HISTORY_SAMPLES; ++j) {
            reimu_chargeshot_p->x[j].v = center_x.v;
            reimu_chargeshot_p->y[j].v = center_y.v;
        }
        reimu_chargeshot_p->angle = 0xC0;
        reimu_chargeshot_p->speed = 0xC0;
        break;
    }
    reimu_chargeshot_alternate_hit_frame = 0;
}
void far pascal chargeshot_update_reimu(void)
{
    int vector_x;
    int vector_y;
    reimu_chargeshot_p = &reimu_chargeshots[pid_current][0];
    playfield_clip_negative_radius.x.v = -REIMU_CHARGE_CLIP_RADIUS;
    playfield_clip_negative_radius.y.v = -REIMU_CHARGE_CLIP_RADIUS;
    // Full twelve-entity deceleration/homing/clip update, including
    // a descending 6..1 history shift, uses native-exact nested for loops.
    for(int i = 0; i < REIMU_CHARGE_SLOTS_PER_PLAYER; ++i, ++reimu_chargeshot_p) {
        if(reimu_chargeshot_p->state != REIMU_SHOT_INACTIVE) {
            players[pid_current].gauge_charged = 0;
            // Do not overwrite earlier history before consuming it.
            // Backward signed-index loop preserves physical slot order.
            for(int j = REIMU_CHARGE_LAST_SAMPLE; j > 0; --j) {
                reimu_chargeshot_p->x[j].v = reimu_chargeshot_p->x[j - 1].v;
                reimu_chargeshot_p->y[j].v = reimu_chargeshot_p->y[j - 1].v;
            }
            vector2(vector_x, vector_y, reimu_chargeshot_p->angle,
                reimu_chargeshot_p->speed);
            reimu_chargeshot_p->x[0].v += vector_x;
            reimu_chargeshot_p->y[0].v += vector_y;
            if(reimu_chargeshot_p->state == REIMU_SHOT_SLOWING) {
                if(reimu_chargeshot_p->speed > 0) {
                    reimu_chargeshot_p->speed -= 4;
                } else if(reimu_chargeshot_p->frame >= REIMU_CHARGE_STOP_FRAME) {
                    reimu_chargeshot_p->state = REIMU_SHOT_HOMING;
                    if(i < REIMU_CHARGE_FIRST_PAIR) {
                        reimu_chargeshot_p->angle = 0xB0;
                    } else {
                        reimu_chargeshot_p->angle = 0xD0;
                    }
                    reimu_chargeshot_p->speed = 0xE0;
                }
            }
            // Mutable byte frame postfix emits original CODE; prefix
            // did not (original compiler negative af911h).
            reimu_chargeshot_p->frame++;
            if(playfield_clip(reimu_chargeshot_p->x[REIMU_CHARGE_LAST_SAMPLE], reimu_chargeshot_p->y[REIMU_CHARGE_LAST_SAMPLE])) {
                reimu_chargeshot_p->state = REIMU_SHOT_INACTIVE;
            }
        }
    }
}
void near pascal reimu_chargeshot_sprite_put(int x, int y, int phase)
{
    sprite16_offset_t sprite_offset;
    phase += round_or_result_frame;
    phase &= REIMU_CHARGE_SPRITE_PHASE_MASK;
    sprite_offset = phase * 6 + pid.so_attack + 0x1180;
    x = playfield_fg_x_to_screen(x, pid_current) - REIMU_CHARGE_RENDER_LEFT_OFFSET;
    y = (y >> 4) - REIMU_CHARGE_RENDER_TOP_OFFSET;
    sprite16_put(x, y, sprite_offset);
}
uint8_t far chargeshot_hittest_reimu(void)
{
    if(reimu_chargeshot_alternate_hit_frame && (round_or_result_frame % 2)) {
        return 0;
    }
    reimu_chargeshot_p = &reimu_chargeshots[hitbox.pid][0];
    // Scan the original six hit-test slots, not all twelve visible slots;
    // both continue paths advance the index and near pointer in the header.
    for(int i = 0; i < REIMU_CHARGE_HITTEST_SLOTS; ++i, ++reimu_chargeshot_p) {
        if(reimu_chargeshot_p->state == REIMU_SHOT_INACTIVE) {
            continue;
        }
        if(reimu_chargeshot_p->x[0].v <= -TO_SP(16) ||
           reimu_chargeshot_p->x[0].v >= TO_SP(PLAYFIELD_W) ||
           reimu_chargeshot_p->y[0].v <= -TO_SP(16)) {
            continue;
        }
        if(reimu_chargeshot_p->x[0].v - hitbox.right.v <= REIMU_CHARGE_HIT_MARGIN &&
           hitbox.origin.topleft.x.v - reimu_chargeshot_p->x[0].v <= REIMU_CHARGE_HIT_MARGIN &&
           reimu_chargeshot_p->y[0].v - hitbox.bottom.v <= REIMU_CHARGE_HIT_MARGIN &&
           hitbox.origin.topleft.y.v - reimu_chargeshot_p->y[0].v <= REIMU_CHARGE_HIT_MARGIN) {
            hitcircles_enemy_add(reimu_chargeshot_p->x[0].v,
                reimu_chargeshot_p->y[0].v, hitbox.pid);
            return 1;
        }
    }
    return 0;
}
void far pascal chargeshot_render_reimu(void)
{
    reimu_chargeshot_p = &reimu_chargeshots[pid_current][0];
    sprite16_clip_set_for_pid(pid_current);
    sprite16_put_size.set(REIMU_CHARGE_RENDER_SPRITE_WIDTH, REIMU_CHARGE_RENDER_SPRITE_HEIGHT);
    // Full 12-slot real GRCG mono-and-color sprite loop, retaining
    // the original DX=0 hardware service after the third mono cel.
    for(int i = 0; i < REIMU_CHARGE_SLOTS_PER_PLAYER; ++i, ++reimu_chargeshot_p) {
        if(reimu_chargeshot_p->state == REIMU_SHOT_INACTIVE) {
            continue;
        }
        sprite16_mono_(true);
        sprite16_mono_color_(2);
        reimu_chargeshot_sprite_put(reimu_chargeshot_p->x[REIMU_CHARGE_LAST_SAMPLE].v, reimu_chargeshot_p->y[REIMU_CHARGE_LAST_SAMPLE].v, 3);
        sprite16_mono_color_(5);
        reimu_chargeshot_sprite_put(reimu_chargeshot_p->x[4].v, reimu_chargeshot_p->y[4].v, 2);
        sprite16_mono_color_(6);
        reimu_chargeshot_sprite_put(reimu_chargeshot_p->x[2].v, reimu_chargeshot_p->y[2].v, 1);
        // Real SPRITE16 service boundary: DX=0 disables monochrome mode.
        // Maintained Kana renderer uses the same symbolic DX-zero idiom.
        asm xor dx, dx;
        _AH = SPRITE16_SET_MONO;
        geninterrupt(SPRITE16);
        reimu_chargeshot_sprite_put(reimu_chargeshot_p->x[0].v, reimu_chargeshot_p->y[0].v, 0);
    }
}
void near pascal gauge_pattern_reimu(bullet_type_t type)
{
    unsigned char pid_other;
    unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
    if(type == BT_BULLET16_DEFAULT) {
        flag_expected = flag_expected + GBAF_PELLET_TO_BULLET;
    }
    if(gba_flag_active[pid_current] == flag_expected) {
        reimu_gauge_frame[pid_current] = 0;
        gba_flag_active[pid_current]++;
        gauge_pattern_timing[pid_current].total_frames = gba_gauge_level[pid_current] + REIMU_GAUGE_INIT_TICKS;
        gauge_pattern_timing[pid_current].byte_1 = REIMU_GAUGE_INIT_TICKS - gba_gauge_level[pid_current];
        return; // Internal RET 2 at 14EB0, not a separate routine.
    }
    if(gba_flag_active[pid_current] != flag_expected + 1) {
        return;
    }
    bullet_template.type = type;
    bullet_template.center.y.v = TO_SP(8);
    pid_other = 1 - pid_current;
    bullet_template.pid = pid_other;
    bullet_template.speed.v = TO_SP(2);
    bullet_template.angle = 0;
    // Separate byte Gauge phase accepts a natural zero-remainder test
    // without changing the original RNG/paired-spawn code (af911g).
    if(!(reimu_gauge_frame[pid_current] % gauge_pattern_timing[pid_current].byte_1)) {
        bullet_template.group = BG_5_SPREAD_MEDIUM_AIMED;
        bullet_template.center.x.v = TO_SP(32);
        bomb_center_add(TO_SP(32), TO_SP(8), pid_other);
        bullets_add();
        bullet_template.center.x.v = TO_SP(256);
        bomb_center_add(TO_SP(256), TO_SP(8), pid_other);
        bullets_add();
    }
    if((reimu_gauge_frame[pid_current] % REIMU_GAUGE_RING_PERIOD) == REIMU_GAUGE_RING_PHASE) {
        bullet_template.group = BG_RING;
        bullet_template.count = gauge_pattern_timing[pid_current].total_frames;
        bullet_template.speed.v = TO_SP(3) + 2;
        bullet_template.center.x.v = TO_SP(64);
        bomb_center_add(TO_SP(64), TO_SP(8), pid_other);
        bullets_add();
        bullet_template.center.x.v = TO_SP(PLAYFIELD_W - 64);
        bomb_center_add(TO_SP(PLAYFIELD_W - 64), TO_SP(8), pid_other);
        bullets_add();
    }
    if(reimu_gauge_frame[pid_current] > REIMU_GAUGE_FINISH_AFTER) {
        gba_flag_active[pid_current] = GBAF_NONE;
        palette_restore_for_pid(pid_other);
    }
    reimu_gauge_frame[pid_current]++;
}
void far gba_gauge_pattern_pellet_reimu(void)
{
    if(gba_flag_active[pid_current] != GBAF_NONE) {
        gauge_pattern_reimu(BT_PELLET);
    }
}
void far gba_gauge_pattern_bullet_reimu(void)
{
    if(gba_flag_active[pid_current] != GBAF_NONE) {
        gauge_pattern_reimu(BT_BULLET16_DEFAULT);
    }
}
