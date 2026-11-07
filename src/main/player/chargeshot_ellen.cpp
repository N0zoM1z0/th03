// Complete source-native Turbo C++ for original Ellen Chargeshot/Gauge,
// including the full 32-slot homing/arrival state engine, sprite and
// collision dispatch and original 16-bit/byte ownership in MAIN_08_TEXT.
#pragma codeseg MAIN_08_TEXT

#include <stddef.h>
#include "src/main/player/chargeshot_ellen.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"

// Each Ellen charged projectile occupies one 12-byte DGROUP record.
// Slot arrays have 32 projectiles per player, with a total of 64.
enum ellen_chargeshot_limits_t {
    ELLEN_CHARGE_SLOTS_PER_PLAYER = 32,
    ELLEN_CHARGE_SLOTS_TOTAL = 64,
    ELLEN_CHARGE_SPREAD_STATE_END = 0x40,
    ELLEN_CHARGE_LENGTH_INIT = 0x50,
    ELLEN_CHARGE_LENGTH_DECAY = 2,
    ELLEN_CHARGE_HOMING_SPEED = 160,
    ELLEN_CHARGE_ACTIVE_STATE = 1,
    ELLEN_CHARGE_INACTIVE_STATE = 0,
    ELLEN_CHARGE_DECELERATE_PHASE = 0,
    ELLEN_CHARGE_TARGET_PHASE = 1,
    ELLEN_CHARGE_TARGET_Y_OFFSET = TO_SP(-110),
    ELLEN_CHARGE_CLIP_NEGATIVE_RADIUS = TO_SP(-8),
    ELLEN_CHARGE_SPRITE_ANGLE_BIAS = 0x10,
    ELLEN_CHARGE_SPRITE_ANGLE_SHIFT = 5,
    ELLEN_CHARGE_SPRITE_CEL_SHIFT = 1,
    ELLEN_CHARGE_HIT_DAMAGE = 2,
};

struct ellen_chargeshot_t {
	unsigned char state;
	unsigned char phase;
	unsigned char angle;
	unsigned char length;
	PlayfieldPoint center;
	SPPoint velocity;
};

typedef char ellen_charge_12byte_stride[
    (sizeof(ellen_chargeshot_t) == 12) ? 1 : -1
];
typedef char ellen_charge_center_at_04[
    (offsetof(ellen_chargeshot_t, center) == 4) ? 1 : -1
];
typedef char ellen_charge_velocity_at_08[
    (offsetof(ellen_chargeshot_t, velocity) == 8) ? 1 : -1
];

struct gauge_pattern_timing_t {
	unsigned char total_frames;
	unsigned char byte_1;
	unsigned char byte_2;
	unsigned char byte_3;
};

typedef char ellen_gauge_timing_4bytes[
    (sizeof(gauge_pattern_timing_t) == 4) ? 1 : -1
];

extern int ellen_gauge_x[PLAYER_COUNT];
extern int ellen_gauge_y[PLAYER_COUNT];
extern unsigned char ellen_gauge_frame[PLAYER_COUNT];
extern ellen_chargeshot_t ellen_chargeshots[PLAYER_COUNT][32];
extern ellen_chargeshot_t near *ellen_chargeshot_p;
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];

extern int ellen_target_x;
extern int ellen_target_y;
extern "C" void far pascal ellen_target_set(pid_t pid);
extern "C" void far pascal bomb_center_add(int x, int y, int pid);
extern "C" void far pascal palette_restore_for_pid(pid_t pid);

// The whole source owns the 32-slot scan, spread allocator, decelerate /
// homing controller and gauge emission alongside its sprite leaf. Preserve
// byte-memory state and length mutation order, including the original
// predecrement of the per-projectile state at the activation boundary.

void far pascal chargeshots_reset_ellen(void)
{
	ellen_chargeshot_p = &ellen_chargeshots[0][0];
	// Clear all 64 original 12-byte physical shot records, not only
	// a per-player slice. This whole-source while is native-exact.
	int i = 0;
	while(i < ELLEN_CHARGE_SLOTS_TOTAL) {
		ellen_chargeshot_p->state = ELLEN_CHARGE_INACTIVE_STATE;
		++i;
		ellen_chargeshot_p++;
	}
}

void far pascal chargeshot_add_ellen(Subpixel center_x, Subpixel center_y)
{
	ellen_chargeshot_p = &ellen_chargeshots[pid.current][0];
	// Every second byte state creates one of 32 separately randomized
	// physical shots. Its signed state and near pointer advance AFTER
	// each original independent RNG call (native af905a).
	int state = 0;
	while(state < ELLEN_CHARGE_SPREAD_STATE_END) {
		ellen_chargeshot_p->state = state;
		ellen_chargeshot_p->phase = ELLEN_CHARGE_DECELERATE_PHASE;
		ellen_chargeshot_p->center.x = center_x;
		ellen_chargeshot_p->center.y = center_y;
		ellen_chargeshot_p->angle = randring_far_next16();
		ellen_chargeshot_p->length = ELLEN_CHARGE_LENGTH_INIT;
		state += 2;
		ellen_chargeshot_p++;
	}
}

void far pascal ellen_hyper(Subpixel center_x, Subpixel center_y)
{
	ellen_chargeshot_p = &ellen_chargeshots[pid.current][0];
	// Unlike the complete update/hit/render loops, this first-free-slot
	// Hyper allocator must keep for/continue/return: natural while
	// changed actual TC4 CODE (negative af905e).
	for(int i = 0; i < ELLEN_CHARGE_SLOTS_PER_PLAYER; (++i, ellen_chargeshot_p++)) {
		if(ellen_chargeshot_p->state) {
			continue;
		}
		ellen_chargeshot_p->state = ELLEN_CHARGE_ACTIVE_STATE;
		ellen_chargeshot_p->phase = ELLEN_CHARGE_DECELERATE_PHASE;
		ellen_chargeshot_p->center.x = center_x;
		ellen_chargeshot_p->center.y = center_y;
		ellen_chargeshot_p->angle = randring_far_next16();
		ellen_chargeshot_p->length = ELLEN_CHARGE_LENGTH_INIT;
		return;
	}
}

void far pascal chargeshot_update_ellen(void)
{
	int target_x;
	int target_y;
	int player_x;
	int player_y;
	unsigned char length;

	ellen_chargeshot_p = &ellen_chargeshots[pid_current][0];
	int i;
	// Original active-scan enters the same historical label immediately;
	// explicit pointer/index while preserves native goto register state.
	i = 0;
	while(i < ELLEN_CHARGE_SLOTS_PER_PLAYER) {
		if(ellen_chargeshot_p->state) {
			goto active;
		}
		++i;
		ellen_chargeshot_p++;
	}
	return;

// The original active-scan jumps here immediately on the first live slot.
// A bounded for/break plus a final index check changes TC4 CODE (af854b).
active:
	ellen_chargeshot_p = &ellen_chargeshots[pid_current][0];
	ellen_target_set(pid_current);
	target_x = ellen_target_x;
	target_y = (ellen_target_y + ELLEN_CHARGE_TARGET_Y_OFFSET);
	players[pid_current].gauge_charged = 0;
	player_x = players[pid_current].center.x.v;
	player_y = players[pid_current].center.y.v;
	playfield_clip_negative_radius.x.v = ELLEN_CHARGE_CLIP_NEGATIVE_RADIUS;
	playfield_clip_negative_radius.y.v = ELLEN_CHARGE_CLIP_NEGATIVE_RADIUS;

	// Complete 32-slot decelerating/homing/arrival update, including
	// the inactive continue that advances both original near pointer
	// and signed index; natural while is byte-exact (af905d).
	i = 0;
	while(i < ELLEN_CHARGE_SLOTS_PER_PLAYER) {
		if(!ellen_chargeshot_p->state) {
			++i;
			ellen_chargeshot_p++;
			continue;
		}
		if(ellen_chargeshot_p->state == ELLEN_CHARGE_ACTIVE_STATE) {
			ellen_chargeshot_p->center.x.v += ellen_chargeshot_p->velocity.x.v;
			ellen_chargeshot_p->center.y.v += ellen_chargeshot_p->velocity.y.v;
			if(ellen_chargeshot_p->phase == ELLEN_CHARGE_DECELERATE_PHASE) {
				length = (ellen_chargeshot_p->length - ELLEN_CHARGE_LENGTH_DECAY);
				vector2(
					ellen_chargeshot_p->velocity.x.v,
					ellen_chargeshot_p->velocity.y.v,
					ellen_chargeshot_p->angle,
					length
				);
				ellen_chargeshot_p->length = length;
				if(!length) {
					ellen_chargeshot_p->phase = ELLEN_CHARGE_TARGET_PHASE;
					ellen_chargeshot_p->angle = iatan2(
						(target_y - ellen_chargeshot_p->center.y.v),
						(target_x - ellen_chargeshot_p->center.x.v)
					);
					vector2(
						ellen_chargeshot_p->velocity.x.v,
						ellen_chargeshot_p->velocity.y.v,
						ellen_chargeshot_p->angle,
						ELLEN_CHARGE_HOMING_SPEED
					);
				}
			} else if(playfield_clip(
				ellen_chargeshot_p->center.x,
				ellen_chargeshot_p->center.y
			)) {
				ellen_chargeshot_p->state = ELLEN_CHARGE_INACTIVE_STATE;
			}
		} else {
			// Preserve byte predecrement as part of the comparison; spelling
			// this as separate state-- and ==ACTIVE changed CODE (af854c).
			// Predecrement must remain INSIDE this byte comparison:
			// splitting state-- and ==ACTIVE changed native CODE again
			// (af905i). Original sound onset and phase remain intact.
			if((--ellen_chargeshot_p->state) == 1) {
				snd_se_play(1);
			}
			ellen_chargeshot_p->center.x.v = player_x;
			ellen_chargeshot_p->center.y.v = player_y;
		}
		++i;
		ellen_chargeshot_p++;
	}
}

void near pascal ellen_chargeshot_private(Subpixel x, Subpixel y)
{
	// TC4 naturally assigns SI to left and DI to top in this order.
	// Swapping declarations changes original CODE (af752d); no manual
	// _SI/_DI/_AX register writes are required here anymore.
	register screen_x_t left = x.v;
	register screen_y_t top = y.v;
	sprite16_offset_t sprite_offset = (pid.so_attack + 0x10);
	// Preserve the byte carrier before the two separate angular shifts.
	// Collapsing the expression before byte truncation is not equivalent
	// near 0xFF and changes native CODE (negative original af854a).
	unsigned char cel = (ellen_chargeshot_p->angle + ELLEN_CHARGE_SPRITE_ANGLE_BIAS);
	cel >>= ELLEN_CHARGE_SPRITE_ANGLE_SHIFT;
	cel <<= ELLEN_CHARGE_SPRITE_CEL_SHIFT;
	sprite_offset += cel;

	left = (playfield_fg_x_to_screen(left, pid_current) - 8);
	top = ((top >> 4) + 8);
	sprite16_put(left, top, sprite_offset);
}

uint8_t far chargeshot_hittest_ellen(void)
{
	unsigned char hits = 0;
	ellen_chargeshot_p = &ellen_chargeshots[hitbox.pid][0];

	// Native-exact full thirty-two-slot active-only scan: every skipped
	// state advances index and near pointer before continuing (af905b).
	int i = 0;
	while(i < ELLEN_CHARGE_SLOTS_PER_PLAYER) {
		if(ellen_chargeshot_p->state != ELLEN_CHARGE_ACTIVE_STATE) {
			++i;
			ellen_chargeshot_p++;
			continue;
		}
		if(
			(ellen_chargeshot_p->center.x.v >= hitbox.origin.topleft.x.v) &&
			(ellen_chargeshot_p->center.x.v <= hitbox.right.v) &&
			(ellen_chargeshot_p->center.y.v >= hitbox.origin.topleft.y.v) &&
			(ellen_chargeshot_p->center.y.v <= hitbox.bottom.v)
		) {
			hitcircles_enemy_add(
				ellen_chargeshot_p->center.x.v,
				ellen_chargeshot_p->center.y.v,
				hitbox.pid
			);
			ellen_chargeshot_p->state = ELLEN_CHARGE_INACTIVE_STATE;
			// Original byte `hits += 2` accepts a named enum ONLY through
			// the natural explicit assignment (af905h), not an assumed
			// compiler-neutral mutation.
			hits = hits + ELLEN_CHARGE_HIT_DAMAGE;
		}
		++i;
		ellen_chargeshot_p++;
	}
	return hits;
}

void far pascal chargeshot_render_ellen(void)
{
	ellen_chargeshot_p = &ellen_chargeshots[pid_current][0];
	sprite16_put_size.set(16, 16);
	sprite16_clip_set_for_pid(pid_current);

	int i = 0;
	while(i < ELLEN_CHARGE_SLOTS_PER_PLAYER) {
		if(ellen_chargeshot_p->state != ELLEN_CHARGE_ACTIVE_STATE) {
			++i;
			ellen_chargeshot_p++;
			continue;
		}
		ellen_chargeshot_private(
			ellen_chargeshot_p->center.x,
			ellen_chargeshot_p->center.y
		);
		++i;
		ellen_chargeshot_p++;
	}
}

// The Gauge attack first traverses the upper row from both sides, then
// fires successive mirrored side volleys every eight frames. These
// phase limits are unrelated to the charged-projectile length counter.
enum ellen_gauge_phase_t {
    ELLEN_GAUGE_VOLLEY_PERIOD = 8,
    ELLEN_GAUGE_FIRST_X = TO_SP(144),
    ELLEN_GAUGE_SIDE_Y_LIMIT = TO_SP(144),
    ELLEN_GAUGE_STEP = TO_SP(24),
};

void near pascal gauge_pattern_ellen(bullet_type_t type)
{
	unsigned char pid_other;
	unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
	if(type == BT_BULLET16_DEFAULT) {
		flag_expected = (flag_expected + GBAF_PELLET_TO_BULLET);
	}

	if(gba_flag_active[pid_current] == flag_expected) {
		ellen_gauge_frame[pid_current] = 0;
		gba_flag_active[pid_current]++;
		ellen_gauge_x[pid_current] = ELLEN_GAUGE_FIRST_X;
		ellen_gauge_y[pid_current] = 0;
		gauge_pattern_timing[pid_current].total_frames = (
			gba_gauge_level[pid_current] + 0x0E
		);
		gauge_pattern_timing[pid_current].byte_1 = (
			gba_gauge_level[pid_current] + 0x1C
		);
		return;
	}
	if(gba_flag_active[pid_current] != (flag_expected + 1)) {
		return;
	}

	// This byte-valued eight-frame Gauge event accepts natural
	// `if(!remainder)` in original TC4 (af905f), unlike some masks.
	if(!(ellen_gauge_frame[pid_current] % ELLEN_GAUGE_VOLLEY_PERIOD)) {
		bullet_template.type = type;
		bullet_template.center.y.v = TO_SP(8);
		pid_other = (1 - pid_current);
		bullet_template.pid = pid_other;

		if(ellen_gauge_x[pid_current] > 0) {
			bullet_template.angle = 0;
			bullet_template.speed.v = ((3 << 4) + 8);
			bullet_template.group = BG_RING_AIMED;
			bullet_template.count = gauge_pattern_timing[pid_current].total_frames;
			bullet_template.center.y.v = 0;
			bomb_center_add(
				(bullet_template.center.x.v = ellen_gauge_x[pid_current]),
				0,
				pid_other
			);
			bullets_add();

			_DX = (TO_SP(PLAYFIELD_W) - ellen_gauge_x[pid_current]);
			bullet_template.center.x.v = _DX;
			bomb_center_add(_DX, 0, pid_other);
			bullets_add();
			ellen_gauge_x[pid_current] -= ELLEN_GAUGE_STEP;
		} else if(ellen_gauge_y[pid_current] < ELLEN_GAUGE_SIDE_Y_LIMIT) {
			bullet_template.angle = randring_far_next16();
			bullet_template.speed.v = gauge_pattern_timing[pid_current].byte_1;
			bullet_template.group = BG_16_RING;
			bullet_template.center.y.v = ellen_gauge_y[pid_current];
			bullet_template.center.x.v = 0;
			bomb_center_add(0, ellen_gauge_y[pid_current], pid_other);
			bullets_add();

			bullet_template.center.x.v = TO_SP(PLAYFIELD_W);
			bomb_center_add(
				TO_SP(PLAYFIELD_W),
				ellen_gauge_y[pid_current],
				pid_other
			);
			bullets_add();
			bullet_template.angle = randring_far_next16();
			ellen_gauge_y[pid_current] += ELLEN_GAUGE_STEP;
		} else {
			gba_flag_active[pid_current] = GBAF_NONE;
			palette_restore_for_pid(pid_other);
		}
	}
	// Byte-memory postfix is required: changing to prefix changed
	// original native CODE (af905g).
	ellen_gauge_frame[pid_current]++;
}

void far gba_gauge_pattern_pellet_ellen(void)
{
	if(gba_flag_active[pid_current]) {
		gauge_pattern_ellen(BT_PELLET);
	}
}

void far gba_gauge_pattern_bullet_ellen(void)
{
	if(gba_flag_active[pid_current]) {
		gauge_pattern_ellen(BT_BULLET16_DEFAULT);
	}
}
