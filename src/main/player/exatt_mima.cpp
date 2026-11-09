// Natural Turbo C++ source for the complete Mima Extra Attack CODE owner
// in TH03 MAIN_06_TEXT. Its original 727-byte extent is reproduced by a
// compiler-generated object in the repository-local two-round Oracle.
// Historical entity DATA/BSS remains owned by the frozen carrier; this
// source does not claim the original physical producer of that state.
#pragma codeseg MAIN_06_TEXT

#include "src/main/player/exatt_mima.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"

#pragma option -a2

// The same 32-byte live entity view used by the shared flight/Reimu code.
#include "src/main/player/exatt_entity.hpp"

extern exatt_entity_t exatt_entities[PLAYER_COUNT][16];
extern exatt_entity_t near *exatt_entity_p;

extern "C" unsigned char near cdecl exatt_fly_update(void);
extern "C" void near pascal exatt_fly_init(
    int x, int y, int target_x, int target_y, unsigned char pid, int speed
);
extern "C" void near pascal exatt_render_state2(
    screen_x_t left, screen_y_t top, unsigned char frame
);
extern "C" void near pascal exatt_render_state_other(
    screen_x_t left, screen_y_t top, unsigned int state_and_frame
);

// Each retained entity is exactly 32 bytes in the original 16-bit ABI;
// do not change the two-player × 16-slot allocation while this attack
// traverses only its first six slots per player.
typedef char mima_exatt_original_entity_stride[
    (sizeof(exatt_entity_t) == 32) ? 1 : -1
];

// The physical Mima Extra Attack uses six slots per player. Its
// elapsed duration is read as an int in the full motion and collision
// update, but the parity test must preserve its unsigned 16-bit bit.
enum mima_exatt_phase_t {
    MIMA_EXATT_SLOTS = 6,
    MIMA_EXATT_INITIAL_RENDER_FRAME = 3,
    MIMA_EXATT_START_ACCEL_FRAME = 0x10,
    MIMA_EXATT_PARITY_ACCEL_END = 0x20,
    MIMA_EXATT_LAST_ACCEL_FRAME = 0x50,
    MIMA_EXATT_FLYING_STATE = 2,
    MIMA_EXATT_APPEAR_END = 0x1C,
    MIMA_EXATT_FREE = 0,
    MIMA_EXATT_ACTIVE = 1,
    MIMA_EXATT_HALF_FRAME_COUNT = 2,
    MIMA_EXATT_RANDOM_TARGET_RANGE = 0x1200,
    MIMA_EXATT_INITIAL_SPEED = 0x5A,
    MIMA_EXATT_COLLISION_TILE_SPAN = 16,
    MIMA_EXATT_COLLISION_RADIUS = TO_SP(16),
    MIMA_EXATT_BOUNCE_RECOIL_SUBPIXELS = 8,
};

void far pascal exatt_add_mima(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];

    for(register int i = 0; i < MIMA_EXATT_SLOTS; ++i, ++p) {
        if(!p->state) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y,
                randring_far_next16_mod(MIMA_EXATT_RANDOM_TARGET_RANGE),
                randring_far_next16_mod(MIMA_EXATT_RANDOM_TARGET_RANGE),
                pid_, MIMA_EXATT_INITIAL_SPEED
            );
            p->duration = 0;
            p->frame = MIMA_EXATT_INITIAL_RENDER_FRAME;
            return;
        }
    }
}

void near mima_exatt_render_one(void)
{
    screen_x_t left;
    screen_x_t top;
    unsigned char phase;
    register exatt_entity_t near *p = exatt_entity_p;
    register sprite16_offset_t sprite_offset;

    left = playfield_fg_x_to_screen(p->x, p->pid);
    top = ((p->y >> 4) + 16);
    sprite16_put_size.set(48, 48);

    if(pid_current == 1) {
        sprite16_clip.set_for_pid_0();
    } else {
        sprite16_clip.set_for_pid_1();
    }
    phase = (unsigned char)p->duration;

    if(p->state == MIMA_EXATT_ACTIVE) {
        sprite_offset = (pid.so_attack + 0x280);
        if(!p->frame) {
            sprite_offset += 0x786;
        } else if(p->frame == 1) {
            sprite_offset += 0x780;
        } else if(p->frame == 2) {
            sprite_offset += 6;
        }
        sprite16_put((left - 24), (top - 24), sprite_offset);
        return;
    }
    if(p->state == MIMA_EXATT_FLYING_STATE) {
        exatt_render_state2(left, top, phase);
    } else {
        exatt_render_state_other(left, top, *(unsigned int near *)p);
    }
}

void far pascal exatt_update_mima(void)
{
    int i;
    int center_y;
    int duration;
    unsigned char pid_other;
    register int center_x;
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];

    pid_other = (1 - pid_current);
    collmap_stripe_tile_w.set(MIMA_EXATT_COLLISION_TILE_SPAN);
    collmap_tile_h.set(MIMA_EXATT_COLLISION_TILE_SPAN);
    collmap_pid = pid_other;
    i = 0;

    for(; i < MIMA_EXATT_SLOTS; ++i, ++p) {
        if(!p->state) {
            continue;
        }

        if(p->state == MIMA_EXATT_ACTIVE) {
            center_x = p->x + p->velocity_x;
            center_y = p->y + p->velocity_y;
            if((center_x <= 0) || (center_x >= TO_SP(PLAYFIELD_W))) {
                if(!p->frame) {
                    p->state = MIMA_EXATT_FREE;
                    continue;
                }
                p->frame--;
                // Preserve native signed unary negation: multiplication
                // by -1 failed previously (af770c), and even writing
                // `0 - p->velocity_x` failed fresh native CODE (af852d).
                p->velocity_x = -p->velocity_x;
                p->angle = iatan2(p->velocity_y, p->velocity_x);
            } else if((center_y <= 0) || (center_y >= TO_SP(PLAYFIELD_H))) {
                if(p->frame) {
                    p->frame--;
                    p->velocity_y = -p->velocity_y;
                    p->angle = iatan2(p->velocity_y, p->velocity_x);
                } else {
                    p->state = MIMA_EXATT_FREE;
                    continue;
                }
            } else {
                p->x = center_x;
                p->y = center_y;
            }

            duration = p->duration;
            if(duration >= MIMA_EXATT_START_ACCEL_FRAME) {
                if(duration < MIMA_EXATT_PARITY_ACCEL_END) {
                    // Although duration is a signed local, its original
                    // parity operation is a word-mask. Explicit unsigned
                    // C++ modulo emits the same instructions (af852a/c),
                    // while signed duration %2 changes CODE (af852b).
                    p->speed += (
                        static_cast<unsigned int>(duration) %
                        MIMA_EXATT_HALF_FRAME_COUNT
                    );
                } else if(duration < MIMA_EXATT_LAST_ACCEL_FRAME) {
                    p->speed++;
                }
            }

            if(duration < MIMA_EXATT_LAST_ACCEL_FRAME) {
                vector2(p->velocity_x, p->velocity_y, p->angle, p->speed);
            }

            hitbox_hittest_skip_explosions = true;
            hitbox.radius.x.v = MIMA_EXATT_COLLISION_RADIUS;
            hitbox.radius.y.v = MIMA_EXATT_COLLISION_RADIUS;
            hitbox.pid = pid_other;
            hitbox.origin.center.x.v = center_x;
            hitbox.origin.center.y.v = center_y;
            if(hitbox_hittest()) {
                p->velocity_y -= MIMA_EXATT_BOUNCE_RECOIL_SUBPIXELS;
            }
            hitbox_hittest_skip_explosions = false;

            collmap_center.x.v = center_x;
            collmap_center.y.v = center_y;
            collmap_set_rect_striped();
        } else if(p->state == MIMA_EXATT_FLYING_STATE) {
            exatt_entity_p = p;
            if(exatt_fly_update()) {
                p->angle = (unsigned char)randring_far_next16();
                p->speed = 0;
                p->velocity_x = 0;
                p->velocity_y = 0;
                continue;
            }
        } else if(p->state <= MIMA_EXATT_APPEAR_END) {
            p->state++;
        } else {
            p->duration = 0;
            p->state = MIMA_EXATT_ACTIVE;
            snd_se_play(10);
        }
        p->duration++;
    }
}

void far pascal exatt_render_mima(void)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];

    for(register int i = 0; i < MIMA_EXATT_SLOTS; ++i, ++p) {
        if(p->state) {
            exatt_entity_p = p;
            mima_exatt_render_one();
        }
    }
}
