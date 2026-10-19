// Complete Mima bomb hypothesis, in original target function order.
#pragma codeseg BULLET_TEXT main_04
#pragma option -a1
#include "src/main/player/mima_gameplay.hpp"
#pragma option -a2
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
extern "C" void far bomb_bg_fill(void); // Existing genuine BX hardware ABI.

void far mima_bomb_update(void)
{
    int i;
    if(bomb_flag[pid_current] == BF_INACTIVE) {
        return;
    }
    if(bomb_flag[pid_current] == BF_PREPARING) {
        bomb_flag[pid_current] = BF_ACTIVE;
        bomb_frame[pid_current] = 0;
        for(i = 0; i < 8; i++) {
            mima_bomb_columns[pid_current][i].sprite_offset = 0;
        }
        snd_se_play(18);
    }
    bomb_frame[pid_current]++;
    i = bomb_frame[pid_current] / 8 - 1;
    if(i < 8 && (bomb_frame[pid_current] % 8) == 0) {
        mima_bomb_columns[pid_current][i].x = randring2_next16_mod(TO_SP(PLAYFIELD_W));
        mima_bomb_columns[pid_current][i].sprite_offset =
            (i / 3) * 2 + pid.so_attack + 0x1C;
    }
    if(bomb_frame[pid_current] >= BOMB_FRAMES) {
        bomb_flag[pid_current] = BF_INACTIVE;
        palette_restore_for_pid(pid_current);
    }
}
void near mima_bomb_columns_render(void)
{
    int x;
    mima_bomb_column_p = &mima_bomb_columns[pid_current][0];
    sprite16_put_size.set(16, 16);
    sprite16_clip.reset();
    for(int i = 0; i < 8; i++, mima_bomb_column_p++) {
        if(mima_bomb_column_p->sprite_offset == 0) {
            break; // Target stops on the first uninitialized column.
        }
        x = playfield_fg_x_to_screen(mima_bomb_column_p->x, pid_current);
        sprite16_putx(x, PLAYFIELD_TOP, mima_bomb_column_p->sprite_offset,
            SPF_DOWNWARDS_COLUMN);
    }
}
void far mima_bomb(void)
{
    unsigned char frame;
    unsigned char color;
    if(bomb_flag[pid_current] == BF_INACTIVE) {
        return;
    }
    egc_off();
    frame = bomb_frame[pid_current];
    if(frame <= 80) {
        grcg_setcolor(GC_RMW, pid_current);
        // Hardware boundary: target B39E calls B37C, which copies BX to DI
        // for its VRAM fill. Same maintained Marisa/Reimu helper convention.
        _BX = 0x3932;
        if(pid_current != 0) {
            _BX += 40;
        }
        bomb_bg_fill();
        grcg_off();
        color = 0 - frame * 3;
        Palettes[pid_current].c.r = color;
        Palettes[pid_current].c.g = color;
        Palettes[pid_current].c.b = color;
        palette_changed = true;
        egc_on();
        mima_bomb_columns_render();
    } else if(frame < 144) {
        if((frame & 1) == 0) {
            snd_se_play(16);
            Palettes[pid_current].c.r = 100;
        } else {
            Palettes[pid_current].c.r = 0;
        }
        Palettes[pid_current].c.g = 0;
        Palettes[pid_current].c.b = 0;
        palette_changed = true;
        color = frame % 8;
        if(color == 0) {
            bomb_explosion_add(TO_SP(144), TO_SP(184), pid_current);
        }
        if((color & 3) < 2) {
            playfield_fg_shift_x[pid_current] = 4;
        } else {
            playfield_fg_shift_x[pid_current] = -4;
        }
        // Same-family TC4 caller-lowering compatibility: preserve the bool
        // formal while zero-extending its word stack carrier. The actual
        // callee reads byte [BP+6]; this is not an AX-parameter ABI.
        mrs_put_noalpha_8(pid_current * PLAYFIELD_W_BORDERED +
            playfield_fg_shift_x[pid_current] + PLAYFIELD_LEFT,
            PLAYFIELD_TOP, pid_current + 2, (_AX = pid_current));
    } else {
        playfield_fg_shift_x[pid_current] = 0;
        color = 255 - (frame << 3);
        Palettes[pid_current].c.r = color;
        Palettes[pid_current].c.g = color;
        Palettes[pid_current].c.b = color;
        palette_changed = true;
    }
    egc_on(); // Target also repeats this call on the <=80 branch.
}
