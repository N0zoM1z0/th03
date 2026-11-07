// Natural Turbo C++ reconstruction candidate for the complete Rikako
// contribution inside TH03 MAIN_03_TEXT. Shared boss helpers and historical
// state remain external until full-link ownership is proved.
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
};

void far pascal boss_rikako_template_init(int player_id)
{
	boss_template_state_t near *p =
		&boss_character_template[player_id];

	p->center_x = 0x900;
	p->center_y = 0x500;
	p->velocity_x = -0x20;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = 0;
	p->hp = 0x6E;
	p->pattern_i = 0;
	p->spin_delta = 4;
	p->effect_radius = 0;
	p->sprite_offset = 0x286;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->render_mode = 0;
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
	register int i;

	if(boss_spin_delta <= 8) {
		if((boss_frame % RIKAKO_SPIN_TICK_PERIOD) == 0) {
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
			? 0x30
			: (signed char)-0x30
		);

		for(i = 0; i < rikako_orbit_count; ++i) {
			angle = ((i * 256) / rikako_orbit_count);
			bullet_template.center.x.v = polar(
				boss_center_x,
				TO_SP(48),
				CosTable8[angle]
			);
			bullet_template.center.y.v = polar(
				boss_center_y,
				TO_SP(48),
				SinTable8[angle]
			);
			bullet_template.angle = (angle + angle_delta);
			bullets_add();
		}
		snd_se_play(5);
		return;
	}

	if(boss_frame > RIKAKO_ORBIT_FINISH_AFTER) {
		boss_frame = 0;
		boss_mode = 1;
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

	if(boss_spin_delta >= -8) {
		if((boss_frame % RIKAKO_SPIN_TICK_PERIOD) == 0) {
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
		for(i = 0; i < rikako_entity_count; ++i) {
			angle = ((i * 256) / rikako_entity_count);
			rikako_extra_add(
				boss_center_x,
				boss_center_y,
				angle
			);
		}
		snd_se_play(5);
		return;
	}

	if(boss_frame == RIKAKO_ENTITIES_PELLET_FRAME) {
		bullet_template.type = BT_PELLET;
		bullet_template.group = BG_RING;
		bullet_template.count = rikako_pellet_count;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.speed.v = TO_SP(2);

		for(i = 0; i < 4; ++i) {
			bullet_template.angle = randring_far_next16();
			bullet_template.speed.v += 8;
			bullets_add();
		}
		snd_se_play(10);
		return;
	}

	if(boss_frame > RIKAKO_ENTITIES_FINISH_AFTER) {
		boss_frame = 0;
		boss_mode = 1;
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

	if(boss_spin_delta != 2) {
		if((boss_frame % RIKAKO_SPIN_TICK_PERIOD) == 0) {
			boss_spin_delta += ((boss_spin_delta > 2) ? -1 : 1);
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
		snd_se_play(10);
		bullets_add();

		bullet_template.angle = (rikako_random_angle + 0x80);
		bullets_add();
	}

	if(boss_frame >= RIKAKO_BURST_FINISH_FRAME) {
		boss_mode = 1;
		boss_frame = 0;
	}
}

void far gba_boss_update_rikako(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		rikako_orbit_count = ((gba_boss_level / 2) + 0x10);
		rikako_entity_count = ((gba_boss_level / 4) + 8);
		rikako_pellet_count = ((gba_boss_level / 2) + 0x1C);
		rikako_burst_interval = (0x20 - gba_boss_level);
		rikako_burst_speed = (gba_boss_level + 0x40);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	bullet_template.pid = pid_other;
	boss_target_update();
	boss_frame++;

	switch(boss_mode) {
	case RIKAKO_MODE_INTRO:
		if(boss_frame != RIKAKO_INTRO_FINISH_FRAME) {
			return;
		}
		boss_frame = 0;
		boss_mode = 1;
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

	boss_render_frame += boss_spin_delta;

	collmap_center.x.v = boss_center_x;
	collmap_center.y.v = boss_center_y;
	collmap_stripe_tile_w.set(64);
	collmap_tile_h.set(48);
	collmap_pid = pid_other;
	collmap_set_rect_striped();

	hitbox_hittest_skip_explosions = true;
	hitbox.radius.x.v = TO_SP(32);
	hitbox.radius.y.v = TO_SP(32);
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
	unsigned char angle;
	register sprite16_offset_t sprite_offset;
	register int i;

	sprite16_put_size.w = 96;
	sprite16_put_size.h = 48;

	left = (
		playfield_fg_x_to_screen(
			boss_center_x,
			(1 - pid_current)
		) - 48
	);
	top = ((boss_center_y >> 4) - 32);

	sprite_offset = boss_sprite_offset;
	if(boss_hit) {
		sprite_offset += 0x0C;
	}
	sprite16_put(left, top, sprite_offset);

	sprite16_put_size.w = 16;
	sprite16_put_size.h = 8;
	angle = boss_render_frame;
	left += 40;
	top += 40;

	for(i = 0; i < RIKAKO_MAIN_SPRITE_COUNT; (++i, angle += 0x20)) {
		x = polar(left, 48, CosTable8[angle]);
		y = polar(top, 48, SinTable8[angle]);

		if(i & 3) {
			sprite_offset = (((i & 3) * 2) + 0x167E);
		} else {
			sprite_offset = 0x284;
		}

		sprite16_put(
			x,
			y,
			(pid.so_attack + sprite_offset)
		);
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
	unsigned char angle;
	register int i;
	register screen_x_t left;

	radius = (0xC80 - ((boss_frame * 2) * 16));

	sprite16_put_size.w = 48;
	sprite16_put_size.h = 24;

	if((boss_frame < RIKAKO_INTRO_FLICKER_END) && (round_or_result_frame & 1)) {
		return;
	}

	sprite_offset = (pid.so_attack + 0x780);
	if((boss_frame % 2) != 0) {
		sprite_offset += 0x780;
	}

	angle = ((unsigned char)boss_frame * 4);
	angle = (0 - angle);

	for(i = 0; i < RIKAKO_INTRO_SPRITE_COUNT; (++i, angle += 0x10)) {
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
			playfield_fg_x_to_screen(
				left,
				(1 - pid_current)
			) - 24
		);
		// The original signed AX shift and ADD AX,-8 both arise naturally
		// from this local assignment; passing it as an inline argument
		// instead changes TC4 CODE (af763c).
		top = static_cast<screen_y_t>((top >> 4) - 8);
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
