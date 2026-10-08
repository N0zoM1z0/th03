// Natural Turbo C++ reconstruction of the complete Reimu Extra Attack CODE
// owner in TH03 MAIN_06_TEXT. Six functions precede update/render physically.
// TC4 emits two ordered OMF producers from this same semantic source so that
// the original MZ relocation order is preserved without raw instruction blobs.
// Shared render/collision helpers are independently target-reviewed; historical
// DATA/BSS ownership is outside this CODE-only acceptance.
#pragma codeseg MAIN_06_TEXT

#include "src/main/player/exatt_reimu.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/main/difficul.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/math/vector.hpp"
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

// One semantic owner has two consecutive physical compiler producers.
// Separate source sections preserve the target's OMF FIXUPP order without
// replacing any executable instruction with assembly byte carriers.
void near reimu_exatt_render_one(void);

#ifndef TH03_EXATT_REIMU_UPDATE_ONLY
void far pascal exatt_add_reimu(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;
    for(; i < 8; i++, p++) {
        if(p->state == 0) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y,
                randring_far_next16_mod(0x1200),
                randring_far_next16_and(0x7FF),
                pid_, 0x5A
            );
            return;
        }
    }
}

void far pascal reimu_extra_add(int x, int y, unsigned char angle_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    for(; i < 8; i++, p++) {
        if(p->state == 0) {
            p->state = 1;
            p->frame = 0;
            p->x = x;
            p->y = y;
            p->pid = (1 - pid_current);
            vector2(p->velocity_x, p->velocity_y, angle_, 0x50);
            return;
        }
    }
}

void near pascal exatt_render_state2(
    screen_x_t left, screen_y_t top, unsigned char frame
)
{
    register sprite16_offset_t sprite_offset;
    if((frame & 1) == 0) {
        sprite_offset = 0x1928;
        if((frame & 7) <= 3) {
            sprite_offset += 4;
        }
        sprite16_put_size.set(32, 32);
        sprite16_clip.reset();
        sprite16_put(left - 16, top - 16, sprite_offset);
    }
}

void near pascal exatt_render_state_other(
    screen_x_t left, screen_y_t top, unsigned char frame
)
{
    register sprite16_offset_t sprite_offset;
    sprite16_clip.reset();
    sprite16_put_size.set(48, 48);
    sprite_offset = 0x1930;
    sprite_offset += ((frame / 4) % 3) * 6;
    sprite16_put(left - 24, top - 24, sprite_offset);
}

void near reimu_exatt_render_one(void)
{
    screen_x_t left;
    screen_y_t top;
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

    if(p->state == 1) {
        sprite_offset = (pid.so_attack + 0x280);
        phase = (p->frame / 4);
        if((phase & 3) == 1) {
            sprite_offset += 6;
        } else if((phase & 3) != 0) {
            sprite_offset += (0x780 + ((phase & 1) * 6));
        }
        sprite16_put(left - 24, top - 24, sprite_offset);
        return;
    }
    if(p->state == 2) {
        exatt_render_state2(left, top, *(unsigned int near *)&p->frame);
    } else {
        exatt_render_state_other(left, top, *(unsigned int near *)&p->state);
    }
}

void near pascal exatt_collmap_set(int x, int y)
{
    collmap_center.x.v = x;
    collmap_center.y.v = y;
    collmap_stripe_tile_w.set(16);
    collmap_tile_h.set(32);
    collmap_pid = (1 - pid_current);
    collmap_set_rect_striped();

    collmap_center.x.v -= TO_SP(12);
    collmap_stripe_tile_w.set(8);
    collmap_tile_h.set(16);
    collmap_set_rect_striped();

    collmap_center.x.v += TO_SP(24);
    collmap_set_rect_striped();
}

#endif // !TH03_EXATT_REIMU_UPDATE_ONLY

#ifndef TH03_EXATT_REIMU_PREFIX_ONLY
void far pascal exatt_update_reimu(void)
{
    unsigned char angle;
    register exatt_entity_t near *p;
    register int i;
    hitbox_hittest_skip_explosions = true;
    hitbox.radius.x.v = TO_SP(16);
    hitbox.radius.y.v = TO_SP(16);
    hitbox.pid = (1 - pid_current);
    p = &exatt_entities[pid_current][0];

    i = 0;
    for(; i < 8; i++, p++) {
        if(p->state == 0) {
            continue;
        }
        if(p->state == 1) {
            p->x += p->velocity_x;
            if((p->x <= 0) || (p->x >= TO_SP(PLAYFIELD_W))) {
                p->velocity_x *= -1;
                p->x += p->velocity_x;
            }
            p->y += p->velocity_y;
            if(p->y < TO_SP(-24)) {
                p->velocity_y *= -1;
                p->y = TO_SP(-24);
            }
            if(p->y >= TO_SP(PLAYFIELD_H)) {
                p->state = 0;
                continue;
            }
            p->velocity_y++;
            hitbox.origin.center.x.v = p->x;
            hitbox.origin.center.y.v = p->y;
            hitbox_hittest();
            exatt_collmap_set(p->x, p->y);
        } else if(p->state == 2) {
            exatt_entity_p = p;
            if(exatt_fly_update() != 0) {
                angle = randring_far_next16_and(0x1F);
                angle = ((randring_far_next16_and(1) * 0x60) + angle + 0x80);
                vector2(
                    p->velocity_x, p->velocity_y,
                    angle, ((round_speed / 8) + 0x32)
                );
            }
        } else if(p->state <= 0x14) {
            p->state++;
        } else {
            p->state = 1;
        }
    }
    hitbox_hittest_skip_explosions = false;
}

void far pascal exatt_render_reimu(void)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    for(; i < 8; i++, p++) {
        if(p->state != 0) {
            exatt_entity_p = p;
            reimu_exatt_render_one();
            p->frame++;
        }
    }
}

#endif // !TH03_EXATT_REIMU_PREFIX_ONLY
