// Natural Turbo C++ reconstruction of the complete Kana Extra
// Attack CODE owner in TH03 P_EXATT_TEXT. Historical state remains in
// the maintained frozen carrier; no private entity DATA/BSS is emitted.
#pragma codeseg P_EXATT_TEXT

#include "src/main/player/exatt_kana.hpp"
#include "src/main/math/vector_far.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
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
    unsigned char unused_11;
    unsigned char angle;
    unsigned char speed;
    int radius;
    unsigned char tail[10];
};
typedef char kana_exatt_entity_is_32[(sizeof(exatt_entity_t)==32)?1:-1];

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
    screen_x_t left, screen_y_t top, unsigned char frame
);

void far pascal exatt_add_kana(int x, int y, unsigned char pid_)
{
    int target_x = randring_far_next16_mod(0x1200);
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;

    for(; i < 8; i++, p++) {
        if(p->state != 0) {
            continue;
        }
        exatt_entity_p = p;
        exatt_fly_init(
            x, y,
            target_x, randring_far_next16_mod(0x800),
            pid_, 0x5A
        );
        p->angle = (randring_far_next16_and(0x1F) - 0x0F);
        if(target_x >= 0x900) {
            p->angle += 0x80;
        }
        return;
    }
}

void far pascal kana_extra_add(int x, int y, unsigned char angle_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    for(; i < 8; i++, p++) {
        if(p->state == 0) {
            p->state = 1;
            p->x = x;
            p->y = y;
            p->angle = angle_;
            p->speed = 8;
            p->frame = 0;
            return;
        }
    }
}

void near kana_exatt_render_one(void)
{
    screen_x_t left;
    screen_y_t top;
    unsigned char frame;
    register exatt_entity_t near *p = exatt_entity_p;
    register sprite16_offset_t sprite_offset;

    left = playfield_fg_x_to_screen(p->x, p->pid);
    top = ((p->y >> 4) + 16);
    if((1 - pid_current) == 0) {
        sprite16_clip.set_for_pid_0();
    } else {
        sprite16_clip.set_for_pid_1();
    }
    frame = p->frame;

    if(p->state == 1) {
        sprite16_put_size.set(32, 32);
        sprite_offset = (pid.so_attack + 0x284);
        sprite_offset += (((frame / 4) % 4) << 5) * 0x28;
        sprite16_put(left - 16, top - 16, sprite_offset);
    } else if(p->state == 2) {
        exatt_render_state2(left, top, frame);
    } else {
        exatt_render_state_other(left, top, frame);
    }
}

void far pascal exatt_update_kana(void)
{
    int vector_x;
    int vector_y;
    unsigned char pid_other;
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i;

    pid_other = (1 - pid_current);
    playfield_clip_negative_radius.x.v = -TO_SP(24);
    playfield_clip_negative_radius.y.v = -TO_SP(24);
    i = 0;

    for(; i < 8; i++, p++) {
        if(p->state == 0) {
            continue;
        }
        exatt_entity_p = p;
        if(p->state == 1) {
            vector2(vector_x, vector_y, p->angle, p->speed);
            p->speed++;
            p->x += vector_x;
            p->y += vector_y;
            if((p->frame % 0x10) == 0) {
                bullet_template.type = BT_BULLET16_CUSTOM_WITH_ACCEL;
                bullet_template.angle = 0x40;
                bullet_template.group = BG_1;
                bullet_template.accel_type = BAT_Y;
                bullet_template.sprite_offset = (pid.so_attack + (72 * ROW_SIZE));
                bullet_template.speed.v = TO_SP(1);
                bullet_template.center.x.v = p->x;
                bullet_template.center.y.v = p->y;
                bullet_template.pid = pid_other;
                bullets_add();
            }
            if(playfield_clip(
                *(PlayfieldSubpixel near *)&p->x,
                *(PlayfieldSubpixel near *)&p->y
            )) {
                p->state = 0;
                continue;
            }
        } else if(p->state == 2) {
            exatt_fly_update();
        } else if(p->state <= 0x1C) {
            p->state++;
        } else {
            p->frame = 0;
            p->state = 1;
            p->speed = 8;
        }
        p->frame++;
    }
}

void far pascal exatt_render_kana(void)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    for(; i < 8; i++, p++) {
        if(p->state != 0) {
            exatt_entity_p = p;
            kana_exatt_render_one();
        }
    }
}
