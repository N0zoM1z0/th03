// Source-native complete Yumemi triangle/GRCG Bomb producer.
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

// The two three-vertex triangles have separate first/second phases.
// Preserve the original unadjusted 200-line vertical raster domain
// and the explicit original shift-mask shake comparison.
enum yumemi_bomb_phase_t {
    YUMEMI_BOMB_TRIANGLE_FIRST_END = 32,
    YUMEMI_BOMB_TRIANGLE_FINAL_FRAME = 64,
    YUMEMI_BOMB_SECOND_TRIANGLE_START = 32,
    YUMEMI_BOMB_SHAKE_END = 144,
    YUMEMI_BOMB_VERTICES_PER_TRIANGLE = 3,
    YUMEMI_BOMB_BOTH_TRIANGLES = 6,
    YUMEMI_BOMB_FIRST_RADIUS = 224,
    YUMEMI_BOMB_SECOND_RADIUS = 320,
    YUMEMI_BOMB_RADIUS_DECAY = 3,
    YUMEMI_BOMB_CENTER_X = 144,
    YUMEMI_BOMB_RASTER_ORIGIN_Y = 200,
    YUMEMI_BOMB_RASTER_HALF_Y_DIVISOR = 2,
};

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
    if(frame <= YUMEMI_BOMB_TRIANGLE_FINAL_FRAME) {
        if(frame < YUMEMI_BOMB_TRIANGLE_FIRST_END) {
            radius = YUMEMI_BOMB_FIRST_RADIUS - frame * YUMEMI_BOMB_RADIUS_DECAY;
            grcg_setcolor(GC_RMW, 8);
        } else {
            radius = 128;
            grcg_setcolor(GC_RMW, 7);
        }
        // GRC triangle coordinates use the 200-line vertical domain here.
        if(!pid_current) {
            grc_setclip(16, 8, 303, 191);
            playfield_left = 16;
        } else {
            grc_setclip(336, 8, 623, 191);
            playfield_left = 336;
        }
        for(i = 0; i < YUMEMI_BOMB_VERTICES_PER_TRIANGLE; ++i) {
            x[i] = polar(YUMEMI_BOMB_CENTER_X, radius, CosTable8[yumemi_bomb_triangle_angles[i]])
                + playfield_left;
            y[i] = polar(YUMEMI_BOMB_RASTER_ORIGIN_Y, radius, SinTable8[yumemi_bomb_triangle_angles[i]]) / YUMEMI_BOMB_RASTER_HALF_Y_DIVISOR;
        }
        grcg_triangle(x[0], y[0], x[1], y[1], x[2], y[2]);
        if(frame > YUMEMI_BOMB_SECOND_TRIANGLE_START) {
            radius = YUMEMI_BOMB_SECOND_RADIUS - frame * YUMEMI_BOMB_RADIUS_DECAY;
            grcg_setcolor(GC_RMW, 8);
            for(i = YUMEMI_BOMB_VERTICES_PER_TRIANGLE; i < YUMEMI_BOMB_BOTH_TRIANGLES; ++i) {
                x[i - YUMEMI_BOMB_VERTICES_PER_TRIANGLE] = polar(
                    YUMEMI_BOMB_CENTER_X, radius, CosTable8[yumemi_bomb_triangle_angles[i]]
                ) + playfield_left;
                y[i - YUMEMI_BOMB_VERTICES_PER_TRIANGLE] = polar(
                    YUMEMI_BOMB_RASTER_ORIGIN_Y, radius, SinTable8[yumemi_bomb_triangle_angles[i]]
                ) / YUMEMI_BOMB_RASTER_HALF_Y_DIVISOR;
            }
            grcg_triangle(x[0], y[0], x[1], y[1], x[2], y[2]);
        }
        grc_setclip(0, 0, 639, 199);
        grcg_off();
        color = frame * 4;
    } else if(frame < YUMEMI_BOMB_SHAKE_END) {
        if((static_cast<unsigned int>(frame) % 8) == 0) {
            snd_se_play(5);
            PaletteTone = 140;
            palette_show();
            bomb_axis_add(TO_SP(144), TO_SP(184), pid_current);
        } else {
            PaletteTone = 60;
            palette_show();
        }
        color = frame % 8;
        // The typed unsigned %4 form was original-native-unequal (af687f);
        // retain this exact original shake mask.
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
        color = 255 - (frame * 8);
    }
    Palettes[pid_current].c.r = color;
    Palettes[pid_current].c.g = color;
    Palettes[pid_current].c.b = color;
    palette_changed = true;
    egc_on();
}
