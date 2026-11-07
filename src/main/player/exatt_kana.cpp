// Complete current native-source Turbo C++ for the original Kana
// Extra Attack physical owner in P_EXATT_TEXT. Historical state remains in
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

// All characters use the same 32-byte entity pool; +0x11 is per-character.
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
    screen_x_t left, screen_y_t top, unsigned char frame
);

// The same eight original physical slots pass through distinct byte
// entity states; preserve the original per-frame bullet RNG and clip.
enum kana_exatt_state_t {
    KANA_EXATT_SLOTS = 8,
    KANA_EXATT_FREE = 0,
    KANA_EXATT_ACTIVE = 1,
    KANA_EXATT_FLYING = 2,
    KANA_EXATT_APPEARING_END = 0x1C,
    KANA_EXATT_BULLET_PERIOD = 0x10,
    KANA_EXATT_TARGET_X_RANGE = 0x1200,
    KANA_EXATT_TARGET_Y_RANGE = 0x800,
    KANA_EXATT_TARGET_MID_X = 0x900,
    KANA_EXATT_INITIAL_FLY_SPEED = 0x5A,
    KANA_EXATT_BULLET_ANGLE_RANDOM_MASK = 0x1F,
    KANA_EXATT_BULLET_ANGLE_RANDOM_BIAS = 0x0F,
    KANA_EXATT_BULLET_ANGLE_EXTRA_HALF_TURN = 0x80,
    KANA_EXATT_ACTIVE_SPRITE_DIM = 32,
    KANA_EXATT_ACTIVE_SPRITE_BASE = 0x284,
};

void far pascal exatt_add_kana(int x, int y, unsigned char pid_)
{
    int target_x = randring_far_next16_mod(KANA_EXATT_TARGET_X_RANGE);
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;

    // Ordinary first-free allocation remains for/continue/return;
    // genuine TC4 rejected its natural while (af918c).
    for(; i < KANA_EXATT_SLOTS; ++i, p++) {
        if(p->state) {
            continue;
        }
        exatt_entity_p = p;
        exatt_fly_init(
            x, y,
            target_x, randring_far_next16_mod(KANA_EXATT_TARGET_Y_RANGE),
            pid_, KANA_EXATT_INITIAL_FLY_SPEED
        );
        p->angle = (randring_far_next16_and(KANA_EXATT_BULLET_ANGLE_RANDOM_MASK) - KANA_EXATT_BULLET_ANGLE_RANDOM_BIAS);
        if(target_x >= KANA_EXATT_TARGET_MID_X) {
            p->angle += KANA_EXATT_BULLET_ANGLE_EXTRA_HALF_TURN;
        }
        return;
    }
}

void far pascal kana_extra_add(int x, int y, unsigned char angle_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    // Special first-free allocation *does* accept natural while,
    // despite the different ordinary allocator (af918d).
    while(i < KANA_EXATT_SLOTS) {
        if(!p->state) {
            p->state = KANA_EXATT_ACTIVE;
            p->x = x;
            p->y = y;
            p->angle = angle_;
            p->speed = 8;
            p->frame = 0;
            return;
        }
        ++i;
        p++;
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

    if(p->state == KANA_EXATT_ACTIVE) {
        sprite16_put_size.set(KANA_EXATT_ACTIVE_SPRITE_DIM, KANA_EXATT_ACTIVE_SPRITE_DIM);
        sprite_offset = (pid.so_attack + KANA_EXATT_ACTIVE_SPRITE_BASE);
        // Both the byte /4 and following %4 must remain separate:
        // changing either to shift/mask changed TC4 CODE (af781c/d/e).
        // Keep /4 then %4: >>2 changed native CODE again (af918i).
        sprite_offset += (((frame / 4) % 4) << 5) * 0x28;
        sprite16_put(left - 16, top - 16, sprite_offset);
    } else if(p->state == KANA_EXATT_FLYING) {
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

    // Full eight-entity move/clip/accelerated-shot controller with
    // both early-continue paths native exact as while (af918a).
    while(i < KANA_EXATT_SLOTS) {
        if(!p->state) {
            ++i;
            p++;
            continue;
        }
        exatt_entity_p = p;
        if(p->state == KANA_EXATT_ACTIVE) {
            vector2(vector_x, vector_y, p->angle, p->speed);
            p->speed++;
            p->x += vector_x;
            p->y += vector_y;
            // Original byte %16 is not native-equal to &15 here
            // (negative compiler stage af781b).
            // Byte frame zero remainder accepts natural truth
            // spelling under the actual TC4 (af918f).
            if(!(p->frame % KANA_EXATT_BULLET_PERIOD)) {
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
                p->state = KANA_EXATT_FREE;
                ++i;
                p++;
                continue;
            }
        } else if(p->state == KANA_EXATT_FLYING) {
            exatt_fly_update();
        } else if(p->state <= KANA_EXATT_APPEARING_END) {
            p->state++;
        } else {
            p->frame = 0;
            p->state = KANA_EXATT_ACTIVE;
            p->speed = 8;
        }
        // Byte frame postfix cannot be replaced by prefix (af918h).
        p->frame++;
        ++i;
        p++;
    }
}

void far pascal exatt_render_kana(void)
{
    register exatt_entity_t near *p = &exatt_entities[pid_current][0];
    register int i = 0;
    // All eight physical sprite slots retain their original
    // near-pointer render order (af918e).
    while(i < KANA_EXATT_SLOTS) {
        if(p->state) {
            exatt_entity_p = p;
            kana_exatt_render_one();
        }
        ++i;
        p++;
    }
}
