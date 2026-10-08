// Maintained natural Turbo C++ reconstruction of the complete Chiyuri
// Extra Attack P_EXATT_TEXT CODE owner (5 functions / 1029 exact bytes).
// The 518-byte beam renderer and 298-byte entity updater are included.
// Historical entity/trajectory BSS is declared extern and not duplicated.
#pragma codeseg P_EXATT_TEXT

#include "src/main/player/exatt_chiyuri.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/main/v_colors.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#pragma option -a2

struct exatt_entity_t {
    unsigned char state, frame;
    int x, y, velocity_x, velocity_y, target_x, boundary_x, duration;
    unsigned char pid, mode, angle, speed;
    int radius;
    unsigned char tail[10];
};
typedef char chiyuri_entity_size32[(sizeof(exatt_entity_t)==32)?1:-1];
struct ellen_slot_t {
    exatt_entity_t near *entity;
    unsigned char history[28];
};
typedef char ellen_slot_size30[(sizeof(ellen_slot_t)==30)?1:-1];
extern exatt_entity_t exatt_entities[PLAYER_COUNT][16];
extern exatt_entity_t near *exatt_entity_p;
extern ellen_slot_t ellen_exatt_slots[PLAYER_COUNT][12];

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

void far pascal exatt_add_chiyuri(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    register int i = 0;
    for(; i < 16; (i += 2, p += 2)) {
        if(p->state != 0) {
            continue;
        }
        exatt_entity_p = p;
        exatt_fly_init(x, y, (randring_far_next16_mod(0x1140) + 0x60),
                       0, pid_, 0x50);
        exatt_entity_p++;
        exatt_fly_init(x, y, (randring_far_next16_mod(0x1140) + 0x60),
                       0x1780, pid_, 0x50);
        return;
    }
}

void near chiyuri_exatt_render_one(void)
{
    unsigned char phase;
    int left;
    int top;
    int left_other;
    int top_other;
    register exatt_entity_t near *p = exatt_entity_p;
    register int radius;

    phase = p->frame;
    left = playfield_fg_x_to_screen(p->x, p->pid);
    top = ((p->y >> 4) + 16);
    p++;
    left_other = playfield_fg_x_to_screen(p->x, p->pid);
    top_other = ((p->y >> 4) + 16);
    p--;

    if(p->state == 1) {
        egc_off();
        if(phase < 0x10) {
            goto beam_line;
        }
        if(phase < 0x28) {
            _AX = (phase - 0x10);
            goto beam_radius;
        }
        if(phase >= 0x70) {
            goto beam_late;
        }
        grcg_setcolor(GC_RMW, 9);
        grcg_trapezoid(8, left - 6, left + 6,
                       192, left_other - 6, left_other + 6);
        grcg_setcolor(GC_RMW, 10);
        grcg_trapezoid(8, left - 3, left + 3,
                       192, left_other - 3, left_other + 3);
        grcg_setcolor(GC_RMW, V_WHITE);
        grcg_trapezoid(8, left - 1, left + 1,
                       192, left_other - 1, left_other + 1);
        goto beam_end;

beam_late:
        if(phase >= 0x88) {
            goto beam_end;
        }
        asm {
            mov al, phase
            mov ah, 0
            push ax
            mov ax, 88h
            pop dx
        }
        _AX -= _DX;

beam_radius:
        radius = (static_cast<int>(_AX) / 4);
        grcg_setcolor(GC_RMW, 9);
        grcg_trapezoid(8, left - radius, left + radius,
                       192, left_other - radius, left_other + radius);
        radius /= 2;
        grcg_setcolor(GC_RMW, 10);
        grcg_trapezoid(8, left - radius, left + radius,
                       192, left_other - radius, left_other + radius);

beam_line:
        grcg_setcolor(GC_RMW, V_WHITE);
        grcg_line(left, 8, left_other, 192);

beam_end:
        grcg_off();
        egc_on();
    } else {
        if(p->state == 2) {
            exatt_render_state2(left, top, phase);
        } else {
            exatt_render_state_other(left, top, phase);
        }
        exatt_entity_p++;
        p++;
        phase = p->frame;
        if(p->state == 2) {
            exatt_render_state2(left_other, top_other, phase);
        } else {
            exatt_render_state_other(left_other, top_other, phase);
        }
        exatt_entity_p--;
    }
}

void far pascal exatt_update_chiyuri(void)
{
    int first_arrived;
    unsigned char pid_other;
    register exatt_entity_t near *p;
    register int i;

    exatt_entity_p = &exatt_entities[pid_current][0];
    pid_other = (1 - pid_current);
    collmap_stripe_tile_w.set(4);
    collmap_pid = pid_other;
    i = 0;
    for(; i < 16; (i += 2, exatt_entity_p++)) {
        asm {
            mov bx, exatt_entity_p
            cmp byte ptr [bx], 0
            je short chiyuri_first_done
        }
        p = exatt_entity_p;
        if(p->state == 1) {
                p->frame++;
                if(p->frame == 4) {
                    bomb_center_add(p->x, 0, p->pid);
                    p++;
                    bomb_center_add(p->x, 0x1700, p->pid);
                } else if(p->frame == 0x10) {
                    snd_se_play(20);
                } else if(p->frame > 0x28 && p->frame < 0x70) {
                    collmap_topleft.x.v = p->x;
                    p++;
                    collmap_bottomright.x.v = p->x;
                    collmap_set_slope_striped();
                } else if(p->frame > 0x88) {
                    p->state = 0;
                    p++;
                    p->state = 0;
                }
chiyuri_first_done:
                exatt_entity_p++;
                continue;
            }

            first_arrived = 0;
            if(p->state == 2) {
                if(exatt_fly_update() != 0) {
                    p->y = 0;
                }
            } else if(p->state <= 0x1C) {
                p->state++;
            } else {
                p->frame = 0;
                first_arrived = 1;
            }
            p->frame++;
            p++;
            exatt_entity_p++;
            if(p->state == 2) {
                if(exatt_fly_update() != 0) {
                    p->y = 0x1700;
                }
            } else if(p->state <= 0x1C) {
                p->state++;
            } else {
                p->frame = 0;
                if(first_arrived != 0) {
                    p--;
                    p->state = 1;
                }
            }
            p->frame++;

    }
}

void far pascal exatt_render_chiyuri(void)
{
    register int i;
    exatt_entity_p = &exatt_entities[pid_current][0];
    i = 0;
    for(; i < 16; i += 2, exatt_entity_p += 2) {
        if(exatt_entity_p->state != 0) {
            chiyuri_exatt_render_one();
        }
    }
}

void far pascal exatt_ellen_slots_init(void)
{
    register ellen_slot_t near *p0 = &ellen_exatt_slots[0][0];
    register ellen_slot_t near *p1 = &ellen_exatt_slots[1][0];
    register int i = 0;
    for(; i < 12; i++, p0++, p1++) {
        p0->entity = &exatt_entities[0][i];
        p1->entity = &exatt_entities[1][i];
    }
}
