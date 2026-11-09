// Complete current-source native TC4 reconstruction for Ellen's entire
// original Extra Attack P_EXATT_TEXT owner. The 30-byte trailing-history slots and each
// referenced 32-byte entity stay in historical DGROUP. The slot initializer
// precedes the other five functions in this native compiler producer.
#pragma codeseg P_EXATT_TEXT

#include "src/main/player/exatt_ellen.hpp"
#include "src/main/math/polar.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"

#pragma option -a2

// Ellen interprets byte +0x11 as a signed spin step.
#include "src/main/player/exatt_entity.hpp"

// Original trailing-history storage is a near pointer followed by two
// seven-word coordinate sequences, 30 bytes per physical slot.
enum ellen_exatt_limits_t {
    ELLEN_EXATT_SLOTS = 12,
    ELLEN_HISTORY_SAMPLES = 7,
    ELLEN_HISTORY_LAST = ELLEN_HISTORY_SAMPLES - 1,
    ELLEN_HISTORY_RENDER_STEP = 2,
    ELLEN_EXPAND_RADIUS_LIMIT = 0xD00,
    ELLEN_RADIUS_GROWTH = 0x18,
    ELLEN_APPEARING_END = 0x1C,
    ELLEN_FLYING_STATE = 2,
    ELLEN_RANDOM_TARGET_X_RANGE = 0x0C80,
    ELLEN_RANDOM_TARGET_X_BIAS = 0x2C0,
    ELLEN_RANDOM_TARGET_Y_RANGE = 0x0C80,
    ELLEN_RANDOM_TARGET_Y_BIAS = 0x500,
    ELLEN_FLY_INITIAL_SPEED = 0x46,
    ELLEN_TRAIL_SPRITE_WIDTH = 32,
    ELLEN_TRAIL_SPRITE_HEIGHT = 32,
    ELLEN_HITTEST_MARGIN = TO_SP(16),
    ELLEN_CLIP_MARGIN = TO_SP(24),
    ELLEN_COLLMAP_STRIPE_TILES = 12,
    ELLEN_ACTIVE_SOUND = 10,
};

// The original two-player Extra Attack follows a byte-valued state
// machine; global trailing history and the seven positions stay in place.
enum ellen_exatt_state_t {
    ELLEN_EXATT_FREE = 0,
    ELLEN_EXATT_ACTIVE = 1,
};

struct ellen_exatt_slot_t {
    exatt_entity_t near *entity;
    int history_x[ELLEN_HISTORY_SAMPLES];
    int history_y[ELLEN_HISTORY_SAMPLES];
};
typedef char ellen_exatt_slot_size_is_30[(sizeof(ellen_exatt_slot_t) == 30)?1:-1];
typedef char ellen_history_x_at_02[
    (offsetof(ellen_exatt_slot_t, history_x) == 0x02) ? 1 : -1
];
typedef char ellen_history_y_at_10[
    (offsetof(ellen_exatt_slot_t, history_y) == 0x10) ? 1 : -1
];

extern ellen_exatt_slot_t ellen_exatt_slots[PLAYER_COUNT][12];
extern ellen_exatt_slot_t near *ellen_exatt_slot_p;
extern exatt_entity_t near *exatt_entity_p;
extern exatt_entity_t exatt_entities[PLAYER_COUNT][16];
extern "C" unsigned char near cdecl exatt_fly_update(void);
extern "C" void near pascal exatt_fly_init(
    int x, int y, int target_x, int target_y,
    unsigned char pid, int speed
);
extern "C" void near pascal exatt_render_state2(
    screen_x_t left, screen_y_t top, unsigned char frame
);
extern "C" void near pascal exatt_render_state_other(
    screen_x_t left, screen_y_t top, unsigned char frame
);

void near ellen_exatt_render_one(void);

void far pascal exatt_ellen_slots_init(void)
{
    register ellen_exatt_slot_t near *p0 = &ellen_exatt_slots[0][0];
    register ellen_exatt_slot_t near *p1 = &ellen_exatt_slots[1][0];
    // Original paired 12-slot initializer; both pointers advance only
    // after both history records receive the physical entity link.
    for(register int i = 0; i < ELLEN_EXATT_SLOTS; ++i, ++p0, ++p1) {
        p0->entity = &exatt_entities[0][i];
        p1->entity = &exatt_entities[1][i];
    }
}

void far pascal exatt_add_ellen(int x, int y, unsigned char pid_)
{
    int target_x;
    int target_y;
    unsigned char added;
    signed char spin;
    unsigned char angle;
    added = 0;
    target_x = randring_far_next16_mod(ELLEN_RANDOM_TARGET_X_RANGE) + ELLEN_RANDOM_TARGET_X_BIAS;
    target_y = randring_far_next16_mod(ELLEN_RANDOM_TARGET_Y_RANGE) + ELLEN_RANDOM_TARGET_Y_BIAS;
    spin = (randring_far_next16_and(1) == 0) ? -1 : 1;
    angle = (unsigned char)randring_far_next16();

    ellen_exatt_slot_p = &ellen_exatt_slots[pid_][0];
    for(register int i = 0; i < ELLEN_EXATT_SLOTS; ++i, ++ellen_exatt_slot_p) {
        if(ellen_exatt_slot_p->entity->state) {
            continue;
        }
        exatt_entity_p = ellen_exatt_slot_p->entity;
        exatt_fly_init(x, y, target_x, target_y, pid_, ELLEN_FLY_INITIAL_SPEED);
        exatt_entity_p->radius = 0;
        exatt_entity_p->character_mode.ellen_spin_delta = spin;
        if(!added) {
            exatt_entity_p->angle = angle;
            // The mutable byte uses original postfix codegen: prefix
            // ++added changes TC4's full physical object (af746b).
            added++;
        } else {
            exatt_entity_p->angle = angle + 0x80;
            return;
        }
    }
}

void far pascal ellen_extra_add(int x, int y, unsigned char angle_, unsigned char mode)
{
    ellen_exatt_slot_p = &ellen_exatt_slots[pid_current][0];
    for(int i = 0; i < ELLEN_EXATT_SLOTS; ++i, ++ellen_exatt_slot_p) {
        if(ellen_exatt_slot_p->entity->state) {
            continue;
        }
        register exatt_entity_t near *p = ellen_exatt_slot_p->entity;
        p->state = ELLEN_EXATT_ACTIVE;
        p->frame = 0;
        p->x = x;
        p->y = y;
        p->radius = 0;
        p->character_mode.ellen_spin_delta = mode;
        p->angle = angle_;
        p->pid = (1 - pid_current);
        return;
    }
}

void near ellen_exatt_render_one(void)
{
    screen_x_t left;
    screen_y_t top;
    screen_y_t trail_top;
    screen_x_t trail_left;
    unsigned char frame;

    left = playfield_fg_x_to_screen(
        ellen_exatt_slot_p->entity->x,
        ellen_exatt_slot_p->entity->pid
    );
    top = ((ellen_exatt_slot_p->entity->y >> 4) + 16);
    if(!ellen_exatt_slot_p->entity->pid) {
        sprite16_clip.set_for_pid_0();
    } else {
        sprite16_clip.set_for_pid_1();
    }
    frame = ellen_exatt_slot_p->entity->frame;

    if(ellen_exatt_slot_p->entity->state == ELLEN_EXATT_ACTIVE) {
        sprite16_put_size.set(ELLEN_TRAIL_SPRITE_WIDTH, ELLEN_TRAIL_SPRITE_HEIGHT);
        register sprite16_offset_t sprite_offset = pid.so_attack + 0x28C;
        // Active spiral draws history samples 6, 4, 2, 0, in reverse.
        // The signed index advances in the loop header after each sprite.
        for(register int i = ELLEN_HISTORY_LAST; i >= 0; i -= ELLEN_HISTORY_RENDER_STEP) {
            trail_left = playfield_fg_x_to_screen(
                ellen_exatt_slot_p->history_x[i],
                ellen_exatt_slot_p->entity->pid
            );
            trail_top = ((ellen_exatt_slot_p->history_y[i] >> 4) + 16);
            sprite16_put(trail_left - 16, trail_top - 16, sprite_offset);
            sprite_offset -= 4;
        }
    } else if(ellen_exatt_slot_p->entity->state == ELLEN_FLYING_STATE) {
        exatt_render_state2(left, top, frame);
    } else {
        exatt_render_state_other(
            left, top, *(unsigned int near *)&ellen_exatt_slot_p->entity->state
        );
    }
}

void far pascal exatt_update_ellen(void)
{
    int i;
    int j;
    register ellen_exatt_slot_t near *slot = &ellen_exatt_slots[pid_current][0];

    unsigned char pid_other = (1 - pid_current);
    playfield_clip_negative_radius.x.v = -ELLEN_CLIP_MARGIN;
    playfield_clip_negative_radius.y.v = -ELLEN_CLIP_MARGIN;
    collmap_stripe_tile_w.set(ELLEN_COLLMAP_STRIPE_TILES);
    collmap_tile_h.set(ELLEN_COLLMAP_STRIPE_TILES);
    collmap_pid = pid_other;
    i = 0;

    for(; i < ELLEN_EXATT_SLOTS; ++i, ++slot) {
        if(!slot->entity->state) {
            continue;
        }
        if(slot->entity->state == ELLEN_EXATT_ACTIVE) {
            // Shift history 6..1 BACKWARDS before computing sample zero.
            for(j = ELLEN_HISTORY_LAST; j > 0; --j) {
                slot->history_x[j] = slot->history_x[j - 1];
                slot->history_y[j] = slot->history_y[j - 1];
            }
            if(slot->entity->radius <= ELLEN_EXPAND_RADIUS_LIMIT) {
                slot->history_x[0] = polar(
                    slot->entity->x, slot->entity->radius,
                    CosTable8[slot->entity->angle]
                );
                slot->history_y[0] = polar(
                    slot->entity->y, slot->entity->radius,
                    SinTable8[slot->entity->angle]
                );
                slot->entity->velocity_x = slot->history_x[0] - slot->history_x[1];
                slot->entity->velocity_y = slot->history_y[0] - slot->history_y[1];
                slot->entity->radius += ELLEN_RADIUS_GROWTH;
                slot->entity->angle += slot->entity->character_mode.ellen_spin_delta;
            } else {
                if(
                    playfield_clip(
                        *(PlayfieldSubpixel near *)&slot->history_x[0],
                        *(PlayfieldSubpixel near *)&slot->history_y[0]
                    ) &&
                    playfield_clip(
                        *(PlayfieldSubpixel near *)&slot->history_x[ELLEN_HISTORY_LAST],
                        *(PlayfieldSubpixel near *)&slot->history_y[ELLEN_HISTORY_LAST]
                    )
                ) {
                    slot->entity->state = ELLEN_EXATT_FREE;
                    continue;
                }
                slot->history_x[0] += slot->entity->velocity_x;
                slot->history_y[0] += slot->entity->velocity_y;
            }
            hitbox_hittest_skip_explosions = true;
            hitbox.radius.x.v = ELLEN_HITTEST_MARGIN;
            hitbox.radius.y.v = ELLEN_HITTEST_MARGIN;
            hitbox.pid = pid_other;
            hitbox.origin.center.x.v = slot->history_x[0];
            hitbox.origin.center.y.v = slot->history_y[0];
            hitbox_hittest();
            hitbox_hittest_skip_explosions = false;

            collmap_center.x.v = slot->history_x[0];
            collmap_center.y.v = slot->history_y[0];
            collmap_set_rect_striped();
        } else if(slot->entity->state == ELLEN_FLYING_STATE) {
            exatt_entity_p = slot->entity;
            if(exatt_fly_update()) {
                // On arrival initialize all seven history samples,
                // not only the four visible spiral sprites.
                for(j = 0; j < ELLEN_HISTORY_SAMPLES; ++j) {
                    slot->history_x[j] = exatt_entity_p->x;
                    slot->history_y[j] = exatt_entity_p->y;
                }
            }
        } else if(slot->entity->state <= ELLEN_APPEARING_END) {
            slot->entity->state++;
        } else {
            slot->entity->frame = 0;
            slot->entity->state = ELLEN_EXATT_ACTIVE;
            snd_se_play(ELLEN_ACTIVE_SOUND);
        }
        // Keep original byte postfix; prefix changed original
        // TC4 CODE in fresh negative control af873f.
        slot->entity->frame++;
    }
}


void far pascal exatt_render_ellen(void)
{
    register ellen_exatt_slot_t near *p = &ellen_exatt_slots[pid_current][0];
    // Every real render call preserves per-slot post-call pointer order.
    for(register int i = 0; i < ELLEN_EXATT_SLOTS; ++i, ++p) {
        if(p->entity->state) {
            ellen_exatt_slot_p = p;
            ellen_exatt_render_one();
        }
    }
}
