// Source-native complete original Chiyuri bomb state machine.
// Arithmetic phase geometry uses the original two-stage 16-bit order.
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

// The original two-stage byte palette and four signed Cartesian
// explosion axes; compile-time enum values do not allocate DATA.
enum chiyuri_bomb_physical_t {
    CHIYURI_BOMB_PALETTE_END = 64,
    CHIYURI_BOMB_SHAKE_END = 144,
    CHIYURI_BOMB_WARNING_PERIOD = 8,
    CHIYURI_BOMB_AXIS_PERIOD = 16,
    CHIYURI_BOMB_CENTER_X = TO_SP(144),
    CHIYURI_BOMB_CENTER_Y = TO_SP(184),
};

void far chiyuri_bomb(void)
{
	unsigned char frame;
	unsigned char color;

	// The original inactive enum is zero; natural truth negation
	// is exact under genuine TC4 (af926g).
	if(!bomb_flag[pid_current]) {
		return;
	}
	egc_off();
	frame = bomb_frame[pid_current];

	// The first 64 byte frames own the original palette/center warnings;
	// do not reorder the GRCG disable/fill/enable sequence.
	if(frame < CHIYURI_BOMB_PALETTE_END) {
		grcg_setcolor(GC_RMW, pid_current);
		_BX = 0x3932;
		// Explicit player-byte truth checks select the original
		// page/VRAM offset, native exact at both sites (af926b).
		if(pid_current) {
			_BX += 40;
		}
		bomb_bg_fill();
		grcg_off();

		color = (255 - (frame * 4));
		bomb_palette_step(color, pid_current);
		// Byte modulo zero cadence accepts the natural predicate;
		// keep the one far-pascal explosion-add call (af926a/d).
		if(!(frame % CHIYURI_BOMB_WARNING_PERIOD)) {
			bomb_center_add(CHIYURI_BOMB_CENTER_X, CHIYURI_BOMB_CENTER_Y, pid_current);
		}
	} else if(frame < CHIYURI_BOMB_SHAKE_END) {
		palette_changed = true;
		// The original frame&3 shake comparison is codegen-visible:
		// unsigned %4 changed original CODE (af682d).
		// This *different* byte shake cadence must retain &3:
		// substituting %4 changed native CODE in fresh af926c.
		if((frame & 3) < 2) {
			PaletteTone = 60;
			palette_changed = true;
			playfield_fg_shift_x[pid_current] = 4;
		} else {
			playfield_fg_shift_x[pid_current] = -4;
			PaletteTone = 120;
			palette_changed = true;
		}

		// Four physical signed Cartesian axis explosions share this
		// 16-frame cadence and one original sound event.
		if(!(frame % CHIYURI_BOMB_AXIS_PERIOD)) {
			snd_se_play(10);
			// Preserve two successive 16-bit multiplications, not
			// a single equivalent *32 (real original negative af926e).
			int distance = (((frame - CHIYURI_BOMB_PALETTE_END) * 2) * 16);
			bomb_axis_add((CHIYURI_BOMB_CENTER_X - distance), CHIYURI_BOMB_CENTER_Y, pid_current);
			bomb_axis_add((CHIYURI_BOMB_CENTER_X + distance), CHIYURI_BOMB_CENTER_Y, pid_current);
			bomb_axis_add(CHIYURI_BOMB_CENTER_X, (CHIYURI_BOMB_CENTER_Y - distance), pid_current);
			bomb_axis_add(CHIYURI_BOMB_CENTER_X, (CHIYURI_BOMB_CENTER_Y + distance), pid_current);
		}

		int left = PLAYFIELD_LEFT;
		if(pid_current) {
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

		frame = (255 - (frame * 8));
		color = (frame * 2);
		Palettes[pid_current].c.r = color;
		Palettes[pid_current].c.g = color;
		Palettes[pid_current].c.b = frame;
		palette_changed = true;
	}
	egc_on();
}
