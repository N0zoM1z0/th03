// Natural Turbo C++ reconstruction of the complete 676-byte Marisa Extra
// Attack CODE owner in TH03 P_EXATT_TEXT. Historical 32-byte entity
// storage and shared flight/render helpers remain separately owned.
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

struct exatt_entity_t {
    unsigned char state, frame;
    int x, y, velocity_x, velocity_y, target_x, boundary_x, duration;
    unsigned char pid, unused_11, angle, speed;
    int radius;
    unsigned char tail[10];
};
typedef char exatt_entity_size_is_32[(sizeof(exatt_entity_t)==32)?1:-1];
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

void far pascal exatt_add_marisa(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;
    for(; i < 14; i++, p++) {
        if(p->state == 0) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y, randring_far_next16_mod(0x1200),
                TO_SP(PLAYFIELD_H), pid_, 0x6E
            );
            return;
        }
    }
}

void far pascal marisa_exatt_add(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[1 - pid_][0];
    register int i = 0;
    for(; i < 14; i++, p++) {
        if(p->state == 0) {
            p->state = 3;
            p->frame = 0;
            p->x = x;
            p->y = y;
            p->pid = pid_;
            return;
        }
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
    if(p->state == 1) {
        sprite16_put_size.set(16, 16);
        sprite_offset = (pid.so_attack + 0x1A);
        left -= 8;
        top -= 8;
        frame = p->frame;
        if(frame < 0x30) {
            sprite16_put(left, top, sprite_offset);
            sprite_offset += 2;
        } else if(frame < 0x60) {
            sprite_offset += 2;
        } else if(frame < 0x66) {
            sprite_offset += 4;
        } else if(frame < 0x6C) {
            sprite_offset += 6;
        } else if(frame < 0x72) {
            sprite_offset += 8;
        } else {
            sprite_offset += 10;
        }
        sprite16_putx(left, top + 16, sprite_offset, SPF_DOWNWARDS_COLUMN);
    } else if(p->state == 2) {
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

    collmap_stripe_tile_w.set(4);
    p = &exatt_entities[pid_current][0];
    i = 0;
    for(; i < 14; i++, p++) {
        if(p->state == 0) {
            continue;
        }
        if(p->state == 1) {
            if(p->frame < 0x30) {
                p->y -= 0x100;
                if(p->y < -0x100) {
                    p->frame = 0x30;
                    p->y = -0x100;
                }
            } else if(p->frame >= 0x78) {
                p->state = 0;
                continue;
            }
            center_x = p->x;
            bottom = p->y;
            if(bottom < 0) {
                bottom = 0;
            }
            height = 0x1700 - bottom;
            if(p->frame < 0x64) {
                collmap_center.x.v = center_x;
                collmap_center.y.v = bottom + (height / 2);
                collmap_tile_h.v = height / 32;
                collmap_pid = (1 - pid_current);
                collmap_set_rect_striped();
            }
        } else if(p->state == 2) {
            exatt_entity_p = p;
            if(exatt_fly_update() != 0) {
                p->y = 0x1700;
                continue;
            }
        } else if(p->state <= 0x1C) {
            p->state++;
            if(p->state == 0x0C) {
                bomb_center_add(p->x, 0x1820, p->pid);
            }
        } else {
            p->frame = 0;
            p->state = 1;
            snd_se_play(20);
        }
        p->frame++;
    }
}

void far pascal exatt_render_marisa(void)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    for(; i < 14; i++, p++) {
        if(p->state != 0) {
            exatt_entity_p = p;
            marisa_exatt_render_one();
        }
    }
}
