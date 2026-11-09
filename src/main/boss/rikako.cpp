// Complete current native-source reconstruction of the original Rikako
// major BOSS in MAIN_03_TEXT. Real shared BOSS storage and helpers remain
// externally owned; complete normal MAIN is checked by original TLINK.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/rikako.hpp"
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

// Shares the physical 32-byte BOSS layout; trailing bytes are per-character.
#include "src/main/boss/template_state.hpp"

extern boss_template_state_t boss_character_template[PLAYER_COUNT];

extern int boss_center_x;
extern int boss_center_y;
extern int boss_hp;
extern sprite16_offset_t boss_sprite_offset;
extern unsigned char boss_hit;
extern unsigned char boss_mode;
extern unsigned char boss_render_frame;
extern signed char boss_spin_delta;
extern unsigned int boss_frame;

extern unsigned char rikako_orbit_count;
extern unsigned char rikako_entity_count;
extern unsigned char rikako_pellet_count;
extern unsigned char rikako_burst_interval;
extern unsigned char rikako_burst_speed;

extern unsigned char rikako_random_angle;
extern unsigned char rikako_bullet_type;

extern int SinTable8[256];
extern int CosTable8[256];

extern "C" {
void far pascal bomb_center_add(int x, int y, int pid);
void far pascal bomb_axis_add(int x, int y, int pid);
void far pascal bomb_explosion_add(int x, int y, int pid);
void far pascal rikako_extra_add(int x, int y, unsigned char angle);
}

// Values selected by the shared BOSS scheduler, with Rikako's original
// per-character orbit / entity / alternating barrage mapping.
enum rikako_boss_mode_t {
    RIKAKO_MODE_INTRO = 0x00,
    RIKAKO_MODE_SELECT = 0x01,
    RIKAKO_MODE_ORBIT_0 = 0x02,
    RIKAKO_MODE_ORBIT_1 = 0x03,
    RIKAKO_MODE_ORBIT_2 = 0x04,
    RIKAKO_MODE_ORBIT_3 = 0x05,
    RIKAKO_MODE_ALTERNATE_0 = 0x06,
    RIKAKO_MODE_ENTITIES_0 = 0x07,
    RIKAKO_MODE_ENTITIES_1 = 0x08,
    RIKAKO_MODE_ENTITIES_2 = 0x09,
    RIKAKO_MODE_ENTITIES_3 = 0x0A,
    RIKAKO_MODE_ENTITIES_4 = 0x0B,
    RIKAKO_MODE_ENTITIES_5 = 0x0C,
    RIKAKO_MODE_ALTERNATE_1 = 0x0D,
    RIKAKO_MODE_ALTERNATE_2 = 0x0E,
    RIKAKO_MODE_ALTERNATE_3 = 0x0F,
    RIKAKO_MODE_ALTERNATE_4 = 0x10,
    RIKAKO_MODE_ALTERNATE_5 = 0x11,
    RIKAKO_MODE_DESCEND = 0x80,
    RIKAKO_MODE_EXPLODE = 0xFF,
};

// The same BOSS dispatcher owns its attack patterns, eight-sprite
// orbital renderer and sixteen-sprite arrival. These original gates are
// not interchangeable with the signed spin-delta update cadence.
enum rikako_render_timing_t {
    RIKAKO_INTRO_FINISH_FRAME = 0x64,
    RIKAKO_INTRO_FLICKER_END = 0x40,
    RIKAKO_MAIN_SPRITE_COUNT = 8,
    RIKAKO_INTRO_SPRITE_COUNT = 0x10,
    RIKAKO_CIRCLE_ANGLE_UNITS = 256,
    RIKAKO_RING_ANIM_PERIOD = 4,
    RIKAKO_INTRO_BLINK_PERIOD = 2,
    RIKAKO_ORBIT_RING_RADIUS = 48,
    RIKAKO_RENDER_MAIN_ANGLE_STEP = 0x20,
    RIKAKO_RENDER_INTRO_ANGLE_STEP = 0x10,
    RIKAKO_ORBIT_SUBPIXEL_RADIUS = TO_SP(48),
    RIKAKO_PELLET_VOLLEY_COUNT = 4,
    RIKAKO_PELLET_VOLLEY_SPEED_INC = 8,
    RIKAKO_BURST_HALF_TURN = 0x80,
    RIKAKO_COLLISION_STRIPE_WIDTH = 64,
    RIKAKO_COLLISION_TILE_HEIGHT = 48,
    RIKAKO_COLLISION_HALF_RADIUS = TO_SP(32),
    RIKAKO_RENDER_MAIN_W = 96,
    RIKAKO_RENDER_MAIN_H = 48,
    RIKAKO_RENDER_MAIN_LEFT = 48,
    RIKAKO_RENDER_MAIN_TOP = 32,
    RIKAKO_RENDER_RING_W = 16,
    RIKAKO_RENDER_RING_H = 8,
    RIKAKO_RENDER_INTRO_W = 48,
    RIKAKO_RENDER_INTRO_H = 24,
};

enum rikako_template_layout_t {
    RIKAKO_TEMPLATE_CENTER_X = 0x900,
    RIKAKO_TEMPLATE_CENTER_Y = 0x500,
    RIKAKO_TEMPLATE_VELOCITY_X = -0x20,
    RIKAKO_TEMPLATE_HP = 0x6E,
    RIKAKO_TEMPLATE_SPIN = 4,
    RIKAKO_TEMPLATE_SPRITE_OFF = 0x286,
    RIKAKO_TEMPLATE_PLAYER2_OFF = 0x28,
};

enum rikako_render_layout_t {
    RIKAKO_RENDER_HIT_SPRITE_OFF = 0x0C,
    RIKAKO_RENDER_RING_CENTER_OFF = 40,
    RIKAKO_RENDER_RING_SPRITE_BASE = 0x167E,
    RIKAKO_RENDER_RING_SPRITE_STEP = 2,
    RIKAKO_RENDER_INTRO_RADIUS = 0xC80,
    RIKAKO_INTRO_RAD_SCALE_A = 2,
    RIKAKO_INTRO_RAD_SCALE_B = 16,
    RIKAKO_RENDER_INTRO_SPRITE_BASE = 0x780,
    RIKAKO_RENDER_INTRO_SPRITE_ALT = 0x780,
    RIKAKO_RENDER_INTRO_LEFT_HALF = 24,
    RIKAKO_RENDER_INTRO_TOP_SHIFT = 4,
    RIKAKO_RENDER_INTRO_TOP_BIAS = 8,
    RIKAKO_RENDER_INTRO_ANGLE_SCALE = 4,
};

enum rikako_level_scaling_t {
    RIKAKO_ORBIT_COUNT_DIV = 2,
    RIKAKO_ORBIT_COUNT_BASE = 0x10,
    RIKAKO_ENTITY_COUNT_DIV = 4,
    RIKAKO_ENTITY_COUNT_BASE = 8,
    RIKAKO_PELLET_COUNT_DIV = 2,
    RIKAKO_PELLET_COUNT_BASE = 0x1C,
    RIKAKO_BURST_INTERVAL_BASE = 0x20,
    RIKAKO_BURST_SPEED_BASE = 0x40,
};

enum rikako_spin_limits_t {
    RIKAKO_SPIN_POSITIVE_LIMIT = 8,
    RIKAKO_SPIN_NEGATIVE_LIMIT = -8,
    RIKAKO_SPIN_NEUTRAL = 2,
};

enum rikako_render_state_t {
    RIKAKO_RENDER_MODE_NORMAL = 0,
    RIKAKO_RENDER_RING_STATIC_OFF = 0x284,
};

enum rikako_orbit_angle_t {
    RIKAKO_ORBIT_ANGLE_DELTA = 0x30,
    RIKAKO_ORBIT_ANGLE_DELTA_NEG = -0x30,
};

enum rikako_sound_effect_t {
    RIKAKO_SOUND_BOMB = 5,
    RIKAKO_SOUND_BULLET = 10,
};

void far pascal boss_rikako_template_init(int player_id)
{
	boss_template_state_t near *p =
		&boss_character_template[player_id];

	p->center_x = RIKAKO_TEMPLATE_CENTER_X;
	p->center_y = RIKAKO_TEMPLATE_CENTER_Y;
	p->velocity_x = RIKAKO_TEMPLATE_VELOCITY_X;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = RIKAKO_MODE_INTRO;
	p->hp = RIKAKO_TEMPLATE_HP;
	p->pattern_i = 0;
	p->spin_delta = RIKAKO_TEMPLATE_SPIN;
	p->effect_radius = 0;
	p->sprite_offset = RIKAKO_TEMPLATE_SPRITE_OFF;
	if(player_id != 0) {
		p->sprite_offset += RIKAKO_TEMPLATE_PLAYER2_OFF;
	}
	p->render_mode = RIKAKO_RENDER_MODE_NORMAL;
}

// The same 0x10 warning and 0x28 release drive Rikako's orbiting
// spread and the unrelated entity barrage, but the shots differ.
enum rikako_orbit_phase_t {
    RIKAKO_ORBIT_WARNING_FRAME = 0x10,
    RIKAKO_ORBIT_FIRE_FRAME = 0x28,
    RIKAKO_ORBIT_FINISH_AFTER = 0x50,
    RIKAKO_SPIN_TICK_PERIOD = 8,
};

// The original 256-step signed angular distribution must be multiplied
// BEFORE the physical integer division and byte-angle truncation.
void near rikako_pattern_orbit_spread(void)
{
	unsigned char angle;
	signed char angle_delta;

	// The unsigned-word eight-frame spin clock uses a low-bit test,
	// distinct from the signed byte spin delta.
	if(boss_spin_delta <= RIKAKO_SPIN_POSITIVE_LIMIT) {
		if((boss_frame & (RIKAKO_SPIN_TICK_PERIOD - 1)) == 0) {
			boss_spin_delta++;
		}
	}

	if(boss_frame == RIKAKO_ORBIT_WARNING_FRAME) {
		bomb_center_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);
		return;
	}

	if(boss_frame == RIKAKO_ORBIT_FIRE_FRAME) {
		bomb_explosion_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);

		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.group = BG_5_SPREAD_WIDE;
		bullet_template.speed.v = (TO_SP(1) + 12);

		angle_delta = (
			randring_far_next16_and(1)
			? RIKAKO_ORBIT_ANGLE_DELTA
			: RIKAKO_ORBIT_ANGLE_DELTA_NEG
		);

		// Original 256-unit angle distribution precedes signed division;
		// ordinary C++ for retains the complete ring call order.
		for(register int i = 0; i < rikako_orbit_count; ++i) {
			angle = ((i * RIKAKO_CIRCLE_ANGLE_UNITS) / rikako_orbit_count);
			bullet_template.center.x.v = polar(
				boss_center_x,
				RIKAKO_ORBIT_SUBPIXEL_RADIUS,
				CosTable8[angle]
			);
			bullet_template.center.y.v = polar(
				boss_center_y,
				RIKAKO_ORBIT_SUBPIXEL_RADIUS,
				SinTable8[angle]
			);
			bullet_template.angle = (angle + angle_delta);
			bullets_add();
		}
		snd_se_play(RIKAKO_SOUND_BOMB);
		return;
	}

	if(boss_frame > RIKAKO_ORBIT_FINISH_AFTER) {
		boss_frame = 0;
		boss_mode = RIKAKO_MODE_SELECT;
	}
}

enum rikako_entities_phase_t {
    RIKAKO_ENTITIES_WARNING_FRAME = 0x10,
    RIKAKO_ENTITIES_RELEASE_FRAME = 0x28,
    RIKAKO_ENTITIES_PELLET_FRAME = 0x40,
    RIKAKO_ENTITIES_FINISH_AFTER = 0x50,
};

void near rikako_pattern_entities_and_pellets(void)
{
	unsigned char angle;
	register int i;

	if(boss_spin_delta >= RIKAKO_SPIN_NEGATIVE_LIMIT) {
		if((boss_frame & (RIKAKO_SPIN_TICK_PERIOD - 1)) == 0) {
			boss_spin_delta--;
		}
	}

	if(boss_frame == RIKAKO_ENTITIES_WARNING_FRAME) {
		bomb_axis_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);
		return;
	}

	if(boss_frame == RIKAKO_ENTITIES_RELEASE_FRAME) {
		bomb_explosion_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);
		// This RNG word is overwritten by the first ring angle, but
		// consuming it still changes all subsequent game randomness.
		angle = randring_far_next16();
		// This separate emitter consumes the original otherwise overwritten
		// RNG result before its same 256-step angular distribution.
		i = 0;
		while(i < rikako_entity_count) {
			angle = ((i * RIKAKO_CIRCLE_ANGLE_UNITS) / rikako_entity_count);
			rikako_extra_add(
				boss_center_x,
				boss_center_y,
				angle
			);
			++i;
		}
		snd_se_play(RIKAKO_SOUND_BOMB);
		return;
	}

	if(boss_frame == RIKAKO_ENTITIES_PELLET_FRAME) {
		bullet_template.type = BT_PELLET;
		bullet_template.group = BG_RING;
		bullet_template.count = rikako_pellet_count;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.speed.v = TO_SP(2);

		// Four genuinely distinct RNG angles, speed +8 and bullets_add
		// calls. This natural while preserves the original mutation order
		// and all original CODE bytes (native TC4 trial af904a).
		i = 0;
		while(i < RIKAKO_PELLET_VOLLEY_COUNT) {
			bullet_template.angle = randring_far_next16();
			bullet_template.speed.v += RIKAKO_PELLET_VOLLEY_SPEED_INC;
			bullets_add();
			++i;
		}
		snd_se_play(RIKAKO_SOUND_BULLET);
		return;
	}

	if(boss_frame > RIKAKO_ENTITIES_FINISH_AFTER) {
		boss_frame = 0;
		boss_mode = RIKAKO_MODE_SELECT;
	}
}

// Alternating bursts draw RNG at remainder 1, then fire paired volleys
// at 1/5/9/13; the speed and signed angle delta are unchanged.
enum rikako_burst_phase_t {
    RIKAKO_BURST_FIRST = 1,
    RIKAKO_BURST_SECOND = 5,
    RIKAKO_BURST_THIRD = 9,
    RIKAKO_BURST_FOURTH = 0x0D,
    RIKAKO_BURST_FINISH_FRAME = 0x80,
};

void near rikako_pattern_alternating_burst(void)
{
	unsigned char remainder;

	boss_move_sine();

	if(boss_spin_delta != RIKAKO_SPIN_NEUTRAL) {
		if((boss_frame & (RIKAKO_SPIN_TICK_PERIOD - 1)) == 0) {
			boss_spin_delta += ((boss_spin_delta > RIKAKO_SPIN_NEUTRAL) ? -1 : 1);
		}
	}

	remainder = (boss_frame % rikako_burst_interval);
	if(remainder == RIKAKO_BURST_FIRST) {
		rikako_random_angle = randring_far_next16();
		rikako_bullet_type = (randring_far_next16_and(1) + 1);
	}

	bullet_template.type = rikako_bullet_type;
	bullet_template.group = BG_4_SPREAD_NARROW;
	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = boss_center_y;
	bullet_template.angle = rikako_random_angle;
	bullet_template.speed.v = rikako_burst_speed;

	if(
		(remainder == RIKAKO_BURST_FIRST) ||
		(remainder == RIKAKO_BURST_SECOND) ||
		(remainder == RIKAKO_BURST_THIRD) ||
		(remainder == RIKAKO_BURST_FOURTH)
	) {
		snd_se_play(RIKAKO_SOUND_BULLET);
		bullets_add();

		bullet_template.angle = (rikako_random_angle + RIKAKO_BURST_HALF_TURN);
		bullets_add();
	}

	if(boss_frame >= RIKAKO_BURST_FINISH_FRAME) {
		boss_mode = RIKAKO_MODE_SELECT;
		boss_frame = 0;
	}
}

void far gba_boss_update_rikako(void)
{
	if(boss_update_start()) {
		rikako_orbit_count = ((gba_boss_level / RIKAKO_ORBIT_COUNT_DIV) + RIKAKO_ORBIT_COUNT_BASE);
		rikako_entity_count = ((gba_boss_level / RIKAKO_ENTITY_COUNT_DIV) + RIKAKO_ENTITY_COUNT_BASE);
		rikako_pellet_count = ((gba_boss_level / RIKAKO_PELLET_COUNT_DIV) + RIKAKO_PELLET_COUNT_BASE);
		rikako_burst_interval = (RIKAKO_BURST_INTERVAL_BASE - gba_boss_level);
		rikako_burst_speed = (gba_boss_level + RIKAKO_BURST_SPEED_BASE);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_t pid_other = (1 - pid_current);
	bullet_template.pid = pid_other;
	boss_target_update();
	boss_frame++;

	switch(boss_mode) {
	case RIKAKO_MODE_INTRO:
		if(boss_frame == RIKAKO_INTRO_FINISH_FRAME) {
			boss_frame = 0;
			boss_mode = RIKAKO_MODE_SELECT;
		} else {
			return;
		}
		break;

	case RIKAKO_MODE_SELECT:
		boss_pattern_next();
		break;

	case RIKAKO_MODE_ORBIT_0:
	case RIKAKO_MODE_ORBIT_1:
	case RIKAKO_MODE_ORBIT_2:
	case RIKAKO_MODE_ORBIT_3:
		rikako_pattern_orbit_spread();
		break;

	case RIKAKO_MODE_ENTITIES_0:
	case RIKAKO_MODE_ENTITIES_1:
	case RIKAKO_MODE_ENTITIES_2:
	case RIKAKO_MODE_ENTITIES_3:
	case RIKAKO_MODE_ENTITIES_4:
	case RIKAKO_MODE_ENTITIES_5:
		rikako_pattern_entities_and_pellets();
		break;

	case RIKAKO_MODE_ALTERNATE_0:
	case RIKAKO_MODE_ALTERNATE_1:
	case RIKAKO_MODE_ALTERNATE_2:
	case RIKAKO_MODE_ALTERNATE_3:
	case RIKAKO_MODE_ALTERNATE_4:
	case RIKAKO_MODE_ALTERNATE_5:
		rikako_pattern_alternating_burst();
		break;

	case RIKAKO_MODE_DESCEND:
		boss_fall();
		break;

	case RIKAKO_MODE_EXPLODE:
		return;
	}

	// Keep compound signed-byte spin mutation: writing an explicit
	// byte = byte + signed_delta changed original CODE (af904c).
	boss_render_frame += boss_spin_delta;

	collmap_center.x.v = boss_center_x;
	collmap_center.y.v = boss_center_y;
	collmap_stripe_tile_w.set(RIKAKO_COLLISION_STRIPE_WIDTH);
	collmap_tile_h.set(RIKAKO_COLLISION_TILE_HEIGHT);
	collmap_pid = pid_other;
	collmap_set_rect_striped();

	hitbox_hittest_skip_explosions = true;
	hitbox.radius.x.v = RIKAKO_COLLISION_HALF_RADIUS;
	hitbox.radius.y.v = RIKAKO_COLLISION_HALF_RADIUS;
	hitbox.pid = pid_other;
	hitbox.origin.center.x.v = boss_center_x;
	hitbox.origin.center.y.v = boss_center_y;
	boss_hit = hitbox_hittest();
	boss_hp -= boss_hit;
	hitbox_hittest_skip_explosions = false;
	boss_hittest_end();

}

void near rikako_render_main(void)
{
	screen_x_t left;
	screen_y_t top;
	int x;
	int y;
	register sprite16_offset_t sprite_offset;

	sprite16_put_size.w = RIKAKO_RENDER_MAIN_W;
	sprite16_put_size.h = RIKAKO_RENDER_MAIN_H;

	left = (
		playfield_fg_x_to_screen(
			boss_center_x,
			(1 - pid_current)
		) - RIKAKO_RENDER_MAIN_LEFT
	);
	top = ((boss_center_y >> 4) - RIKAKO_RENDER_MAIN_TOP);

	sprite_offset = boss_sprite_offset;
	if(boss_hit) {
		sprite_offset += RIKAKO_RENDER_HIT_SPRITE_OFF;
	}
	sprite16_put(left, top, sprite_offset);

	sprite16_put_size.w = RIKAKO_RENDER_RING_W;
	sprite16_put_size.h = RIKAKO_RENDER_RING_H;
	unsigned char angle = boss_render_frame;
	left += RIKAKO_RENDER_RING_CENTER_OFF;
	top += RIKAKO_RENDER_RING_CENTER_OFF;

	// Native original sprite loop accepts signed-index C++ for,
	// but its %4 MUST explicitly promote that signed `i` to unsigned:
	// ordinary signed `i %4` differs in original TC4 (af862f).
	for(register int i = 0; i < RIKAKO_MAIN_SPRITE_COUNT; ++i, angle = angle + RIKAKO_RENDER_MAIN_ANGLE_STEP) {
		x = polar(left, RIKAKO_ORBIT_RING_RADIUS, CosTable8[angle]);
		y = polar(top, RIKAKO_ORBIT_RING_RADIUS, SinTable8[angle]);

		// This signed *index* needs unsigned promotion before %4;
		// plain signed modulo changed original CODE (af904e).
		if(static_cast<unsigned int>(i) % RIKAKO_RING_ANIM_PERIOD) {
			sprite_offset = (((static_cast<unsigned int>(i) % RIKAKO_RING_ANIM_PERIOD) * RIKAKO_RENDER_RING_SPRITE_STEP) + RIKAKO_RENDER_RING_SPRITE_BASE);
		} else {
			sprite_offset = RIKAKO_RENDER_RING_STATIC_OFF;
		}

		sprite16_put(
			x,
			y,
			(pid.so_attack + sprite_offset)
		);
		// Original mutable byte += can naturally use explicit
		// assignment with named step, unlike signed spin_delta (af904f).
	}
}

// The signed intro radius keeps two natural 16-bit scale stages:
// flattening to frame*32 changes TC4 CODE (af679f). Keep the
// original binary zero-minus angle form; unary negation differs
// in native code (af679e).
void near rikako_render_intro(void)
{
	screen_y_t top;
	sprite16_offset_t sprite_offset;
	int radius;

	radius = (RIKAKO_RENDER_INTRO_RADIUS - ((boss_frame * RIKAKO_INTRO_RAD_SCALE_A) * RIKAKO_INTRO_RAD_SCALE_B));

	sprite16_put_size.w = RIKAKO_RENDER_INTRO_W;
	sprite16_put_size.h = RIKAKO_RENDER_INTRO_H;

	if((boss_frame < RIKAKO_INTRO_FLICKER_END) && (round_or_result_frame & (RIKAKO_INTRO_BLINK_PERIOD - 1))) {
		return;
	}

	sprite_offset = (pid.so_attack + RIKAKO_RENDER_INTRO_SPRITE_BASE);
	if(boss_frame & (RIKAKO_INTRO_BLINK_PERIOD - 1)) {
		sprite_offset += RIKAKO_RENDER_INTRO_SPRITE_ALT;
	}

	unsigned char angle = ((unsigned char)boss_frame * RIKAKO_RENDER_INTRO_ANGLE_SCALE);
	// Preserve binary zero-minus: the superficially natural unary
	// -angle changed native CODE again in independent af862d.
	angle = (0 - angle);

	// The second 16-sprite signed-step for loop and named +0x10
	// angle mutation preserve all original original TC4 instructions.
	for(register int i = 0; i < RIKAKO_INTRO_SPRITE_COUNT; ++i, angle = angle + RIKAKO_RENDER_INTRO_ANGLE_STEP) {
		register screen_x_t left = polar(
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
			playfield_fg_x_to_screen(
				left,
				(1 - pid_current)
			) - RIKAKO_RENDER_INTRO_LEFT_HALF
		);
		// The original signed AX shift and ADD AX,-8 both arise naturally
		// from this local assignment; passing it as an inline argument
		// instead changes TC4 CODE (af763c).
		top = static_cast<screen_y_t>((top >> RIKAKO_RENDER_INTRO_TOP_SHIFT) - RIKAKO_RENDER_INTRO_TOP_BIAS);
		sprite16_put(left, top, sprite_offset);
	}
}

void far gba_boss_render_rikako(void)
{
	if(pid_current != gba_boss_launched_by) {
		return;
	}

	sprite16_clip_set_for_pid(1 - pid_current);

	if(boss_mode == RIKAKO_MODE_INTRO) {
		rikako_render_intro();
		return;
	}
	if(boss_mode != RIKAKO_MODE_EXPLODE) {
		rikako_render_main();
		return;
	}
	boss_explosion_render();
}
