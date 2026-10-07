// Natural Turbo C++ reconstruction candidate for the complete Kana
// contribution inside TH03 MAIN_03_TEXT. Shared boss helpers and historical
// state remain external until full-link ownership is proved.
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

struct boss_character_template_kana_t {
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

extern boss_character_template_kana_t boss_character_template[PLAYER_COUNT];

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

void far pascal boss_kana_template_init(int player_id)
{
	boss_character_template_kana_t near *p =
		&boss_character_template[player_id];

	p->center_x = 0x900;
	p->center_y = 0x500;
	p->velocity_x = -0x20;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = 0;
	p->hp = 0x64;
	p->pattern_i = 0;
	p->effect_radius = 0;
	p->sprite_offset = 0x288;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->render_mode = 0;
}

void near kana_pattern_accel_ring(void)
{
	if(boss_frame == 1) {
		boss_render_mode = 1;
		return;
	}
	if(boss_frame == 0x10) {
		boss_render_frame = 0;
		boss_render_mode = 2;
		bomb_center_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);
		return;
	}
	if(boss_frame == 0x28) {
		bomb_explosion_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);
		kana_extra_add(boss_center_x, boss_center_y, 0xE0);
		kana_extra_add(boss_center_x, boss_center_y, 0x08);
		kana_extra_add(boss_center_x, boss_center_y, 0x78);
		kana_extra_add(boss_center_x, boss_center_y, 0xA0);

		bullet_template.type = BT_BULLET16_DEFAULT_WITH_ACCEL;
		bullet_template.group = BG_RING;
		bullet_template.count = kana_accel_count;
		bullet_template.accel_type = BAT_Y;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.speed.v = TO_SP(3);
		bullets_add();
		snd_se_play(10);
		return;
	}
	if(boss_frame > 0x50) {
		boss_render_mode = 0;
		boss_frame = 0;
		boss_mode = 1;
	}
}

void near kana_pattern_staged_ring(void)
{
	pid_t pid_other = (1 - pid_current);
	register int i;

	if(boss_frame == 1) {
		boss_render_mode = 1;
		return;
	}
	if(boss_frame == 0x10) {
		boss_render_frame = 0;
		boss_render_mode = 2;
		bomb_center_add(boss_center_x, boss_center_y, pid_other);
		return;
	}

	if((boss_frame >= 0x28) && (boss_frame < 0x50)) {
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.group = BG_RING;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;

		if(boss_frame == 0x28) {
			bomb_explosion_add(
				boss_center_x,
				boss_center_y,
				pid_other
			);
			bullet_template.speed.v = TO_SP(1);
			bullet_template.count = kana_ring_count_slow;
			bullets_add();
			snd_se_play(10);
			return;
		}

		if(boss_frame == 0x40) {
			bomb_explosion_add(
				boss_center_x,
				boss_center_y,
				pid_other
			);
			bullet_template.speed.v = (TO_SP(2) + 8);
			bullet_template.count = kana_ring_count_mid;
			bullets_add();
			snd_se_play(10);

			bullet_template.type = BT_PELLET;
			bullet_template.angle = 0x20;
			bullet_template.speed.v = TO_SP(1);
			bullet_template.group =
				BG_2_SPREAD_HORIZONTALLY_SYMMETRIC;
			for(i = 0; i < 0x10; i++) {
				bullets_add();
				_AL = bullet_template.angle;
				_AL += 6;
				bullet_template.angle = _AL;
				_AL = bullet_template.speed.v;
				_AL += 3;
				bullet_template.speed.v = _AL;
			}
			return;
		}

		if(boss_frame == 0x48) {
			bomb_explosion_add(
				boss_center_x,
				boss_center_y,
				pid_other
			);
			bullet_template.speed.v = (TO_SP(3) + 8);
			bullet_template.count = kana_ring_count_fast;
			bullets_add();
			snd_se_play(10);
			return;
		}
		return;
	}

	if(boss_frame > 0x60) {
		boss_render_mode = 0;
		boss_frame = 0;
		boss_mode = 1;
	}
}

void near kana_pattern_cloud_ring(void)
{
	signed char angle;

	boss_move_sine();

	if((boss_frame % kana_cloud_interval) == 0) {
		_AL = randring_far_next16_and(0x1F);
		asm { sub al, 10h }
		angle = _AL;
		if(randring_far_next16_and(1) != 0) {
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
		snd_se_play(10);
	}

	if(boss_frame > 0x64) {
		boss_render_mode = 0;
		boss_frame = 0;
		boss_mode = 1;
	}
}

void near kana_pattern_rotating_ring(void)
{
	if(boss_frame == 1) {
		boss_render_mode = 1;
		return;
	}
	if(boss_frame == 0x10) {
		boss_render_frame = 0;
		boss_render_mode = 2;
		bomb_center_add(
			boss_center_x,
			boss_center_y,
			(1 - pid_current)
		);
		kana_rotating_angle = (unsigned char)-0x40;
		kana_rotating_delta = randring_far_next16_and(3);
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

	if((boss_frame >= 0x20) && (boss_frame < 0x6C)) {
		if((boss_frame & 3) == 0) {
			bullet_template.type = BT_BULLET16_DEFAULT;
			bullet_template.group = BG_RING;
			bullet_template.count = 5;
			bullet_template.center.x.v = boss_center_x;
			bullet_template.center.y.v = boss_center_y;
			bullet_template.speed.v = kana_rotating_speed;
			bullet_template.angle = kana_rotating_angle;
			bullets_add();
			snd_se_play(10);
		}
		if(boss_frame > 0x40) {
			kana_rotating_angle += kana_rotating_delta;
			return;
		}
		return;
	}

	if(boss_frame > 0x70) {
		boss_render_mode = 0;
		boss_frame = 0;
		boss_mode = 1;
	}
}

void far gba_boss_update_kana(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		kana_accel_count = ((gba_boss_level / 2) + 0x10);
		kana_ring_count_slow = ((gba_boss_level / 2) + 0x18);
		kana_ring_count_mid = ((gba_boss_level / 2) + 0x10);
		kana_ring_count_fast = ((gba_boss_level / 2) + 0x14);
		kana_cloud_interval = (0x20 - gba_boss_level);
		kana_cloud_count = ((gba_boss_level / 2) + 0x18);
		kana_rotating_speed = (gba_boss_level + 0x40);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	bullet_template.pid = pid_other;
	boss_target_update();
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
		kana_pattern_accel_ring();
		break;

	case 7:
	case 8:
	case 9:
	case 0x0A:
	case 0x0B:
	case 0x0C:
		kana_pattern_staged_ring();
		break;

	case 0x0D:
	case 0x0E:
	case 0x0F:
		kana_pattern_cloud_ring();
		break;

	case 5:
	case 6:
	case 0x10:
	case 0x11:
		kana_pattern_rotating_ring();
		break;

	case 0x80:
		boss_fall();
		break;

	case 0xFF:
		return;
	}

	boss_render_frame++;

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

void near kana_render_main(void)
{
	screen_y_t top;
	register sprite16_offset_t sprite_offset;
	register screen_x_t left;

	sprite16_put_size.w = 128;
	sprite16_put_size.h = 40;

	left = (
		playfield_fg_x_to_screen(
			boss_center_x,
			(1 - pid_current)
		) - 64
	);
	top = ((boss_center_y >> 4) - 24);

	sprite_offset = boss_sprite_offset;
	if(boss_hit != 0) {
		sprite_offset += 0x10;
	}
	sprite16_put(left, top, sprite_offset);

	sprite16_put_size.w = 64;
	sprite16_put_size.h = 32;
	left += 32;

	if(boss_render_mode == 1) {
		sprite16_put(
			left,
			top,
			(boss_sprite_offset + 0xC80)
		);
		return;
	}
	if(boss_render_mode != 2) {
		return;
	}

	sprite_offset = (boss_sprite_offset + 0xC80);
	if(boss_render_frame < 8) {
		;
	} else if(boss_render_frame < 0x10) {
		sprite_offset += 8;
	} else if(boss_render_frame < 0x18) {
		sprite_offset += 0x10;
	} else {
		sprite_offset += 0x18;
	}
	sprite16_put(left, top, sprite_offset);
}

void near kana_render_intro(void)
{
	screen_y_t top;
	sprite16_offset_t sprite_offset;
	int radius;
	unsigned char angle;
	register int i;
	register screen_x_t left;

	radius = (0xC80 - ((boss_frame * 2) << 4));

	sprite16_put_size.w = 32;
	sprite16_put_size.h = 16;

	if((boss_frame < 0x20) && (round_frame_mod2 != 0)) {
		return;
	}

	sprite_offset = (pid.so_attack + 0x284);
	sprite_offset = (
		sprite_offset +
		((((boss_frame >> 2) & 3) << 5) * 0x28)
	);

	angle = boss_move_phase;
	angle = (0 - angle);

	for(i = 0; i < 0x10; (i++, angle += 0x10)) {
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
			) - 16
		);
		_AX = top;
		asm { sar ax, 4 }
		top = _AX;
		sprite16_put(left, _AX, sprite_offset);

	}
}

void far gba_boss_render_kana(void)
{
	if(pid_current != gba_boss_launched_by) {
		return;
	}

	sprite16_clip_set_for_pid(1 - pid_current);

	if(boss_mode == 0) {
		kana_render_intro();
		return;
	}
	if(boss_mode != 0xFF) {
		kana_render_main();
		return;
	}
	boss_explosion_render();
}
