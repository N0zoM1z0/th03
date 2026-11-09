// Maintained natural Turbo C++ reconstruction of the complete Chiyuri
// Extra Attack P_EXATT_TEXT CODE producer (4 functions / 978 bytes).
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

// Chiyuri uses the same physical 32-byte flight entity.
#include "src/main/player/exatt_entity.hpp"
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

// Paired physical entities: even/odd slots render the top and bottom
// ends of the same GRCG beam. The real update advances the shared pointer
// twice per pair and retains its native skip-branch register contract.
enum chiyuri_exatt_phase_t {
    CHIYURI_EXATT_PHYSICAL_SLOTS = 16,
    CHIYURI_EXATT_PAIR_STRIDE = 2,
    CHIYURI_BEAM_LINE_END = 0x10,
    CHIYURI_BEAM_GROW_END = 0x28,
    CHIYURI_BEAM_SHRINK_START = 0x70,
    CHIYURI_BEAM_FINISH = 0x88,
    CHIYURI_BEAM_FIRST_WARNING = 4,
    CHIYURI_BEAM_SOUND_FRAME = 0x10,
    CHIYURI_BEAM_ARRIVAL_END_STATE = 0x1C,
    CHIYURI_EXATT_FREE = 0,
    CHIYURI_EXATT_ACTIVE = 1,
    CHIYURI_EXATT_FLYING = 2,
    CHIYURI_EXATT_RANDOM_X_RANGE = 0x1140,
    CHIYURI_EXATT_RANDOM_X_BIAS = 0x60,
    // Spawn target is 0x1780; after flight it SNAPS to 0x1700.
    // They are genuinely different original 16-bit coordinates.
    CHIYURI_EXATT_TARGET_BOTTOM_Y = 0x1780,
    CHIYURI_EXATT_LAUNCH_SPEED = 0x50,
    CHIYURI_EXATT_BEAM_BOTTOM_Y = 0x1700,
    CHIYURI_EXATT_COLLISION_TILE_WIDTH = 4,
};

void far pascal exatt_add_chiyuri(int x, int y, unsigned char pid_)
{
    register exatt_entity_t near *p = &exatt_entities[pid_][0];
    // Advance by complete two-entity pairs after checking each free slot.
    for(register int i = 0; i < CHIYURI_EXATT_PHYSICAL_SLOTS;
        i += CHIYURI_EXATT_PAIR_STRIDE, p += CHIYURI_EXATT_PAIR_STRIDE) {
        if(!p->state) {
            exatt_entity_p = p;
            exatt_fly_init(
                x, y,
                (randring_far_next16_mod(CHIYURI_EXATT_RANDOM_X_RANGE) +
                 CHIYURI_EXATT_RANDOM_X_BIAS),
                0, pid_, CHIYURI_EXATT_LAUNCH_SPEED
            );
            exatt_entity_p++;
            exatt_fly_init(
                x, y,
                (randring_far_next16_mod(CHIYURI_EXATT_RANDOM_X_RANGE) +
                 CHIYURI_EXATT_RANDOM_X_BIAS),
                CHIYURI_EXATT_TARGET_BOTTOM_Y,
                pid_, CHIYURI_EXATT_LAUNCH_SPEED
            );
            return;
        }
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

    if(p->state == CHIYURI_EXATT_ACTIVE) {
        egc_off();
        if(phase < CHIYURI_BEAM_LINE_END) {
            goto beam_line;
        }
        if(phase < CHIYURI_BEAM_GROW_END) {
            _AX = (phase - 0x10);
            goto beam_radius;
        }
        if(phase >= CHIYURI_BEAM_SHRINK_START) {
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
        if(phase >= CHIYURI_BEAM_FINISH) {
            goto beam_end;
        }
        // The late-beam signed radius keeps its original AX/DX and
        // stack ordering: typed CHIYURI_BEAM_FINISH - phase changed
        // original CODE independently in af779c.
        asm {
            mov al, phase
            mov ah, 0
            push ax
            mov ax, 88h
            pop dx
        }
        _AX -= _DX;

beam_radius:
        // Original signed division rounds toward zero; arithmetic >>2
        // rounds negative values differently and changed CODE (af867f).
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
        if(p->state == CHIYURI_EXATT_FLYING) {
            exatt_render_state2(left, top, phase);
        } else {
            exatt_render_state_other(left, top, phase);
        }
        exatt_entity_p++;
        p++;
        phase = p->frame;
        if(p->state == CHIYURI_EXATT_FLYING) {
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

    exatt_entity_p = &exatt_entities[pid_current][0];
    pid_other = (1 - pid_current);
    collmap_stripe_tile_w.set(CHIYURI_EXATT_COLLISION_TILE_WIDTH);
    collmap_pid = pid_other;
    // Both completion paths advance the signed index and shared pointer
    // at the same physical pair boundary, including the active `continue`.
    for(register int i = 0; i < CHIYURI_EXATT_PHYSICAL_SLOTS;
        i += CHIYURI_EXATT_PAIR_STRIDE, ++exatt_entity_p) {
        // The original BX/memory CMP/Jcc sequence is emitted naturally
        // by this direct C++ byte-state test (proved in af779b).
        if(!exatt_entity_p->state) {
            goto chiyuri_first_done;
        }
        p = exatt_entity_p;
        if(p->state == CHIYURI_EXATT_ACTIVE) {
            p->frame++;
            if(p->frame == CHIYURI_BEAM_FIRST_WARNING) {
                bomb_center_add(p->x, 0, p->pid);
                p++;
                bomb_center_add(p->x, CHIYURI_EXATT_BEAM_BOTTOM_Y, p->pid);
            } else if(p->frame == CHIYURI_BEAM_SOUND_FRAME) {
                snd_se_play(20);
            } else if(p->frame > CHIYURI_BEAM_GROW_END && p->frame < CHIYURI_BEAM_SHRINK_START) {
                collmap_topleft.x.v = p->x;
                p++;
                collmap_bottomright.x.v = p->x;
                collmap_set_slope_striped();
            } else if(p->frame > CHIYURI_BEAM_FINISH) {
                p->state = CHIYURI_EXATT_FREE;
                p++;
                p->state = CHIYURI_EXATT_FREE;
            }
chiyuri_first_done:
            ++exatt_entity_p;
            continue;
        }

        first_arrived = 0;
        if(p->state == CHIYURI_EXATT_FLYING) {
            if(exatt_fly_update()) {
                p->y = 0;
            }
        } else if(p->state <= CHIYURI_BEAM_ARRIVAL_END_STATE) {
            p->state++;
        } else {
            p->frame = 0;
            first_arrived = 1;
        }
        p->frame++;
        p++;
        exatt_entity_p++;
        if(p->state == CHIYURI_EXATT_FLYING) {
            if(exatt_fly_update()) {
                p->y = CHIYURI_EXATT_BEAM_BOTTOM_Y;
            }
        } else if(p->state <= CHIYURI_BEAM_ARRIVAL_END_STATE) {
            p->state++;
        } else {
            p->frame = 0;
            if(first_arrived) {
                p--;
                p->state = CHIYURI_EXATT_ACTIVE;
            }
        }
        p->frame++;
    }
}

void far pascal exatt_render_chiyuri(void)
{
    exatt_entity_p = &exatt_entities[pid_current][0];
    // Every rendered beam consumes two physical entity records.
    for(register int i = 0; i < CHIYURI_EXATT_PHYSICAL_SLOTS;
        i += CHIYURI_EXATT_PAIR_STRIDE,
        exatt_entity_p += CHIYURI_EXATT_PAIR_STRIDE) {
        if(exatt_entity_p->state) {
            chiyuri_exatt_render_one();
        }
    }
}
