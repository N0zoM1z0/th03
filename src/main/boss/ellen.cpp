// Natural Turbo C++ reconstruction candidate for the complete Ellen
// contribution inside TH03 MAIN_03_TEXT. Shared boss helpers and historical
// state remain external until full-link ownership is proved.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/ellen.hpp"
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
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/sprite16/sprite16.h"

#pragma option -a2

struct boss_character_template_ellen_t {
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
	unsigned char tail[8];
};

extern boss_character_template_ellen_t boss_character_template[PLAYER_COUNT];

extern int boss_center_x;
extern int boss_center_y;
extern int boss_hp;
extern sprite16_offset_t boss_sprite_offset;
extern unsigned char boss_hit;
extern unsigned char boss_mode;
extern unsigned char boss_render_mode;
extern unsigned char boss_render_frame;
extern unsigned int boss_frame;

// Ellen's four level-derived pattern parameters.
extern unsigned char ellen_bullet_speed;
extern unsigned char ellen_extra_count;
extern unsigned char ellen_pellet_speed;
extern unsigned char ellen_pellet_interval;

// Ellen-private pattern state in the historical player-state tail.
extern unsigned char ellen_spread_angle;
extern unsigned char ellen_pellet_angle;

// Two historical anonymous 9-word renderer tables immediately following
// FIVE_DIGIT_POWERS_OF_10 in DATA.
extern int ellen_render_y_offsets[9];
extern int ellen_render_heights[9];

extern int SinTable8[256];
extern int CosTable8[256];

extern "C" {
void far pascal bomb_center_add(int x, int y, int pid);
void far pascal ellen_extra_add(
	int x, int y, unsigned char angle, unsigned char mode
);
}

void far pascal boss_ellen_template_init(int player_id)
{
	boss_character_template_ellen_t near *p =
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
	p->render_frame = 0;
	p->move_phase = 0;
	p->sprite_offset = 0x780;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->render_mode = 0;
}

void near ellen_pattern_spread(void)
{
	pid_t pid_other = (1 - pid_current);
	register int i;

	if((boss_frame == 0x10) || (boss_frame == 0x14)) {
		bomb_center_add(boss_center_x, boss_center_y, pid_other);
		return;
	}
	if(boss_frame == 0x18) {
		bomb_center_add(boss_center_x, boss_center_y, pid_other);
		ellen_spread_angle = 0x40;
		return;
	}
	if(boss_frame < 0x1C) {
		return;
	}

	bullet_template.angle = ellen_spread_angle;
	bullet_template.group = BG_2_SPREAD_HORIZONTALLY_SYMMETRIC;
	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = boss_center_y;
	bullet_template.speed.v = ellen_bullet_speed;
	bullet_template.type = BT_BULLET16_DEFAULT;
	bullet_template.pid = pid_other;
	bullet_template.sprite_offset = (64 / BYTE_DOTS);
	if(pid_current != 0) {
		bullet_template.sprite_offset += (8 * ROW_SIZE);
	}

	if(boss_frame < 0x24) {
		if((boss_frame & 1) == 0) {
			goto fire_single;
		}
		goto done;
	}
	if(boss_frame == 0x24) {
		snd_se_play(3);
		for(i = 0; i < 8; i++) {
			bullets_add();
			ellen_spread_angle += 8;
			bullet_template.angle = ellen_spread_angle;
		}
		goto done;
	}
	if(boss_frame > 0x2C) {
		goto done;
	}
	if((boss_frame & 1) != 0) {
		goto done;
	}

fire_single:
	snd_se_play(3);
	bullets_add();
	ellen_spread_angle += 8;

done:
	if(boss_frame >= 0x2C) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near ellen_pattern_extra(void)
{
	pid_t pid_other = (1 - pid_current);
	unsigned char angle;
	register int i;

	boss_render_frame += 3;

	if(boss_frame < 0x20) {
		return;
	}
	if(
		(boss_frame == 0x20) ||
		(boss_frame == 0x24) ||
		(boss_frame == 0x28)
	) {
		bomb_center_add(boss_center_x, boss_center_y, pid_other);
		return;
	}

	if(boss_frame == 0x30) {
		for(
			i = 0, angle = randring_far_next16();
			i < ellen_extra_count;
			(i++, angle += (256 / ellen_extra_count))
		) {
			ellen_extra_add(
				boss_center_x,
				boss_center_y,
				angle,
				2
			);
		}
		return;
	}

	if(boss_frame == 0x60) {
		for(
			i = 0, angle = randring_far_next16();
			i < ellen_extra_count;
			(i++, angle += (256 / ellen_extra_count))
		) {
			ellen_extra_add(
				boss_center_x,
				boss_center_y,
				angle,
				0xFE
			);
		}
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near ellen_pattern_pellets(void)
{
	boss_move_sine();

	if((boss_frame % ellen_pellet_interval) == 1) {
		snd_se_play(10);
		bullet_template.group = BG_4_SPREAD_NARROW;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.angle = ellen_pellet_angle;
		bullet_template.speed.v = ellen_pellet_speed;
		bullet_template.type = BT_PELLET;
		bullet_template.pid = (1 - pid_current);
		bullets_add();

		bullet_template.angle = (ellen_pellet_angle + 0x80);
		bullets_add();

		bullet_template.speed.v = (ellen_pellet_speed / 2);
		bullets_add();

		bullet_template.angle = ellen_pellet_angle;
		bullets_add();

		ellen_pellet_angle += 0x10;
	}

	if(boss_frame >= 0x60) {
		boss_mode = 1;
		boss_frame = 0;
	}
}

void far gba_boss_update_ellen(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		ellen_bullet_speed = ((gba_boss_level * 2) + 0x32);
		ellen_extra_count = ((gba_boss_level / 10) + 4);
		ellen_pellet_speed = (gba_boss_level + 0x30);
		ellen_pellet_interval = (10 - (gba_boss_level / 3));
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	boss_target_update();
	boss_render_frame++;
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
		ellen_pattern_spread();
		break;

	case 6:
	case 7:
	case 8:
	case 9:
	case 0x0A:
		ellen_pattern_extra();
		break;

	case 0x0B:
	case 0x0C:
	case 0x0D:
	case 0x0E:
	case 0x0F:
	case 0x10:
	case 0x11:
		ellen_pattern_pellets();
		break;

	case 0x80:
		boss_fall();
		break;

	case 0xFF:
		return;
	}

	collmap_center.x.v = boss_center_x;
	collmap_center.y.v = boss_center_y;
	collmap_stripe_tile_w.set(40);
	collmap_tile_h.set(48);
	collmap_pid = pid_other;
	collmap_set_rect_striped();

	hitbox_hittest_skip_explosions = true;
	hitbox.radius.x.v = TO_SP(24);
	hitbox.radius.y.v = TO_SP(24);
	hitbox.pid = pid_other;
	hitbox.origin.center.x.v = boss_center_x;
	hitbox.origin.center.y.v = boss_center_y;
	boss_hit = hitbox_hittest();
	boss_hp -= boss_hit;
	hitbox_hittest_skip_explosions = false;
	boss_hittest_end();
}

void near pascal ellen_render_strip(int frame_i)
{
	screen_x_t left;
	screen_y_t top;
	sprite16_offset_t sprite_offset;
	register int i = frame_i;

	sprite_offset = (
		(ellen_render_y_offsets[i] * 0x28) +
		boss_sprite_offset +
		0xFB10
	);
	sprite16_put_size.w = 96;
	sprite16_put_size.h = (ellen_render_heights[i] / 2);

	left = (
		playfield_fg_x_to_screen(
			boss_center_x,
			(1 - pid_current)
		) - 48
	);
	top = (
		(boss_center_y >> 4) +
		ellen_render_y_offsets[i] -
		40
	);
	sprite16_put(left, top, sprite_offset);
}

void near ellen_render_main(void)
{
	screen_x_t left;
	screen_y_t top;
	pid_t pid_other = (1 - pid_current);
	register int i;
	register sprite16_offset_t sprite_offset;

	sprite16_put_size.set(64, 48);
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - 32);
	top = ((boss_center_y >> 4) - 32);

	sprite_offset = boss_sprite_offset;
	if(boss_hit != 0) {
		sprite_offset += 8;
	}
	sprite16_put(left, top, sprite_offset);

	i = ((boss_render_frame / 4) % 9);
	ellen_render_strip(i);
	i--;
	if(i < 0) {
		i = 8;
	}
	ellen_render_strip(i);
	i--;
	if(i < 0) {
		i = 8;
	}
	ellen_render_strip(i);
}

void near pascal ellen_render_intro(
	int length,
	unsigned char frame,
	unsigned char angle
)
{
	screen_y_t top;
	int pid_other;
	sprite16_offset_t sprite_offset;
	int j;
	register int i;
	register screen_x_t left;

	pid_other = (1 - pid_current);

	i = (frame % 9);
	ellen_render_strip(i);
	i--;
	if(i < 0) {
		i = 8;
	}
	ellen_render_strip(i);
	i--;
	if(i < 0) {
		i = 8;
	}
	ellen_render_strip(i);

	if((round_frame_mod2 != 0) && (boss_frame < 0x40)) {
		return;
	}

	sprite16_put_size.set(32, 16);
	sprite_offset = (pid.so_attack + 0x28C);

	for(i = 0; i < 4; i++) {
		for(j = 0; j < 8; (angle += 0x20, j++)) {
			left = polar(
				boss_center_x,
				length,
				CosTable8[angle]
			);
			top = polar(
				boss_center_y,
				length,
				SinTable8[angle]
			);
			left = (
				playfield_fg_x_to_screen(left, pid_other) - 16
			);
			_AX = top;
			asm { sar ax, 4 }
			top = _AX;
			sprite16_put(left, _AX, sprite_offset);
		}
		angle += 3;
		sprite_offset -= 4;
	}
}

void far gba_boss_render_ellen(void)
{
	pid_t pid_other;

	if(pid_current != gba_boss_launched_by) {
		return;
	}
	pid_other = (1 - pid_current);
	sprite16_clip_set_for_pid(pid_other);

	if(boss_mode == 0) {
		ellen_render_intro(
			TO_SP(0xC8 - (boss_frame * 2)),
			(unsigned char)boss_frame,
			(unsigned char)(boss_frame * 3)
		);
		return;
	}
	if(boss_mode != 0xFF) {
		ellen_render_main();
		return;
	}
	boss_explosion_render();
}
