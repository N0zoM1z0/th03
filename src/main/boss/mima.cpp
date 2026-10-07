// Natural Turbo C++ reconstruction candidate for the complete Mima
// contribution inside TH03 MAIN_03_TEXT. The shared boss helper prefix is
// maintained separately; historical boss and Mima-private state stays in the
// frozen carrier until full-link ownership is proved.
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

struct boss_character_template_t {
	int center_x;
	int center_y;
	int unused_04;
	int unused_06;
	int velocity_x;
	int velocity_y;
	int hp;
	sprite16_offset_t sprite_offset;
	unsigned char byte_10;
	unsigned char byte_11;
	unsigned char byte_12;
	unsigned char byte_13;
	unsigned char byte_14;
	unsigned char byte_15;
	unsigned char tail[10];
};

extern boss_character_template_t boss_character_template[PLAYER_COUNT];

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

void far pascal boss_mima_template_init(int player_id)
{
	boss_character_template_t near *p = &boss_character_template[player_id];

	p->center_x = 0x900;
	p->center_y = 0x500;
	p->velocity_x = -0x20;
	p->velocity_y = 0;
	p->byte_12 = 0;
	p->byte_10 = 0;
	p->byte_11 = 0;
	p->hp = 0x6E;
	p->byte_13 = 0;
	p->sprite_offset = 0x28C;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->byte_15 = 0;
}

void near mima_pattern_spread(void)
{
	if(boss_frame < 2) {
		boss_render_mode = 2;
		boss_render_frame = 0;
		mima_spread_angle = 0;
		mima_pellet_angle = 0xC0;
		return;
	}

	if(boss_frame < 0x20) {
		return;
	}

	if((boss_frame & 1) == 0) {
		snd_se_play(3);

		bullet_template.angle = mima_spread_angle;
		bullet_template.group = BG_2_SPREAD_HORIZONTALLY_SYMMETRIC;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.speed.v = mima_bullet_speed;
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.is_animated = false;
		bullets_add();
		bullet_template.is_animated = true;
		mima_spread_angle += 9;

		if(
			(mima_pellet_until > boss_frame) &&
			((boss_frame % 6) == 0)
		) {
			bullet_template.type = BT_PELLET;
			bullet_template.group = BG_4_SPREAD_MEDIUM;
			bullet_template.speed.v = mima_pellet_speed;
			bullet_template.angle = mima_pellet_angle;
			bullets_add();

			bullet_template.angle = (0x80 - mima_pellet_angle);
			bullets_add();
		}
		mima_pellet_angle += 3;
	}

	if(boss_frame > 0x82) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near mima_pattern_bomb_random(void)
{
	pid_t pid_other = (1 - pid_current);
	register int x;
	register int y;

	if(boss_frame == 0x10) {
		boss_render_mode = 5;
	} else if(boss_frame < 0x20) {
		return;
	}

	x = (boss_center_x + TO_SP(24));
	y = (boss_center_y - TO_SP(32));

	if(
		(boss_frame == 0x20) ||
		(boss_frame == 0x24) ||
		(boss_frame == 0x28)
	) {
		bomb_center_add(x, y, pid_other);
		return;
	}

	if(boss_frame <= 0x30) {
		return;
	}

	if((boss_frame & 3) == 0) {
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

	if(boss_frame == 0x40) {
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

	if((boss_frame & 1) == 0) {
		snd_se_play(3);
	}

	if(boss_frame >= 0x80) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near mima_pattern_trail(void)
{
	unsigned char remainder = (boss_frame % mima_trail_interval);

	boss_move_sine();
	boss_render_mode = 5;

	if(
		(remainder == 1) ||
		(remainder == (mima_trail_interval / 2))
	) {
		if(remainder == (mima_trail_interval / 2)) {
			bullet_template.group = BG_4_SPREAD_MEDIUM_AIMED;
		} else {
			bullet_template.group = BG_5_SPREAD_MEDIUM_AIMED;
		}

		snd_se_play(10);
		bullet_template.angle = 0;
		bullet_template.center.x.v = (boss_center_x + TO_SP(24));
		bullet_template.center.y.v = (boss_center_y - TO_SP(32));
		bullet_template.speed.v = (TO_SP(5) + 8);
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.is_animated = false;
		bullet_template.has_trail = true;
		bullets_add();
		bullet_template.has_trail = false;
		bullet_template.is_animated = true;
	}

	if(boss_frame >= 0x96) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near mima_pattern_orbit(void)
{
	boss_move_sine();

	if(boss_frame == 1) {
		if(randring_far_next16_and(1)) {
			_AL = 7;
		} else {
			_AL = -7;
		}
		mima_orbit_delta = _AL;
		mima_orbit_angle = randring_far_next16();
	}

	if((boss_frame & 1) == 0) {
		bullet_template.center.x.v = polar(
			boss_center_x, TO_SP(48), CosTable8[mima_orbit_angle]
		);
		bullet_template.center.y.v = polar(
			boss_center_y, TO_SP(48), SinTable8[mima_orbit_angle]
		);
		bullet_template.angle = (mima_orbit_angle + 0x40);
		bullet_template.type = BT_PELLET_CLOUD;
		bullet_template.group = BG_2_RING;
		bullet_template.speed.v = mima_orbit_speed;
		bullets_add();
		snd_se_play(10);

		mima_orbit_angle += mima_orbit_delta;
	}

	if(boss_frame >= 0x48) {
		boss_mode = 1;
		boss_frame = 0;
	}
}

void far gba_boss_update_mima(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		mima_bullet_speed = (gba_boss_level + 0x20);
		mima_random_count = ((gba_boss_level / 4) + 2);
		mima_random_speed = (gba_boss_level + 0x20);
		mima_trail_interval = (0x40 - (gba_boss_level * 2));
		mima_pellet_speed = (gba_boss_level + 0x28);
		mima_pellet_until = ((gba_boss_level * 4) + 0x40);
		mima_orbit_speed = (gba_boss_level + 0x36);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	boss_target_update();
	// The target deliberately recomputes this after the shared helper call
	// instead of reusing [pid_other].
	_AL = 1;
	_AL -= pid_current;
	bullet_template.pid = _AL;
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
		mima_pattern_spread();
		break;

	case 6:
	case 7:
	case 8:
	case 9:
	case 0x0A:
		mima_pattern_bomb_random();
		break;

	case 0x0B:
	case 0x0C:
	case 0x0D:
		mima_pattern_trail();
		break;

	case 0x0E:
	case 0x0F:
	case 0x10:
	case 0x11:
		mima_pattern_orbit();
		break;

	case 0x80:
		boss_fall();
		break;

	case 0xFF:
		return;
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

void near mima_render_main(void)
{
	sprite16_offset_t sprite_offset;
	pid_t pid_other = (1 - pid_current);
	register screen_x_t left;
	register screen_y_t top;

	sprite16_put_size.set(144, 112);
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - 72);
	top = ((boss_center_y >> 4) - 40);
	sprite16_put(left, top, boss_sprite_offset);

	if(boss_hit != 0) {
		sprite16_put_size.set(64, 80);
		left += 32;
		top += 16;
		sprite16_put(left, top, (boss_sprite_offset + 0x12));
		return;
	}

	if(boss_render_mode == 2) {
render_mode_2:
		sprite16_put_size.set(16, 16);
		sprite_offset = (boss_sprite_offset + 0x1A);
		sprite16_put((left + 48), (top + 32), sprite_offset);

		sprite16_put_size.set(32, 32);
		left += 80;
		sprite_offset = (boss_sprite_offset + 0xEF4);
		if(boss_render_frame >= 0x10) {
			sprite_offset += 4;
			if(boss_render_frame >= 0x20) {
				boss_render_mode = 3;
			}
		}
		sprite16_put(left, top, sprite_offset);
		boss_render_frame++;
		return;
	}

	if(boss_render_mode == 3) {
		sprite16_put_size.set(80, 48);
		sprite16_put(
			(left + 32),
			(top + 16),
			(boss_sprite_offset + 0xC92)
		);
		return;
	}

	if(boss_render_mode == 4) {
		sprite16_put_size.set(16, 16);
		sprite_offset = (boss_sprite_offset + 0x1A);
		sprite16_put((left + 48), (top + 32), sprite_offset);
		return;
	}

	if(boss_render_mode == 5) {
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
	register screen_x_t left;

	_SI = distance;
	pid_other = (1 - pid_current);
	sprite16_put_size.set(144, 112);
	base_left = (
		playfield_fg_x_to_screen(boss_center_x, pid_other) - 72
	);
	base_top = ((boss_center_y >> 4) - 40);

	_AH = SPRITE16_SET_MASK;
	_DX = 0xAAAA;
	geninterrupt(SPRITE16);
	left = polar(base_left, _SI, CosTable8[angle]);
	top = polar(base_top, _SI, SinTable8[angle]);
	sprite16_put(left, top, boss_sprite_offset);

	_AH = SPRITE16_SET_MASK;
	_DX = 0x5555;
	geninterrupt(SPRITE16);
	angle += 0x80;
	left = polar(base_left, _SI, CosTable8[angle]);
	top = polar(base_top, _SI, SinTable8[angle]);
	sprite16_put(left, top, boss_sprite_offset);

	_AH = SPRITE16_SET_MASK;
	_DX = 0xFFFF;
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

	if(boss_mode == 0) {
		mima_render_split(
			(0xC8 - (boss_frame * 2)),
			(boss_frame * 3)
		);
		return;
	}
	if(boss_mode != 0xFF) {
		mima_render_main();
		return;
	}
	boss_explosion_render();
}
