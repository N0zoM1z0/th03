// Complete original Reimu Chargeshot and Gauge physical source.
// The native source/code/whole-link proof is distinct from canonical
// packed-game acceptance; see docs/MAIN_REIMU_CHARGESHOT_STATES_AFTER826_REVIEW.md.
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
    for(int i = 0; i < REIMU_CHARGE_TOTAL_SLOTS; i++, reimu_chargeshot_p++) {
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
    for(i = 0; i < REIMU_CHARGE_STANDARD_LAUNCH; i++, reimu_chargeshot_p++) {
        reimu_chargeshot_p->state = REIMU_SHOT_SLOWING;
        reimu_chargeshot_p->frame = 0;
        for(j = 0; j < REIMU_CHARGE_HISTORY_SAMPLES; j++) {
            reimu_chargeshot_p->x[j].v = center_x.v;
            reimu_chargeshot_p->y[j].v = center_y.v;
        }
        reimu_chargeshot_p->angle = angle;
        // The literal 0x20 reuses AL after the previous byte-angle store.
        // An enum-valued 0x20 emits a different TC4 direct-memory ADD
        // (native failed stage af826c); retain the original expression.
        angle += 0x20;
        reimu_chargeshot_p->speed = REIMU_CHARGE_LAUNCH_SPEED;
    }
    reimu_chargeshot_alternate_hit_frame = 1;
}
void far pascal reimu_hyper_shot_add(Subpixel center_x, Subpixel center_y)
{
    reimu_chargeshot_p = &reimu_chargeshots[pid.current][0];
    for(int i = 0; i < REIMU_CHARGE_SLOTS_PER_PLAYER; i++, reimu_chargeshot_p++) {
        if(reimu_chargeshot_p->state != REIMU_SHOT_INACTIVE) {
            continue;
        }
        reimu_chargeshot_p->state = REIMU_SHOT_HOMING;
        reimu_chargeshot_p->frame = 0;
        for(int j = 0; j < REIMU_CHARGE_HISTORY_SAMPLES; j++) {
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
    playfield_clip_negative_radius.x.v = -TO_SP(24);
    playfield_clip_negative_radius.y.v = -TO_SP(24);
    for(int i = 0; i < REIMU_CHARGE_SLOTS_PER_PLAYER; i++, reimu_chargeshot_p++) {
        if(reimu_chargeshot_p->state != REIMU_SHOT_INACTIVE) {
            players[pid_current].gauge_charged = 0;
            for(int j = REIMU_CHARGE_LAST_SAMPLE; j > 0; j--) {
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
    x = playfield_fg_x_to_screen(x, pid_current) - 24;
    y = (y >> 4) - 8;
    sprite16_put(x, y, sprite_offset);
}
uint8_t far chargeshot_hittest_reimu(void)
{
    if(reimu_chargeshot_alternate_hit_frame && (round_or_result_frame % 2)) {
        return 0;
    }
    reimu_chargeshot_p = &reimu_chargeshots[hitbox.pid][0];
    // Target really scans six slots, despite twelve updated/rendered slots.
    for(int i = 0; i < REIMU_CHARGE_HITTEST_SLOTS; i++, reimu_chargeshot_p++) {
        if(reimu_chargeshot_p->state == REIMU_SHOT_INACTIVE) {
            continue;
        }
        if(reimu_chargeshot_p->x[0].v <= -TO_SP(16) ||
           reimu_chargeshot_p->x[0].v >= TO_SP(PLAYFIELD_W) ||
           reimu_chargeshot_p->y[0].v <= -TO_SP(16)) {
            continue;
        }
        if(reimu_chargeshot_p->x[0].v - hitbox.right.v <= TO_SP(20) &&
           hitbox.origin.topleft.x.v - reimu_chargeshot_p->x[0].v <= TO_SP(20) &&
           reimu_chargeshot_p->y[0].v - hitbox.bottom.v <= TO_SP(20) &&
           hitbox.origin.topleft.y.v - reimu_chargeshot_p->y[0].v <= TO_SP(20)) {
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
    sprite16_put_size.set(48, 48);
    for(int i = 0; i < REIMU_CHARGE_SLOTS_PER_PLAYER; i++, reimu_chargeshot_p++) {
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
    if((reimu_gauge_frame[pid_current] % gauge_pattern_timing[pid_current].byte_1) == 0) {
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
