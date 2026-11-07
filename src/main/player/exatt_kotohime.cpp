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

// Kotohime reuses byte +0x11 as an extra projectile mode.
#include "src/main/player/exatt_entity.hpp"

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

// Shared 32-byte Extra Attack entity slots, with Kotohime's own 8
// ordinary + 2 explicit projectile policy. These are fixed physical counts.
enum kotohime_exatt_limits_t {
    KOTO_EXATT_NORMAL_SLOTS = 8,
    KOTO_EXATT_ALL_SLOTS = 10,
    KOTO_EXATT_RING4_COUNT = 4,
    KOTO_EXATT_RING10_COUNT = 10,
    KOTO_EXATT_FLYING_STATE = 2,
    KOTO_EXATT_APPEARING_MAX_STATE = 0x1C,
    KOTO_EXATT_TARGET_X_RANGE = 0x1200,
    KOTO_EXATT_TARGET_Y_RANGE = 0x400,
    KOTO_EXATT_INITIAL_FLY_SPEED = 0x5A,
    KOTO_EXATT_SPECIAL_FLY_SPEED = 0x78,
    KOTO_EXATT_FOUR_DELTA_RIGHT = 12,
    KOTO_EXATT_FOUR_DELTA_LEFT = -12,
    KOTO_EXATT_TEN_DELTA_RIGHT = 7,
    KOTO_EXATT_TEN_DELTA_LEFT = -7,
    KOTO_EXATT_PATTERN_SPEED_STEP = 2,
    KOTO_EXATT_COLLISION_TILE_W = 12,
    KOTO_EXATT_COLLISION_HALF_WIDTH = TO_SP(16),
};

// The original 32-byte entity byte-state protocol is shared by all eight
// Kotohime Extra Attack functions, not by a synthetic new object type.
enum kotohime_exatt_state_t {
    KOTO_EXATT_FREE = 0,
    KOTO_EXATT_BEAM = 1,
    KOTO_EXATT_FLYING = 2,
};
enum kotohime_exatt_flicker_t {
    KOTO_EXATT_FLICKER_PERIOD = 4,
    KOTO_EXATT_FLICKER_FIRST_HALF = 2,
    KOTO_EXATT_ORBIT_NEAR_TARGET = 0x600,
};

// Angle is reused as an event counter once this projectile has reached
// its Y destination; it is not a geometric angle on those frames.
enum kotohime_exatt_event_t {
    KOTO_EXATT_FIRST_PULSE = 4,
    KOTO_EXATT_SECOND_PULSE = 8,
    KOTO_EXATT_THIRD_PULSE = 12,
    KOTO_EXATT_FINAL_PULSE = 16,
};

void far pascal exatt_add_kotohime(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;
    for(; i < KOTO_EXATT_NORMAL_SLOTS; ++i, p++) {
        if(!p->state) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y,
                randring_far_next16_mod(KOTO_EXATT_TARGET_X_RANGE),
                randring_far_next16_mod(KOTO_EXATT_TARGET_Y_RANGE),
                pid_, KOTO_EXATT_INITIAL_FLY_SPEED
            );
            p->duration = (randring_far_next16_and(0xFFF) + 0x600);
            p->radius = (randring_far_next16_and(0x1F) + 0x10);
            p->angle = 0;
            p->character_mode.kotohime_extra_mode = 0;
            return;
        }
    }
}

void far pascal kotohime_extra_add(int target_x, int target_y)
{
    register exatt_kotohime_player_view_t near *player = &players[pid_current];
    register exatt_entity_t near *p = &exatt_entities[pid_current][8];
    if(p->state) {
        p++;
    }
    exatt_entity_p = p;
    exatt_fly_init(
        player->center.x.v, player->center.y.v,
        target_x, target_y,
        *(unsigned short near *)&pid_current,
        KOTO_EXATT_SPECIAL_FLY_SPEED
    );
    p->duration = 0xC00;
    p->radius = 0x20;
    p->angle = 0;
    p->character_mode.kotohime_extra_mode = 1;
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

    if(p->state == KOTO_EXATT_BEAM) {
        sprite_offset = (pid.so_attack + 0x280);
        if((p->duration - p->y) <= KOTO_EXATT_ORBIT_NEAR_TARGET) {
            // The unsigned-byte %4 is *not* native-equal to a C++
            // &3 mask here (three-byte shrink in af750a).
            if((frame % KOTO_EXATT_FLICKER_PERIOD) <
               KOTO_EXATT_FLICKER_FIRST_HALF) {
                sprite_offset += 0xA00;
            }
        }

        if(!p->character_mode.kotohime_extra_mode) {
            sprite_offset += 0x282;
            sprite16_put_size.set(32, 32);
            sprite16_put(left - 16, top - 16, sprite_offset);
        } else {
            sprite16_put_size.set(64, 64);
            sprite16_put(left - 32, top - 32, sprite_offset);
        }
    } else if(p->state == KOTO_EXATT_FLYING) {
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
    if(kotohime_exatt_pattern[pid_current].direction) {
        delta = KOTO_EXATT_FOUR_DELTA_LEFT;
    } else {
        delta = KOTO_EXATT_FOUR_DELTA_RIGHT;
    }
    bullet_template.speed.v = TO_SP(1);
    i = 0;
    // Four shot group: this typed while loop preserves original
    // bullet spawn, speed increase and byte-angle update order.
    while(i < KOTO_EXATT_RING4_COUNT) {
        bullets_add();
        bullet_template.speed.v += KOTO_EXATT_PATTERN_SPEED_STEP;
        bullet_template.angle += delta;
        ++i;
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
    if(kotohime_exatt_pattern[pid_current].direction) {
        delta = KOTO_EXATT_TEN_DELTA_RIGHT;
    } else {
        delta = KOTO_EXATT_TEN_DELTA_LEFT;
    }
    i = 0;
    // Ten shot group: the same source-level traversal is byte-exact,
    // despite the distinct negative angle delta and bullet counts.
    while(i < KOTO_EXATT_RING10_COUNT) {
        bullets_add();
        bullet_template.speed.v += KOTO_EXATT_PATTERN_SPEED_STEP;
        bullet_template.angle += delta;
        ++i;
    }
}

void far pascal exatt_update_kotohime(void)
{
    unsigned char pid_other;
    register int i;
    register exatt_entity_t near *p;

    exatt_entity_p = &exatt_entities[pid_current][0];
    pid_other = (1 - pid_current);
    collmap_stripe_tile_w.set(KOTO_EXATT_COLLISION_TILE_W);
    collmap_tile_h.set(KOTO_EXATT_COLLISION_TILE_W);
    collmap_pid = pid_other;
    i = 0;
    for(; i < KOTO_EXATT_ALL_SLOTS; ++i, exatt_entity_p++) {
        if(!exatt_entity_p->state) {
            continue;
        }
        p = exatt_entity_p;
        if(p->state == KOTO_EXATT_BEAM) {
            if(p->y >= p->duration) {
                if(p->angle == KOTO_EXATT_FIRST_PULSE) {
                    kotohime_exatt_effect();
                    if(p->character_mode.kotohime_extra_mode) {
                        bullet_template.speed.v = TO_SP(1) + 12;
                        bullet_template.angle = (unsigned char)randring_far_next16();
                        bullet_template.group = BG_RING;
                        bullet_template.pid = pid_other;
                        bullet_template.center.x.v = p->x;
                        bullet_template.center.y.v = p->y;
                        kotohime_exatt_pattern_four();
                    }
                } else if(p->angle == KOTO_EXATT_SECOND_PULSE || p->angle == KOTO_EXATT_THIRD_PULSE) {
                    kotohime_exatt_effect();
                } else if(p->angle == KOTO_EXATT_FINAL_PULSE) {
                    kotohime_exatt_effect();
                    bullet_template.speed.v = TO_SP(1) + 8;
                    bullet_template.angle = (unsigned char)randring_far_next16();
                    bullet_template.group = BG_RING;
                    bullet_template.pid = pid_other;
                    bullet_template.center.x.v = p->x;
                    bullet_template.center.y.v = p->y;
                    if(!p->character_mode.kotohime_extra_mode) {
                        bullet_template.type = BT_BULLET16_DEFAULT;
                        bullet_template.count = KOTO_EXATT_RING10_COUNT;
                        bullets_add();
                    } else {
                        kotohime_exatt_pattern_ten();
                    }
                    p->state = KOTO_EXATT_FREE;
                }
                // This angle is an 8-bit event counter after reaching
                // its target. Prefix ++p->angle changes original TC4
                // CODE again in independent native trial af861e.
                p->angle++;
            } else {
                // Preserve original word compound addition. An explicit
                // p->y = p->y + p->radius changes TC4 CODE (af861f).
                p->y += p->radius;
                hitbox_hittest_skip_explosions = true;
                hitbox.radius.x.v = KOTO_EXATT_COLLISION_HALF_WIDTH;
                hitbox.radius.y.v = KOTO_EXATT_COLLISION_HALF_WIDTH;
                hitbox.pid = pid_other;
                hitbox.origin.center.x.v = p->x;
                hitbox.origin.center.y.v = p->y;
                hitbox_hittest();
                hitbox_hittest_skip_explosions = false;
                collmap_center.x.v = p->x;
                collmap_center.y.v = p->y;
                collmap_set_rect_striped();
            }
        } else if(p->state == KOTO_EXATT_FLYING_STATE) {
            exatt_fly_update();
        } else if(p->state <= KOTO_EXATT_APPEARING_MAX_STATE) {
            p->state++;
        } else {
            p->frame = 0;
            p->state = KOTO_EXATT_BEAM;
        }
        p->frame++;
    }
}

void far pascal exatt_render_kotohime(void)
{
    register int i;
    exatt_entity_p = &exatt_entities[pid_current][0];
    i = 0;
    // Both loop and pointer advance are real original ten-slot
    // traversal. Native TC4 emits the exact source CODE (af861b).
    while(i < KOTO_EXATT_ALL_SLOTS) {
        if(exatt_entity_p->state) {
            kotohime_exatt_render_one();
        }
        ++i;
        exatt_entity_p++;
    }
}
