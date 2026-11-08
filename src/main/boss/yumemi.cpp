// Entire maintained original Yumemi major BOSS native C++ in MAIN_03_TEXT.
// Shared BOSS helper and DGROUP storage remain externally owned; the full
// Japanese normal MAIN linker proof is separate from canonical Factory.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/yumemi.hpp"
#include "src/main/boss/shared.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/libs/sprite16/sprite16.h"

#pragma option -a2

struct yumemi_player_view_t {
	PlayfieldPoint center;
	unsigned char rest[124];
};
extern yumemi_player_view_t players[PLAYER_COUNT];

#include "src/main/boss/template_state.hpp"

extern boss_template_state_t boss_character_template[PLAYER_COUNT];

extern int boss_center_x;
extern int boss_center_y;
extern PlayfieldPoint boss_aux_point;
extern int boss_hp;
extern sprite16_offset_t boss_sprite_offset;
extern unsigned char boss_hit;
extern unsigned char boss_mode;
extern unsigned char boss_render_mode;
extern unsigned char boss_render_frame;
extern unsigned char boss_move_phase;
extern unsigned int boss_effect_radius;
extern unsigned int boss_frame;

// Yumemi's six level-derived pattern parameters.
extern unsigned char yumemi_ring_speed;
extern unsigned char yumemi_ring_count;
extern unsigned char yumemi_aimed_speed_base;
extern unsigned char yumemi_cross_interval;
extern unsigned char yumemi_chase_until;
extern unsigned char yumemi_rain_interval;

// Yumemi-private pattern state.
extern unsigned char yumemi_speed_add;
extern signed char yumemi_angle_delta;
extern unsigned char yumemi_angle;
extern int yumemi_origin_x;
extern int yumemi_origin_y;

// Five fixed bullet groups in the original DATA segment.
extern unsigned char yumemi_groups[5];

extern "C" {
void far pascal bomb_axis_add(int x, int y, int pid);
void far pascal bomb_explosion_add(int x, int y, int pid);
void far pascal yumemi_extra_add(int x, int y);
}

// The original boss scheduler selects a value in 2..17 for each attack.
// These mode *values* are shared; Yumemi's grouping of them is character-specific.
enum yumemi_boss_mode_t {
    YUMEMI_MODE_INTRO = 0,
    YUMEMI_MODE_SELECT = 1,
    YUMEMI_MODE_RING_0 = 2,
    YUMEMI_MODE_RING_1 = 3,
    YUMEMI_MODE_RING_2 = 4,
    YUMEMI_MODE_RAIN_0 = 5,
    YUMEMI_MODE_RAIN_1 = 6,
    YUMEMI_MODE_AIMED_0 = 7,
    YUMEMI_MODE_AIMED_1 = 8,
    YUMEMI_MODE_AIMED_2 = 9,
    YUMEMI_MODE_RAIN_2 = 0x0A,
    YUMEMI_MODE_CROSS_0 = 0x0B,
    YUMEMI_MODE_CROSS_1 = 0x0C,
    YUMEMI_MODE_CROSS_2 = 0x0D,
    YUMEMI_MODE_CROSS_3 = 0x0E,
    YUMEMI_MODE_CHASE_0 = 0x0F,
    YUMEMI_MODE_CHASE_1 = 0x10,
    YUMEMI_MODE_CHASE_2 = 0x11,
    YUMEMI_MODE_DESCEND = 0x80,
    YUMEMI_MODE_EXPLODE = 0xFF,
};

enum yumemi_template_layout_t {
    YUMEMI_TEMPLATE_CENTER_X = 0x900,
    YUMEMI_TEMPLATE_CENTER_Y = 0x500,
    YUMEMI_TEMPLATE_VELOCITY_X = -0x20,
    YUMEMI_TEMPLATE_HP = 0x82,
    YUMEMI_TEMPLATE_SPRITE_OFFSET = 0x288,
    YUMEMI_TEMPLATE_PLAYER2_OFF = 0x28,
};

enum yumemi_render_mode_t {
    YUMEMI_RENDER_MODE_NONE = 0,
    YUMEMI_RENDER_MODE_PRIMARY = 1,
    YUMEMI_RENDER_MODE_ALTERNATE = 2,
};

enum yumemi_render_geometry_t {
    YUMEMI_RENDER_MAIN_SIZE = 112,
    YUMEMI_RENDER_MAIN_LEFT_HALF = 56,
    YUMEMI_RENDER_MAIN_TOP_OFFSET = 40,
    YUMEMI_RENDER_EFFECT_SIZE = 64,
    YUMEMI_RENDER_EFFECT_SPRITE_OFF = 0x0E,
    YUMEMI_RENDER_EFFECT_ALT_OFF = 0xA00,
    YUMEMI_RENDER_EFFECT_LEFT = 32,
    YUMEMI_RENDER_HIT_WIDTH = 80,
    YUMEMI_RENDER_HIT_HEIGHT = 96,
    YUMEMI_RENDER_HIT_LEFT = 16,
    YUMEMI_RENDER_HIT_SPRITE_OFF = 0x16,
    YUMEMI_RENDER_EFFECT_ORIGIN_SHIFT = 5,
    YUMEMI_RENDER_EFFECT_ORIGIN_BIAS = 8,
    YUMEMI_RENDER_EFFECT_COLOR = 10,
};

enum yumemi_render_clip_t {
    YUMEMI_CLIP_PLAYER0_LEFT = 16,
    YUMEMI_CLIP_PLAYER1_LEFT = 0x150,
    YUMEMI_CLIP_TOP = 8,
    YUMEMI_CLIP_PLAYER0_RIGHT = 0x12F,
    YUMEMI_CLIP_PLAYER1_RIGHT = 0x26F,
    YUMEMI_CLIP_BOTTOM = 0xBF,
};

enum yumemi_sound_effect_t {
    YUMEMI_SOUND_EXPLOSION = 5,
    YUMEMI_SOUND_AIMED_SHOT = 3,
};

void far pascal boss_yumemi_template_init(int player_id)
{
	boss_template_state_t near *p =
		&boss_character_template[player_id];

	p->center_x = YUMEMI_TEMPLATE_CENTER_X;
	p->center_y = YUMEMI_TEMPLATE_CENTER_Y;
	p->velocity_x = YUMEMI_TEMPLATE_VELOCITY_X;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = 0;
	p->hp = YUMEMI_TEMPLATE_HP;
	p->pattern_i = 0;
	p->render_frame = 0;
	p->move_phase = 0;
	p->effect_radius = 0;
	p->sprite_offset = YUMEMI_TEMPLATE_SPRITE_OFFSET;
	if(player_id != 0) {
		p->sprite_offset += YUMEMI_TEMPLATE_PLAYER2_OFF;
	}
	p->render_mode = 0;
}

// Yumemi's expanding/rotating ring pattern has a distinct warning
// interval before bullets appear. The frame comparisons retain the
// original unsigned 16-bit timer behavior.
enum yumemi_ring_phase_t {
    YUMEMI_RING_INIT_FRAME = 1,
    YUMEMI_RING_WARNING_END = 4,
    YUMEMI_RING_BULLET_START = 0x20,
    YUMEMI_RING_FINISH_AFTER = 0x3C,
    YUMEMI_RING_FIRE_PERIOD = 4,
    YUMEMI_RING_INITIAL_RADIUS = 0x100,
    YUMEMI_RING_ANGLE_DELTA_RIGHT = 3,
    YUMEMI_RING_ANGLE_DELTA_LEFT = -3,
    YUMEMI_RING_SPEED_ADD_STEP = 8,
};

void near yumemi_pattern_ring(void)
{
	if(boss_frame == YUMEMI_RING_INIT_FRAME) {
		boss_render_mode = YUMEMI_RENDER_MODE_PRIMARY;
		yumemi_angle = randring_far_next16();
		yumemi_speed_add = 0;
		boss_effect_radius = YUMEMI_RING_INITIAL_RADIUS;
		yumemi_angle_delta = (
			(randring_far_next16_and(1) == 0) ? YUMEMI_RING_ANGLE_DELTA_RIGHT : YUMEMI_RING_ANGLE_DELTA_LEFT
		);
	}

	if(boss_frame < YUMEMI_RING_WARNING_END) {
		bomb_axis_add(
			yumemi_origin_x,
			yumemi_origin_y,
			bullet_template.pid
		);
		return;
	}

	if(boss_frame < YUMEMI_RING_BULLET_START) {
		return;
	}

	if(boss_frame == YUMEMI_RING_BULLET_START) {
		bomb_explosion_add(
			yumemi_origin_x,
			yumemi_origin_y,
			bullet_template.pid
		);
		boss_render_mode = YUMEMI_RENDER_MODE_ALTERNATE;
		snd_se_play(YUMEMI_SOUND_EXPLOSION);
	}

	// Original 16-bit frame clock is genuinely unsigned; natural
	// zero-remainder predicate preserves original ring timing (af897b).
	if(!(boss_frame % YUMEMI_RING_FIRE_PERIOD)) {
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.angle = yumemi_angle;
		bullet_template.group = BG_RING;
		bullet_template.center.x.v = yumemi_origin_x;
		bullet_template.center.y.v = yumemi_origin_y;
		bullet_template.speed.v = (yumemi_ring_speed + yumemi_speed_add);
		bullet_template.count = yumemi_ring_count;
		bullets_add();

		// Keep original compound byte addition of signed delta. A
		// direct `angle = angle + signed_delta` changed native CODE
		// in the fresh original compiler trial af897c.
		yumemi_angle += yumemi_angle_delta;
		yumemi_speed_add += YUMEMI_RING_SPEED_ADD_STEP;
	}

	if(boss_frame > YUMEMI_RING_FINISH_AFTER) {
		boss_render_mode = YUMEMI_RENDER_MODE_NONE;
		boss_mode = YUMEMI_MODE_SELECT;
		boss_frame = 0;
	}
}

// Timing gates for the long aimed, cross, chase and rain BOSS attacks.
// Preserve each attack's exact inclusive/exclusive frame transition.
enum yumemi_attack_timing_t {
    YUMEMI_AIMED_INIT_FRAME = 1,
    YUMEMI_AIMED_WARNING_END = 0x10,
    YUMEMI_AIMED_WARNING_PERIOD = 4,
    YUMEMI_AIMED_WARNING_PHASE = 1,
    YUMEMI_AIMED_FIRE_PERIOD = 2,
    YUMEMI_AIMED_FIRE_START = 0x20,
    YUMEMI_AIMED_FINISH_AFTER = 0x60,
    YUMEMI_CROSS_FINISH_AT = 0x60,
    YUMEMI_CHASE_TRACK_END = 0x20,
    // The real near-stage movement first reaches the side margins.
    YUMEMI_CHASE_LEFT_BOUNDARY = 0x380,
    YUMEMI_CHASE_RIGHT_BOUNDARY = 0xE80,
    YUMEMI_CHASE_BEAM_PERIOD = 16,
    YUMEMI_CHASE_BEAM_PHASE = 15,
    YUMEMI_RAIN_BEGIN = 0x20,
    YUMEMI_RAIN_SPREAD_END = 0x40,
    YUMEMI_RAIN_FINISH_AT = 0x60,
    YUMEMI_RAIN_DROPS_PER_WAVE = 12,
    YUMEMI_CROSS_RING_DISPLACEMENT = TO_SP(32),
    YUMEMI_ORIGIN_X_OFFSET = 0x90,
    YUMEMI_ORIGIN_Y_OFFSET = 0x180,
    YUMEMI_INTRO_SOUND_FIRST_FRAME = 0x18,
    YUMEMI_INTRO_SOUND_SECOND_FRAME = 0x48,
    YUMEMI_INTRO_FINISH_FRAME = 0x60,
    YUMEMI_COLLISION_TILE_SIZE = 56,
    YUMEMI_COLLISION_HALF_RADIUS = TO_SP(32),
    YUMEMI_RAIN_RANDOM_ANGLE_MASK = 0x3F,
    YUMEMI_RAIN_RANDOM_ANGLE_BIAS = 0x20,
    YUMEMI_RAIN_SMALL_SPEED = TO_SP(2) + 4,
    YUMEMI_RAIN_INITIAL_ANGLE = -0x40,
    YUMEMI_RAIN_SPREAD_SPEED = TO_SP(6),
    YUMEMI_CHASE_RENDER_FRAME = 2,
    YUMEMI_EFFECT_RADIUS_DECAY = 8,
    YUMEMI_AIMED_RENDER_FRAME_START = 0x20,
};

void near yumemi_pattern_aimed_random(void)
{
	if(boss_frame == YUMEMI_AIMED_INIT_FRAME) {
		boss_render_mode = YUMEMI_RENDER_MODE_PRIMARY;
		boss_aux_point.x = players[bullet_template.pid].center.x;
		boss_aux_point.y = players[bullet_template.pid].center.y;
		yumemi_angle = iatan2(
			(boss_aux_point.y.v - yumemi_origin_y),
			(boss_aux_point.x.v - yumemi_origin_x)
		);
		boss_effect_radius = YUMEMI_RING_INITIAL_RADIUS;
		boss_render_frame = YUMEMI_AIMED_RENDER_FRAME_START;
	}

	if(boss_frame < YUMEMI_AIMED_WARNING_END) {
		if((boss_frame % YUMEMI_AIMED_WARNING_PERIOD) == YUMEMI_AIMED_WARNING_PHASE) {
			bomb_axis_add(
				boss_aux_point.x.v,
				boss_aux_point.y.v,
				bullet_template.pid
			);
		}
		return;
	}

	if(boss_frame < YUMEMI_AIMED_FIRE_START) {
		return;
	}

	if(boss_frame == YUMEMI_AIMED_FIRE_START) {
		bomb_explosion_add(
			yumemi_origin_x,
			yumemi_origin_y,
			bullet_template.pid
		);
		boss_render_mode = YUMEMI_RENDER_MODE_ALTERNATE;
	}

	if(!(boss_frame % YUMEMI_AIMED_FIRE_PERIOD)) {
		snd_se_play(YUMEMI_SOUND_AIMED_SHOT);
		bullet_template.center.x.v = yumemi_origin_x;
		bullet_template.center.y.v = yumemi_origin_y;
		bullet_template.angle = yumemi_angle;
		bullet_template.speed.v = (
			randring_far_next16_and(0x1F) + yumemi_aimed_speed_base
		);
		bullet_template.type = (randring_far_next16_and(1) + 1);
		bullet_template.group = yumemi_groups[randring_far_next16_mod(5)];
		bullets_add();
	}

	if(boss_frame > YUMEMI_AIMED_FINISH_AFTER) {
		boss_render_mode = YUMEMI_RENDER_MODE_NONE;
		boss_mode = YUMEMI_MODE_SELECT;
		boss_frame = 0;
	}
}

void near yumemi_pattern_cross_rings(void)
{
	boss_move_sine();

	if(!(boss_frame % yumemi_cross_interval)) {
		bullet_template.group = BG_4_RING;
		bullet_template.speed.v = TO_SP(2);
		bullet_template.type = (randring_far_next16_and(1) + 1);

		bullet_template.angle = randring_far_next16();
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = (boss_center_y - YUMEMI_CROSS_RING_DISPLACEMENT);
		bullets_add();

		bullet_template.angle = randring_far_next16();
		bullet_template.center.y.v = (boss_center_y + YUMEMI_CROSS_RING_DISPLACEMENT);
		bullets_add();

		bullet_template.angle = randring_far_next16();
		bullet_template.center.x.v = (boss_center_x - YUMEMI_CROSS_RING_DISPLACEMENT);
		bullet_template.center.y.v = boss_center_y;
		bullets_add();

		bullet_template.angle = randring_far_next16();
		bullet_template.center.x.v = (boss_center_x + YUMEMI_CROSS_RING_DISPLACEMENT);
		bullets_add();
	}

	if(boss_frame >= YUMEMI_CROSS_FINISH_AT) {
		boss_mode = YUMEMI_MODE_SELECT;
		boss_frame = 0;
	}
}

void near yumemi_pattern_chase(void)
{
	if(!boss_move_phase) {
		// Keep the original positive, short-circuit range test. Reversing
		// this into an early exit changes original TC4 branching (af848d).
		if(
			(boss_center_x > YUMEMI_CHASE_LEFT_BOUNDARY) &&
			(boss_center_x < YUMEMI_CHASE_RIGHT_BOUNDARY)
		) {
			boss_move_sine();
			return;
		}
		boss_move_phase = 1;
		boss_frame = 0;
		return;
	}

	boss_render_frame = YUMEMI_CHASE_RENDER_FRAME;
	boss_aux_point.x = players[bullet_template.pid].center.x;
	boss_aux_point.y = players[bullet_template.pid].center.y;

	if(boss_frame < YUMEMI_CHASE_TRACK_END) {
		return;
	}

	boss_move_sine();
	boss_move_sine();

	if((boss_frame % YUMEMI_CHASE_BEAM_PERIOD) == YUMEMI_CHASE_BEAM_PHASE) {
		boss_render_mode = YUMEMI_RENDER_MODE_PRIMARY;
		bomb_axis_add(
			boss_aux_point.x.v,
			boss_aux_point.y.v,
			bullet_template.pid
		);
		yumemi_extra_add(boss_aux_point.x.v, boss_aux_point.y.v);
		return;
	}

	if(boss_frame > yumemi_chase_until) {
		boss_render_mode = YUMEMI_RENDER_MODE_NONE;
		boss_mode = YUMEMI_MODE_SELECT;
		boss_frame = 0;
		boss_move_phase = 0;
	}
}

void near yumemi_pattern_rain(void)
{
	register int i;

	boss_move_sine();

	// Distinct rain clock, also native-exact as if(!remainder).
	if(!(boss_frame % yumemi_rain_interval)) {
		bullet_template.type = BT_BULLET16_DEFAULT;

		if(boss_frame < YUMEMI_RAIN_SPREAD_END) {
			bullet_template.center.x.v = yumemi_origin_x;
			bullet_template.center.y.v = yumemi_origin_y;
			bullet_template.angle = YUMEMI_RAIN_INITIAL_ANGLE;
			bullet_template.speed.v = YUMEMI_RAIN_SPREAD_SPEED;
			bullet_template.group = BG_5_SPREAD_WIDE;
			bullets_add();
			bullet_template.group = BG_4_SPREAD_WIDE;
			bullets_add();
		}

		if(boss_frame >= YUMEMI_RAIN_BEGIN) {
			bullet_template.group = BG_1;
			bullet_template.speed.v = YUMEMI_RAIN_SMALL_SPEED;
			bullet_template.center.y.v = 0;
			// Twelve physically separate RNG-X and byte-angle draws, with
			// one bullet add per iteration before advancing signed i.
			// Native original 16-bit TC4 accepts this natural while.
			i = 0;
			while(i < YUMEMI_RAIN_DROPS_PER_WAVE) {
				bullet_template.center.x.v =
					randring_far_next16_mod(TO_SP(PLAYFIELD_W));
				bullet_template.angle = (
					randring_far_next16_and(YUMEMI_RAIN_RANDOM_ANGLE_MASK) + YUMEMI_RAIN_RANDOM_ANGLE_BIAS
				);
				bullets_add();
				++i;
			}
		}
	}

	if(boss_frame >= YUMEMI_RAIN_FINISH_AT) {
		boss_mode = YUMEMI_MODE_SELECT;
		boss_frame = 0;
	}
}

void far gba_boss_update_yumemi(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		yumemi_ring_speed = ((gba_boss_level / 2) + 0x10);
		yumemi_ring_count = ((gba_boss_level / 2) + 0x10);
		yumemi_aimed_speed_base = (gba_boss_level + 0x40);
		yumemi_cross_interval = (0x12 - gba_boss_level);
		yumemi_chase_until = ((gba_boss_level * 4) + 0x50);
		yumemi_rain_interval = (0x10 - (gba_boss_level / 2));
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	bullet_template.pid = pid_other;
	boss_target_update();
	boss_frame++;

	yumemi_origin_x = (boss_center_x + YUMEMI_ORIGIN_X_OFFSET);
	yumemi_origin_y = (boss_center_y - YUMEMI_ORIGIN_Y_OFFSET);

	switch(boss_mode) {
	case YUMEMI_MODE_INTRO:
		if((boss_frame == YUMEMI_INTRO_SOUND_FIRST_FRAME) || (boss_frame == YUMEMI_INTRO_SOUND_SECOND_FRAME)) {
			snd_se_reset();
			snd_se_play(YUMEMI_SOUND_EXPLOSION);
		}
		if(boss_frame != YUMEMI_INTRO_FINISH_FRAME) {
			return;
		}
		boss_frame = 0;
		boss_mode = YUMEMI_MODE_SELECT;
		break;

	case YUMEMI_MODE_SELECT:
		boss_pattern_next();
		break;

	case YUMEMI_MODE_RING_0:
	case YUMEMI_MODE_RING_1:
	case YUMEMI_MODE_RING_2:
		yumemi_pattern_ring();
		break;

	case YUMEMI_MODE_AIMED_0:
	case YUMEMI_MODE_AIMED_1:
	case YUMEMI_MODE_AIMED_2:
		yumemi_pattern_aimed_random();
		break;

	case YUMEMI_MODE_CROSS_0:
	case YUMEMI_MODE_CROSS_1:
	case YUMEMI_MODE_CROSS_2:
	case YUMEMI_MODE_CROSS_3:
		yumemi_pattern_cross_rings();
		break;

	case YUMEMI_MODE_CHASE_0:
	case YUMEMI_MODE_CHASE_1:
	case YUMEMI_MODE_CHASE_2:
		yumemi_pattern_chase();
		break;

	case YUMEMI_MODE_RAIN_0:
	case YUMEMI_MODE_RAIN_1:
	case YUMEMI_MODE_RAIN_2:
		yumemi_pattern_rain();
		break;

	case YUMEMI_MODE_DESCEND:
		boss_fall();
		break;

	case YUMEMI_MODE_EXPLODE:
		return;
	}

	if(boss_effect_radius != 0) {
		boss_effect_radius -= YUMEMI_EFFECT_RADIUS_DECAY;
	}
	if(boss_render_frame != 0) {
		// Original byte-field postfix is codegen-visible; prefix
		// changed actual original TC4 CODE (af897h).
		boss_render_frame--;
	}

	collmap_center.x.v = boss_center_x;
	collmap_center.y.v = boss_center_y;
	collmap_stripe_tile_w.set(YUMEMI_COLLISION_TILE_SIZE);
	collmap_tile_h.set(YUMEMI_COLLISION_TILE_SIZE);
	collmap_pid = pid_other;
	collmap_set_rect_striped();

	hitbox_hittest_skip_explosions = true;
	hitbox.radius.x.v = YUMEMI_COLLISION_HALF_RADIUS;
	hitbox.radius.y.v = YUMEMI_COLLISION_HALF_RADIUS;
	hitbox.pid = pid_other;
	hitbox.origin.center.x.v = boss_center_x;
	hitbox.origin.center.y.v = boss_center_y;
	boss_hit = hitbox_hittest();
	boss_hp -= boss_hit;
	hitbox_hittest_skip_explosions = false;
	boss_hittest_end();
}

void near yumemi_render_main(void)
{
	sprite16_offset_t sprite_offset;
	screen_x_t target_left;
	vram_y_t target_top;
	pid_t pid_other = (1 - pid_current);
	register screen_x_t left;
	register vram_y_t top;

	sprite16_put_size.set(YUMEMI_RENDER_MAIN_SIZE, YUMEMI_RENDER_MAIN_SIZE);
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - YUMEMI_RENDER_MAIN_LEFT_HALF);
	top = ((boss_center_y >> 4) - YUMEMI_RENDER_MAIN_TOP_OFFSET);
	sprite16_put(left, top, boss_sprite_offset);

	if(boss_render_mode != YUMEMI_RENDER_MODE_NONE) {
		sprite16_put_size.set(YUMEMI_RENDER_EFFECT_SIZE, YUMEMI_RENDER_EFFECT_SIZE);
		sprite_offset = (boss_sprite_offset + YUMEMI_RENDER_EFFECT_SPRITE_OFF);
		if(boss_render_mode == YUMEMI_RENDER_MODE_ALTERNATE) {
			sprite_offset += YUMEMI_RENDER_EFFECT_ALT_OFF;
		}
		sprite16_put((left + YUMEMI_RENDER_EFFECT_LEFT), top, sprite_offset);
	} else if(boss_hit) {
		sprite16_put_size.set(YUMEMI_RENDER_HIT_WIDTH, YUMEMI_RENDER_HIT_HEIGHT);
		left += YUMEMI_RENDER_HIT_LEFT;
		sprite16_put(left, top, (boss_sprite_offset + YUMEMI_RENDER_HIT_SPRITE_OFF));
	}

	// These are two independent original visual effect state values.
	// Explicit natural conjunction is TC4 byte-exact (af897e).
	if(!boss_effect_radius && !boss_render_frame) {
		return;
	}

	if(pid_current != 0) {
		grc_setclip(YUMEMI_CLIP_PLAYER0_LEFT, YUMEMI_CLIP_TOP, YUMEMI_CLIP_PLAYER0_RIGHT, YUMEMI_CLIP_BOTTOM);
	} else {
		grc_setclip(YUMEMI_CLIP_PLAYER1_LEFT, YUMEMI_CLIP_TOP, YUMEMI_CLIP_PLAYER1_RIGHT, YUMEMI_CLIP_BOTTOM);
	}

	egc_off();
	grcg_setcolor(GC_RMW, YUMEMI_RENDER_EFFECT_COLOR);

	left = playfield_fg_x_to_screen(yumemi_origin_x, pid_other);
	top = ((yumemi_origin_y >> YUMEMI_RENDER_EFFECT_ORIGIN_SHIFT) + YUMEMI_RENDER_EFFECT_ORIGIN_BIAS);

	if(boss_render_frame == 0) {
		grcg_circle(left, top, boss_effect_radius);
	} else {
		target_left = playfield_fg_x_to_screen(
			boss_aux_point.x.v, pid_other
		);
		target_top = ((boss_aux_point.y.v >> YUMEMI_RENDER_EFFECT_ORIGIN_SHIFT) + YUMEMI_RENDER_EFFECT_ORIGIN_BIAS);
		grcg_line(left, top, target_left, target_top);
	}

	grcg_off();
	egc_on();
	grc_setclip(0, 0, (RES_X - 1), (SPRITE16_RES_Y - 1));
}

// The original entrance position uses two separate scale stages.
// Natural (frame << 3) << 4 reproduces both original TC4 stages;
// combining them into one << 7 changed CODE in af780b, just as
// the earlier single frame*128 attempt changed CODE in af675c.
enum yumemi_arrival_gate_t {
    YUMEMI_ARRIVAL_PHASE1_END = 0x18,
    YUMEMI_ARRIVAL_PHASE2_END = 0x30,
    YUMEMI_ARRIVAL_PHASE3_END = 0x48,
    YUMEMI_ARRIVAL_PHASE4_END = 0x60,
    YUMEMI_ARRIVAL_POS_LOW_SHIFT = 3,
    YUMEMI_ARRIVAL_POS_HIGH_SHIFT = 4,
    YUMEMI_ARRIVAL_RASTER_STEP = 8,
};

// These four entrance raster phases intentionally use the same real
// 8-pixel signed-step traversal but different original clipping bounds.
// TC4 4.02 reuses the original instructions with typed while loops.
void near yumemi_render_arrival(void)
{
	screen_y_t top;
	pid_t pid_other = (1 - pid_current);
	unsigned char phase;
	register screen_x_t left;
	register screen_x_t right;

	// TC4 DX = 0 selects XOR DX,DX as 33 D2; original uses 31 D2.
	// Keep this explicit original register encoding.
	// This exact historical XOR DX,DX operand order is visible in
    // original CODE. Natural _DX^=_DX changed it (af780c).
    asm { xor dx, dx }
	_AH = SPRITE16_SET_OVERLAP;
	geninterrupt(SPRITE16);

	sprite16_put_size.set(YUMEMI_RENDER_MAIN_SIZE, YUMEMI_RENDER_MAIN_SIZE);
	top = ((boss_center_y >> 4) - YUMEMI_RENDER_MAIN_TOP_OFFSET);

	if(boss_frame < YUMEMI_ARRIVAL_PHASE1_END) {
		// Two original signed scaling stages MUST stay separate:
		// collapsing <<3 then <<4 into <<7 changed TC4 CODE (af897g).
		left = playfield_fg_x_to_screen(TO_SP(-104), pid_other);
		right = playfield_fg_x_to_screen(
			((boss_frame << YUMEMI_ARRIVAL_POS_LOW_SHIFT) << YUMEMI_ARRIVAL_POS_HIGH_SHIFT) - TO_SP(104),
			pid_other
		);
		while(left <= right) {
			sprite16_put(left, top, boss_sprite_offset);
			left += YUMEMI_ARRIVAL_RASTER_STEP;
		}
	} else if(boss_frame < YUMEMI_ARRIVAL_PHASE2_END) {
		phase = (boss_frame - YUMEMI_ARRIVAL_PHASE1_END);
		left = playfield_fg_x_to_screen(
			((phase << YUMEMI_ARRIVAL_POS_LOW_SHIFT) << YUMEMI_ARRIVAL_POS_HIGH_SHIFT) - TO_SP(104),
			pid_other
		);
		right = playfield_fg_x_to_screen(TO_SP(88), pid_other);
		while(left <= right) {
			sprite16_put(left, top, boss_sprite_offset);
			left += YUMEMI_ARRIVAL_RASTER_STEP;
		}
	} else if(boss_frame < YUMEMI_ARRIVAL_PHASE3_END) {
		phase = (boss_frame - YUMEMI_ARRIVAL_PHASE2_END);
		left = playfield_fg_x_to_screen(TO_SP(272), pid_other);
		right = playfield_fg_x_to_screen(
			TO_SP(272) - ((phase << YUMEMI_ARRIVAL_POS_LOW_SHIFT) << YUMEMI_ARRIVAL_POS_HIGH_SHIFT),
			pid_other
		);
		while(left >= right) {
			sprite16_put(left, top, boss_sprite_offset);
			left -= YUMEMI_ARRIVAL_RASTER_STEP;
		}
		left = playfield_fg_x_to_screen(TO_SP(88), pid_other);
		sprite16_put(left, top, boss_sprite_offset);
	} else if(boss_frame < YUMEMI_ARRIVAL_PHASE4_END) {
		phase = (boss_frame - YUMEMI_ARRIVAL_PHASE3_END);
		left = playfield_fg_x_to_screen(
			TO_SP(272) - ((phase << YUMEMI_ARRIVAL_POS_LOW_SHIFT) << YUMEMI_ARRIVAL_POS_HIGH_SHIFT),
			pid_other
		);
		right = playfield_fg_x_to_screen(TO_SP(88), pid_other);
		while(left >= right) {
			sprite16_put(left, top, boss_sprite_offset);
			left -= YUMEMI_ARRIVAL_RASTER_STEP;
		}
	}

	_DX = OVERLAP_CLEAR;
	_AH = SPRITE16_SET_OVERLAP;
	geninterrupt(SPRITE16);
}

void far gba_boss_render_yumemi(void)
{
	pid_t pid_other;

	if(pid_current != gba_boss_launched_by) {
		return;
	}
	pid_other = (1 - pid_current);
	sprite16_clip_set_for_pid(pid_other);

	if(boss_mode == YUMEMI_MODE_INTRO) {
		yumemi_render_arrival();
		return;
	}
	if(boss_mode != YUMEMI_MODE_EXPLODE) {
		yumemi_render_main();
		return;
	}
	boss_explosion_render();
}
