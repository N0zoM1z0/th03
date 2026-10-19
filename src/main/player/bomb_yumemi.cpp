// Natural complete-function proposal. Original 698-byte P_COMBO_TEXT owner.
// All storage remains external; this file does not claim DATA/BSS ownership.
#pragma codeseg P_COMBO_TEXT main_04
#pragma option -a1
#include "src/main/player/yumemi_gameplay.hpp"
#pragma option -a2
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "src/main/math/polar.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

void far yumemi_bomb(void)
{
    int playfield_left;
    int x[3];
    int y[3];
    unsigned char frame;
    unsigned char color;
    int i;
    int radius;

    if(bomb_flag[pid_current] == BF_INACTIVE) {
        return;
    }
    egc_off();
    frame = bomb_frame[pid_current];
    if(frame <= 64) {
        if(frame < 32) {
            radius = 224 - frame * 3;
            grcg_setcolor(GC_RMW, 8);
        } else {
            radius = 128;
            grcg_setcolor(GC_RMW, 7);
        }
        // GRC triangle coordinates use the 200-line vertical domain here.
        if(pid_current == 0) {
            grc_setclip(16, 8, 303, 191);
            playfield_left = 16;
        } else {
            grc_setclip(336, 8, 623, 191);
            playfield_left = 336;
        }
        for(i = 0; i < 3; i++) {
            x[i] = polar(144, radius, CosTable8[yumemi_bomb_triangle_angles[i]])
                + playfield_left;
            y[i] = polar(200, radius, SinTable8[yumemi_bomb_triangle_angles[i]]) / 2;
        }
        grcg_triangle(x[0], y[0], x[1], y[1], x[2], y[2]);
        if(frame > 32) {
            radius = 320 - frame * 3;
            grcg_setcolor(GC_RMW, 8);
            for(i = 3; i < 6; i++) {
                x[i - 3] = polar(
                    144, radius, CosTable8[yumemi_bomb_triangle_angles[i]]
                ) + playfield_left;
                y[i - 3] = polar(
                    200, radius, SinTable8[yumemi_bomb_triangle_angles[i]]
                ) / 2;
            }
            grcg_triangle(x[0], y[0], x[1], y[1], x[2], y[2]);
        }
        grc_setclip(0, 0, 639, 199);
        grcg_off();
        color = frame << 2;
    } else if(frame < 144) {
        if((frame & 7) == 0) {
            snd_se_play(5);
            PaletteTone = 140;
            palette_show();
            bomb_axis_add(TO_SP(144), TO_SP(184), pid_current);
        } else {
            PaletteTone = 60;
            palette_show();
        }
        color = frame % 8;
        if((color & 3) < 2) {
            playfield_fg_shift_x[pid_current] = 4;
        } else {
            playfield_fg_shift_x[pid_current] = -4;
        }
        // Target updates the shift state but does not add it to this MRS x.
        // Established MRS bool argument has a word stack carrier; _AX merely
        // preserves that caller promotion and does not invent a register ABI.
        mrs_put_noalpha_8(
            pid_current * PLAYFIELD_W_BORDERED + PLAYFIELD_LEFT,
            PLAYFIELD_TOP, pid_current + 2, (_AX = pid_current)
        );
        egc_on();
        return;
    } else {
        PaletteTone = 100;
        palette_show();
        playfield_fg_shift_x[pid_current] = 0;
        color = 255 - (frame << 3);
    }
    Palettes[pid_current].c.r = color;
    Palettes[pid_current].c.g = color;
    Palettes[pid_current].c.b = color;
    palette_changed = true;
    egc_on();
}
