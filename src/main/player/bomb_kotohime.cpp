// Natural Turbo C++ reconstruction for the Kotohime contribution to
// TH03 MAIN_05_TEXT. Full-link proof confirms its CODE/MAP/relocation producer
// behavior; the two-byte private BSS placement remains outside exactness.
#pragma codeseg MAIN_05_TEXT

#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

static int explosion_y;

extern "C" void far bomb_bg_fill(void);
extern "C" void far pascal bomb_explosion_add(int x, int y, int pid);

void far kotohime_bomb(void)
{
	unsigned char frame;
	unsigned char color;
	int x;
	int i;

	if(bomb_flag[pid_current] == BF_INACTIVE) {
		return;
	}
	egc_off();
	frame = bomb_frame[pid_current];

	if(frame < 64) {
		grcg_setcolor(GC_RMW, pid_current);
		_BX = 0x3932;
		if(pid_current != 0) {
			_BX += 40;
		}
		bomb_bg_fill();
		grcg_off();

		color = (frame * 3);
		Palettes[pid_current].c.r = (color + 64);
		Palettes[pid_current].c.g = (color + 32);
		Palettes[pid_current].c.b = color;
		palette_changed = true;

		if((frame % 8) == 0) {
			x = (0x11B8 - (frame * 0x48));
			explosion_y = ((frame * 0x5C) + 0x5C);
			bomb_explosion_add(x, explosion_y, pid_current);
		}
	} else if(frame < 128) {
		palette_changed = true;
		if((frame & 3) < 2) {
			snd_se_play(10);
			PaletteTone = 170;
			palette_changed = true;
			playfield_fg_shift_x[pid_current] = 4;
		} else {
			playfield_fg_shift_x[pid_current] = -4;
			PaletteTone = 100;
			palette_changed = true;
		}

		if((frame % 8) == 0) {
			x = 0;
			i = ((frame % 16) / 2);
			for(; x <= 0x1200; (x += 0x600, i++)) {
				bomb_explosion_add(x, explosion_y, pid_current);
			}
			explosion_y -= 0x2E0;
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
	} else {
		PaletteTone = 100;
		palette_changed = true;
		playfield_fg_shift_x[pid_current] = 0;
		frame = (255 - (frame << 3));

		// Target behavior: color is read from the uninitialized stack local here.
		color = (color * 2);
		Palettes[pid_current].c.r = color;
		Palettes[pid_current].c.g = color;
		Palettes[pid_current].c.b = frame;
		palette_changed = true;
	}
	egc_on();
}
