// Original source-bound Kotohime Bomb controller; its two-byte explosion
// Y private state belongs to the separately preserved Bomb data carrier.
#pragma codeseg MAIN_05_TEXT

#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

#ifdef TH03_BOMB_EXTERNAL_STORAGE
extern int kotohime_bomb_explosion_y;
#else
static int kotohime_bomb_explosion_y;
#endif

// Two original palette/flash phases and a real 96-pixel explosion row.
// These are source-only integer constants; the two-byte explosion-Y state
// remains in its historical external Bomb carrier, not newly allocated.
enum kotohime_bomb_native_phase_t {
    KOTO_BOMB_PALETTE_START_END = 64,
    KOTO_BOMB_SHAKE_END = 128,
    KOTO_BOMB_EXPLOSION_TICK_PERIOD = 8,
    KOTO_BOMB_ROW_CLOCK_PERIOD = 16,
    KOTO_BOMB_ROW_END_X = TO_SP(288),
    KOTO_BOMB_ROW_STEP_X = TO_SP(96),
    KOTO_BOMB_ROW_Y_DECAY = 0x2E0,
    KOTO_BOMB_FIRST_EXPLOSION_X = 0x11B8,
    KOTO_BOMB_FIRST_EXPLOSION_X_STEP = 0x48,
    KOTO_BOMB_FIRST_EXPLOSION_Y_STEP = 0x5C,
};

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

	if(frame < KOTO_BOMB_PALETTE_START_END) {
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

		// Exact native byte `%8` truth test; original TC4 preserves
		// the 8-frame first-phase explosion trigger (af870c).
		if(!(frame % KOTO_BOMB_EXPLOSION_TICK_PERIOD)) {
			x = (
				KOTO_BOMB_FIRST_EXPLOSION_X -
				(frame * KOTO_BOMB_FIRST_EXPLOSION_X_STEP)
			);
			kotohime_bomb_explosion_y = (
				(frame * KOTO_BOMB_FIRST_EXPLOSION_Y_STEP) +
				KOTO_BOMB_FIRST_EXPLOSION_Y_STEP
			);
			bomb_explosion_add(x, kotohime_bomb_explosion_y, pid_current);
		}
	} else if(frame < KOTO_BOMB_SHAKE_END) {
		palette_changed = true;
		// Unlike the above byte `%8` test, this original byte `&3`
		// *cannot* be written as `%4` without changing TC4 CODE
		// (fresh original negative compiler stage af870b).
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

		if(!(frame % KOTO_BOMB_EXPLOSION_TICK_PERIOD)) {
			x = 0;
			// This apparently dead signed 16-bit index still generates
			// original machine CODE. Eliminating it changed 528 -> 505
			// bytes in genuine TC4 negative trial af870e.
			i = ((frame % KOTO_BOMB_ROW_CLOCK_PERIOD) / 2);
			while(x <= KOTO_BOMB_ROW_END_X) {
				bomb_explosion_add(x, kotohime_bomb_explosion_y, pid_current);
				x += KOTO_BOMB_ROW_STEP_X;
				++i;
			}
			kotohime_bomb_explosion_y -= KOTO_BOMB_ROW_Y_DECAY;
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
		frame = (255 - (frame * 8));

		// This original fade branch reads an uninitialized stack byte.
		// Do NOT initialize `color`: it is genuinely undefined C++
		// behavior retained because it is what the historical target does.
		// No invented defensive product fix or zero fill is justified.
		color = (color * 2);
		Palettes[pid_current].c.r = color;
		Palettes[pid_current].c.g = color;
		Palettes[pid_current].c.b = frame;
		palette_changed = true;
	}
	egc_on();
}
