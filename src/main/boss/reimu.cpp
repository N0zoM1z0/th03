// Natural Turbo C++ reconstruction candidate for the complete Reimu
// contribution inside TH03 MAIN_03_TEXT. Shared boss helpers and all historical
// state remain external until full-link ownership is proved.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/reimu.hpp"
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

#pragma option -a2

struct boss_character_template_reimu_t {
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
	unsigned char tail[10];
};

extern boss_character_template_reimu_t boss_character_template[PLAYER_COUNT];

extern int boss_center_x;
extern int boss_center_y;
extern PlayfieldPoint boss_aux_point;
extern int boss_hp;
extern sprite16_offset_t boss_sprite_offset;
extern unsigned char boss_hit;
extern unsigned char boss_mode;
extern unsigned char boss_render_mode;
extern unsigned int boss_frame;

// Reimu's six level-derived pattern parameters.
extern unsigned char reimu_cloud_interval;
extern unsigned char reimu_unused_param;
extern unsigned char reimu_bullet_speed;
extern unsigned char reimu_orbit_count;
extern unsigned char reimu_ring_speed;
extern unsigned char reimu_ring_count;

// Reimu-private state and point arrays in the historical player-state tail.
extern unsigned char reimu_direction;
extern unsigned char reimu_cloud_speed;
extern unsigned char reimu_orbit_angle;
extern int reimu_orbit_x[6];
extern int reimu_orbit_y[6];

extern int SinTable8[256];
extern int CosTable8[256];

extern "C" void far pascal reimu_extra_add(int x, int y, unsigned char angle);

void far pascal boss_reimu_template_init(int player_id)
{
	boss_character_template_reimu_t near *p =
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
	p->render_mode = 0;
	p->sprite_offset = 0x28C;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
}

void near reimu_pattern_orbit_cloud(void)
{
	unsigned char angle;

	if(boss_frame == 0) {
		boss_aux_point.x.v = boss_center_x;
		boss_aux_point.y.v = (boss_center_y + TO_SP(48));
		reimu_direction = randring_far_next16_and(1);
		reimu_cloud_speed = 0x10;
	}

	angle = ((unsigned char)boss_frame * 2);
	if(reimu_direction != 0) {
		angle = (0 - angle);
	}

	if((boss_frame % reimu_cloud_interval) == 0) {
		bullet_template.type = BT_PELLET_CLOUD;
		bullet_template.group = BG_1;
		bullet_template.pid = (1 - pid_current);
		bullet_template.angle = (angle * 2);
		bullet_template.speed.v = reimu_cloud_speed;
		bullet_template.center.x.v = polar(
			boss_center_x, TO_SP(32), CosTable8[angle]
		);
		bullet_template.center.y.v = polar(
			boss_center_y, TO_SP(32), SinTable8[angle]
		);
		bullets_add();

		bullet_template.angle = ((angle * 2) + 0x80);
		angle += 0x80;
		bullet_template.center.x.v = polar(
			boss_center_x, TO_SP(32), CosTable8[angle]
		);
		bullet_template.center.y.v = polar(
			boss_center_y, TO_SP(32), SinTable8[angle]
		);
		bullets_add();
	}

	if((boss_frame & 1) == 0) {
		reimu_cloud_speed++;
	}

	angle = ((unsigned char)boss_frame * 2);
	angle += -0x40;
	boss_center_y = polar(
		boss_aux_point.y.v, TO_SP(48), SinTable8[angle]
	);

	if(boss_frame >= 0x80) {
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near reimu_pattern_spreads(void)
{
	boss_move_sine();

	bullet_template.type = BT_BULLET16_DEFAULT;
	bullet_template.speed.v = reimu_bullet_speed;
	bullet_template.pid = (1 - pid_current);
	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = boss_center_y;

	if(boss_frame < 0x40) {
		if(round_frame_mod16 != 0) {
			return;
		}
		bullet_template.angle = 0x20;
		bullet_template.group = BG_3_SPREAD_NARROW;
		bullets_add();
		bullet_template.angle = 0x60;
		bullets_add();
		return;
	}

	if(boss_frame < 0x64) {
		if(round_frame_mod16 != 0) {
			return;
		}
		bullet_template.group = BG_5_SPREAD_MEDIUM;
		bullet_template.angle = 0x40;
		bullets_add();
		return;
	}

	boss_mode = 1;
	boss_frame = 0;
}

void near reimu_pattern_orbit_burst(void)
{
	unsigned char angle;
	register int i;

	boss_move_sine();

	if(boss_frame == 0) {
		boss_render_mode = 1;
		reimu_orbit_angle = randring_far_next16();
	}

	if(boss_frame < 0x18) {
		for(i = 0; i < reimu_orbit_count; i++) {
			angle = (((i << 8) / reimu_orbit_count) + reimu_orbit_angle);
			reimu_orbit_x[i] = polar(
				boss_center_x,
				((boss_frame << 4) * 2),
				CosTable8[angle]
			);
			reimu_orbit_y[i] = polar(
				boss_center_y,
				((boss_frame << 4) * 2),
				SinTable8[angle]
			);
		}
		reimu_orbit_angle += 8;
		return;
	}

	if(boss_frame < 0x50) {
		for(i = 0; i < reimu_orbit_count; i++) {
			angle = (((i << 8) / reimu_orbit_count) + reimu_orbit_angle);
			reimu_orbit_x[i] = polar(
				boss_center_x, TO_SP(48), CosTable8[angle]
			);
			reimu_orbit_y[i] = polar(
				boss_center_y, TO_SP(48), SinTable8[angle]
			);
		}
		reimu_orbit_angle += 8;

		if(round_frame_mod16 == 0) {
			bullet_template.type = BT_BULLET16_DEFAULT;
			bullet_template.speed.v = reimu_ring_speed;
			bullet_template.pid = (1 - pid_current);
			bullet_template.center.x.v = boss_center_x;
			bullet_template.center.y.v = boss_center_y;
			bullet_template.angle = randring_far_next16();
			bullet_template.group = BG_RING;
			bullet_template.count = reimu_ring_count;
			bullets_add();
		}
		return;
	}

	if(boss_frame == 0x50) {
		for(i = 0; i < reimu_orbit_count; i++) {
			angle = (((i << 8) / reimu_orbit_count) + reimu_orbit_angle);
			reimu_extra_add(reimu_orbit_x[i], reimu_orbit_y[i], angle);
		}
		boss_mode = 1;
		boss_frame = 0;
		boss_render_mode = 0;
	}
}

void near reimu_pattern_mirrored_spread(void)
{
	boss_move_sine();

	if(boss_frame < 0x80) {
		if((boss_frame & 0x0F) != 0) {
			return;
		}
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.speed.v = reimu_bullet_speed;
		bullet_template.pid = (1 - pid_current);
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.angle = (unsigned char)boss_frame;
		bullet_template.group = BG_4_SPREAD_NARROW;
		bullets_add();

		bullet_template.angle = (0x78 - (unsigned char)boss_frame);
		bullets_add();
		return;
	}

	boss_mode = 1;
	boss_frame = 0;
}

void far gba_boss_update_reimu(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		reimu_cloud_interval = (5 - (gba_boss_level / 5));
		reimu_unused_param = (gba_boss_level + 0x18);
		reimu_bullet_speed = ((gba_boss_level * 2) + 0x28);
		reimu_orbit_count = ((gba_boss_level / 8) + 4);
		reimu_ring_speed = (gba_boss_level + 0x10);
		reimu_ring_count = (gba_boss_level + 0x10);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	boss_target_update();
	boss_frame++;

	if(boss_mode == 0) {
		if(boss_frame != 0x64) {
			return;
		}
		boss_frame = 0;
		boss_mode = 1;
	}

	if(boss_mode == 1) {
		boss_pattern_next();
	}

	switch(boss_mode) {
	case 2:
	case 3:
	case 4:
	case 5:
	case 6:
		reimu_pattern_orbit_cloud();
		break;

	case 8:
	case 9:
	case 0x0A:
	case 0x0D:
		reimu_pattern_spreads();
		break;

	case 0x0F:
	case 0x10:
	case 0x11:
		reimu_pattern_orbit_burst();
		break;

	case 7:
	case 0x0B:
	case 0x0C:
	case 0x0E:
		reimu_pattern_mirrored_spread();
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

void near reimu_render_main(void)
{
	screen_x_t left;
	screen_y_t top;
	pid_t pid_other;
	unsigned char anim;
	register sprite16_offset_t sprite_offset;
	register int i;

	pid_other = (1 - pid_current);
	sprite16_put_size.set(96, 96);

	if(pid_other == 0) {
		sprite16_clip.set_for_pid_0();
	} else {
		sprite16_clip.set_for_pid_1();
	}

	sprite_offset = boss_sprite_offset;
	if(boss_hit != 0) {
		sprite_offset += 0x0C;
	}

	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - 48);
	top = ((boss_center_y >> 4) - 32);
	sprite16_put(left, top, sprite_offset);

	if(boss_render_mode != 1) {
		return;
	}

	sprite16_put_size.set(48, 48);
	sprite_offset = (boss_sprite_offset + 0xFFF4);
	anim = (boss_frame >> 2);
	if((anim & 3) == 1) {
		sprite_offset += 6;
	} else if((anim & 3) != 0) {
		sprite_offset += (((anim & 1) * 6) + 0x780);
	}

	for(i = 0; i < reimu_orbit_count; i++) {
		left = (
			playfield_fg_x_to_screen(reimu_orbit_x[i], pid_other) - 24
		);
		top = ((reimu_orbit_y[i] >> 4) - 8);
		sprite16_put(left, top, sprite_offset);
	}
}

void near pascal reimu_render_intro(unsigned char angle, int length)
{
	screen_y_t top;
	int i;
	unsigned char anim;
	pid_t pid_other;
	register sprite16_offset_t sprite_offset;
	register screen_x_t left;

	pid_other = (1 - pid_current);

	if((round_frame_mod2 != 0) && (boss_frame < 0x40)) {
		return;
	}

	sprite16_put_size.set(48, 48);
	if(pid_current != 0) {
		sprite16_clip.set_for_pid_0();
	} else {
		sprite16_clip.set_for_pid_1();
	}

	sprite_offset = (pid.so_attack + 0x280);
	anim = (boss_frame >> 2);
	if((anim & 3) == 1) {
		sprite_offset += 6;
	} else if((anim & 3) != 0) {
		sprite_offset += (((anim & 1) * 6) + 0x780);
	}

	for(i = 0; i < 8; (i++, angle += 0x20)) {
		left = polar(boss_center_x, length, CosTable8[angle]);
		top = polar(boss_center_y, length, SinTable8[angle]);
		left = (playfield_fg_x_to_screen(left, pid_other) - 24);
		top = ((top >> 4) - 8);
		sprite16_put(left, top, sprite_offset);
	}
}

void far gba_boss_render_reimu(void)
{
	if(pid_current != gba_boss_launched_by) {
		return;
	}

	if(boss_mode == 0) {
		reimu_render_intro(
			(unsigned char)boss_frame,
			(0xC80 - (boss_frame << 5))
		);
		return;
	}

	if(boss_mode != 0xFF) {
		reimu_render_main();
		return;
	}

	boss_explosion_render();
}
