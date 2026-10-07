// Natural Turbo C++ reconstruction candidate for the complete Yumemi
// contribution inside TH03 MAIN_03_TEXT. Shared boss helpers and all historical
// state remain external until full-link ownership is proved.
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

struct boss_character_template_yumemi_t {
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

extern boss_character_template_yumemi_t boss_character_template[PLAYER_COUNT];

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

void far pascal boss_yumemi_template_init(int player_id)
{
	boss_character_template_yumemi_t near *p =
		&boss_character_template[player_id];

	p->center_x = 0x900;
	p->center_y = 0x500;
	p->velocity_x = -0x20;
	p->velocity_y = 0;
	p->pattern_count = 0;
	p->hit = 0;
	p->mode = 0;
	p->hp = 0x82;
	p->pattern_i = 0;
	p->render_frame = 0;
	p->move_phase = 0;
	p->effect_radius = 0;
	p->sprite_offset = 0x288;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->render_mode = 0;
}

void near yumemi_pattern_ring(void)
{
	if(boss_frame == 1) {
		boss_render_mode = 1;
		yumemi_angle = randring_far_next16();
		yumemi_speed_add = 0;
		boss_effect_radius = 0x100;
		if(randring_far_next16_and(1) == 0) {
			_AL = 3;
		} else {
			_AL = -3;
		}
		yumemi_angle_delta = _AL;
	}

	if(boss_frame < 4) {
		bomb_axis_add(
			yumemi_origin_x,
			yumemi_origin_y,
			bullet_template.pid
		);
		return;
	}

	if(boss_frame < 0x20) {
		return;
	}

	if(boss_frame == 0x20) {
		bomb_explosion_add(
			yumemi_origin_x,
			yumemi_origin_y,
			bullet_template.pid
		);
		boss_render_mode = 2;
		snd_se_play(5);
	}

	if((boss_frame & 3) == 0) {
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.angle = yumemi_angle;
		bullet_template.group = BG_RING;
		bullet_template.center.x.v = yumemi_origin_x;
		bullet_template.center.y.v = yumemi_origin_y;
		bullet_template.speed.v = (yumemi_ring_speed + yumemi_speed_add);
		bullet_template.count = yumemi_ring_count;
		bullets_add();

		yumemi_angle += yumemi_angle_delta;
		yumemi_speed_add += 8;
	}

	if(boss_frame > 0x3C) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near yumemi_pattern_aimed_random(void)
{
	if(boss_frame == 1) {
		boss_render_mode = 1;
		boss_aux_point.x = players[bullet_template.pid].center.x;
		boss_aux_point.y = players[bullet_template.pid].center.y;
		yumemi_angle = iatan2(
			(boss_aux_point.y.v - yumemi_origin_y),
			(boss_aux_point.x.v - yumemi_origin_x)
		);
		boss_effect_radius = 0x100;
		boss_render_frame = 0x20;
	}

	if(boss_frame < 0x10) {
		if((boss_frame & 3) == 1) {
			bomb_axis_add(
				boss_aux_point.x.v,
				boss_aux_point.y.v,
				bullet_template.pid
			);
		}
		return;
	}

	if(boss_frame < 0x20) {
		return;
	}

	if(boss_frame == 0x20) {
		bomb_explosion_add(
			yumemi_origin_x,
			yumemi_origin_y,
			bullet_template.pid
		);
		boss_render_mode = 2;
	}

	if((boss_frame & 1) == 0) {
		snd_se_play(3);
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

	if(boss_frame > 0x60) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near yumemi_pattern_cross_rings(void)
{
	boss_move_sine();

	if((boss_frame % yumemi_cross_interval) == 0) {
		bullet_template.group = BG_4_RING;
		bullet_template.speed.v = TO_SP(2);
		bullet_template.type = (randring_far_next16_and(1) + 1);

		bullet_template.angle = randring_far_next16();
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = (boss_center_y - TO_SP(32));
		bullets_add();

		bullet_template.angle = randring_far_next16();
		bullet_template.center.y.v = (boss_center_y + TO_SP(32));
		bullets_add();

		bullet_template.angle = randring_far_next16();
		bullet_template.center.x.v = (boss_center_x - TO_SP(32));
		bullet_template.center.y.v = boss_center_y;
		bullets_add();

		bullet_template.angle = randring_far_next16();
		bullet_template.center.x.v = (boss_center_x + TO_SP(32));
		bullets_add();
	}

	if(boss_frame >= 0x60) {
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near yumemi_pattern_chase(void)
{
	if(boss_move_phase == 0) {
		if(
			(boss_center_x > 0x380) &&
			(boss_center_x < 0xE80)
		) {
			boss_move_sine();
			return;
		}
		boss_move_phase = 1;
		boss_frame = 0;
		return;
	}

	boss_render_frame = 2;
	boss_aux_point.x = players[bullet_template.pid].center.x;
	boss_aux_point.y = players[bullet_template.pid].center.y;

	if(boss_frame < 0x20) {
		return;
	}

	boss_move_sine();
	boss_move_sine();

	if((boss_frame & 0x0F) == 0x0F) {
		boss_render_mode = 1;
		bomb_axis_add(
			boss_aux_point.x.v,
			boss_aux_point.y.v,
			bullet_template.pid
		);
		yumemi_extra_add(boss_aux_point.x.v, boss_aux_point.y.v);
		return;
	}

	if(boss_frame > yumemi_chase_until) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
		boss_move_phase = 0;
	}
}

void near yumemi_pattern_rain(void)
{
	register int i;

	boss_move_sine();

	if((boss_frame % yumemi_rain_interval) == 0) {
		bullet_template.type = BT_BULLET16_DEFAULT;

		if(boss_frame < 0x40) {
			bullet_template.center.x.v = yumemi_origin_x;
			bullet_template.center.y.v = yumemi_origin_y;
			bullet_template.angle = -0x40;
			bullet_template.speed.v = TO_SP(6);
			bullet_template.group = BG_5_SPREAD_WIDE;
			bullets_add();
			bullet_template.group = BG_4_SPREAD_WIDE;
			bullets_add();
		}

		if(boss_frame >= 0x20) {
			bullet_template.group = BG_1;
			bullet_template.speed.v = (TO_SP(2) + 4);
			bullet_template.center.y.v = 0;
			for(i = 0; i < 12; i++) {
				bullet_template.center.x.v =
					randring_far_next16_mod(TO_SP(PLAYFIELD_W));
				bullet_template.angle = (
					randring_far_next16_and(0x3F) + 0x20
				);
				bullets_add();
			}
		}
	}

	if(boss_frame >= 0x60) {
		boss_mode = 1;
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

	yumemi_origin_x = (boss_center_x + 0x90);
	yumemi_origin_y = (boss_center_y - 0x180);

	switch(boss_mode) {
	case 0:
		if((boss_frame == 0x18) || (boss_frame == 0x48)) {
			snd_se_reset();
			snd_se_play(5);
		}
		if(boss_frame != 0x60) {
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
		yumemi_pattern_ring();
		break;

	case 7:
	case 8:
	case 9:
		yumemi_pattern_aimed_random();
		break;

	case 0x0B:
	case 0x0C:
	case 0x0D:
	case 0x0E:
		yumemi_pattern_cross_rings();
		break;

	case 0x0F:
	case 0x10:
	case 0x11:
		yumemi_pattern_chase();
		break;

	case 5:
	case 6:
	case 0x0A:
		yumemi_pattern_rain();
		break;

	case 0x80:
		boss_fall();
		break;

	case 0xFF:
		return;
	}

	if(boss_effect_radius != 0) {
		boss_effect_radius -= 8;
	}
	if(boss_render_frame != 0) {
		boss_render_frame--;
	}

	collmap_center.x.v = boss_center_x;
	collmap_center.y.v = boss_center_y;
	collmap_stripe_tile_w.set(56);
	collmap_tile_h.set(56);
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

void near yumemi_render_main(void)
{
	sprite16_offset_t sprite_offset;
	screen_x_t target_left;
	vram_y_t target_top;
	pid_t pid_other = (1 - pid_current);
	register screen_x_t left;
	register vram_y_t top;

	sprite16_put_size.set(112, 112);
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - 56);
	top = ((boss_center_y >> 4) - 40);
	sprite16_put(left, top, boss_sprite_offset);

	if(boss_render_mode != 0) {
		sprite16_put_size.set(64, 64);
		sprite_offset = (boss_sprite_offset + 0x0E);
		if(boss_render_mode == 2) {
			sprite_offset += 0xA00;
		}
		sprite16_put((left + 32), top, sprite_offset);
	} else if(boss_hit != 0) {
		sprite16_put_size.set(80, 96);
		left += 16;
		sprite16_put(left, top, (boss_sprite_offset + 0x16));
	}

	if((boss_effect_radius == 0) && (boss_render_frame == 0)) {
		return;
	}

	if(pid_current != 0) {
		grc_setclip(16, 8, 0x12F, 0xBF);
	} else {
		grc_setclip(0x150, 8, 0x26F, 0xBF);
	}

	egc_off();
	grcg_setcolor(GC_RMW, 10);

	left = playfield_fg_x_to_screen(yumemi_origin_x, pid_other);
	top = ((yumemi_origin_y >> 5) + 8);

	if(boss_render_frame == 0) {
		grcg_circle(left, top, boss_effect_radius);
	} else {
		target_left = playfield_fg_x_to_screen(
			boss_aux_point.x.v, pid_other
		);
		target_top = ((boss_aux_point.y.v >> 5) + 8);
		grcg_line(left, top, target_left, target_top);
	}

	grcg_off();
	egc_on();
	grc_setclip(0, 0, (RES_X - 1), (SPRITE16_RES_Y - 1));
}

void near yumemi_render_arrival(void)
{
	unsigned char phase;
	pid_t pid_other = (1 - pid_current);
	screen_y_t top;
	register screen_x_t left;
	register screen_x_t right;

	_DX = 0;
	_AH = SPRITE16_SET_OVERLAP;
	geninterrupt(SPRITE16);

	sprite16_put_size.set(112, 112);
	top = ((boss_center_y >> 4) - 40);

	if(boss_frame < 0x18) {
		left = playfield_fg_x_to_screen(TO_SP(-104), pid_other);
		right = playfield_fg_x_to_screen(
			((boss_frame << 3) << 4) - TO_SP(104),
			pid_other
		);
		for(; left <= right; left += 8) {
			sprite16_put(left, top, boss_sprite_offset);
		}
	} else if(boss_frame < 0x30) {
		phase = (boss_frame - 0x18);
		left = playfield_fg_x_to_screen(
			((phase << 3) << 4) - TO_SP(104),
			pid_other
		);
		right = playfield_fg_x_to_screen(TO_SP(88), pid_other);
		for(; left <= right; left += 8) {
			sprite16_put(left, top, boss_sprite_offset);
		}
	} else if(boss_frame < 0x48) {
		phase = (boss_frame - 0x30);
		left = playfield_fg_x_to_screen(TO_SP(272), pid_other);
		right = playfield_fg_x_to_screen(
			TO_SP(272) - ((phase << 3) << 4),
			pid_other
		);
		for(; left >= right; left -= 8) {
			sprite16_put(left, top, boss_sprite_offset);
		}
		left = playfield_fg_x_to_screen(TO_SP(88), pid_other);
		sprite16_put(left, top, boss_sprite_offset);
	} else if(boss_frame < 0x60) {
		phase = (boss_frame - 0x48);
		left = playfield_fg_x_to_screen(
			TO_SP(272) - ((phase << 3) << 4),
			pid_other
		);
		right = playfield_fg_x_to_screen(TO_SP(88), pid_other);
		for(; left >= right; left -= 8) {
			sprite16_put(left, top, boss_sprite_offset);
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

	if(boss_mode == 0) {
		yumemi_render_arrival();
		return;
	}
	if(boss_mode != 0xFF) {
		yumemi_render_main();
		return;
	}
	boss_explosion_render();
}
