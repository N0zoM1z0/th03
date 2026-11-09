// Complete current native-source C++ for Rikako Bomb's original
// MAIN_05_TEXT physical owner. The original private line-offset state
// remains at its historical DGROUP carrier address.
#pragma codeseg MAIN_05_TEXT

#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/main/v_colors.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

#ifdef TH03_BOMB_EXTERNAL_STORAGE
extern int rikako_bomb_line_offset;
#else
static int rikako_bomb_line_offset;
#endif

extern "C" void far bomb_bg_fill(void);
extern "C" void far pascal bomb_palette_step(int level, pid_t pid);
extern "C" void far pascal bomb_explosion_add(int x, int y, int pid);

// Original two-phase palette/quake window, eight-frame explosion row and
// the physical 0x480 subpixel line-offset reset. No new state is allocated.
enum rikako_bomb_native_timing_t {
    RIKAKO_BOMB_FIRST_PHASE_END = 64,
    RIKAKO_BOMB_SHAKE_PHASE_END = 128,
    RIKAKO_BOMB_EXPLOSION_PERIOD = 8,
    RIKAKO_BOMB_SFX_PERIOD = 4,
    RIKAKO_BOMB_ROW_END_X = TO_SP(288),
    RIKAKO_BOMB_ROW_STEP_X = TO_SP(96),
    RIKAKO_BOMB_EXPLOSION_Y = 0x1700,
    RIKAKO_BOMB_OFFSET_STEP = 0x41,
    RIKAKO_BOMB_OFFSET_RESET = 0x480,
};

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

	if(frame < RIKAKO_BOMB_FIRST_PHASE_END) {
		grcg_setcolor(GC_RMW, pid_current);
		_BX = 0x3932;
		if(pid_current) {
			_BX += 40;
		}
		bomb_bg_fill();
		grcg_off();

		color = (frame * 4);
		bomb_palette_step(color, pid_current);
		rikako_bomb_line_offset = 0;
	} else if(frame < RIKAKO_BOMB_SHAKE_PHASE_END) {
		// The byte shake uses its original &3, not byte %4:
		// actual TC4 rejects that rewrite (af894c).
		if((frame & 3) < 2) {
			playfield_fg_shift_x[pid_current] = 4;
		} else {
			playfield_fg_shift_x[pid_current] = -4;
		}

		x = PLAYFIELD_LEFT;
		if(pid_current) {
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
			(TO_SP(144) - rikako_bomb_line_offset), pid_current
		);
		grcg_vline(x, 8, 192);

		x = playfield_fg_x_to_screen(
			(rikako_bomb_line_offset + TO_SP(144)), pid_current
		);
		grcg_vline(x, 8, 192);

		x = playfield_fg_x_to_screen(
			(TO_SP(144) - (rikako_bomb_line_offset * 2)), pid_current
		);
		grcg_vline(x, 8, 192);

		x = playfield_fg_x_to_screen(
			((rikako_bomb_line_offset * 2) + TO_SP(144)), pid_current
		);
		grcg_vline(x, 8, 192);

		// This is a live signed word line-offset, not a byte frame.
		// The original +0x41 and >=0x480 reset are separately tested.
		rikako_bomb_line_offset += RIKAKO_BOMB_OFFSET_STEP;
		if(RIKAKO_BOMB_OFFSET_RESET <= rikako_bomb_line_offset) {
			rikako_bomb_line_offset = 0;
		}

		grcg_off();

		// The original randomized starting point and 96-pixel spacing
		// must be preserved across the 288-pixel-wide row.
		// This *different* eight-frame event accepts natural
		// `if(!remainder)` under original TC4 (af894b).
		if(!(frame % RIKAKO_BOMB_EXPLOSION_PERIOD)) {
			x = randring_far_next16_and(0x3FF);
			// Real 96-pixel explosion row, starting at the original RNG
			// position and advancing after each explosion in the for header.
			for(; x <= RIKAKO_BOMB_ROW_END_X; x += RIKAKO_BOMB_ROW_STEP_X) {
				bomb_explosion_add(x, RIKAKO_BOMB_EXPLOSION_Y, pid_current);
			}
		}

		if(!(frame % RIKAKO_BOMB_SFX_PERIOD)) {
			snd_se_play(5);
		}
	} else {
		playfield_fg_shift_x[pid_current] = 0;
		frame = (255 - (frame * 8));
		color = (frame * 2);
		Palettes[pid_current].c.r = color;
		Palettes[pid_current].c.g = color;
		Palettes[pid_current].c.b = frame;
		palette_changed = true;
	}
	egc_on();
}
