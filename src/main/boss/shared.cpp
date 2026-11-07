// Maintained natural Turbo C++ reconstruction candidate for the complete
// shared boss-helper prefix of TH03 MAIN_03_TEXT.
#include "src/main/math/polar.hpp"
#include "src/main/player/combo.hpp"
#include "src/main/player/score_add.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include <dos.h>

#pragma codeseg MAIN_03_TEXT
#include "src/main/boss/shared.hpp"
#pragma option -a2

// Shared controller copies the identical physical per-player BOSS record.
#include "src/main/boss/template_state.hpp"
typedef boss_template_state_t boss_state_t;

// Bounds and rewards are global to the shared boss controller, not
// character-specific attacks. These remain compile-time 16-bit constants.
enum boss_shared_limits_t {
    BOSS_TURN_LEFT_X = 0x300,
    BOSS_TURN_RIGHT_X = 0xF00,
    BOSS_HORIZONTAL_STEP = 0x20,
    BOSS_DESCEND_STEP = 0x20,
    BOSS_DESPAWN_Y = 0x1A00,
    BOSS_PATTERN_WAIT_FRAMES = 0x50,
    BOSS_COMBO_POINTS = 5120,
};

extern boss_state_t boss_state;
extern boss_state_t boss_character_template[PLAYER_COUNT];

extern int SinTable8[256];
extern int CosTable8[256];

extern int boss_center_x;
extern int boss_center_y;
extern int boss_velocity_x;
extern int boss_velocity_y;
extern int boss_hp;
extern unsigned char boss_mode;
extern unsigned char boss_angle;
extern unsigned char boss_pattern_i;
extern unsigned char boss_pattern_count;
extern unsigned int boss_frame;

extern int boss_active[PLAYER_COUNT];
extern unsigned char boss_pattern_previous;
extern int boss_target_x;
extern int boss_target_y;

extern "C" void far pascal palette_restore_for_pid(pid_t pid);

signed char near pascal boss_explosion_ring(int x, int y, int length);

#ifndef TH03_BOSS_SHARED_REST_ONLY
signed char near pascal boss_explosion_ring(
	int x, int y, int length
)
{
	screen_x_t left;
	screen_y_t top;
	unsigned char angle;
	register int i;

	if(length == 1) {
		snd_se_play(16);
	}

	x = playfield_fg_x_to_screen(x, (1 - pid_current));
	y = ((y >> 4) + PLAYFIELD_TOP);
	length *= 8;
	angle = length;

	// Native TC4 distinguishes pid_current==1 from if(pid_current)
    // in this physical ring producer (negative control af708d).
    // Preserve the target's direct PID comparison instead of expanding the
	// generic (1 - pid) clip macro through a temporary register.
	if(pid_current == 1) {
		sprite16_clip.set_for_pid_0();
	} else {
		sprite16_clip.set_for_pid_1();
	}
	sprite16_put_size.set(48, 48);

	for(i = 0; i < 16; (++i, angle += 0x10)) {
		left = (polar(x, length, CosTable8[angle]) - 24);
		top = (polar(y, length, SinTable8[angle]) - 24);
		sprite16_put(left, top, 0x1930);
	}

	angle = (0 - (unsigned char)length);
	for(i = 0; i < 8; (++i, angle += 0x20)) {
		left = (polar(x, (length * 2), CosTable8[angle]) - 24);
		top = (polar(y, (length * 2), SinTable8[angle]) - 24);
		sprite16_put(left, top, 0x1930);
	}

	if(length >= 0xC8) {
		score_add(2560, (1 - pid_current));
		return 0;
	}
	return -1;
}

#endif

#ifndef TH03_BOSS_SHARED_RING_ONLY
extern "C" void near boss_move_sine(void)
{
	boss_center_x += boss_velocity_x;
	boss_center_y += boss_velocity_y;
	// This 8-bit angle increment must stay postfix: prefix changes the
    // native shared controller output (af708b).
    boss_angle++;
	boss_velocity_y = polar(0, 16, SinTable8[boss_angle]);

	if(boss_center_x <= BOSS_TURN_LEFT_X) {
		boss_velocity_x = BOSS_HORIZONTAL_STEP;
		return;
	}
	if(boss_center_x >= BOSS_TURN_RIGHT_X) {
		boss_velocity_x = -BOSS_HORIZONTAL_STEP;
	}
}

extern "C" void near boss_fall(void)
{
	boss_center_x += boss_velocity_x;
	boss_center_y += BOSS_DESCEND_STEP;

	if(boss_center_x <= BOSS_TURN_LEFT_X) {
		boss_velocity_x = BOSS_HORIZONTAL_STEP;
	} else if(boss_center_x >= BOSS_TURN_RIGHT_X) {
		boss_velocity_x = -BOSS_HORIZONTAL_STEP;
	}

	boss_active[1 - pid_current] = 0;
	if(boss_center_y >= BOSS_DESPAWN_Y) {
		boss_mode = 0;
		gba_boss_launched_by = PID_NONE;
		combo_points_for_boss_attack = BOSS_COMBO_POINTS;
	}
}

extern "C" unsigned char near boss_update_start(void)
{
	if(gba_flag_active[pid_current] != GBAF_BOSS) {
		return 0;
	}

	if(gba_boss_launched_by == PID_NONE) {
		// The original TC4 producer performs this fixed 32-byte state copy
		// inline with SI/DI and REP MOVSW rather than calling F_SCOPY@.
		_SI = FP_OFF(&boss_character_template[0]);
		if(pid_current == 1) {
			_SI += sizeof(boss_state_t);
		}
		_DI = FP_OFF(&boss_state);
		_AX = _DS;
		_ES = _AX;
		_CX = (sizeof(boss_state_t) / 2);
		asm { rep movsw }
		boss_pattern_count = (randring_far_next16_and(7) + 1);
		boss_frame = 0;
		gba_boss_launched_by = pid_current;
		gba_flag_active[pid_current] = GBAF_NONE;
		snd_se_play(18);
		palette_restore_for_pid(1 - pid_current);
		boss_active[1 - pid_current] = 1;
		return 1;
	}

	if(boss_mode != static_cast<unsigned char>(-1)) {
		boss_mode = -1;
		boss_frame = 0;
		palette_restore_for_pid(1 - pid_current);
		boss_active[pid_current] = 0;
	}
	return 0;
}

extern "C" void far boss_hittest_end(void)
{
	pid_t pid_other = (1 - pid_current);

	if((boss_hp <= 0) && (boss_mode != static_cast<unsigned char>(-1))) {
		boss_mode = -1;
		boss_frame = 0;
		palette_restore_for_pid(pid_other);
		if(gba_flag_active[pid_other] != GBAF_BOSS) {
			combo_points_for_boss_attack = BOSS_COMBO_POINTS;
		}
		boss_active[pid_other] = 0;
		if(gba_boss_level < GBA_BOSS_LEVEL_MAX) {
			gba_boss_level++;
		}
	}
}

extern "C" void near boss_target_update(void)
{
	if(boss_mode != 0x80) {
		boss_target_x = boss_center_x;
		boss_target_y = (boss_center_y + 0x800);
	}
}

extern "C" void near boss_pattern_next(void)
{
	unsigned char pattern;

	boss_move_sine();
	if(boss_frame < BOSS_PATTERN_WAIT_FRAMES) {
		return;
	}

	do {
		pattern = randring_far_next16_and(0x0F);
	} while(
		((boss_pattern_previous + 2) >= pattern) &&
		((boss_pattern_previous - 2) <= pattern)
	);

	boss_pattern_previous = pattern;
	boss_frame = 0;
	boss_mode = (pattern + 2);
	// The BOSS pattern-index postfix is also codegen-visible;
    // ++boss_pattern_i failed original TC4 bytes (af708c).
    boss_pattern_i++;
	if(boss_pattern_i > boss_pattern_count) {
		boss_mode = 0x80;
	}
}

extern "C" void near boss_explosion_render(void)
{
	boss_mode = boss_explosion_ring(boss_center_x, boss_center_y, boss_frame);
	if(!boss_mode) {
		gba_boss_launched_by = PID_NONE;
	}
}
#endif
