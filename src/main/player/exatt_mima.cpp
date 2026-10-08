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

struct exatt_entity_t {
    unsigned char state;
    unsigned char frame;
    int x;
    int y;
    int velocity_x;
    int velocity_y;
    int target_x;
    int boundary_x;
    int duration;
    unsigned char pid;
    unsigned char unknown_11;
    unsigned char angle;
    unsigned char speed;
    int radius;
    unsigned char tail[10];
};
typedef char exatt_entity_size_must_be_20[(sizeof(exatt_entity_t) == 0x20) ? 1 : -1];

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

void far pascal exatt_add_mima(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;

    for(; i < 6; i++, p++) {
        if(p->state == 0) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y,
                randring_far_next16_mod(0x1200),
                randring_far_next16_mod(0x1200),
                pid_, 0x5A
            );
            p->duration = 0;
            p->frame = 3;
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

    if(p->state == 1) {
        sprite_offset = (pid.so_attack + 0x280);
        if(p->frame == 0) {
            sprite_offset += 0x786;
        } else if(p->frame == 1) {
            sprite_offset += 0x780;
        } else if(p->frame == 2) {
            sprite_offset += 6;
        }
        sprite16_put((left - 24), (top - 24), sprite_offset);
        return;
    }
    if(p->state == 2) {
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
    collmap_stripe_tile_w.set(16);
    collmap_tile_h.set(16);
    collmap_pid = pid_other;
    i = 0;

    for(; i < 6; i++, p++) {
        if(p->state == 0) {
            continue;
        }

        if(p->state == 1) {
            center_x = p->x + p->velocity_x;
            center_y = p->y + p->velocity_y;
            if((center_x <= 0) || (center_x >= TO_SP(PLAYFIELD_W))) {
                if(p->frame == 0) {
                    p->state = 0;
                    continue;
                }
                p->frame--;
                p->velocity_x = -p->velocity_x;
                p->angle = iatan2(p->velocity_y, p->velocity_x);
            } else if((center_y <= 0) || (center_y >= TO_SP(PLAYFIELD_H))) {
                if(p->frame != 0) {
                    p->frame--;
                    p->velocity_y = -p->velocity_y;
                    p->angle = iatan2(p->velocity_y, p->velocity_x);
                } else {
                    p->state = 0;
                    continue;
                }
            } else {
                p->x = center_x;
                p->y = center_y;
            }

            duration = p->duration;
            if(duration >= 0x10) {
                if(duration < 0x20) {
                    p->speed += (duration & 1);
                } else if(duration < 0x50) {
                    p->speed++;
                }
            }

            if(duration < 0x50) {
                vector2(p->velocity_x, p->velocity_y, p->angle, p->speed);
            }

            hitbox_hittest_skip_explosions = true;
            hitbox.radius.x.v = TO_SP(16);
            hitbox.radius.y.v = TO_SP(16);
            hitbox.pid = pid_other;
            hitbox.origin.center.x.v = center_x;
            hitbox.origin.center.y.v = center_y;
            if(hitbox_hittest() != 0) {
                p->velocity_y -= 8;
            }
            hitbox_hittest_skip_explosions = false;

            collmap_center.x.v = center_x;
            collmap_center.y.v = center_y;
            collmap_set_rect_striped();
        } else if(p->state == 2) {
            exatt_entity_p = p;
            if(exatt_fly_update() != 0) {
                p->angle = (unsigned char)randring_far_next16();
                p->speed = 0;
                p->velocity_x = 0;
                p->velocity_y = 0;
                continue;
            }
        } else if(p->state <= 0x1C) {
            p->state++;
        } else {
            p->duration = 0;
            p->state = 1;
            snd_se_play(10);
        }
        p->duration++;
    }
}

void far pascal exatt_render_mima(void)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;

    for(; i < 6; i++, p++) {
        if(p->state != 0) {
            exatt_entity_p = p;
            mima_exatt_render_one();
        }
    }
}
