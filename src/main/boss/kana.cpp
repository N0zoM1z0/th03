// Complete current source-native C++ reconstruction of the original Kana
// major BOSS. Historical shared BOSS helpers and state remain in their
// separate original objects; the normal complete MAIN link is exact.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/kana.hpp"
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
extern unsigned int boss_frame;

extern unsigned char kana_accel_count;
extern unsigned char kana_ring_count_slow;
extern unsigned char kana_ring_count_mid;
extern unsigned char kana_ring_count_fast;
extern unsigned char kana_cloud_interval;
extern unsigned char kana_cloud_count;
extern unsigned char kana_rotating_speed;

extern unsigned char kana_rotating_angle;
extern signed char kana_rotating_delta;

extern int SinTable8[256];
extern int CosTable8[256];

extern "C" {
void far pascal bomb_center_add(int x, int y, int pid);
void far pascal bomb_explosion_add(int x, int y, int pid);
void far pascal kana_extra_add(int x, int y, unsigned char angle);
}

enum kana_template_layout_t {
    KANA_TEMPLATE_CENTER_X = 0x900,
    KANA_TEMPLATE_CENTER_Y = 0x500,
    KANA_TEMPLATE_VELOCITY_X = -0x20,
    KANA_TEMPLATE_HP = 0x64,
    KANA_TEMPLATE_SPRITE_OFF = 0x288,
    KANA_TEMPLATE_PLAYER2_OFF = 0x28,
};

enum kana_render_mode_t {
    KANA_RENDER_MODE_NORMAL = 0,
    KANA_RENDER_MODE_EXPANDING = 1,
    KANA_RENDER_MODE_WARNING = 2,
};

enum kana_level_scaling_t {
    KANA_LEVEL_HALF = 2,
    KANA_LEVEL_ACCEL_BASE = 0x10,
    KANA_LEVEL_RING_SLOW_BASE = 0x18,
    KANA_LEVEL_RING_MID_BASE = 0x10,
    KANA_LEVEL_RING_FAST_BASE = 0x14,
    KANA_LEVEL_CLOUD_INTERVAL_BASE = 0x20,
    KANA_LEVEL_CLOUD_COUNT_BASE = 0x18,
    KANA_LEVEL_ROTATING_SPEED_BASE = 0x40,
};

enum kana_sound_effect_t {
    KANA_SOUND_ATTACK = 10,
};

// Original scheduler IDs, grouped by Kana's four distinct whole attack
// controllers; the shared 2..17 selection distribution is unchanged.
enum kana_boss_mode_t {
    KANA_MODE_INTRO = 0x00,
    KANA_MODE_SELECT = 0x01,
    KANA_MODE_ACCEL_0 = 0x02,
    KANA_MODE_ACCEL_1 = 0x03,
    KANA_MODE_ACCEL_2 = 0x04,
    KANA_MODE_ROTATING_0 = 0x05,
    KANA_MODE_ROTATING_1 = 0x06,
    KANA_MODE_STAGED_0 = 0x07,
    KANA_MODE_STAGED_1 = 0x08,
    KANA_MODE_STAGED_2 = 0x09,
    KANA_MODE_STAGED_3 = 0x0A,
    KANA_MODE_STAGED_4 = 0x0B,
    KANA_MODE_STAGED_5 = 0x0C,
    KANA_MODE_CLOUD_0 = 0x0D,
    KANA_MODE_CLOUD_1 = 0x0E,
    KANA_MODE_CLOUD_2 = 0x0F,
    KANA_MODE_ROTATING_2 = 0x10,
    KANA_MODE_ROTATING_3 = 0x11,
    KANA_MODE_DESCEND = 0x80,
    KANA_MODE_EXPLODE = 0xFF,
};

// Timing gates shared by Kana's whole BOSS dispatcher and both sprite
// renderers. The mutable 8-bit phase/rotation counters stay byte-accurate.
enum kana_boss_render_timing_t {
    KANA_INTRO_COMPLETE_FRAME = 0x64,
    KANA_INTRO_BLINK_END = 0x20,
    KANA_INTRO_SPRITE_COUNT = 0x10,
    KANA_INTRO_SPRITE_ANGLE_STEP = 0x10,
    KANA_STAGED_PELLET_ANGLE_STEP = 6,
    KANA_STAGED_PELLET_SPEED_STEP = 3,
    KANA_MIDDLE_PELLET_COUNT = 0x10,
    KANA_ROTATING_RING_PERIOD = 4,
    KANA_RENDER_ANIMATION_PERIOD = 4,
    KANA_RENDER_ANIMATION_SHIFT = 2,
    KANA_RENDER_WARNING_STEP_1 = 8,
    KANA_RENDER_WARNING_STEP_2 = 0x10,
    KANA_RENDER_WARNING_STEP_3 = 0x18,
    KANA_ACCEL_ORBIT_ANGLE_0 = 0xE0,
    KANA_ACCEL_ORBIT_ANGLE_1 = 0x08,
    KANA_ACCEL_ORBIT_ANGLE_2 = 0x78,
    KANA_ACCEL_ORBIT_ANGLE_3 = 0xA0,
    KANA_ROTATING_RING_BULLETS = 5,
    KANA_INTRO_RADIUS_ORIGINAL_SUBPIXEL = 0xC80,
    KANA_COLLISION_STRIPE_WIDTH = 64,
    KANA_COLLISION_TILE_HEIGHT = 48,
    KANA_COLLISION_HALF_RADIUS = TO_SP(32),
    KANA_RENDER_MAIN_WIDTH = 128,
    KANA_RENDER_MAIN_HEIGHT = 40,
    KANA_RENDER_WARNING_WIDTH = 64,
    KANA_RENDER_WARNING_HEIGHT = 32,
    KANA_RENDER_INTRO_WIDTH = 32,
    KANA_RENDER_INTRO_HEIGHT = 16,
    KANA_RENDER_MAIN_LEFT = 64,
    KANA_RENDER_MAIN_TOP = 24,
    KANA_RENDER_HIT_OFF = 0x10,
    KANA_RENDER_WARN_LEFT = 32,
    KANA_RENDER_WARN_SPRITE = 0xC80,
    KANA_RENDER_WARN_FRAME_2 = 8,
    KANA_RENDER_WARN_FRAME_3 = 0x10,
    KANA_RENDER_WARN_FRAME_4 = 0x18,
    KANA_RENDER_INTRO_SPRITE = 0x284,
    KANA_RENDER_INTRO_FRAME_WIDTH = 32,
    KANA_RENDER_INTRO_FRAME_HEIGHT = 0x28,
    KANA_RENDER_INTRO_HALF = 16,
};

void far pascal boss_kana_template_init(int player_id)
{
	boss_template_state_t near *p =
		&boss_character_template[player_id];

	p->center_x = KANA_TEMPLATE_CENTER_X;
	p->center_y = KANA_TEMPLATE_CENTER_Y;
	p->velocity_x = KANA_TEMPLATE_VELOCITY_X;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = KANA_MODE_INTRO;
	p->hp = KANA_TEMPLATE_HP;
	p->pattern_i = 0;
	p->effect_radius = 0;
	p->sprite_offset = KANA_TEMPLATE_SPRITE_OFF;
	if(player_id) {
		p->sprite_offset += KANA_TEMPLATE_PLAYER2_OFF;
	}
	p->render_mode = KANA_RENDER_MODE_NORMAL;
}

// Original clock phases for this full Kana attack; no new state.
enum kana_accel_phase_t {
    KANA_ACCEL_START = 1,
    KANA_ACCEL_WARN = 0x10,
    KANA_ACCEL_RELEASE = 0x28,
    KANA_ACCEL_FINISH_AFTER = 0x50,
};

void near kana_pattern_accel_ring(void)
{
	if(boss_frame == KANA_ACCEL_START) {
		boss_render_mode = KANA_RENDER_MODE_EXPANDING;
		return;
	}
	if(boss_frame == KANA_ACCEL_WARN) {
		boss_render_frame = 0;
		boss_render_mode = KANA_RENDER_MODE_WARNING;
		bomb_center_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);
		return;
	}
	if(boss_frame == KANA_ACCEL_RELEASE) {
		bomb_explosion_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);
		kana_extra_add(boss_center_x, boss_center_y, KANA_ACCEL_ORBIT_ANGLE_0);
		kana_extra_add(boss_center_x, boss_center_y, KANA_ACCEL_ORBIT_ANGLE_1);
		kana_extra_add(boss_center_x, boss_center_y, KANA_ACCEL_ORBIT_ANGLE_2);
		kana_extra_add(boss_center_x, boss_center_y, KANA_ACCEL_ORBIT_ANGLE_3);

		bullet_template.type = BT_BULLET16_DEFAULT_WITH_ACCEL;
		bullet_template.group = BG_RING;
		bullet_template.count = kana_accel_count;
		bullet_template.accel_type = BAT_Y;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.speed.v = TO_SP(3);
		bullets_add();
		snd_se_play(KANA_SOUND_ATTACK);
		return;
	}
	if(boss_frame > KANA_ACCEL_FINISH_AFTER) {
		boss_render_mode = KANA_RENDER_MODE_NORMAL;
		boss_frame = 0;
		boss_mode = KANA_MODE_SELECT;
	}
}

// Original clock phases for this full Kana attack; no new state.
enum kana_staged_phase_t {
    KANA_STAGED_START = 1,
    KANA_STAGED_WARN = 0x10,
    KANA_STAGED_SLOW = 0x28,
    KANA_STAGED_MIDDLE = 0x40,
    KANA_STAGED_FAST = 0x48,
    KANA_STAGED_EMISSION_END = 0x50,
    KANA_STAGED_FINISH_AFTER = 0x60,
};

void near kana_pattern_staged_ring(void)
{
	pid_t pid_other = (1 - pid_current);

	if(boss_frame == KANA_STAGED_START) {
		boss_render_mode = KANA_RENDER_MODE_EXPANDING;
		return;
	}
	if(boss_frame == KANA_STAGED_WARN) {
		boss_render_frame = 0;
		boss_render_mode = KANA_RENDER_MODE_WARNING;
		bomb_center_add(boss_center_x, boss_center_y, pid_other);
		return;
	}

	// The ring template is only active between the initial slow release
	// and the end of its staggered volley window.
	if(
		(boss_frame >= KANA_STAGED_SLOW) &&
		(boss_frame < KANA_STAGED_EMISSION_END)
	) {
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.group = BG_RING;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;

		if(boss_frame == KANA_STAGED_SLOW) {
			bomb_explosion_add(
				boss_center_x,
				boss_center_y,
				pid_other
			);
			bullet_template.speed.v = TO_SP(1);
			bullet_template.count = kana_ring_count_slow;
			bullets_add();
			snd_se_play(KANA_SOUND_ATTACK);
			return;
		}

		if(boss_frame == KANA_STAGED_MIDDLE) {
			bomb_explosion_add(
				boss_center_x,
				boss_center_y,
				pid_other
			);
			bullet_template.speed.v = (TO_SP(2) + 8);
			bullet_template.count = kana_ring_count_mid;
			bullets_add();
			snd_se_play(KANA_SOUND_ATTACK);

			bullet_template.type = BT_PELLET;
			bullet_template.angle = 0x20;
			bullet_template.speed.v = TO_SP(1);
			bullet_template.group =
				BG_2_SPREAD_HORIZONTALLY_SYMMETRIC;
			// The pre-tested 16-projectile volley preserves bullets_add,
			// byte angle +6, and speed +3 before the signed-index advance.
			register int i = 0;
			while(i < KANA_MIDDLE_PELLET_COUNT) {
				bullets_add();
				bullet_template.angle += KANA_STAGED_PELLET_ANGLE_STEP;
				bullet_template.speed.v += KANA_STAGED_PELLET_SPEED_STEP;
				++i;
			}
			return;
		}

		if(boss_frame == KANA_STAGED_FAST) {
			bomb_explosion_add(
				boss_center_x,
				boss_center_y,
				pid_other
			);
			bullet_template.speed.v = (TO_SP(3) + 8);
			bullet_template.count = kana_ring_count_fast;
			bullets_add();
			snd_se_play(KANA_SOUND_ATTACK);
			return;
		}
		return;
	}

	if(boss_frame <= KANA_STAGED_FINISH_AFTER) {
		return;
	}
	boss_render_mode = KANA_RENDER_MODE_NORMAL;
	boss_frame = 0;
	boss_mode = KANA_MODE_SELECT;
}

// Original clock phases for this full Kana attack; no new state.
enum kana_cloud_phase_t {
    KANA_CLOUD_FINISH_AFTER = 0x64,
};

// The random cloud's single parity draw remains exactly once per
// emission tick. A natural truthiness condition compiles identical x86.
void near kana_pattern_cloud_ring(void)
{
	signed char angle;

	boss_move_sine();

	// The variable unsigned-word cloud interval compares its remainder
	// with zero; the original RNG order is unchanged.
	if((boss_frame % kana_cloud_interval) == 0) {
		_AL = randring_far_next16_and(0x1F);
		// Genuine TC4 keeps the original SUB AL,10; direct C++ subtraction
		// changes the full source CODE (fresh failed af836c).
		asm { sub al, 10h }
		angle = _AL;
		if(randring_far_next16_and(1)) {
			angle = (0x80 - angle);
		}
		kana_extra_add(
			boss_center_x,
			boss_center_y,
			(unsigned char)angle
		);

		bullet_template.type = BT_PELLET_CLOUD;
		bullet_template.group = BG_RING;
		bullet_template.count = kana_cloud_count;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.speed.v = TO_SP(3);
		bullets_add();
		snd_se_play(KANA_SOUND_ATTACK);
	}

	if(boss_frame > KANA_CLOUD_FINISH_AFTER) {
		boss_render_mode = KANA_RENDER_MODE_NORMAL;
		boss_frame = 0;
		boss_mode = KANA_MODE_SELECT;
	}
}

// Original clock phases for this full Kana attack; no new state.
enum kana_rotating_phase_t {
    KANA_ROTATING_START = 1,
    KANA_ROTATING_WARN = 0x10,
    KANA_ROTATING_VOLLEY_START = 0x20,
    KANA_ROTATING_TURN_AFTER = 0x40,
    KANA_ROTATING_VOLLEY_END = 0x6C,
    KANA_ROTATING_FINISH_AFTER = 0x70,
};

void near kana_pattern_rotating_ring(void)
{
	if(boss_frame == KANA_ROTATING_START) {
		boss_render_mode = KANA_RENDER_MODE_EXPANDING;
		return;
	}
	if(boss_frame == KANA_ROTATING_WARN) {
		boss_render_frame = 0;
		boss_render_mode = KANA_RENDER_MODE_WARNING;
		bomb_center_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);
		kana_rotating_angle = (unsigned char)-0x40;
		kana_rotating_delta = randring_far_next16_and(3);
		// These four signed angular choices must keep the AL-mediated
		// write: direct byte assignments changed original TC4 CODE
		// (native negative control af704a).
		if(kana_rotating_delta == 0) {
			_AL = (unsigned char)-3;
		} else if(kana_rotating_delta == 1) {
			_AL = (unsigned char)-1;
		} else if(kana_rotating_delta == 2) {
			_AL = 1;
		} else {
			_AL = 3;
		}
		kana_rotating_delta = _AL;
		return;
	}

	// The rotating-ring fire window has its own four-frame shot cadence;
	// angle steering continues independently after the turn frame.
	if(
		(boss_frame >= KANA_ROTATING_VOLLEY_START) &&
		(boss_frame < KANA_ROTATING_VOLLEY_END)
	) {
		// Distinct four-frame unsigned-word remainder clock, not byte angle.
		if((boss_frame % KANA_ROTATING_RING_PERIOD) == 0) {
			bullet_template.type = BT_BULLET16_DEFAULT;
			bullet_template.group = BG_RING;
			bullet_template.count = KANA_ROTATING_RING_BULLETS;
			bullet_template.center.x.v = boss_center_x;
			bullet_template.center.y.v = boss_center_y;
			bullet_template.speed.v = kana_rotating_speed;
			bullet_template.angle = kana_rotating_angle;
			bullets_add();
			snd_se_play(KANA_SOUND_ATTACK);
		}
		if(boss_frame > KANA_ROTATING_TURN_AFTER) {
			// The explicit byte assignment angle=angle+signed_delta
			// changed original CODE (af884i). Keep compound update.
			kana_rotating_angle += kana_rotating_delta;
		}
		return;
	}

	if(boss_frame <= KANA_ROTATING_FINISH_AFTER) {
		return;
	}
	boss_render_mode = KANA_RENDER_MODE_NORMAL;
	boss_frame = 0;
	boss_mode = KANA_MODE_SELECT;
}

void far gba_boss_update_kana(void)
{
	if(boss_update_start()) {
		kana_accel_count = ((gba_boss_level / KANA_LEVEL_HALF) + KANA_LEVEL_ACCEL_BASE);
		kana_ring_count_slow = ((gba_boss_level / KANA_LEVEL_HALF) + KANA_LEVEL_RING_SLOW_BASE);
		kana_ring_count_mid = ((gba_boss_level / KANA_LEVEL_HALF) + KANA_LEVEL_RING_MID_BASE);
		kana_ring_count_fast = ((gba_boss_level / KANA_LEVEL_HALF) + KANA_LEVEL_RING_FAST_BASE);
		kana_cloud_interval = (KANA_LEVEL_CLOUD_INTERVAL_BASE - gba_boss_level);
		kana_cloud_count = ((gba_boss_level / KANA_LEVEL_HALF) + KANA_LEVEL_CLOUD_COUNT_BASE);
		kana_rotating_speed = (gba_boss_level + KANA_LEVEL_ROTATING_SPEED_BASE);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_t pid_other = (1 - pid_current);
	bullet_template.pid = pid_other;
	boss_target_update();
	++boss_frame;

	switch(boss_mode) {
	case KANA_MODE_INTRO:
		if(boss_frame != KANA_INTRO_COMPLETE_FRAME) {
			return;
		}
		boss_frame = 0;
		boss_mode = KANA_MODE_SELECT;
		break;

	case KANA_MODE_SELECT:
		boss_pattern_next();
		break;

	case KANA_MODE_ACCEL_0:
	case KANA_MODE_ACCEL_1:
	case KANA_MODE_ACCEL_2:
		kana_pattern_accel_ring();
		break;

	case KANA_MODE_STAGED_0:
	case KANA_MODE_STAGED_1:
	case KANA_MODE_STAGED_2:
	case KANA_MODE_STAGED_3:
	case KANA_MODE_STAGED_4:
	case KANA_MODE_STAGED_5:
		kana_pattern_staged_ring();
		break;

	case KANA_MODE_CLOUD_0:
	case KANA_MODE_CLOUD_1:
	case KANA_MODE_CLOUD_2:
		kana_pattern_cloud_ring();
		break;

	case KANA_MODE_ROTATING_0:
	case KANA_MODE_ROTATING_1:
	case KANA_MODE_ROTATING_2:
	case KANA_MODE_ROTATING_3:
		kana_pattern_rotating_ring();
		break;

	case KANA_MODE_DESCEND:
		boss_fall();
		break;

	case KANA_MODE_EXPLODE:
		return;
	}

	boss_render_frame++;

	collmap_center.x.v = boss_center_x;
	collmap_center.y.v = boss_center_y;
	collmap_stripe_tile_w.set(KANA_COLLISION_STRIPE_WIDTH);
	collmap_tile_h.set(KANA_COLLISION_TILE_HEIGHT);
	collmap_pid = pid_other;
	collmap_set_rect_striped();

	hitbox_hittest_skip_explosions = true;
	hitbox.radius.x.v = KANA_COLLISION_HALF_RADIUS;
	hitbox.radius.y.v = KANA_COLLISION_HALF_RADIUS;
	hitbox.pid = pid_other;
	hitbox.origin.center.x.v = boss_center_x;
	hitbox.origin.center.y.v = boss_center_y;
	boss_hit = hitbox_hittest();
	boss_hp -= boss_hit;
	hitbox_hittest_skip_explosions = false;
	boss_hittest_end();

}

void near kana_render_main(void)
{
	screen_y_t top;
	register sprite16_offset_t sprite_offset;
	register screen_x_t left;

	sprite16_put_size.w = KANA_RENDER_MAIN_WIDTH;
	sprite16_put_size.h = KANA_RENDER_MAIN_HEIGHT;

	left = (
		playfield_fg_x_to_screen(
			boss_center_x,
			(1 - pid_current)
		) - KANA_RENDER_MAIN_LEFT
	);
	top = ((boss_center_y >> 4) - KANA_RENDER_MAIN_TOP);

	sprite_offset = boss_sprite_offset;
	if(boss_hit) {
		sprite_offset += KANA_RENDER_HIT_OFF;
	}
	sprite16_put(left, top, sprite_offset);

	sprite16_put_size.w = KANA_RENDER_WARNING_WIDTH;
	sprite16_put_size.h = KANA_RENDER_WARNING_HEIGHT;
	left += KANA_RENDER_WARN_LEFT;

	if(boss_render_mode == KANA_RENDER_MODE_EXPANDING) {
		sprite16_put(
			left,
			top,
			(boss_sprite_offset + KANA_RENDER_WARN_SPRITE)
		);
		return;
	}
	if(boss_render_mode != KANA_RENDER_MODE_WARNING) {
		return;
	}

	sprite_offset = (boss_sprite_offset + 0xC80);
	if(boss_render_frame >= KANA_RENDER_WARNING_STEP_1) {
		if(boss_render_frame < KANA_RENDER_WARNING_STEP_2) {
			sprite_offset += KANA_RENDER_WARN_FRAME_2;
		} else if(boss_render_frame < KANA_RENDER_WARNING_STEP_3) {
			sprite_offset += KANA_RENDER_WARN_FRAME_3;
		} else {
			sprite_offset += KANA_RENDER_WARN_FRAME_4;
		}
	}
	sprite16_put(left, top, sprite_offset);
}

// Original TC4 emits native matching shifts from the two-stage
// natural multiplications below. Collapsing the animation scale
// to one *1280 changes its machine instructions (af674e).
void near kana_render_intro(void)
{
	screen_y_t top;
	sprite16_offset_t sprite_offset;

	int radius = (KANA_INTRO_RADIUS_ORIGINAL_SUBPIXEL - ((boss_frame * 2) * 16));

	sprite16_put_size.w = KANA_RENDER_INTRO_WIDTH;
	sprite16_put_size.h = KANA_RENDER_INTRO_HEIGHT;

	if((boss_frame < KANA_INTRO_BLINK_END) && round_frame_mod2) {
		return;
	}

	sprite_offset = (pid.so_attack + KANA_RENDER_INTRO_SPRITE);
	sprite_offset = (
		sprite_offset +
		((((boss_frame >> KANA_RENDER_ANIMATION_SHIFT) & (KANA_RENDER_ANIMATION_PERIOD - 1)) * KANA_RENDER_INTRO_FRAME_WIDTH) * KANA_RENDER_INTRO_FRAME_HEIGHT)
	);

	unsigned char angle = boss_move_phase;
	// Binary zero-minus is not the same original TC4 CODE as unary
	// minus (genuine failed trial af884e).
	angle = (0 - angle);

	// Sixteen arrival sprites use a pre-tested signed-index loop. Each
	// polar draw precedes the signed-index and byte-angle advances.
	register int i = 0;
	while(i < KANA_INTRO_SPRITE_COUNT) {
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
			) - KANA_RENDER_INTRO_HALF
		);
		// Original signed AX conversion is native-exact as this C++
		// assignment; compound top >>=4 changed CODE (af761b).
		top = static_cast<screen_y_t>(top >> 4);
		sprite16_put(left, top, sprite_offset);
		++i;
		angle += KANA_INTRO_SPRITE_ANGLE_STEP;
	}
}

void far gba_boss_render_kana(void)
{
	if(pid_current != gba_boss_launched_by) {
		return;
	}

	sprite16_clip_set_for_pid(1 - pid_current);

	if(boss_mode == KANA_MODE_INTRO) {
		kana_render_intro();
		return;
	}
	if(boss_mode != KANA_MODE_EXPLODE) {
		kana_render_main();
		return;
	}
	boss_explosion_render();
}
