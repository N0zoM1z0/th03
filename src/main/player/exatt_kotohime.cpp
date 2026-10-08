// Natural TC4J reconstruction of all eight functions in Kotohime's
// TH03 P_EXATT_TEXT Extra Attack CODE owner. Entity slots, current-player
// controls and bullet pattern settings retain their original frozen DGROUP
// locations; this object emits no private DATA/BSS.
#pragma codeseg P_EXATT_TEXT

#include "src/main/player/exatt_kotohime.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
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
    unsigned char mode;
    unsigned char angle;
    unsigned char speed;
    int radius;
    unsigned char tail[10];
};
typedef char exatt_entity_size_is_32[(sizeof(exatt_entity_t)==32)?1:-1];

struct exatt_kotohime_player_view_t {
    PlayfieldPoint center;
    unsigned char rest[124];
};
typedef char kotohime_player_view_is_128[(sizeof(exatt_kotohime_player_view_t)==128)?1:-1];

struct kotohime_exatt_pattern_t {
    unsigned char bullet_count;
    unsigned char direction;
    unsigned char bullet_type;
    unsigned char unused;
};
typedef char kotohime_exatt_pattern_is_4[(sizeof(kotohime_exatt_pattern_t)==4)?1:-1];

extern exatt_entity_t exatt_entities[PLAYER_COUNT][16];
extern exatt_entity_t near *exatt_entity_p;
extern exatt_kotohime_player_view_t players[PLAYER_COUNT];
extern kotohime_exatt_pattern_t kotohime_exatt_pattern[PLAYER_COUNT];

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
extern "C" void far pascal bomb_explosion_add(int x, int y, int pid);

void far pascal exatt_add_kotohime(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;
    for(; i < 8; i++, p++) {
        if(p->state == 0) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y,
                randring_far_next16_mod(0x1200),
                randring_far_next16_mod(0x400),
                pid_, 0x5A
            );
            p->duration = (randring_far_next16_and(0xFFF) + 0x600);
            p->radius = (randring_far_next16_and(0x1F) + 0x10);
            p->angle = 0;
            p->mode = 0;
            return;
        }
    }
}

void far pascal kotohime_extra_add(int target_x, int target_y)
{
    register exatt_kotohime_player_view_t near *player = &players[pid_current];
    register exatt_entity_t near *p = &exatt_entities[pid_current][8];
    if(p->state != 0) {
        p++;
    }
    exatt_entity_p = p;
    exatt_fly_init(
        player->center.x.v, player->center.y.v,
        target_x, target_y,
        *(unsigned short near *)&pid_current,
        0x78
    );
    p->duration = 0xC00;
    p->radius = 0x20;
    p->angle = 0;
    p->mode = 1;
}

void near kotohime_exatt_render_one(void)
{
    screen_x_t left;
    screen_y_t top;
    unsigned char frame;
    register exatt_entity_t near *p = exatt_entity_p;
    register sprite16_offset_t sprite_offset;

    left = playfield_fg_x_to_screen(p->x, p->pid);
    top = ((p->y >> 4) + 16);
    sprite16_clip.reset();
    frame = p->frame;

    if(p->state == 1) {
        sprite_offset = (pid.so_attack + 0x280);
        if((p->duration - p->y) <= 0x600) {
            if((frame % 4) < 2) {
                sprite_offset += 0xA00;
            }
        }

        if(p->mode == 0) {
            sprite_offset += 0x282;
            sprite16_put_size.set(32, 32);
            sprite16_put(left - 16, top - 16, sprite_offset);
        } else {
            sprite16_put_size.set(64, 64);
            sprite16_put(left - 32, top - 32, sprite_offset);
        }
    } else if(p->state == 2) {
        exatt_render_state2(left, top, frame);
    } else {
        exatt_render_state_other(left, top, frame);
    }
}

void near kotohime_exatt_effect(void)
{
    snd_se_play(3);
    bomb_explosion_add(
        exatt_entity_p->x,
        exatt_entity_p->y,
        (1 - pid_current)
    );
}

void near kotohime_exatt_pattern_four(void)
{
    unsigned char delta;
    register int i;

    bullet_template.type = static_cast<bullet_type_t>(
        kotohime_exatt_pattern[pid_current].bullet_type
    );
    bullet_template.count = kotohime_exatt_pattern[pid_current].bullet_count;
    if(kotohime_exatt_pattern[pid_current].direction != 0) {
        delta = -12;
    } else {
        delta = 12;
    }
    bullet_template.speed.v = TO_SP(1);
    i = 0;
    for(; i < 4; i++) {
        bullets_add();
        bullet_template.speed.v += 2;
        bullet_template.angle += delta;
    }
}

void near kotohime_exatt_pattern_ten(void)
{
    unsigned char delta;
    register int i;

    bullet_template.type = static_cast<bullet_type_t>(
        kotohime_exatt_pattern[pid_current].bullet_type
    );
    bullet_template.speed.v = TO_SP(1);
    bullet_template.count = kotohime_exatt_pattern[pid_current].bullet_count;
    if(kotohime_exatt_pattern[pid_current].direction != 0) {
        delta = 7;
    } else {
        delta = -7;
    }
    i = 0;
    for(; i < 10; i++) {
        bullets_add();
        bullet_template.speed.v += 2;
        bullet_template.angle += delta;
    }
}

void far pascal exatt_update_kotohime(void)
{
    unsigned char pid_other;
    register int i;
    register exatt_entity_t near *p;

    exatt_entity_p = &exatt_entities[pid_current][0];
    pid_other = (1 - pid_current);
    collmap_stripe_tile_w.set(12);
    collmap_tile_h.set(12);
    collmap_pid = pid_other;
    i = 0;
    for(; i < 10; i++, exatt_entity_p++) {
        if(exatt_entity_p->state == 0) {
            continue;
        }
        p = exatt_entity_p;
        if(p->state == 1) {
            if(p->y >= p->duration) {
                if(p->angle == 4) {
                    kotohime_exatt_effect();
                    if(p->mode != 0) {
                        bullet_template.speed.v = TO_SP(1) + 12;
                        bullet_template.angle = (unsigned char)randring_far_next16();
                        bullet_template.group = BG_RING;
                        bullet_template.pid = pid_other;
                        bullet_template.center.x.v = p->x;
                        bullet_template.center.y.v = p->y;
                        kotohime_exatt_pattern_four();
                    }
                } else if(p->angle == 8 || p->angle == 12) {
                    kotohime_exatt_effect();
                } else if(p->angle == 16) {
                    kotohime_exatt_effect();
                    bullet_template.speed.v = TO_SP(1) + 8;
                    bullet_template.angle = (unsigned char)randring_far_next16();
                    bullet_template.group = BG_RING;
                    bullet_template.pid = pid_other;
                    bullet_template.center.x.v = p->x;
                    bullet_template.center.y.v = p->y;
                    if(p->mode == 0) {
                        bullet_template.type = BT_BULLET16_DEFAULT;
                        bullet_template.count = 10;
                        bullets_add();
                    } else {
                        kotohime_exatt_pattern_ten();
                    }
                    p->state = 0;
                }
                p->angle++;
            } else {
                p->y += p->radius;
                hitbox_hittest_skip_explosions = true;
                hitbox.radius.x.v = TO_SP(16);
                hitbox.radius.y.v = TO_SP(16);
                hitbox.pid = pid_other;
                hitbox.origin.center.x.v = p->x;
                hitbox.origin.center.y.v = p->y;
                hitbox_hittest();
                hitbox_hittest_skip_explosions = false;
                collmap_center.x.v = p->x;
                collmap_center.y.v = p->y;
                collmap_set_rect_striped();
            }
        } else if(p->state == 2) {
            exatt_fly_update();
        } else if(p->state <= 0x1C) {
            p->state++;
        } else {
            p->frame = 0;
            p->state = 1;
        }
        p->frame++;
    }
}

void far pascal exatt_render_kotohime(void)
{
    register int i;
    exatt_entity_p = &exatt_entities[pid_current][0];
    i = 0;
    for(; i < 10; i++, exatt_entity_p++) {
        if(exatt_entity_p->state != 0) {
            kotohime_exatt_render_one();
        }
    }
}
