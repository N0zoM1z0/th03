// Complete native-source Turbo C++ reconstruction of the original Mima
// major BOSS. Shared BOSS helpers and Mima-private state remain in their
// separately owned original physical storage; the normal MAIN is exact.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/mima.hpp"
#include "src/main/boss/shared.hpp"
#include "src/main/math/polar.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/sprite16/sprite16.h"

#pragma option -a2

// Reuse the same physical 32-byte shared BOSS template, with semantic
// names for the historical +10..+15 state bytes.
#include "src/main/boss/template_state.hpp"

extern boss_template_state_t boss_character_template[PLAYER_COUNT];

extern int boss_center_x;
extern int boss_center_y;
extern int boss_hp;
extern sprite16_offset_t boss_sprite_offset;
extern unsigned char boss_hit;
extern unsigned char boss_mode;
extern unsigned char boss_render_mode;
extern unsigned char boss_render_frame;
extern unsigned int boss_frame;

// Mima's seven level-derived pattern parameters.
extern unsigned char mima_bullet_speed;
extern unsigned char mima_random_count;
extern unsigned char mima_random_speed;
extern unsigned char mima_trail_interval;
extern unsigned char mima_pellet_speed;
extern unsigned char mima_pellet_until;
extern unsigned char mima_orbit_speed;

// Mima-private pattern state.
extern unsigned char mima_spread_angle;
extern unsigned char mima_pellet_angle;
extern signed char mima_orbit_delta;
extern unsigned char mima_orbit_angle;

extern int SinTable8[256];
extern int CosTable8[256];

extern "C" void far pascal bomb_center_add(int x, int y, int pid);

// The shared BOSS scheduler selects 2..17; Mima maps those IDs to
// four different full bullet-pattern controllers.
enum mima_boss_mode_t {
    MIMA_MODE_INTRO = 0x00,
    MIMA_MODE_SELECT = 0x01,
    MIMA_MODE_SPREAD_0 = 0x02,
    MIMA_MODE_SPREAD_1 = 0x03,
    MIMA_MODE_SPREAD_2 = 0x04,
    MIMA_MODE_SPREAD_3 = 0x05,
    MIMA_MODE_RANDOM_0 = 0x06,
    MIMA_MODE_RANDOM_1 = 0x07,
    MIMA_MODE_RANDOM_2 = 0x08,
    MIMA_MODE_RANDOM_3 = 0x09,
    MIMA_MODE_RANDOM_4 = 0x0A,
    MIMA_MODE_TRAIL_0 = 0x0B,
    MIMA_MODE_TRAIL_1 = 0x0C,
    MIMA_MODE_TRAIL_2 = 0x0D,
    MIMA_MODE_ORBIT_0 = 0x0E,
    MIMA_MODE_ORBIT_1 = 0x0F,
    MIMA_MODE_ORBIT_2 = 0x10,
    MIMA_MODE_ORBIT_3 = 0x11,
    MIMA_MODE_DESCEND = 0x80,
    MIMA_MODE_EXPLODE = 0xFF,
};

enum mima_template_layout_t {
    MIMA_TEMPLATE_CENTER_X = 0x900,
    MIMA_TEMPLATE_CENTER_Y = 0x500,
    MIMA_TEMPLATE_VELOCITY_X = -0x20,
    MIMA_TEMPLATE_HP = 0x6E,
    MIMA_TEMPLATE_SPRITE_OFFSET = 0x28C,
    MIMA_TEMPLATE_PLAYER2_OFF = 0x28,
    MIMA_TEMPLATE_RENDER_MODE_NORMAL = 0,
};

enum mima_level_scaling_t {
    MIMA_LEVEL_QUARTER = 4,
    MIMA_LEVEL_BULLET_BASE = 0x20,
    MIMA_LEVEL_RANDOM_COUNT_BASE = 2,
    MIMA_LEVEL_TRAIL_INTERVAL_BASE = 0x40,
    MIMA_LEVEL_PELLET_SPEED_BASE = 0x28,
    MIMA_LEVEL_PELLET_UNTIL_MULTIPLIER = 4,
    MIMA_LEVEL_PELLET_UNTIL_BASE = 0x40,
    MIMA_LEVEL_ORBIT_SPEED_BASE = 0x36,
};

void far pascal boss_mima_template_init(int player_id)
{
	boss_template_state_t near *p = &boss_character_template[player_id];

	p->center_x = MIMA_TEMPLATE_CENTER_X;
	p->center_y = MIMA_TEMPLATE_CENTER_Y;
	p->velocity_x = MIMA_TEMPLATE_VELOCITY_X;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = MIMA_MODE_INTRO;
	p->hp = MIMA_TEMPLATE_HP;
	p->pattern_i = 0;
	p->sprite_offset = MIMA_TEMPLATE_SPRITE_OFFSET;
	if(player_id != 0) {
		p->sprite_offset += MIMA_TEMPLATE_PLAYER2_OFF;
	}
	p->render_mode = MIMA_TEMPLATE_RENDER_MODE_NORMAL;
}

// Full BOSS pattern clocks are unsigned 16-bit. The original TC4 emits its
// literal masks naturally from unsigned %2 and %4; the six-frame side volley
// must retain a real integer division. Do not apply this conclusion to
// byte-valued clocks in the Bomb/Extra Attack implementations.
enum mima_render_mode_t {
    MIMA_RMODE_NORMAL = 0,
    MIMA_RMODE_PARTICLE = 2,
    MIMA_RMODE_EXPAND = 3,
    MIMA_RMODE_FLASH = 4,
    MIMA_RMODE_TRAIL = 5,
    MIMA_PART_SPRITE_OFF = 0x1A,
    MIMA_PART_SPRITE_LEFT = 48,
    MIMA_PART_SPRITE_TOP = 32,
    MIMA_PART_CARRIER_OFF = 0xEF4,
    MIMA_EXPAND_SPRITE_OFF = 0xC92,
    MIMA_DAMAGED_SPRITE_OFF = 0x12,
    MIMA_DAMAGED_LEFT = 32,
    MIMA_DAMAGED_TOP = 16,
    MIMA_PART_SPRITE_SIZE = 16,
    MIMA_PART_CARRIER_SIZE = 32,
    MIMA_PART_CARRIER_LEFT = 80,
    MIMA_EXPAND_SPRITE_WIDTH = 80,
    MIMA_EXPAND_SPRITE_HEIGHT = 48,
    MIMA_EXPAND_SPRITE_LEFT = 32,
    MIMA_EXPAND_SPRITE_TOP = 16,
};

enum mima_sound_effect_t {
    MIMA_SOUND_SPREAD = 3,
    MIMA_SOUND_ORBIT = 10,
    MIMA_SOUND_TRAIL = 10,
};

enum mima_spread_angle_t {
    MIMA_SPREAD_INITIAL_PELLET_ANGLE = 0xC0,
    MIMA_PELLET_OPPOSITE_ANGLE = 0x80,
    MIMA_ORBIT_ANGLE_STEP = 7,
    MIMA_TRAIL_FIRST_PHASE = 1,
};

enum mima_native_phase_t {
    MIMA_SPREAD_INITIAL_SETUP_END = 2,
    MIMA_SPREAD_FIRE_BEGIN = 0x20,
    MIMA_SPREAD_FIRE_END_AFTER = 0x82,
    MIMA_SPREAD_PELLET_PERIOD = 6,
    MIMA_RANDOM_BOMB_WARN = 0x10,
    MIMA_RANDOM_BOMB_FIRE_BEGIN = 0x20,
    MIMA_RANDOM_BOMB_FIRE_PERIOD = 4,
    // Three separate warning explosions precede the first live barrage.
    MIMA_RANDOM_BOMB_MARK_SECOND = 0x24,
    MIMA_RANDOM_BOMB_MARK_THIRD = 0x28,
    MIMA_RANDOM_BOMB_BULLET_WAIT_END = 0x30,
    MIMA_RANDOM_BOMB_RING_FRAME = 0x40,
    MIMA_RANDOM_BOMB_END = 0x80,
    MIMA_TRAIL_END = 0x96,
    MIMA_TRAIL_BULLET_SPEED_OFFSET = 8,
    MIMA_BOSS_INTRO_END = 0x64,
    MIMA_FIRE_EVEN_PERIOD = 2,
    MIMA_SPREAD_ANGLE_STEP = 9,
    MIMA_PELLET_ANGLE_STEP = 3,
    MIMA_BOMB_ORIGIN_X_OFFSET = TO_SP(24),
    MIMA_BOMB_ORIGIN_Y_OFFSET = TO_SP(-32),
    MIMA_ORBIT_RADIUS = TO_SP(48),
    MIMA_ORBIT_SHOT_ANGLE_OFFSET = 0x40,
    MIMA_RENDER_PARTICLE_CEL_FIRST = 0x10,
    MIMA_RENDER_PARTICLE_CEL_SECOND = 0x20,
    MIMA_RENDER_HALF_MASK_A = 0xAAAA,
    MIMA_RENDER_HALF_MASK_B = 0x5555,
    MIMA_RENDER_MASK_RESTORE = 0xFFFF,
    MIMA_RENDER_SPLIT_OPPOSITE_ANGLE = 0x80,
    MIMA_INTRO_START_DISTANCE = 0xC8,
    MIMA_INTRO_FRAME_DISTANCE_SHIFT = 1,
    MIMA_COLLISION_TILE_SIZE = 56,
    MIMA_COLLISION_HALF_RADIUS = TO_SP(32),
    MIMA_RENDER_FULL_WIDTH = 144,
    MIMA_RENDER_FULL_HEIGHT = 112,
    MIMA_RENDER_HIT_WIDTH = 64,
    MIMA_RENDER_HIT_HEIGHT = 80,
    MIMA_RENDER_MAIN_LEFT_HALF = 72,
    MIMA_RENDER_MAIN_TOP_HALF = 40,
};

void near mima_pattern_spread(void)
{
	if(boss_frame < MIMA_SPREAD_INITIAL_SETUP_END) {
		boss_render_mode = MIMA_RMODE_PARTICLE;
		boss_render_frame = 0;
		mima_spread_angle = 0;
		mima_pellet_angle = MIMA_SPREAD_INITIAL_PELLET_ANGLE;
		return;
	}

	if(boss_frame >= MIMA_SPREAD_FIRE_BEGIN) {
		if((boss_frame & (MIMA_FIRE_EVEN_PERIOD - 1)) == 0) {
			snd_se_play(MIMA_SOUND_SPREAD);

			bullet_template.angle = mima_spread_angle;
			bullet_template.group = BG_2_SPREAD_HORIZONTALLY_SYMMETRIC;
			bullet_template.center.x.v = boss_center_x;
			bullet_template.center.y.v = boss_center_y;
			bullet_template.speed.v = mima_bullet_speed;
			bullet_template.type = BT_BULLET16_DEFAULT;
			bullet_template.is_animated = false;
			bullets_add();
			bullet_template.is_animated = true;
			// Unlike some other BOSS byte-angle updates, named original
			// increment constants are TC4 byte-exact here (af855f/g).
			mima_spread_angle = mima_spread_angle + MIMA_SPREAD_ANGLE_STEP;

			if(
				(mima_pellet_until > boss_frame) &&
				// The six-frame unsigned-word cadence compares the remainder
				// explicitly with zero; unlike powers of two, it is not a mask.
				((boss_frame % MIMA_SPREAD_PELLET_PERIOD) == 0)
			) {
				bullet_template.type = BT_PELLET;
				bullet_template.group = BG_4_SPREAD_MEDIUM;
				bullet_template.speed.v = mima_pellet_speed;
				bullet_template.angle = mima_pellet_angle;
				bullets_add();

				bullet_template.angle = (MIMA_PELLET_OPPOSITE_ANGLE - mima_pellet_angle);
				bullets_add();
			}
			mima_pellet_angle = mima_pellet_angle + MIMA_PELLET_ANGLE_STEP;
		}

		if(boss_frame > MIMA_SPREAD_FIRE_END_AFTER) {
			boss_render_mode = MIMA_RMODE_NORMAL;
			boss_mode = MIMA_MODE_SELECT;
			boss_frame = 0;
		}
	}
}

void near mima_pattern_bomb_random(void)
{
	pid_t pid_other = (1 - pid_current);
	register int x;
	register int y;

	if(boss_frame == MIMA_RANDOM_BOMB_WARN) {
		boss_render_mode = MIMA_RMODE_TRAIL;
	} else if(boss_frame < MIMA_RANDOM_BOMB_FIRE_BEGIN) {
		return;
	}

	x = (boss_center_x + MIMA_BOMB_ORIGIN_X_OFFSET);
	y = (boss_center_y + MIMA_BOMB_ORIGIN_Y_OFFSET);

	if(
		(boss_frame == MIMA_RANDOM_BOMB_FIRE_BEGIN) ||
		(boss_frame == MIMA_RANDOM_BOMB_MARK_SECOND) ||
		(boss_frame == MIMA_RANDOM_BOMB_MARK_THIRD)
	) {
		bomb_center_add(x, y, pid_other);
		return;
	}

	if(boss_frame > MIMA_RANDOM_BOMB_BULLET_WAIT_END) {
		// Natural unsigned 16-bit four-frame attack clock, not a byte
		// animation division. The original hardware RNG order is unchanged.
		if((boss_frame & (MIMA_RANDOM_BOMB_FIRE_PERIOD - 1)) == 0) {
			bullet_template.angle = 0;
			bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
			bullet_template.center.x.v = x;
			bullet_template.center.y.v = y;
			bullet_template.count = mima_random_count;
			bullet_template.speed.v = mima_random_speed;
			bullet_template.type = BT_BULLET16_DEFAULT;
			bullet_template.is_animated = false;
			bullets_add();

			bullet_template.type = BT_PELLET;
			bullets_add();
			bullet_template.is_animated = true;
		}

		if(boss_frame == MIMA_RANDOM_BOMB_RING_FRAME) {
			bullet_template.angle = randring_far_next16();
			bullet_template.group = BG_32_RING;
			bullet_template.center.x.v = x;
			bullet_template.center.y.v = y;
			bullet_template.speed.v = TO_SP(2);
			bullet_template.type = BT_BULLET16_DEFAULT;
			bullet_template.is_animated = false;
			bullets_add();
			bullet_template.is_animated = true;
		}

		if((boss_frame & (MIMA_FIRE_EVEN_PERIOD - 1)) == 0) {
			snd_se_play(MIMA_SOUND_SPREAD);
		}

		if(boss_frame >= MIMA_RANDOM_BOMB_END) {
			boss_render_mode = MIMA_RMODE_NORMAL;
			boss_mode = MIMA_MODE_SELECT;
			boss_frame = 0;
		}
	}
}

void near mima_pattern_trail(void)
{
	// The original 16-bit frame modulo narrows to a *byte* before the
	// two trail-phase comparisons; widening this local changed TC4 CODE
	// (native negative af855d).
	unsigned char remainder = (boss_frame % mima_trail_interval);

	boss_move_sine();
	boss_render_mode = MIMA_RMODE_TRAIL;

	if(
		(remainder == MIMA_TRAIL_FIRST_PHASE) ||
		// Signed 16-bit promotion of the byte interval/2 must be
		// preserved; using `>>1` changed CODE in real TC4 af898d.
		(remainder == (mima_trail_interval / 2))
	) {
		if(remainder == (mima_trail_interval / 2)) {
			bullet_template.group = BG_4_SPREAD_MEDIUM_AIMED;
		} else {
			bullet_template.group = BG_5_SPREAD_MEDIUM_AIMED;
		}

		snd_se_play(MIMA_SOUND_TRAIL);
		bullet_template.angle = 0;
		bullet_template.center.x.v = (boss_center_x + MIMA_BOMB_ORIGIN_X_OFFSET);
		bullet_template.center.y.v = (boss_center_y + MIMA_BOMB_ORIGIN_Y_OFFSET);
		bullet_template.speed.v = (TO_SP(5) + MIMA_TRAIL_BULLET_SPEED_OFFSET);
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.is_animated = false;
		bullet_template.has_trail = true;
		bullets_add();
		bullet_template.has_trail = false;
		bullet_template.is_animated = true;
	}

	if(boss_frame >= MIMA_TRAIL_END) {
		boss_render_mode = MIMA_RMODE_NORMAL;
		boss_mode = MIMA_MODE_SELECT;
		boss_frame = 0;
	}
}

// The orbit fires only on even timer ticks after its signed direction
// has been chosen at the first frame.
enum mima_orbit_phase_t {
    MIMA_ORBIT_DIRECTION_FRAME = 1,
    MIMA_ORBIT_FINISH_FRAME = 0x48,
};

void near mima_pattern_orbit(void)
{
	boss_move_sine();

	if(boss_frame == MIMA_ORBIT_DIRECTION_FRAME) {
		mima_orbit_delta = (randring_far_next16_and(1) ? MIMA_ORBIT_ANGLE_STEP : -MIMA_ORBIT_ANGLE_STEP);
		mima_orbit_angle = randring_far_next16();
	}

	if((boss_frame & (MIMA_FIRE_EVEN_PERIOD - 1)) == 0) {
		bullet_template.center.x.v = polar(
			boss_center_x, MIMA_ORBIT_RADIUS, CosTable8[mima_orbit_angle]
		);
		bullet_template.center.y.v = polar(
			boss_center_y, MIMA_ORBIT_RADIUS, SinTable8[mima_orbit_angle]
		);
		bullet_template.angle = (mima_orbit_angle + MIMA_ORBIT_SHOT_ANGLE_OFFSET);
		bullet_template.type = BT_PELLET_CLOUD;
		bullet_template.group = BG_2_RING;
		bullet_template.speed.v = mima_orbit_speed;
		bullets_add();
		snd_se_play(MIMA_SOUND_ORBIT);

		// Signed byte angular steering remains compound `+=`;
		// explicit byte = byte + signed_delta changed original CODE
		// in independent genuine native af898b.
		mima_orbit_angle += mima_orbit_delta;
	}

	if(boss_frame >= MIMA_ORBIT_FINISH_FRAME) {
		boss_mode = MIMA_MODE_SELECT;
		boss_frame = 0;
	}
}

void far gba_boss_update_mima(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		mima_bullet_speed = (gba_boss_level + MIMA_LEVEL_BULLET_BASE);
		mima_random_count = ((gba_boss_level / MIMA_LEVEL_QUARTER) + MIMA_LEVEL_RANDOM_COUNT_BASE);
		mima_random_speed = (gba_boss_level + MIMA_LEVEL_BULLET_BASE);
		mima_trail_interval = (MIMA_LEVEL_TRAIL_INTERVAL_BASE - (gba_boss_level * 2));
		mima_pellet_speed = (gba_boss_level + MIMA_LEVEL_PELLET_SPEED_BASE);
		mima_pellet_until = ((gba_boss_level * MIMA_LEVEL_PELLET_UNTIL_MULTIPLIER) + MIMA_LEVEL_PELLET_UNTIL_BASE);
		mima_orbit_speed = (gba_boss_level + MIMA_LEVEL_ORBIT_SPEED_BASE);
	}

	if(pid_current == gba_boss_launched_by) {
		pid_other = (1 - pid_current);
		boss_target_update();
		// The target deliberately recomputes this after the shared helper call
		// instead of reusing [pid_other] (native negative control af749c).
		bullet_template.pid = (1 - pid_current);
		++boss_frame;

		switch(boss_mode) {
		case MIMA_MODE_INTRO:
			if(boss_frame == MIMA_BOSS_INTRO_END) {
				boss_frame = 0;
				boss_mode = MIMA_MODE_SELECT;
				break;
			} else {
				return;
			}

		case MIMA_MODE_SELECT:
			boss_pattern_next();
			break;

		case MIMA_MODE_SPREAD_0:
		case MIMA_MODE_SPREAD_1:
		case MIMA_MODE_SPREAD_2:
		case MIMA_MODE_SPREAD_3:
			mima_pattern_spread();
			break;

		case MIMA_MODE_RANDOM_0:
		case MIMA_MODE_RANDOM_1:
		case MIMA_MODE_RANDOM_2:
		case MIMA_MODE_RANDOM_3:
		case MIMA_MODE_RANDOM_4:
			mima_pattern_bomb_random();
			break;

		case MIMA_MODE_TRAIL_0:
		case MIMA_MODE_TRAIL_1:
		case MIMA_MODE_TRAIL_2:
			mima_pattern_trail();
			break;

		case MIMA_MODE_ORBIT_0:
		case MIMA_MODE_ORBIT_1:
		case MIMA_MODE_ORBIT_2:
		case MIMA_MODE_ORBIT_3:
			mima_pattern_orbit();
			break;

		case MIMA_MODE_DESCEND:
			boss_fall();
			break;

		case MIMA_MODE_EXPLODE:
			return;
		}

		collmap_center.x.v = boss_center_x;
		collmap_center.y.v = boss_center_y;
		collmap_stripe_tile_w.set(MIMA_COLLISION_TILE_SIZE);
		collmap_tile_h.set(MIMA_COLLISION_TILE_SIZE);
		collmap_pid = pid_other;
		collmap_set_rect_striped();

		hitbox_hittest_skip_explosions = true;
		hitbox.radius.x.v = MIMA_COLLISION_HALF_RADIUS;
		hitbox.radius.y.v = MIMA_COLLISION_HALF_RADIUS;
		hitbox.pid = pid_other;
		hitbox.origin.center.x.v = boss_center_x;
		hitbox.origin.center.y.v = boss_center_y;
		boss_hit = hitbox_hittest();
		boss_hp -= boss_hit;
		hitbox_hittest_skip_explosions = false;
		boss_hittest_end();
	}
}

void near mima_render_main(void)
{
	sprite16_offset_t sprite_offset;
	pid_t pid_other = (1 - pid_current);
	register screen_x_t left;
	register screen_y_t top;

	sprite16_put_size.set(MIMA_RENDER_FULL_WIDTH, MIMA_RENDER_FULL_HEIGHT);
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - MIMA_RENDER_MAIN_LEFT_HALF);
	top = ((boss_center_y >> 4) - MIMA_RENDER_MAIN_TOP_HALF);
	sprite16_put(left, top, boss_sprite_offset);

	if(boss_hit) {
		sprite16_put_size.set(MIMA_RENDER_HIT_WIDTH, MIMA_RENDER_HIT_HEIGHT);
		left += MIMA_DAMAGED_LEFT;
		top += MIMA_DAMAGED_TOP;
		sprite16_put(left, top, (boss_sprite_offset + MIMA_DAMAGED_SPRITE_OFF));
		return;
	}

	if(MIMA_RMODE_PARTICLE == boss_render_mode) {
render_mode_2:
		// Mode 5 enters through the original label; merging mode 2/5
		// into one C++ condition changed the full BOSS CODE (af855b).
		sprite16_put_size.set(MIMA_PART_SPRITE_SIZE, MIMA_PART_SPRITE_SIZE);
		sprite_offset = (boss_sprite_offset + MIMA_PART_SPRITE_OFF);
		sprite16_put((left + MIMA_PART_SPRITE_LEFT), (top + MIMA_PART_SPRITE_TOP), sprite_offset);

		sprite16_put_size.set(MIMA_PART_CARRIER_SIZE, MIMA_PART_CARRIER_SIZE);
		left += MIMA_PART_CARRIER_LEFT;
		sprite_offset = (boss_sprite_offset + MIMA_PART_CARRIER_OFF);
		if(boss_render_frame >= MIMA_RENDER_PARTICLE_CEL_FIRST) {
			sprite_offset += 4;
			if(boss_render_frame >= MIMA_RENDER_PARTICLE_CEL_SECOND) {
				boss_render_mode = MIMA_RMODE_EXPAND;
			}
		}
		sprite16_put(left, top, sprite_offset);
		// Byte frame postincrement is codegen-visible; prefix
		// changed real original CODE (af898e).
		boss_render_frame++;
		return;
	}

	if(MIMA_RMODE_EXPAND == boss_render_mode) {
		sprite16_put_size.set(MIMA_EXPAND_SPRITE_WIDTH, MIMA_EXPAND_SPRITE_HEIGHT);
		sprite16_put(
			(left + MIMA_EXPAND_SPRITE_LEFT),
			(top + MIMA_EXPAND_SPRITE_TOP),
			(boss_sprite_offset + MIMA_EXPAND_SPRITE_OFF)
		);
		return;
	}

	if(MIMA_RMODE_FLASH == boss_render_mode) {
		sprite16_put_size.set(MIMA_PART_SPRITE_SIZE, MIMA_PART_SPRITE_SIZE);
		sprite_offset = (boss_sprite_offset + MIMA_PART_SPRITE_OFF);
		sprite16_put((left + MIMA_PART_SPRITE_LEFT), (top + MIMA_PART_SPRITE_TOP), sprite_offset);
		return;
	}

	if(MIMA_RMODE_TRAIL == boss_render_mode) {
		boss_render_frame = 0;
		goto render_mode_2;
	}

}

void near pascal mima_render_split(int distance, unsigned char angle)
{
	screen_x_t base_left;
	screen_y_t base_top;
	screen_y_t top;
	pid_t pid_other;
	register int split_distance = distance;
	register screen_x_t left;
	pid_other = (1 - pid_current);
	sprite16_put_size.set(MIMA_RENDER_FULL_WIDTH, MIMA_RENDER_FULL_HEIGHT);
	base_left = (
		playfield_fg_x_to_screen(boss_center_x, pid_other) - MIMA_RENDER_MAIN_LEFT_HALF
	);
	base_top = ((boss_center_y >> 4) - MIMA_RENDER_MAIN_TOP_HALF);

	_AH = SPRITE16_SET_MASK;
	_DX = MIMA_RENDER_HALF_MASK_A;
	geninterrupt(SPRITE16);
	left = polar(base_left, split_distance, CosTable8[angle]);
	top = polar(base_top, split_distance, SinTable8[angle]);
	sprite16_put(left, top, boss_sprite_offset);

	_AH = SPRITE16_SET_MASK;
	_DX = MIMA_RENDER_HALF_MASK_B;
	geninterrupt(SPRITE16);
	// The split mask's opposite half-turn is byte-valued, but its
	// named original 0x80 increment stays native-exact (af855h).
	angle = angle + MIMA_RENDER_SPLIT_OPPOSITE_ANGLE;
	left = polar(base_left, split_distance, CosTable8[angle]);
	top = polar(base_top, split_distance, SinTable8[angle]);
	sprite16_put(left, top, boss_sprite_offset);

	_AH = SPRITE16_SET_MASK;
	_DX = MIMA_RENDER_MASK_RESTORE;
	geninterrupt(SPRITE16);
}

void far gba_boss_render_mima(void)
{
	pid_t pid_other;

	if(pid_current != gba_boss_launched_by) {
		return;
	}
	pid_other = (1 - pid_current);
	sprite16_clip_set_for_pid(pid_other);

	if(boss_mode == MIMA_MODE_INTRO) {
		mima_render_split(
			(MIMA_INTRO_START_DISTANCE - (boss_frame << MIMA_INTRO_FRAME_DISTANCE_SHIFT)),
			(boss_frame * 3)
		);
		return;
	}
	if(boss_mode != MIMA_MODE_EXPLODE) {
		mima_render_main();
		return;
	}
	boss_explosion_render();
}
