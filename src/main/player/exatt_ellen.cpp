// Natural TC4 reconstruction candidate for the complete TH03 Ellen
// Extra Attack P_EXATT_TEXT owner. The 30-byte trailing-history slot array
// and each referenced 32-byte entity remain in the frozen historical BSS.
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

struct exatt_entity_t {
    unsigned char state;
    unsigned char frame;
    int x, y;
    int velocity_x, velocity_y;
    int target_x, boundary_x;
    int duration;
    unsigned char pid;
    signed char spin_delta;
    unsigned char angle;
    unsigned char speed;
    int radius;
    unsigned char tail[10];
};
typedef char ellen_exatt_entity_size_is_32[(sizeof(exatt_entity_t) == 32)?1:-1];

struct ellen_exatt_slot_t {
    exatt_entity_t near *entity;
    int history_x[7];
    int history_y[7];
};
typedef char ellen_exatt_slot_size_is_30[(sizeof(ellen_exatt_slot_t) == 30)?1:-1];

extern ellen_exatt_slot_t ellen_exatt_slots[PLAYER_COUNT][12];
extern ellen_exatt_slot_t near *ellen_exatt_slot_p;
extern exatt_entity_t near *exatt_entity_p;
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

void far pascal exatt_add_ellen(int x, int y, unsigned char pid_)
{
    int target_y;
    int target_x;
    unsigned char added;
    signed char spin;
    unsigned char angle;
    added = 0;
    target_y = randring_far_next16_mod(0x0C80) + 0x2C0;
    target_x = randring_far_next16_mod(0x0C80) + 0x500;
    spin = (randring_far_next16_and(1) == 0) ? -1 : 1;
    angle = (unsigned char)randring_far_next16();

    ellen_exatt_slot_p = &ellen_exatt_slots[pid_][0];
    register int i = 0;
    for(; i < 12; i++, ellen_exatt_slot_p++) {
        if(ellen_exatt_slot_p->entity->state != 0) {
            continue;
        }
        exatt_entity_p = ellen_exatt_slot_p->entity;
        exatt_fly_init(x, y, target_x, target_y, pid_, 0x46);
        exatt_entity_p->radius = 0;
        exatt_entity_p->spin_delta = spin;
        if(added == 0) {
            exatt_entity_p->angle = angle;
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
    int i = 0;
    for(; i < 12; i++, ellen_exatt_slot_p++) {
        if(ellen_exatt_slot_p->entity->state != 0) {
            continue;
        }
        register exatt_entity_t near *p = ellen_exatt_slot_p->entity;
        p->state = 1;
        p->frame = 0;
        p->x = x;
        p->y = y;
        p->radius = 0;
        p->spin_delta = mode;
        p->angle = angle_;
        p->pid = (1 - pid_current);
        return;
    }
}

void near ellen_exatt_render_one(void)
{
    screen_x_t left;
    screen_y_t top;
    screen_x_t trail_left;
    screen_y_t trail_top;
    unsigned char frame;
    register int i;
    register sprite16_offset_t sprite_offset;

    left = playfield_fg_x_to_screen(
        ellen_exatt_slot_p->entity->x,
        ellen_exatt_slot_p->entity->pid
    );
    top = ((ellen_exatt_slot_p->entity->y >> 4) + 16);
    if(ellen_exatt_slot_p->entity->pid == 0) {
        sprite16_clip.set_for_pid_0();
    } else {
        sprite16_clip.set_for_pid_1();
    }
    frame = ellen_exatt_slot_p->entity->frame;

    if(ellen_exatt_slot_p->entity->state == 1) {
        sprite16_put_size.set(32, 32);
        sprite_offset = pid.so_attack + 0x28C;
        i = 6;
        for(; i >= 0; i -= 2) {
            trail_left = playfield_fg_x_to_screen(
                ellen_exatt_slot_p->history_x[i],
                ellen_exatt_slot_p->entity->pid
            );
            trail_top = ((ellen_exatt_slot_p->history_y[i] >> 4) + 16);
            sprite16_put(trail_left - 16, trail_top - 16, sprite_offset);
            sprite_offset -= 4;
        }
    } else if(ellen_exatt_slot_p->entity->state == 2) {
        exatt_render_state2(left, top, frame);
    } else {
        exatt_render_state_other(
            left, top, *(unsigned int near *)&ellen_exatt_slot_p->entity->state
        );
    }
}

void far pascal exatt_update_ellen(void)
{
    unsigned char pid_other;
    int j;
    int i;
    register ellen_exatt_slot_t near *slot = &ellen_exatt_slots[pid_current][0];

    pid_other = (1 - pid_current);
    playfield_clip_negative_radius.x.v = -TO_SP(24);
    playfield_clip_negative_radius.y.v = -TO_SP(24);
    collmap_stripe_tile_w.set(12);
    collmap_tile_h.set(12);
    collmap_pid = pid_other;
    i = 0;

    for(; i < 12; i++, slot++) {
        if(slot->entity->state == 0) {
            continue;
        }
        if(slot->entity->state == 1) {
            j = 6;
            for(; j > 0; j--) {
                slot->history_x[j] = slot->history_x[j - 1];
                slot->history_y[j] = slot->history_y[j - 1];
            }
            if(slot->entity->radius <= 0xD00) {
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
                slot->entity->radius += 0x18;
                slot->entity->angle += slot->entity->spin_delta;
            } else {
                if(
                    playfield_clip(
                        *(PlayfieldSubpixel near *)&slot->history_x[0],
                        *(PlayfieldSubpixel near *)&slot->history_y[0]
                    ) &&
                    playfield_clip(
                        *(PlayfieldSubpixel near *)&slot->history_x[6],
                        *(PlayfieldSubpixel near *)&slot->history_y[6]
                    )
                ) {
                    slot->entity->state = 0;
                    continue;
                }
                slot->history_x[0] += slot->entity->velocity_x;
                slot->history_y[0] += slot->entity->velocity_y;
            }
            hitbox_hittest_skip_explosions = true;
            hitbox.radius.x.v = TO_SP(16);
            hitbox.radius.y.v = TO_SP(16);
            hitbox.pid = pid_other;
            hitbox.origin.center.x.v = slot->history_x[0];
            hitbox.origin.center.y.v = slot->history_y[0];
            hitbox_hittest();
            hitbox_hittest_skip_explosions = false;

            collmap_center.x.v = slot->history_x[0];
            collmap_center.y.v = slot->history_y[0];
            collmap_set_rect_striped();
        } else if(slot->entity->state == 2) {
            exatt_entity_p = slot->entity;
            if(exatt_fly_update() != 0) {
                j = 0;
                for(; j < 7; j++) {
                    slot->history_x[j] = exatt_entity_p->x;
                    slot->history_y[j] = exatt_entity_p->y;
                }
            }
        } else if(slot->entity->state <= 0x1C) {
            slot->entity->state++;
        } else {
            slot->entity->frame = 0;
            slot->entity->state = 1;
            snd_se_play(10);
        }
        slot->entity->frame++;
    }
}

void far pascal exatt_render_ellen(void)
{
    register ellen_exatt_slot_t near *p = &ellen_exatt_slots[pid_current][0];
    register int i = 0;
    for(; i < 12; i++, p++) {
        if(p->entity->state != 0) {
            ellen_exatt_slot_p = p;
            ellen_exatt_render_one();
        }
    }
}
