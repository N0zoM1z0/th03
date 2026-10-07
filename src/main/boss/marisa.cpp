// Maintained natural Turbo C++ reconstruction of the complete Marisa
// contribution inside TH03 MAIN_03_TEXT. Object-level producer shape is
// verified; full-link exact promotion remains a separate gate. Shared boss
// helpers and historical state remain owned by the frozen carrier.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/marisa.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
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
extern unsigned int boss_frame;

extern unsigned char marisa_bullet_speed;
extern unsigned char marisa_cloud_count_low;
extern unsigned char marisa_cloud_speed;
extern unsigned char marisa_ring_speed;
extern unsigned char marisa_ring_count;
extern unsigned char marisa_cloud_count_high;
extern unsigned char marisa_bullet_angle;

extern unsigned int round_or_result_frame;

// Shared MAIN_03_TEXT owner. These declarations intentionally keep that owner
// external to this producer.
extern "C" {
unsigned char near boss_update_start(void);
void near boss_move_sine(void);
void near boss_fall(void);
void far boss_hittest_end(void);
void near boss_target_update(void);
void near boss_pattern_next(void);
void near boss_explosion_render(void);

// Marisa's Extra Attack producer remains in P_EXATT_TEXT.
void far pascal marisa_exatt_add(int x, int y, pid_t pid);
}

void far pascal boss_marisa_template_init(int player_id)
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
	p->sprite_offset = 0x280;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->byte_15 = 0;
}

void near marisa_pattern_spread(void)
{
	boss_render_mode = 1;
	if(boss_frame < 0x20) {
		return;
	}
	if(boss_frame == 0x20) {
		marisa_bullet_angle = 0;
	}
	if(boss_frame < 0x50) {
		if((boss_frame & 3) != 0) {
			return;
		}

		bullet_template.angle = marisa_bullet_angle;
		bullet_template.group = BG_2_SPREAD_HORIZONTALLY_SYMMETRIC;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.speed.v = marisa_bullet_speed;
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.pid = (1 - pid_current);
		bullets_add();

		bullet_template.speed.v = (marisa_bullet_speed / 2);
		bullets_add();

		marisa_bullet_angle += 7;
		return;
	}
	boss_render_mode = 0;
	boss_mode = 1;
	boss_frame = 0;
}

void near marisa_pattern_columns_wide(void)
{
	pid_t pid_other = (1 - pid_current);
	boss_render_mode = 1;

	if(boss_frame < 0x38) {
		return;
	}
	if(boss_frame == 0x40) {
		marisa_exatt_add(0x80, 0x1700, pid_other);
		marisa_exatt_add(0x1180, 0x1700, pid_other);
		return;
	}
	if(boss_frame == 0x50) {
		marisa_exatt_add(0x380, 0x1700, pid_other);
		marisa_exatt_add(0xE80, 0x1700, pid_other);
		return;
	}
	if(boss_frame == 0x60) {
		marisa_exatt_add(0x680, 0x1700, pid_other);
		marisa_exatt_add(0xB80, 0x1700, pid_other);
		return;
	}
	if(boss_frame == 0x70) {
		marisa_exatt_add(0x980, 0x1700, pid_other);
		marisa_exatt_add(0x880, 0x1700, pid_other);
		return;
	}
	if(boss_frame == 0x84) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near marisa_pattern_ring(void)
{
	boss_move_sine();

	if((boss_frame & 0x1F) == 0) {
		bullet_template.angle = randring_far_next16();
		bullet_template.group = BG_RING;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.pid = (1 - pid_current);

		if(gba_boss_level < 8) {
			bullet_template.count = marisa_cloud_count_low;
		} else {
			bullet_template.speed.v = marisa_ring_speed;
			bullet_template.count = marisa_ring_count;
			bullet_template.type = BT_BULLET16_DEFAULT;
			bullets_add();

			bullet_template.angle += (256 / marisa_ring_count);
			bullet_template.count = marisa_cloud_count_high;
		}
		bullet_template.speed.v = marisa_cloud_speed;
		bullet_template.type = BT_PELLET_CLOUD;
		bullets_add();
	}

	if(boss_frame >= 0x82) {
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near marisa_pattern_columns_narrow(void)
{
	pid_t pid_other = (1 - pid_current);
	boss_render_mode = 1;

	if(boss_frame < 0x38) {
		return;
	}
	if(boss_frame == 0x40) {
		marisa_exatt_add(0x200, 0x1700, pid_other);
		marisa_exatt_add(0x1000, 0x1700, pid_other);
		return;
	}
	if(boss_frame == 0x50) {
		marisa_exatt_add(0x500, 0x1700, pid_other);
		marisa_exatt_add(0xD00, 0x1700, pid_other);
		return;
	}
	if(boss_frame == 0x60) {
		marisa_exatt_add(0x800, 0x1700, pid_other);
		marisa_exatt_add(0xA00, 0x1700, pid_other);
		return;
	}
	if(boss_frame == 0x70) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	}
}

void far gba_boss_update_marisa(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		marisa_bullet_speed = ((gba_boss_level * 2) + 0x32);
		marisa_cloud_count_low = ((gba_boss_level * 2) + 0x18);
		marisa_cloud_speed = (gba_boss_level + 0x20);
		marisa_ring_speed = (gba_boss_level + 0x0A);
		marisa_ring_count = (gba_boss_level + 0x16);
		marisa_cloud_count_high = (gba_boss_level + 0x16);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
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
	case 5:
		marisa_pattern_spread();
		break;

	case 8:
	case 9:
	case 0x0A:
		marisa_pattern_columns_wide();
		break;

	case 0x0B:
	case 0x0C:
	case 0x0D:
	case 0x0E:
	case 0x0F:
	case 0x10:
		marisa_pattern_ring();
		break;

	case 6:
	case 7:
	case 0x11:
		marisa_pattern_columns_narrow();
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

void near marisa_render_main(void)
{
	sprite16_offset_t sprite_offset;
	pid_t pid_other;
	register screen_x_t left;
	register screen_y_t top;

	pid_other = (1 - pid_current);
	sprite16_put_size.set(176, 96);
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - 88);
	top = ((boss_center_y >> 4) - 32);
	sprite16_put(left, top, boss_sprite_offset);

	if(boss_hit != 0) {
		sprite16_put_size.set(48, 80);
		left += 64;
		top += 16;
		sprite16_put(left, top, (boss_sprite_offset + 0x16));
		return;
	}
	if(boss_render_mode != 1) {
		return;
	}
	if((round_or_result_frame & 3) < 2) {
		sprite16_put_size.set(48, 80);
		left += 64;
		top += 16;
		sprite16_put(left, top, (boss_sprite_offset + 0x1C));
		left -= 32;
		top += 32;
		sprite_offset = (boss_sprite_offset + 0xF00);
	} else {
		left += 32;
		top += 48;
		sprite_offset = (boss_sprite_offset + 0x1180);
	}
	sprite16_put_size.set(112, 16);
	sprite16_put(left, top, sprite_offset);
}

void near pascal marisa_render_split(int offset)
{
	screen_y_t top;
	pid_t pid_other;
	register int offset_reg = offset;
	register screen_x_t left;

	pid_other = (1 - pid_current);
	sprite16_put_size.set(176, 96);
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - 88);
	top = ((boss_center_y >> 4) - 32);

	_AH = SPRITE16_SET_MASK;
	_DX = 0xAAAA;
	geninterrupt(SPRITE16);
	sprite16_put((left - offset_reg), top, boss_sprite_offset);

	_AH = SPRITE16_SET_MASK;
	_DX = 0x5555;
	geninterrupt(SPRITE16);
	sprite16_put((left + offset_reg), top, boss_sprite_offset);

	_AH = SPRITE16_SET_MASK;
	_DX = 0xFFFF;
	geninterrupt(SPRITE16);
}

void far gba_boss_render_marisa(void)
{
	pid_t pid_other;

	if(pid_current != gba_boss_launched_by) {
		return;
	}
	pid_other = (1 - pid_current);
	sprite16_clip_set_for_pid(pid_other);

	if(boss_mode == 0) {
		marisa_render_split(0xC8 - (boss_frame * 2));
		return;
	}
	if(boss_mode != 0xFF) {
		marisa_render_main();
		return;
	}
	boss_explosion_render();
}
