// Complete current native-source Turbo C++ reconstruction for the
// original Kotohime major BOSS physical owner inside MAIN_03_TEXT.
// Shared BOSS helpers and storage remain in their own historical slots;
// the full normal Japanese MAIN link is original-exact, while canonical
// packed-game Factory acceptance is an independent open claim.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/kotohime.hpp"
#include "src/main/boss/shared.hpp"
#include "src/main/math/polar.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"

#pragma option -a2

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
extern unsigned char boss_move_phase;
extern int boss_effect_radius;
extern unsigned int boss_frame;

// Kotohime's seven level-derived attack parameters.
extern unsigned char kotohime_random_ring_speed;
extern unsigned char kotohime_orbit_count;
extern unsigned char kotohime_aimed_speed_slow;
extern unsigned char kotohime_aimed_speed_fast;
extern unsigned char kotohime_pellet_speed;
extern unsigned char kotohime_pellet_interval;
extern unsigned char kotohime_burst_count;

extern int SinTable8[256];
extern int CosTable8[256];

// The shared scheduler draws 2..17; Kotohime dispatches four distinct
// ring/arc/volley families by their original byte-valued mode IDs.
enum kotohime_boss_mode_t {
    KOTOHIME_MODE_INTRO = 0x00,
    KOTOHIME_MODE_SELECT = 0x01,
    KOTOHIME_MODE_RANDOM_RING_0 = 0x02,
    KOTOHIME_MODE_RANDOM_RING_1 = 0x03,
    KOTOHIME_MODE_RANDOM_RING_2 = 0x04,
    KOTOHIME_MODE_RANDOM_RING_3 = 0x05,
    KOTOHIME_MODE_RANDOM_RING_4 = 0x06,
    KOTOHIME_MODE_AIMED_RING_0 = 0x07,
    KOTOHIME_MODE_AIMED_RING_1 = 0x08,
    KOTOHIME_MODE_AIMED_RING_2 = 0x09,
    KOTOHIME_MODE_RADIAL_0 = 0x0A,
    KOTOHIME_MODE_RADIAL_1 = 0x0B,
    KOTOHIME_MODE_PELLET_ARC_0 = 0x0C,
    KOTOHIME_MODE_PELLET_ARC_1 = 0x0D,
    KOTOHIME_MODE_PELLET_ARC_2 = 0x0E,
    KOTOHIME_MODE_RADIAL_2 = 0x0F,
    KOTOHIME_MODE_RADIAL_3 = 0x10,
    KOTOHIME_MODE_RADIAL_4 = 0x11,
    KOTOHIME_MODE_DESCEND = 0x80,
    KOTOHIME_MODE_EXPLODE = 0xFF,
};

enum kotohime_template_layout_t {
    KOTOHIME_TEMPLATE_CENTER_X = 0x900,
    KOTOHIME_TEMPLATE_CENTER_Y = 0x500,
    KOTOHIME_TEMPLATE_VELOCITY_X = -0x20,
    KOTOHIME_TEMPLATE_HP = 0x6E,
    KOTOHIME_TEMPLATE_SPRITE_OFF = 0x288,
    KOTOHIME_TEMPLATE_PLAYER2_OFF = 0x28,
};

enum kotohime_render_mode_t {
    KOTOHIME_RENDER_MODE_NORMAL = 0,
    KOTOHIME_RENDER_MODE_EXPANDING = 1,
    KOTOHIME_RENDER_MODE_WARNING = 2,
};

enum kotohime_level_scaling_t {
    KOTOHIME_LEVEL_HALF = 2,
    KOTOHIME_LEVEL_ORBIT_DIV = 3,
    KOTOHIME_LEVEL_ORBIT_BASE = 6,
    KOTOHIME_LEVEL_SPEED_BASE = 0x10,
    KOTOHIME_LEVEL_AIMED_FAST_BASE = 0x20,
    KOTOHIME_LEVEL_PELLET_BASE = 0x18,
    KOTOHIME_LEVEL_INTERVAL_BASE = 0x20,
    KOTOHIME_LEVEL_BURST_BASE = 8,
};

enum kotohime_sound_effect_t {
    KOTOHIME_SOUND_ATTACK = 3,
};

// The intro transition, shared ring display and alternating sprites
// belong to the entire BOSS controller, not an unrelated render leaf.
enum kotohime_boss_timing_t {
    KOTOHIME_INTRO_FINISH_FRAME = 0x64,
    KOTOHIME_INTRO_BLINK_END_FRAME = 0x40,
    KOTOHIME_RENDER_FLICKER_PERIOD = 4,
    KOTOHIME_RENDER_ALT_FRAMES = 2,
    KOTOHIME_INTRO_RING_COUNT = 8,
    KOTOHIME_PELLET_RING_COUNT = 4,
    // Signed 16-bit loop division precedes byte-angle truncation.
    KOTOHIME_FULL_TURN_STEPS = 256,
    KOTOHIME_BURST_HALF_TURN_STEPS = 128,
    KOTOHIME_BURST_CENTER_ANGLE_OFFSET = 0x40,
    KOTOHIME_BURST_SPEED_SCALE = 0x30,
    KOTOHIME_BURST_SPEED_BASE = 0x10,
    KOTOHIME_INTRO_RADIUS_PIXELS = 0xC8,
    KOTOHIME_EFFECT_RADIUS_EXPAND_STEP = 0x20,
    KOTOHIME_PELLET_ARC_X_EXTREME = TO_SP(48),
    KOTOHIME_PELLET_ARC_X_MIDDLE = TO_SP(24),
    KOTOHIME_PELLET_ARC_Y_MIDDLE = TO_SP(12),
    KOTOHIME_PELLET_ARC_Y_CENTER = TO_SP(24),
    KOTOHIME_COLLISION_STRIPE_WIDTH = 64,
    KOTOHIME_COLLISION_TILE_HEIGHT = 48,
    KOTOHIME_COLLISION_HALF_RADIUS = TO_SP(32),
    KOTOHIME_MAIN_SPRITE_WIDTH = 128,
    KOTOHIME_MAIN_SPRITE_HEIGHT = 48,
    KOTOHIME_MAIN_LEFT_OFFSET = 64,
    KOTOHIME_MAIN_TOP_OFFSET = 32,
    KOTOHIME_RING_SPRITE_WIDTH = 32,
    KOTOHIME_RING_SPRITE_HEIGHT = 16,
    KOTOHIME_RING_SPRITE_OFFSET = 0x502,
    KOTOHIME_RING_SPRITE_ALTERNATE_OFFSET = 0xA00,
};

void far pascal boss_kotohime_template_init(int player_id)
{
	boss_template_state_t near *p =
		&boss_character_template[player_id];

	p->center_x = KOTOHIME_TEMPLATE_CENTER_X;
	p->center_y = KOTOHIME_TEMPLATE_CENTER_Y;
	p->velocity_x = KOTOHIME_TEMPLATE_VELOCITY_X;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = KOTOHIME_MODE_INTRO;
	p->hp = KOTOHIME_TEMPLATE_HP;
	p->pattern_i = 0;
	p->effect_radius = 0;
	p->sprite_offset = KOTOHIME_TEMPLATE_SPRITE_OFF;
	if(player_id != 0) {
		p->sprite_offset += KOTOHIME_TEMPLATE_PLAYER2_OFF;
	}
	p->render_mode = KOTOHIME_RENDER_MODE_NORMAL;
}

// Full-circle angles use natural 256-step division, keeping the
// original signed 16-bit multiply BEFORE division and byte truncation.
// The optional per-pellet RNG draw is gated by ordinary C++ truthiness,
// preserving exactly one random word per requested randomized bullet.
void near pascal kotohime_ring_emit(int randomize_angle)
{
	bullet_template.type = BT_BULLET16_DEFAULT;
	// This original signed angle calculation and conditional RNG draw must
	// run in the same order for every physical ring projectile. The natural
	// for-header preserves the original signed-angle and RNG instruction order.
	for(int i = 0; i < kotohime_orbit_count; ++i) {
		int x;
		int y;
		unsigned char angle;

		// Original signed-word nonzero RNG selector is exact with an
		// explicit `!=0` (genuine TC4 native test af910d).
		if(randomize_angle != 0) {
			bullet_template.angle = randring_far_next16();
		}
		angle = (
			((i * KOTOHIME_FULL_TURN_STEPS) / kotohime_orbit_count) +
			boss_move_phase
		);
		x = polar(
			boss_center_x,
			boss_effect_radius,
			CosTable8[angle]
		);
		y = polar(
			boss_center_y,
			boss_effect_radius,
			SinTable8[angle]
		);
		bullet_template.center.x.v = x;
		bullet_template.center.y.v = y;
		bullets_add();
	}
}

// The ring grows past 0x400 before the 0x40-frame release phase;
// the aimed and random rings share these physical animation boundaries.
enum kotohime_ring_phase_t {
    KOTOHIME_RING_START_FRAME = 1,
    KOTOHIME_RING_EXPAND_LIMIT = 0x400,
    KOTOHIME_RING_RELEASE_AFTER = 0x40,
};

// The ring and radial variants deliberately use AL-mediated byte phase
// updates. Repeating the *real original compiler* experiment with natural
// boss_move_phase +=2 in both variants shortened CODE by six bytes
// (af866d); radial -=4 likewise changed original CODE (af866e).
// Do not replace these register-visible expressions by C++ assumptions.
void near kotohime_pattern_random_ring(void)
{
	if(boss_frame == KOTOHIME_RING_START_FRAME) {
		boss_render_mode = KOTOHIME_RENDER_MODE_EXPANDING;
		boss_effect_radius = 0;
		boss_render_frame = 0;
	}

	boss_move_phase += 4;

	if(boss_effect_radius > KOTOHIME_RING_EXPAND_LIMIT) {
		boss_render_mode = KOTOHIME_RENDER_MODE_WARNING;
		// Force the original phase-byte reload after the preceding +4.
		// Without volatile, TC4 reuses AL and omits this load (af967c).
		_AL = *(volatile unsigned char near *)&boss_move_phase;
		_AL += 2;
		boss_move_phase = _AL;
		// Byte-memory postfix is real original codegen. Changing all
		// three to prefix altered native CODE (negative af910c).
		boss_render_frame++;
		if(boss_render_frame > KOTOHIME_RING_RELEASE_AFTER) {
			bullet_template.group = BG_16_RING;
			bullet_template.speed.v = kotohime_random_ring_speed;
			kotohime_ring_emit(1);
			snd_se_play(KOTOHIME_SOUND_ATTACK);
			boss_render_mode = KOTOHIME_RENDER_MODE_NORMAL;
			boss_mode = KOTOHIME_MODE_SELECT;
			boss_frame = 0;
		}
	} else {
		boss_move_sine();
		boss_effect_radius += KOTOHIME_EFFECT_RADIUS_EXPAND_STEP;
	}
}

void near kotohime_pattern_aimed_ring(void)
{
	if(boss_frame == KOTOHIME_RING_START_FRAME) {
		boss_render_mode = KOTOHIME_RENDER_MODE_EXPANDING;
		boss_effect_radius = 0;
		boss_render_frame = 0;
		boss_move_phase = 0;
	}

	boss_move_phase -= 2;

	if(boss_effect_radius > KOTOHIME_RING_EXPAND_LIMIT) {
		boss_render_mode = KOTOHIME_RENDER_MODE_WARNING;
		boss_effect_radius += 8;
		_AL = boss_move_phase;
		_AL += 2;
		boss_move_phase = _AL;
		// Byte-memory postfix is real original codegen. Changing all
		// three to prefix altered native CODE (negative af910c).
		boss_render_frame++;
		if(boss_render_frame > KOTOHIME_RING_RELEASE_AFTER) {
			bullet_template.group = BG_2_SPREAD_NARROW_AIMED;
			bullet_template.angle = 0;
			bullet_template.speed.v = kotohime_aimed_speed_fast;
			kotohime_ring_emit(0);

			bullet_template.group = BG_5_SPREAD_MEDIUM_AIMED;
			bullet_template.angle = 0;
			bullet_template.speed.v = kotohime_aimed_speed_slow;
			kotohime_ring_emit(0);

			snd_se_play(KOTOHIME_SOUND_ATTACK);
			boss_render_mode = KOTOHIME_RENDER_MODE_NORMAL;
			boss_mode = KOTOHIME_MODE_SELECT;
			boss_frame = 0;
		}
	} else {
		boss_move_sine();
		boss_effect_radius += KOTOHIME_EFFECT_RADIUS_EXPAND_STEP;
	}
}

enum kotohime_pellet_phase_t {
    KOTOHIME_PELLET_FIRE_REMAINDER = 1,
    KOTOHIME_PELLET_FINISH_FRAME = 0x60,
};

void near kotohime_pattern_pellet_arc(void)
{
	boss_move_sine();

	// The unsigned 16-bit BOSS clock fires exactly at remainder 1.
	// Its natural reversed comparison is TC4 native-exact (af910a).
	if(KOTOHIME_PELLET_FIRE_REMAINDER == (boss_frame % kotohime_pellet_interval)) {
		snd_se_play(KOTOHIME_SOUND_ATTACK);
		bullet_template.type = BT_PELLET;
		bullet_template.angle = (unsigned char)boss_frame;
		bullet_template.speed.v = kotohime_pellet_speed;
		bullet_template.group = BG_RING;
		bullet_template.count = KOTOHIME_PELLET_RING_COUNT;

		bullet_template.center.x.v = (boss_center_x - KOTOHIME_PELLET_ARC_X_EXTREME);
		bullet_template.center.y.v = boss_center_y;
		bullets_add();

		bullet_template.center.x.v = (boss_center_x - KOTOHIME_PELLET_ARC_X_MIDDLE);
		bullet_template.center.y.v = (boss_center_y + KOTOHIME_PELLET_ARC_Y_MIDDLE);
		bullets_add();

		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = (boss_center_y + KOTOHIME_PELLET_ARC_Y_CENTER);
		bullets_add();

		bullet_template.center.x.v = (boss_center_x + KOTOHIME_PELLET_ARC_X_MIDDLE);
		bullet_template.center.y.v = (boss_center_y + KOTOHIME_PELLET_ARC_Y_MIDDLE);
		bullets_add();

		bullet_template.center.x.v = (boss_center_x + KOTOHIME_PELLET_ARC_X_EXTREME);
		bullet_template.center.y.v = boss_center_y;
		bullets_add();
	}

	if(boss_frame >= KOTOHIME_PELLET_FINISH_FRAME) {
		boss_mode = KOTOHIME_MODE_SELECT;
		boss_frame = 0;
	}
}

// Radial burst divides each 256-step central orbit and each
// 128-step local spread with original signed 16-bit operations.
void near kotohime_pattern_radial_burst(void)
{
	if(boss_frame == KOTOHIME_RING_START_FRAME) {
		boss_render_mode = KOTOHIME_RENDER_MODE_EXPANDING;
		boss_effect_radius = 0;
		boss_render_frame = 0;
	}

	_AL = boss_move_phase;
	_AL += (unsigned char)0xFC;
	boss_move_phase = _AL;

	if(boss_effect_radius > KOTOHIME_RING_EXPAND_LIMIT) {
		boss_render_mode = KOTOHIME_RENDER_MODE_WARNING;
		boss_effect_radius += 8;
		boss_move_phase -= 2;
		// Byte-memory postfix is real original codegen. Changing all
		// three to prefix altered native CODE (negative af910c).
		boss_render_frame++;
		if(boss_render_frame <= KOTOHIME_RING_RELEASE_AFTER) {
			return;
		}

		bullet_template.group = BG_1;
		bullet_template.type = BT_BULLET16_DEFAULT;

		// Original inner burst is a genuine nested O(center_count *
		// burst_count) traversal, retaining division before angle truncation.
		// Both natural for-headers preserve the original TC4 code.
		for(int center_i = 0; center_i < kotohime_orbit_count; ++center_i) {
			int x;
			int y;
			unsigned char center_angle;

			center_angle = (
				((center_i * KOTOHIME_FULL_TURN_STEPS) / kotohime_orbit_count) +
				boss_move_phase
			);
			x = polar(
				boss_center_x,
				boss_effect_radius,
				CosTable8[center_angle]
			);
			y = polar(
				boss_center_y,
				boss_effect_radius,
				SinTable8[center_angle]
			);
			bullet_template.center.x.v = x;
			bullet_template.center.y.v = y;

			for(int bullet_i = 0; bullet_i < kotohime_burst_count; ++bullet_i) {
				bullet_template.angle = (
					((bullet_i * KOTOHIME_BURST_HALF_TURN_STEPS) / kotohime_burst_count) +
					center_angle +
					KOTOHIME_BURST_CENTER_ANGLE_OFFSET
				);
				bullet_template.speed.v = (
					((bullet_i * KOTOHIME_BURST_SPEED_SCALE) / kotohime_burst_count) +
					KOTOHIME_BURST_SPEED_BASE
				);
				bullets_add();
			}
		}

		snd_se_play(KOTOHIME_SOUND_ATTACK);
		boss_render_mode = KOTOHIME_RENDER_MODE_NORMAL;
		boss_mode = KOTOHIME_MODE_SELECT;
		boss_frame = 0;
	} else {
		boss_move_sine();
		boss_effect_radius += KOTOHIME_EFFECT_RADIUS_EXPAND_STEP;
	}
}

void far gba_boss_update_kotohime(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		kotohime_random_ring_speed = ((gba_boss_level / KOTOHIME_LEVEL_HALF) + KOTOHIME_LEVEL_SPEED_BASE);
		kotohime_orbit_count = ((gba_boss_level / KOTOHIME_LEVEL_ORBIT_DIV) + KOTOHIME_LEVEL_ORBIT_BASE);
		kotohime_aimed_speed_slow = ((gba_boss_level / KOTOHIME_LEVEL_HALF) + KOTOHIME_LEVEL_SPEED_BASE);
		kotohime_aimed_speed_fast = ((gba_boss_level / KOTOHIME_LEVEL_HALF) + KOTOHIME_LEVEL_AIMED_FAST_BASE);
		kotohime_pellet_speed = ((gba_boss_level / KOTOHIME_LEVEL_HALF) + KOTOHIME_LEVEL_PELLET_BASE);
		kotohime_pellet_interval = (KOTOHIME_LEVEL_INTERVAL_BASE - (gba_boss_level / KOTOHIME_LEVEL_HALF));
		kotohime_burst_count = ((gba_boss_level / KOTOHIME_LEVEL_HALF) + KOTOHIME_LEVEL_BURST_BASE);
	}

	if(pid_current == gba_boss_launched_by) {
		pid_other = (1 - pid_current);
		boss_target_update();
		bullet_template.pid = pid_other;
		++boss_frame;

		switch(boss_mode) {
		case KOTOHIME_MODE_INTRO:
			if(boss_frame == KOTOHIME_INTRO_FINISH_FRAME) {
				boss_frame = 0;
				boss_mode = KOTOHIME_MODE_SELECT;
				break;
			} else {
				return;
			}

		case KOTOHIME_MODE_SELECT:
			boss_pattern_next();
			break;

		case KOTOHIME_MODE_RANDOM_RING_0:
		case KOTOHIME_MODE_RANDOM_RING_1:
		case KOTOHIME_MODE_RANDOM_RING_2:
		case KOTOHIME_MODE_RANDOM_RING_3:
		case KOTOHIME_MODE_RANDOM_RING_4:
			kotohime_pattern_random_ring();
			break;

		case KOTOHIME_MODE_AIMED_RING_0:
		case KOTOHIME_MODE_AIMED_RING_1:
		case KOTOHIME_MODE_AIMED_RING_2:
			kotohime_pattern_aimed_ring();
			break;

		case KOTOHIME_MODE_PELLET_ARC_0:
		case KOTOHIME_MODE_PELLET_ARC_1:
		case KOTOHIME_MODE_PELLET_ARC_2:
			kotohime_pattern_pellet_arc();
			break;

		case KOTOHIME_MODE_RADIAL_0:
		case KOTOHIME_MODE_RADIAL_1:
		case KOTOHIME_MODE_RADIAL_2:
		case KOTOHIME_MODE_RADIAL_3:
		case KOTOHIME_MODE_RADIAL_4:
			kotohime_pattern_radial_burst();
			break;

		case KOTOHIME_MODE_DESCEND:
			boss_fall();
			break;

		case KOTOHIME_MODE_EXPLODE:
			return;
		}

		collmap_center.x.v = boss_center_x;
		collmap_center.y.v = boss_center_y;
		collmap_stripe_tile_w.set(KOTOHIME_COLLISION_STRIPE_WIDTH);
		collmap_tile_h.set(KOTOHIME_COLLISION_TILE_HEIGHT);
		collmap_pid = pid_other;
		collmap_set_rect_striped();

		hitbox_hittest_skip_explosions = true;
		hitbox.radius.x.v = KOTOHIME_COLLISION_HALF_RADIUS;
		hitbox.radius.y.v = KOTOHIME_COLLISION_HALF_RADIUS;
		hitbox.pid = pid_other;
		hitbox.origin.center.x.v = boss_center_x;
		hitbox.origin.center.y.v = boss_center_y;
		boss_hit = hitbox_hittest();
		boss_hp -= boss_hit;
		hitbox_hittest_skip_explosions = false;
		boss_hittest_end();
	} else {
		return;
	}
}

void near pascal kotohime_render_ring(int count)
{
	screen_y_t top;
	sprite16_offset_t sprite_offset;
	int radius;
	register int i;

	radius = boss_effect_radius;
	sprite_offset = (pid.so_attack + KOTOHIME_RING_SPRITE_OFFSET);
	// The warning flicker uses the unsigned-word low two bits.
	if((boss_render_mode == KOTOHIME_RENDER_MODE_WARNING) && (KOTOHIME_RENDER_ALT_FRAMES > (boss_frame & (KOTOHIME_RENDER_FLICKER_PERIOD - 1)))) {
		sprite_offset += KOTOHIME_RING_SPRITE_ALTERNATE_OFFSET;
	}

	sprite16_put_size.w = KOTOHIME_RING_SPRITE_WIDTH;
	sprite16_put_size.h = KOTOHIME_RING_SPRITE_HEIGHT;

	// The natural for-header preserves the original signed 16-bit
	// 256-step angle division before byte truncation.
	for(i = 0; i < count; ++i) {
		register screen_x_t left;
		unsigned char angle;
		angle = (((i * KOTOHIME_FULL_TURN_STEPS) / count) + boss_move_phase);
		left = polar(
			boss_center_x,
			radius,
			CosTable8[angle]
		);
		top = polar(
			boss_center_y,
			radius,
			SinTable8[angle]
		);
		left = (
			playfield_fg_x_to_screen(left, (1 - pid_current)) - 16
		);
		// The signed Y conversion is exact as an assigned C++ expression.
		// Compound top >>=4 changed original TC4 CODE (af762b).
		top = static_cast<screen_y_t>(top >> 4);
		sprite16_put(left, top, sprite_offset);
	}
}

void near kotohime_render_main(void)
{
	screen_x_t left;
	screen_y_t top;
	register sprite16_offset_t sprite_offset;

	sprite16_put_size.w = KOTOHIME_MAIN_SPRITE_WIDTH;
	sprite16_put_size.h = KOTOHIME_MAIN_SPRITE_HEIGHT;

	left = (
		playfield_fg_x_to_screen(
			boss_center_x,
			(1 - pid_current)
		) - KOTOHIME_MAIN_LEFT_OFFSET
	);
	top = ((boss_center_y >> 4) - KOTOHIME_MAIN_TOP_OFFSET);

	sprite_offset = boss_sprite_offset;
	if(boss_hit) {
		sprite_offset += 0x10;
	}
	sprite16_put(left, top, sprite_offset);

	// This byte render-mode guard naturally spells `!=0`, without
	// changing the physical ring's signed-angle/near-pascal ABI.
	if(boss_render_mode) {
		kotohime_render_ring(kotohime_orbit_count);
	}
}

void near pascal kotohime_render_intro(int radius)
{
	if(round_frame_mod2 && (boss_frame < KOTOHIME_INTRO_BLINK_END_FRAME)) {
		return;
	}

	sprite16_put_size.w = KOTOHIME_RING_SPRITE_WIDTH;
	sprite16_put_size.h = KOTOHIME_RING_SPRITE_HEIGHT;
	boss_render_mode = KOTOHIME_RENDER_MODE_EXPANDING;
	boss_move_phase += 2;
	boss_effect_radius = radius;
	kotohime_render_ring(KOTOHIME_INTRO_RING_COUNT);
	boss_render_mode = KOTOHIME_RENDER_MODE_NORMAL;
}

void far gba_boss_render_kotohime(void)
{
	if(pid_current != gba_boss_launched_by) {
		return;
	}

	sprite16_clip_set_for_pid(1 - pid_current);

	if(boss_mode == KOTOHIME_MODE_INTRO) {
		kotohime_render_intro(
			TO_SP(KOTOHIME_INTRO_RADIUS_PIXELS - (boss_frame * 2))
		);
		return;
	}
	if(boss_mode != KOTOHIME_MODE_EXPLODE) {
		kotohime_render_main();
		return;
	}
	boss_explosion_render();
}
