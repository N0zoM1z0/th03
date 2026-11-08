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
    BOSS_EXPLODE_MODE = 0xFF,
    BOSS_DESCEND_MODE = 0x80,
    BOSS_PATTERN_VARIANTS_MASK = 0x0F,
    BOSS_PATTERN_RECENT_RADIUS = 2,
    BOSS_PATTERN_MODE_OFFSET = 2,
    BOSS_PATTERN_COUNT_MASK = 7,
    BOSS_PATTERN_COUNT_BASE = 1,
    BOSS_RING_PRIMARY_SPRITES = 16,
    BOSS_RING_PRIMARY_ANGLE_STEP = 0x10,
    BOSS_RING_SECONDARY_ANGLE_STEP = 0x20,
    BOSS_RING_SPRITE_SIZE = 48,
    BOSS_RING_SPRITE_HALF = 24,
    BOSS_RING_SECONDARY_SPRITES = 8,
    BOSS_RING_SECONDARY_RADIUS_SCALE = 2,
    BOSS_RING_SPRITE_OFFSET = 0x1930,
    BOSS_RING_FINISH_RADIUS = 0xC8,
    BOSS_RING_LENGTH_SCALE = 8,
    BOSS_RING_REWARD = 2560,
    BOSS_RING_START_SOUND = 16,
    BOSS_TARGET_Y_AHEAD = 0x800,
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
	register unsigned char angle;
	register int i;

	if(1 == length) {
		snd_se_play(BOSS_RING_START_SOUND);
	}

	x = playfield_fg_x_to_screen(x, (1 - pid_current));
	y = (PLAYFIELD_TOP + (y >> 4));
	// Original multiply encoding cannot be replaced by <<=3
	// (rejected complete original ring in af768d).
	// Explicit `length = length * 8` changes native CODE (af916g);
	// keep the original signed-word compound multiplication.
	length *= BOSS_RING_LENGTH_SCALE;
	angle = static_cast<unsigned char>(length);

	// Native TC4 distinguishes pid_current==1 from if(pid_current)
	// in this physical ring producer (negative control af708d).
	// Preserve the direct PID comparison rather than expanding the generic
	// (1 - pid) clip macro through a temporary register.
	if(1 == pid_current) {
		sprite16_clip.set_for_pid_0();
	} else {
		sprite16_clip.set_for_pid_1();
	}
	sprite16_put_size.set(BOSS_RING_SPRITE_SIZE, BOSS_RING_SPRITE_SIZE);

	// Sixteen primary sprites: the for-header preserves the original
	// post-draw signed-index then byte-angle update order.
	for(i = 0; i < BOSS_RING_PRIMARY_SPRITES; i++, angle = angle + BOSS_RING_PRIMARY_ANGLE_STEP) {
		left = (-BOSS_RING_SPRITE_HALF + polar(x, length, CosTable8[angle]));
		top = (-BOSS_RING_SPRITE_HALF + polar(y, length, SinTable8[angle]));
		sprite16_put(left, top, BOSS_RING_SPRITE_OFFSET);
	}

	// Signed-angle two-operand subtraction remains byte-critical:
	// direct unary minus changed original CODE (af768e).
	angle = static_cast<unsigned char>(0 - static_cast<unsigned char>(length));
	// Eight secondary sprites at double radius. Binary zero-minus
	// before this for-header differs from unary minus (af916d).
	for(i = 0; i < BOSS_RING_SECONDARY_SPRITES; i++, angle = angle + BOSS_RING_SECONDARY_ANGLE_STEP) {
		left = (-BOSS_RING_SPRITE_HALF + polar(x, (BOSS_RING_SECONDARY_RADIUS_SCALE * length), CosTable8[angle]));
		top = (-BOSS_RING_SPRITE_HALF + polar(y, (BOSS_RING_SECONDARY_RADIUS_SCALE * length), SinTable8[angle]));
		sprite16_put(left, top, BOSS_RING_SPRITE_OFFSET);
	}

	if(BOSS_RING_FINISH_RADIUS <= length) {
		score_add(BOSS_RING_REWARD, (1 - pid_current));
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
    // Keep byte postfix; prefix changed actual TC4 CODE (af916e).
	boss_angle++;
	boss_velocity_y = polar(0, 16, SinTable8[boss_angle]);

	if(BOSS_TURN_LEFT_X >= boss_center_x) {
		boss_velocity_x = BOSS_HORIZONTAL_STEP;
	} else if(BOSS_TURN_RIGHT_X <= boss_center_x) {
		boss_velocity_x = -BOSS_HORIZONTAL_STEP;
	}
}

extern "C" void near boss_fall(void)
{
	boss_center_x += boss_velocity_x;
	boss_center_y += BOSS_DESCEND_STEP;

	if(BOSS_TURN_LEFT_X >= boss_center_x) {
		boss_velocity_x = BOSS_HORIZONTAL_STEP;
	} else if(BOSS_TURN_RIGHT_X <= boss_center_x) {
		boss_velocity_x = -BOSS_HORIZONTAL_STEP;
	}

	boss_active[1 - pid_current] = 0;
	if(BOSS_DESPAWN_Y > boss_center_y) {
		return;
	}
	boss_mode = 0;
	gba_boss_launched_by = PID_NONE;
	combo_points_for_boss_attack = BOSS_COMBO_POINTS;
}

extern "C" unsigned char near boss_update_start(void)
{
	if(GBAF_BOSS == gba_flag_active[pid_current]) {
		if(PID_NONE == gba_boss_launched_by) {
			// The original fixed 32-byte state copy explicitly uses SI/DI,
			// the current DS and REP MOVSW; direct struct assignment and
			// near-pointer assignment changed original CODE (af768a/b).
			_SI = FP_OFF(&boss_character_template[0]);
			if(1 == pid_current) {
				_SI += sizeof(boss_state_t);
			}
			_DI = FP_OFF(&boss_state);
			_AX = _DS;
			_ES = _AX;
			_CX = (sizeof(boss_state_t) / 2);
			asm { rep movsw }
			boss_pattern_count = (BOSS_PATTERN_COUNT_BASE + randring_far_next16_and(BOSS_PATTERN_COUNT_MASK));
			boss_frame = 0;
			gba_boss_launched_by = pid_current;
			gba_flag_active[pid_current] = GBAF_NONE;
			snd_se_play(18);
			palette_restore_for_pid(1 - pid_current);
			boss_active[1 - pid_current] = 1;
			return 1;
		}

		if(BOSS_EXPLODE_MODE == boss_mode) {
			return 0;
		}
		boss_mode = -1;
		boss_frame = 0;
		palette_restore_for_pid(1 - pid_current);
		boss_active[pid_current] = 0;
	}
	return 0;
}

extern "C" void far boss_hittest_end(void)
{
	register pid_t pid_other = (1 - pid_current);

	if((boss_hp > 0) || (boss_mode == BOSS_EXPLODE_MODE)) {
		return;
	}
	boss_mode = -1;
	boss_frame = 0;
	palette_restore_for_pid(pid_other);
	if(GBAF_BOSS != gba_flag_active[pid_other]) {
		combo_points_for_boss_attack = BOSS_COMBO_POINTS;
	}
	boss_active[pid_other] = 0;
	if(GBA_BOSS_LEVEL_MAX > gba_boss_level) {
		gba_boss_level++;
	}
}

extern "C" void near boss_target_update(void)
{
	if(BOSS_DESCEND_MODE == boss_mode) {
		return;
	}
	boss_target_x = boss_center_x;
	boss_target_y = (BOSS_TARGET_Y_AHEAD + boss_center_y);
}

extern "C" void near boss_pattern_next(void)
{
	register unsigned char pattern;

	boss_move_sine();
	if(BOSS_PATTERN_WAIT_FRAMES <= boss_frame) {
		// Each rejected pattern still consumes a separate RNG word.
		while(1) {
			pattern = randring_far_next16_and(BOSS_PATTERN_VARIANTS_MASK);
			if(!(
				((boss_pattern_previous + BOSS_PATTERN_RECENT_RADIUS) >= pattern) &&
				((boss_pattern_previous - BOSS_PATTERN_RECENT_RADIUS) <= pattern)
			)) {
				break;
			}
		}

		boss_pattern_previous = pattern;
		boss_frame = 0;
		boss_mode = (BOSS_PATTERN_MODE_OFFSET + pattern);
		// The BOSS pattern-index postfix is also codegen-visible;
		// prefix ++boss_pattern_i changed original TC4 bytes (af916f).
		boss_pattern_i++;
		if(boss_pattern_i <= boss_pattern_count) {
			return;
		}
		boss_mode = BOSS_DESCEND_MODE;
	}
}

extern "C" void near boss_explosion_render(void)
{
	boss_mode = boss_explosion_ring(boss_center_x, boss_center_y, boss_frame);
	if(0 == boss_mode) {
		gba_boss_launched_by = PID_NONE;
	}
}
#endif
