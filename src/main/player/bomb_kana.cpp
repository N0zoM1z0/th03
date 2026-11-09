// Original source-bound Kana Bomb controller; private angle storage
// belongs to the external Bomb carrier in the physical CODE producer.
#pragma codeseg MAIN_05_TEXT

#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/th03/math/polar.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

#ifdef TH03_BOMB_EXTERNAL_STORAGE
extern unsigned char kana_bomb_angle;
#else
static unsigned char kana_bomb_angle;
#endif

// Original Kana Bomb timeline and circular explosion geometry. These
// byte-timed phases are not the generic shared Bomb lifecycle: the final
// palette calculation intentionally truncates back to `unsigned char`.
enum kana_bomb_timing_t {
    KANA_BOMB_PALETTE_END = 64,
    KANA_BOMB_SHAKE_END = 128,
    KANA_BOMB_CENTER_PERIOD = 8,
    KANA_BOMB_EXPLOSION_PERIOD = 4,
    KANA_BOMB_MIRROR_ANGLE = 0x80,
    KANA_BOMB_CIRCLE_X = 144,
    KANA_BOMB_CIRCLE_Y = 184,
    KANA_BOMB_CIRCLE_RADIUS = 144,
    KANA_BOMB_FADE_WHITE = 255,
    KANA_BOMB_FADE_STEP = 8,
};
typedef char kana_bomb_angle_must_be_byte[(sizeof(kana_bomb_angle) == 1) ? 1 : -1];

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

	if(frame < KANA_BOMB_PALETTE_END) {
		color = (KANA_BOMB_PALETTE_END - frame);
		bomb_palette_step(color, pid_current);
		if(!(frame % KANA_BOMB_CENTER_PERIOD)) {
			bomb_center_add(TO_SP(KANA_BOMB_CIRCLE_X), TO_SP(KANA_BOMB_CIRCLE_Y), pid_current);
		}
		kana_bomb_angle = 0;
		return;
	}

	if(frame < KANA_BOMB_SHAKE_END) {
		egc_off();
		// A natural unsigned %4 shake test is codegen-different here:
		// preserve the actual mask instruction (af684d).
		if((frame & 3) < 2) {
			snd_se_play(10);
			bomb_palette_step(160, pid_current);
			playfield_fg_shift_x[pid_current] = 4;
		} else {
			playfield_fg_shift_x[pid_current] = -4;
			bomb_palette_step(0, pid_current);
		}

		if(!(frame % KANA_BOMB_EXPLOSION_PERIOD)) {
			int x = polar(KANA_BOMB_CIRCLE_X, KANA_BOMB_CIRCLE_RADIUS, CosTable8[kana_bomb_angle]);
			int y = polar(KANA_BOMB_CIRCLE_Y, KANA_BOMB_CIRCLE_RADIUS, SinTable8[kana_bomb_angle]);
			bomb_explosion_add((x * 16), (y * 16), pid_current);

			kana_bomb_angle = (KANA_BOMB_MIRROR_ANGLE - kana_bomb_angle);
			x = polar(KANA_BOMB_CIRCLE_X, KANA_BOMB_CIRCLE_RADIUS, CosTable8[kana_bomb_angle]);
			y = polar(KANA_BOMB_CIRCLE_Y, KANA_BOMB_CIRCLE_RADIUS, SinTable8[kana_bomb_angle]);
			bomb_explosion_add((x * 16), (y * 16), pid_current);

			kana_bomb_angle = (KANA_BOMB_MIRROR_ANGLE - kana_bomb_angle);
			// TC4 must reuse the preceding AL subtraction and store the result.
			// A named enum 0x10 creates an equivalent direct memory ADD
			// instead (native rejected stage af784d).
			kana_bomb_angle += 0x10;
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
		egc_on();
		return;
	}

	playfield_fg_shift_x[pid_current] = 0;
	frame = (KANA_BOMB_FADE_WHITE - (frame * KANA_BOMB_FADE_STEP));
	color = (frame * 2);
	Palettes[pid_current].c.r = color;
	Palettes[pid_current].c.g = color;
	Palettes[pid_current].c.b = frame;
	palette_changed = true;
}
