// Natural Turbo C++ reconstruction candidate for the complete Kotohime
// contribution inside TH03 MAIN_03_TEXT. Shared boss helpers and historical
// state remain external until full-link ownership is proved.
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

struct boss_character_template_kotohime_t {
	int center_x;
	int center_y;
	int scratch_x;
	int scratch_y;
	int velocity_x;
	int velocity_y;
	int hp;
	sprite16_offset_t sprite_offset;
	unsigned char hit;
	unsigned char mode;
	unsigned char angle;
	unsigned char pattern_i;
	unsigned char pattern_count;
	unsigned char render_mode;
	unsigned char render_frame;
	unsigned char move_phase;
	unsigned int effect_radius;
	unsigned char tail[6];
};

extern boss_character_template_kotohime_t boss_character_template[PLAYER_COUNT];

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

void far pascal boss_kotohime_template_init(int player_id)
{
	boss_character_template_kotohime_t near *p =
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
	p->effect_radius = 0;
	p->sprite_offset = 0x288;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->render_mode = 0;
}

void near pascal kotohime_ring_emit(int randomize_angle)
{
	int y;
	int x;
	unsigned char angle;
	register int i;

	bullet_template.type = BT_BULLET16_DEFAULT;
	for(i = 0; i < kotohime_orbit_count; i++) {
		if(randomize_angle != 0) {
			bullet_template.angle = randring_far_next16();
		}
		angle = (
			((i << 8) / kotohime_orbit_count) +
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

void near kotohime_pattern_random_ring(void)
{
	if(boss_frame == 1) {
		boss_render_mode = 1;
		boss_effect_radius = 0;
		boss_render_frame = 0;
	}

	boss_move_phase += 4;

	if(boss_effect_radius > 0x400) {
		boss_render_mode = 2;
		_AL = boss_move_phase;
		_AL += 2;
		boss_move_phase = _AL;
		boss_render_frame++;
		if(boss_render_frame > 0x40) {
			bullet_template.group = BG_16_RING;
			bullet_template.speed.v = kotohime_random_ring_speed;
			kotohime_ring_emit(1);
			snd_se_play(3);
			boss_render_mode = 0;
			boss_mode = 1;
			boss_frame = 0;
		}
	} else {
		boss_move_sine();
		boss_effect_radius += 0x20;
	}
}

void near kotohime_pattern_aimed_ring(void)
{
	if(boss_frame == 1) {
		boss_render_mode = 1;
		boss_effect_radius = 0;
		boss_render_frame = 0;
		boss_move_phase = 0;
	}

	_AL = boss_move_phase;
	_AL += (unsigned char)0xFE;
	boss_move_phase = _AL;

	if(boss_effect_radius > 0x400) {
		boss_render_mode = 2;
		boss_effect_radius += 8;
		_AL = boss_move_phase;
		_AL += 2;
		boss_move_phase = _AL;
		boss_render_frame++;
		if(boss_render_frame > 0x40) {
			bullet_template.group = BG_2_SPREAD_NARROW_AIMED;
			bullet_template.angle = 0;
			bullet_template.speed.v = kotohime_aimed_speed_fast;
			kotohime_ring_emit(0);

			bullet_template.group = BG_5_SPREAD_MEDIUM_AIMED;
			bullet_template.angle = 0;
			bullet_template.speed.v = kotohime_aimed_speed_slow;
			kotohime_ring_emit(0);

			snd_se_play(3);
			boss_render_mode = 0;
			boss_mode = 1;
			boss_frame = 0;
		}
	} else {
		boss_move_sine();
		boss_effect_radius += 0x20;
	}
}

void near kotohime_pattern_pellet_arc(void)
{
	boss_move_sine();

	if((boss_frame % kotohime_pellet_interval) == 1) {
		snd_se_play(3);
		bullet_template.type = BT_PELLET;
		bullet_template.angle = (unsigned char)boss_frame;
		bullet_template.speed.v = kotohime_pellet_speed;
		bullet_template.group = BG_RING;
		bullet_template.count = 4;

		bullet_template.center.x.v = (boss_center_x - TO_SP(48));
		bullet_template.center.y.v = boss_center_y;
		bullets_add();

		bullet_template.center.x.v = (boss_center_x - TO_SP(24));
		bullet_template.center.y.v = (boss_center_y + TO_SP(12));
		bullets_add();

		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = (boss_center_y + TO_SP(24));
		bullets_add();

		bullet_template.center.x.v = (boss_center_x + TO_SP(24));
		bullet_template.center.y.v = (boss_center_y + TO_SP(12));
		bullets_add();

		bullet_template.center.x.v = (boss_center_x + TO_SP(48));
		bullet_template.center.y.v = boss_center_y;
		bullets_add();
	}

	if(boss_frame >= 0x60) {
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near kotohime_pattern_radial_burst(void)
{
	int y;
	int x;
	unsigned char center_angle;
	register int bullet_i;
	register int center_i;

	if(boss_frame == 1) {
		boss_render_mode = 1;
		boss_effect_radius = 0;
		boss_render_frame = 0;
	}

	_AL = boss_move_phase;
	_AL += (unsigned char)0xFC;
	boss_move_phase = _AL;

	if(boss_effect_radius > 0x400) {
		boss_render_mode = 2;
	boss_effect_radius += 8;
	_AL = boss_move_phase;
	_AL += (unsigned char)0xFE;
	boss_move_phase = _AL;
	boss_render_frame++;
	if(boss_render_frame <= 0x40) {
		return;
	}

	bullet_template.group = BG_1;
	bullet_template.type = BT_BULLET16_DEFAULT;

	for(center_i = 0; center_i < kotohime_orbit_count; center_i++) {
		center_angle = (
			((center_i << 8) / kotohime_orbit_count) +
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

		for(bullet_i = 0; bullet_i < kotohime_burst_count; bullet_i++) {
			bullet_template.angle = (
				((bullet_i << 7) / kotohime_burst_count) +
				center_angle +
				0x40
			);
			bullet_template.speed.v = (
				((bullet_i * 0x30) / kotohime_burst_count) +
				0x10
			);
			bullets_add();
		}
	}

		snd_se_play(3);
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	} else {
		boss_move_sine();
		boss_effect_radius += 0x20;
	}
}

void far gba_boss_update_kotohime(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		kotohime_random_ring_speed = ((gba_boss_level / 2) + 0x10);
		kotohime_orbit_count = ((gba_boss_level / 3) + 6);
		kotohime_aimed_speed_slow = ((gba_boss_level / 2) + 0x10);
		kotohime_aimed_speed_fast = ((gba_boss_level / 2) + 0x20);
		kotohime_pellet_speed = ((gba_boss_level / 2) + 0x18);
		kotohime_pellet_interval = (0x20 - (gba_boss_level / 2));
		kotohime_burst_count = ((gba_boss_level / 2) + 8);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	boss_target_update();
	bullet_template.pid = pid_other;
	boss_frame++;

	switch(boss_mode) {
	case 0:
		if(boss_frame != 0x64) {
			return;
		}
		boss_frame = 0;
		boss_mode = 1;
		break;

	case 1:
		boss_pattern_next();
		break;

	case 2:
	case 3:
	case 4:
	case 5:
	case 6:
		kotohime_pattern_random_ring();
		break;

	case 7:
	case 8:
	case 9:
		kotohime_pattern_aimed_ring();
		break;

	case 0x0C:
	case 0x0D:
	case 0x0E:
		kotohime_pattern_pellet_arc();
		break;

	case 0x0A:
	case 0x0B:
	case 0x0F:
	case 0x10:
	case 0x11:
		kotohime_pattern_radial_burst();
		break;

	case 0x80:
		boss_fall();
		break;

	case 0xFF:
		return;
	}

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

void near pascal kotohime_render_ring(int count)
{
	screen_y_t top;
	sprite16_offset_t sprite_offset;
	int radius;
	unsigned char angle;
	register int i;
	register screen_x_t left;

	radius = boss_effect_radius;
	sprite_offset = (pid.so_attack + 0x502);
	if((boss_render_mode == 2) && ((boss_frame & 3) < 2)) {
		sprite_offset += 0xA00;
	}

	sprite16_put_size.w = (32 / 16);
	sprite16_put_size.h = 16;

	for(i = 0; i < count; i++) {
		angle = (((i << 8) / count) + boss_move_phase);
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
		_AX = top;
		asm { sar ax, 4 }
		top = _AX;
		sprite16_put(left, _AX, sprite_offset);
	}
}

void near kotohime_render_main(void)
{
	screen_x_t left;
	screen_y_t top;
	register sprite16_offset_t sprite_offset;

	sprite16_put_size.w = (128 / 16);
	sprite16_put_size.h = 48;

	left = (
		playfield_fg_x_to_screen(
			boss_center_x,
			(1 - pid_current)
		) - 64
	);
	top = ((boss_center_y >> 4) - 32);

	sprite_offset = boss_sprite_offset;
	if(boss_hit != 0) {
		sprite_offset += 0x10;
	}
	sprite16_put(left, top, sprite_offset);

	if(boss_render_mode != 0) {
		kotohime_render_ring(kotohime_orbit_count);
	}
}

void near pascal kotohime_render_intro(int radius)
{
	if((round_frame_mod2 != 0) && (boss_frame < 0x40)) {
		return;
	}

	sprite16_put_size.w = (32 / 16);
	sprite16_put_size.h = 16;
	boss_render_mode = 1;
	boss_move_phase += 2;
	boss_effect_radius = radius;
	kotohime_render_ring(8);
	boss_render_mode = 0;
}

void far gba_boss_render_kotohime(void)
{
	if(pid_current != gba_boss_launched_by) {
		return;
	}

	sprite16_clip_set_for_pid(1 - pid_current);

	if(boss_mode == 0) {
		kotohime_render_intro(
			TO_SP(0xC8 - (boss_frame * 2))
		);
		return;
	}
	if(boss_mode != 0xFF) {
		kotohime_render_main();
		return;
	}
	boss_explosion_render();
}
