// Natural Turbo C++ reconstruction candidate for the Rikako contribution to
// TH03 MAIN_05_TEXT. Producer-local storage placement remains outside accepted
// exactness until the complete character-bomb ownership graph is reconstructed.
#pragma codeseg MAIN_05_TEXT

#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/main/v_colors.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

static int line_offset;

extern "C" void far bomb_bg_fill(void);
extern "C" void far pascal bomb_palette_step(int level, pid_t pid);
extern "C" void far pascal bomb_explosion_add(int x, int y, int pid);

void far rikako_bomb(void)
{
	unsigned char frame;
	unsigned char color;
	int x;

	if(bomb_flag[pid_current] == BF_INACTIVE) {
		return;
	}
	frame = bomb_frame[pid_current];
	egc_off();

	if(frame < 64) {
		grcg_setcolor(GC_RMW, pid_current);
		_BX = 0x3932;
		if(pid_current != 0) {
			_BX += 40;
		}
		bomb_bg_fill();
		grcg_off();

		color = (frame << 2);
		bomb_palette_step(color, pid_current);
		line_offset = 0;
	} else if(frame < 128) {
		if((frame & 3) < 2) {
			playfield_fg_shift_x[pid_current] = 4;
		} else {
			playfield_fg_shift_x[pid_current] = -4;
		}

		x = PLAYFIELD_LEFT;
		if(pid_current != 0) {
			x += PLAYFIELD_W_BORDERED;
		}
		mrs_put_noalpha_8(
			x,
			PLAYFIELD_TOP,
			(pid_current + 2),
			(_AX = pid_current)
		);

		grcg_setcolor(GC_RMW, V_WHITE);

		x = playfield_fg_x_to_screen(
			(TO_SP(144) - line_offset), pid_current
		);
		grcg_vline(x, 8, 192);

		x = playfield_fg_x_to_screen(
			(line_offset + TO_SP(144)), pid_current
		);
		grcg_vline(x, 8, 192);

		x = playfield_fg_x_to_screen(
			(TO_SP(144) - (line_offset * 2)), pid_current
		);
		grcg_vline(x, 8, 192);

		x = playfield_fg_x_to_screen(
			((line_offset * 2) + TO_SP(144)), pid_current
		);
		grcg_vline(x, 8, 192);

		line_offset += 0x41;
		if(line_offset >= 0x480) {
			line_offset = 0;
		}

		grcg_off();

		if((frame % 8) == 0) {
			x = randring_far_next16_and(0x3FF);
			for(; x <= 0x1200; x += 0x600) {
				bomb_explosion_add(x, 0x1700, pid_current);
			}
		}

		if((frame % 4) == 0) {
			snd_se_play(5);
		}
	} else {
		playfield_fg_shift_x[pid_current] = 0;
		frame = (255 - (frame << 3));
		color = (frame * 2);
		Palettes[pid_current].c.r = color;
		Palettes[pid_current].c.g = color;
		Palettes[pid_current].c.b = frame;
		palette_changed = true;
	}
	egc_on();
}
