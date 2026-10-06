// Natural Turbo C++ reconstruction for the Chiyuri contribution to
// TH03 MAIN_05_TEXT. Full-link proof confirms its CODE bytes, MAP placement,
// relocation sites, and relocation order. It stays outside the accepted graph
// until the complete character-bomb owner passes aggregate acceptance.
#pragma codeseg MAIN_05_TEXT

#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

extern "C" void far bomb_bg_fill(void);
extern "C" void far pascal bomb_palette_step(int level, pid_t pid);
extern "C" void far pascal bomb_center_add(int x, int y, int pid);
extern "C" void far pascal bomb_axis_add(int x, int y, int pid);

void far chiyuri_bomb(void)
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
		_BX = 0x3932;
		if(pid_current != 0) {
			_BX += 40;
		}
		bomb_bg_fill();
		grcg_off();

		color = (255 - (frame << 2));
		bomb_palette_step(color, pid_current);
		if((frame % 8) == 0) {
			bomb_center_add(TO_SP(144), TO_SP(184), pid_current);
		}
	} else if(frame < 144) {
		palette_changed = true;
		if((frame & 3) < 2) {
			PaletteTone = 60;
			palette_changed = true;
			playfield_fg_shift_x[pid_current] = 4;
		} else {
			playfield_fg_shift_x[pid_current] = -4;
			PaletteTone = 120;
			palette_changed = true;
		}

		if((frame % 16) == 0) {
			snd_se_play(10);
			int distance = (((frame - 64) * 2) << 4);
			bomb_axis_add((TO_SP(144) - distance), TO_SP(184), pid_current);
			bomb_axis_add((TO_SP(144) + distance), TO_SP(184), pid_current);
			bomb_axis_add(TO_SP(144), (TO_SP(184) - distance), pid_current);
			bomb_axis_add(TO_SP(144), (TO_SP(184) + distance), pid_current);
		}

		int left = PLAYFIELD_LEFT;
		if(pid_current != 0) {
			left += PLAYFIELD_W_BORDERED;
		}
		mrs_put_noalpha_8(
			left,
			PLAYFIELD_TOP,
			(pid_current + 2),
			(_AX = pid_current)
		);
	} else {
		PaletteTone = 100;
		palette_changed = true;
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
