// Natural Turbo C++ reconstruction for the Kana contribution to
// TH03 MAIN_05_TEXT. Full-link proof confirms its CODE/MAP/relocation producer
// behavior; private BSS placement remains open until the complete bomb owner is
// physically reconstructed.
#pragma codeseg MAIN_05_TEXT

#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th03/math/polar.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

static unsigned char angle;

extern "C" void far pascal bomb_palette_step(int level, pid_t pid);
extern "C" void far pascal bomb_center_add(int x, int y, int pid);
extern "C" void far pascal bomb_explosion_add(int x, int y, int pid);

void far kana_bomb(void)
{
	unsigned char frame;
	unsigned char color;
	if(bomb_flag[pid_current] == BF_INACTIVE) {
		return;
	}
	frame = bomb_frame[pid_current];

	if(frame < 64) {
		color = (64 - frame);
		bomb_palette_step(color, pid_current);
		if((frame % 8) == 0) {
			bomb_center_add(TO_SP(144), TO_SP(184), pid_current);
		}
		angle = 0;
		return;
	}

	if(frame < 128) {
		egc_off();
		if((frame & 3) < 2) {
			snd_se_play(10);
			bomb_palette_step(160, pid_current);
			playfield_fg_shift_x[pid_current] = 4;
		} else {
			playfield_fg_shift_x[pid_current] = -4;
			bomb_palette_step(0, pid_current);
		}

		if((frame % 4) == 0) {
			int x;
			int y;
			x = polar(144, 144, CosTable8[angle]);
			y = polar(184, 144, SinTable8[angle]);
			bomb_explosion_add((x << 4), (y << 4), pid_current);

			angle = (0x80 - angle);
			x = polar(144, 144, CosTable8[angle]);
			y = polar(184, 144, SinTable8[angle]);
			bomb_explosion_add((x << 4), (y << 4), pid_current);

			angle = (0x80 - angle);
			angle += 0x10;
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
		egc_on();
		return;
	}

	playfield_fg_shift_x[pid_current] = 0;
	frame = (255 - (frame << 3));
	color = (frame * 2);
	Palettes[pid_current].c.r = color;
	Palettes[pid_current].c.g = color;
	Palettes[pid_current].c.b = frame;
	palette_changed = true;
}
