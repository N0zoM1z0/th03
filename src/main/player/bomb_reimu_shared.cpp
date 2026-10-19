// Source-present shared lifecycle + Reimu bomb producer (925 CODE bytes).
// Exact acceptance pending; see docs/reconstruction/MAIN_REIMU_SHARED_GAMEPLAY_REVIEW.md.
// Shared lifecycle serves Marisa, Kotohime, Kana, Rikako, Chiyuri and Yumemi
// for both players. Reimu uses the separate updater below.
// Existing storage remains external; no DATA/BSS definitions are introduced.
#pragma codeseg HITBOX_TEXT main_04
#pragma option -a1
#include "src/main/player/reimu_gameplay.hpp"
#pragma option -a2
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
extern "C" void far bomb_bg_fill(void); // Actual existing helper consumes BX.
void far shared_bomb_lifecycle_update(void)
{
    if(bomb_flag[pid_current] == BF_INACTIVE) {
        return;
    }
    if(bomb_flag[pid_current] == BF_PREPARING) {
        bomb_flag[pid_current] = BF_ACTIVE;
        bomb_frame[pid_current] = 0;
        snd_se_play(18);
    }
    bomb_frame[pid_current]++;
    if(bomb_frame[pid_current] >= BOMB_FRAMES) {
        bomb_flag[pid_current] = BF_INACTIVE;
        palette_restore_for_pid(pid_current);
    }
}

void far reimu_bomb_update(void)
{
    int i;
    if(bomb_flag[pid_current] == BF_INACTIVE) {
        return;
    }
    if(bomb_flag[pid_current] == BF_PREPARING) {
        bomb_flag[pid_current] = BF_ACTIVE;
        bomb_frame[pid_current] = 0;
        for(i = 0; i < 32; i++) {
            reimu_bomb_particles[pid_current][i].active = 0;
        }
        snd_se_play(18);
    }
    bomb_frame[pid_current]++;
    reimu_bomb_particle_p = &reimu_bomb_particles[pid_current][0];
    for(i = 0; i < 32; i++, reimu_bomb_particle_p++) {
        if(reimu_bomb_particle_p->active == 0) {
            continue;
        }
        reimu_bomb_particle_p->y += reimu_bomb_particle_p->velocity_y;
        if(reimu_bomb_particle_p->y <= -TO_SP(8)) {
            reimu_bomb_particle_p->y = TO_SP(384);
            reimu_bomb_particle_p->velocity_y += 8;
        }
    }
    if(bomb_frame[pid_current] >= BOMB_FRAMES) {
        bomb_flag[pid_current] = BF_INACTIVE;
        palette_restore_for_pid(pid_current);
    }
}
void near reimu_bomb_particles_render(void)
{
    int left;
    int top;
    sprite16_offset_t sprite_offset;
    reimu_bomb_particle_p = &reimu_bomb_particles[pid_current][0];
    sprite16_put_size.set(16, 16);
    sprite16_clip.reset();
    sprite_offset = pid.so_attack + 0x18;
    for(int i = 0; i < 32; i++, reimu_bomb_particle_p++) {
        if(reimu_bomb_particle_p->active == 0) {
            continue;
        }
        left = playfield_fg_x_to_screen(reimu_bomb_particle_p->x, pid_current) - 8;
        top = (reimu_bomb_particle_p->y >> 4) + 8;
        sprite16_put(left, top, sprite_offset);
    }
}
void far reimu_bomb(void)
{
    unsigned char frame;
    unsigned char color;
    if(bomb_flag[pid_current] == BF_INACTIVE) {
        return;
    }
    egc_off();
    frame = bomb_frame[pid_current];
    if(frame < 64) {
        grcg_setcolor(GC_RMW, pid_current);
        // Real register ABI: target sub_B39E calls sub_B37C, whose first
        // fill-loop setup copies BX into DI. See raw helper audit in REVIEW.
        _BX = 0x3932;
        if(pid_current != 0) {
            _BX += 40;
        }
        bomb_bg_fill();
        grcg_off();
        if(frame < 32) {
            reimu_bomb_particle_p = &reimu_bomb_particles[pid_current][frame];
            reimu_bomb_particle_p->active = 1;
            reimu_bomb_particle_p->velocity_y = -96 - randring2_next16_and(127);
            reimu_bomb_particle_p->x = randring2_next16_mod(TO_SP(PLAYFIELD_W));
            reimu_bomb_particle_p->y = TO_SP(384);
        }
        Palettes[pid_current].c.r = frame << 2;
        Palettes[pid_current].c.g = frame * 3;
        Palettes[pid_current].c.b = frame * 3;
        palette_changed = true;
    } else if(frame < 112) {
        if(frame & 1) {
            snd_se_play(16);
        }
        if(frame <= 96) {
            PaletteTone = (frame & 1) * 80 + 100;
            palette_changed = true;
            // Accepted family compiler-compatibility idiom: zero-extended
            // word stack carrier for byte bool formal, not an AX ABI.
            mrs_put_noalpha_8(pid_current * PLAYFIELD_W_BORDERED + PLAYFIELD_LEFT,
                PLAYFIELD_TOP, pid_current + 2, (_AX = pid_current));
        } else {
            PaletteTone = 100;
            palette_changed = true;
        }
        color = frame % 8;
        if((color & 3) < 2) {
            playfield_fg_shift_x[pid_current] = 4;
        } else {
            playfield_fg_shift_x[pid_current] = -4;
        }
    } else {
        playfield_fg_shift_x[pid_current] = 0;
        color = 255 - (frame << 3);
        Palettes[pid_current].c.r = color;
        Palettes[pid_current].c.g = color;
        Palettes[pid_current].c.b = color;
        palette_changed = true;
    }
    egc_on();
    if(frame < 96) {
        reimu_bomb_particles_render();
    }
}
