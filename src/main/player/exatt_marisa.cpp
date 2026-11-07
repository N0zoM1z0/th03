// Complete native-source C++ for the original Marisa Extra Attack
// physical owner in TH03 P_EXATT_TEXT. Its 32-byte entity records
// and shared flight/render helpers remain in their historical slots.
#pragma codeseg P_EXATT_TEXT
#include "src/main/player/exatt_marisa.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"
#pragma option -a2

// All characters use the same 32-byte entity pool; +0x11 is per-character.
#include "src/main/player/exatt_entity.hpp"
extern exatt_entity_t exatt_entities[PLAYER_COUNT][16];
extern exatt_entity_t near *exatt_entity_p;
extern "C" void near pascal exatt_fly_init(
    int x, int y, int target_x, int target_y, unsigned char pid, int speed
);
extern "C" unsigned char near cdecl exatt_fly_update(void);
extern "C" void near pascal exatt_render_state2(
    screen_x_t left, screen_y_t top, unsigned char frame
);
extern "C" void near pascal exatt_render_state_other(
    screen_x_t left, screen_y_t top, unsigned char frame
);
extern "C" void far pascal bomb_center_add(int x, int y, int pid);

// Fourteen original entity slots carry one mutable byte state and distinct
// beam/sprite phase clocks; do not merge their frame increments or RNG calls.
enum marisa_exatt_phases_t {
    MARISA_EXTRA_SLOTS = 14,
    MARISA_EXTRA_FREE = 0,
    MARISA_EXTRA_BEAM = 1,
    MARISA_EXTRA_FLYING = 2,
    MARISA_EXTRA_APPEARING = 3,
    MARISA_EXTRA_SHRINK_BEGIN = 0x30,
    MARISA_EXTRA_SECOND_CEL = 0x60,
    MARISA_EXTRA_THIRD_CEL = 0x66,
    MARISA_EXTRA_FOURTH_CEL = 0x6C,
    MARISA_EXTRA_FIFTH_CEL = 0x72,
    MARISA_EXTRA_BEAM_COLLISION_END = 0x64,
    MARISA_EXTRA_BEAM_END = 0x78,
    MARISA_EXTRA_APPEARING_END = 0x1C,
    MARISA_EXTRA_TARGET_X_RANGE = 0x1200,
    MARISA_EXTRA_START_SPEED = 0x6E,
    MARISA_EXTRA_BEAM_Y_END = 0x1700,
    MARISA_EXTRA_BEAM_RISE_STEP = 0x100,
    MARISA_EXTRA_BEAM_MIN_Y = -0x100,
    MARISA_EXTRA_BEAM_COLLISION_STRIPE = 4,
    MARISA_EXTRA_BEAM_HEIGHT_DIVISOR = 32,
    MARISA_EXTRA_SPAWN_WARNING_Y = 0x1820,
};

void far pascal exatt_add_marisa(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;
    // Natural C++ full fourteen-slot allocator; each occupied slot
    // advances both the signed index and near pointer (af885a).
    while(i < MARISA_EXTRA_SLOTS) {
        if(!p->state) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y, randring_far_next16_mod(MARISA_EXTRA_TARGET_X_RANGE),
                TO_SP(PLAYFIELD_H), pid_, MARISA_EXTRA_START_SPEED
            );
            return;
        }
        ++i;
        p++;
    }
}

void far pascal marisa_exatt_add(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[1 - pid_][0];
    register int i = 0;
    while(i < MARISA_EXTRA_SLOTS) {
        if(!p->state) {
            p->state = MARISA_EXTRA_APPEARING;
            p->frame = 0;
            p->x = x;
            p->y = y;
            p->pid = pid_;
            return;
        }
        ++i;
        p++;
    }
}

void near marisa_exatt_render_one(void)
{
    screen_x_t left;
    screen_y_t top;
    unsigned char frame;
    register exatt_entity_t near *p = exatt_entity_p;
    register sprite16_offset_t sprite_offset;

    left = playfield_fg_x_to_screen(p->x, p->pid);
    top = ((p->y >> 4) + 16);
    if(pid_current == 1) {
        sprite16_clip.set_for_pid_0();
    } else {
        sprite16_clip.set_for_pid_1();
    }
    if(p->state == MARISA_EXTRA_BEAM) {
        sprite16_put_size.set(16, 16);
        sprite_offset = (pid.so_attack + 0x1A);
        left -= 8;
        top -= 8;
        frame = p->frame;
        if(frame < MARISA_EXTRA_SHRINK_BEGIN) {
            sprite16_put(left, top, sprite_offset);
            sprite_offset += 2;
        } else if(frame < MARISA_EXTRA_SECOND_CEL) {
            sprite_offset += 2;
        } else if(frame < MARISA_EXTRA_THIRD_CEL) {
            sprite_offset += 4;
        } else if(frame < MARISA_EXTRA_FOURTH_CEL) {
            sprite_offset += 6;
        } else if(frame < MARISA_EXTRA_FIFTH_CEL) {
            sprite_offset += 8;
        } else {
            sprite_offset += 10;
        }
        sprite16_putx(left, top + 16, sprite_offset, SPF_DOWNWARDS_COLUMN);
    } else if(p->state == MARISA_EXTRA_FLYING) {
        exatt_render_state2(left, top, *(unsigned int near *)&p->frame);
    } else {
        exatt_render_state_other(left, top, *(unsigned int near *)p);
    }
}

void far pascal exatt_update_marisa(void)
{
    int i;
    int height;
    int center_x;
    register exatt_entity_t near *p;
    register int bottom;

    collmap_stripe_tile_w.set(MARISA_EXTRA_BEAM_COLLISION_STRIPE);
    p = &exatt_entities[pid_current][0];
    i = 0;
    // This substantial update has THREE separate `continue` paths,
    // each advancing both registers before the next slot (af885c).
    while(i < MARISA_EXTRA_SLOTS) {
        if(!p->state) {
            ++i;
            p++;
            continue;
        }
        if(p->state == MARISA_EXTRA_BEAM) {
            if(p->frame < MARISA_EXTRA_SHRINK_BEGIN) {
                p->y -= MARISA_EXTRA_BEAM_RISE_STEP;
                if(p->y < MARISA_EXTRA_BEAM_MIN_Y) {
                    p->frame = MARISA_EXTRA_SHRINK_BEGIN;
                    p->y = MARISA_EXTRA_BEAM_MIN_Y;
                }
            } else if(p->frame >= MARISA_EXTRA_BEAM_END) {
                p->state = MARISA_EXTRA_FREE;
                ++i;
                p++;
                continue;
            }
            center_x = p->x;
            bottom = p->y;
            if(bottom < 0) {
                bottom = 0;
            }
            height = MARISA_EXTRA_BEAM_Y_END - bottom;
            if(p->frame < MARISA_EXTRA_BEAM_COLLISION_END) {
                collmap_center.x.v = center_x;
                collmap_center.y.v = bottom + (height / 2);
                // Signed collision height truncates toward zero;
                // >>5 changes original CODE and negative rounding
                // (independent native negative af885d).
                collmap_tile_h.v = height / MARISA_EXTRA_BEAM_HEIGHT_DIVISOR;
                collmap_pid = (1 - pid_current);
                collmap_set_rect_striped();
            }
        } else if(p->state == MARISA_EXTRA_FLYING) {
            exatt_entity_p = p;
            if(exatt_fly_update()) {
                p->y = MARISA_EXTRA_BEAM_Y_END;
                ++i;
                p++;
                continue;
            }
        } else if(p->state <= MARISA_EXTRA_APPEARING_END) {
            p->state++;
            if(p->state == 0x0C) {
                bomb_center_add(p->x, MARISA_EXTRA_SPAWN_WARNING_Y, p->pid);
            }
        } else {
            p->frame = 0;
            p->state = MARISA_EXTRA_BEAM;
            snd_se_play(20);
        }
        // Keep byte-memory postfix: prefix changed complete CODE
        // in fresh negative af885e, independently of older evidence.
        p->frame++;
        ++i;
        p++;
    }
}

void far pascal exatt_render_marisa(void)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    // Every physical slot is visited, native-exact with the original
    // post-render near pointer and signed index mutations (af885b).
    while(i < MARISA_EXTRA_SLOTS) {
        if(p->state) {
            exatt_entity_p = p;
            marisa_exatt_render_one();
        }
        ++i;
        p++;
    }
}
