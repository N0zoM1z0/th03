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

void far pascal boss_kana_template_init(int player_id)
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
	p->hp = 0x64;
	p->pattern_i = 0;
	p->effect_radius = 0;
	p->sprite_offset = 0x288;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->render_mode = 0;
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
		boss_render_mode = 1;
		return;
	}
	if(boss_frame == KANA_ACCEL_WARN) {
		boss_render_frame = 0;
		boss_render_mode = 2;
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
	if(boss_frame > KANA_ACCEL_FINISH_AFTER) {
		boss_render_mode = 0;
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
	register int i;

	if(boss_frame == KANA_STAGED_START) {
		boss_render_mode = 1;
		return;
	}
	if(boss_frame == KANA_STAGED_WARN) {
		boss_render_frame = 0;
		boss_render_mode = 2;
		bomb_center_add(boss_center_x, boss_center_y, pid_other);
		return;
	}

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
			snd_se_play(10);
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
			snd_se_play(10);

			bullet_template.type = BT_PELLET;
			bullet_template.angle = 0x20;
			bullet_template.speed.v = TO_SP(1);
			bullet_template.group =
				BG_2_SPREAD_HORIZONTALLY_SYMMETRIC;
			for(i = 0; i < 0x10; i++) {
				bullets_add();
				bullet_template.angle += 6;
				bullet_template.speed.v += 3;
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
			snd_se_play(10);
			return;
		}
		return;
	}

	if(boss_frame > KANA_STAGED_FINISH_AFTER) {
		boss_render_mode = 0;
		boss_frame = 0;
		boss_mode = KANA_MODE_SELECT;
	}
}

// Original clock phases for this full Kana attack; no new state.
enum kana_cloud_phase_t {
    KANA_CLOUD_FINISH_AFTER = 0x64,
};

void near kana_pattern_cloud_ring(void)
{
	signed char angle;

	boss_move_sine();

	if((boss_frame % kana_cloud_interval) == 0) {
		_AL = randring_far_next16_and(0x1F);
		// TC4 lowers byte -= 0x10 to ADD AL,F0 (04 F0), not
		// the original SUB AL,10 (2C 10); retain the exact opcode.
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

	if(boss_frame > KANA_CLOUD_FINISH_AFTER) {
		boss_render_mode = 0;
		boss_frame = 0;
		boss_mode = 1;
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
		boss_render_mode = 1;
		return;
	}
	if(boss_frame == KANA_ROTATING_WARN) {
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

	if(
		(boss_frame >= KANA_ROTATING_VOLLEY_START) &&
		(boss_frame < KANA_ROTATING_VOLLEY_END)
	) {
		if((boss_frame % 4) == 0) {
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
		if(boss_frame > KANA_ROTATING_TURN_AFTER) {
			kana_rotating_angle += kana_rotating_delta;
			return;
		}
		return;
	}

	if(boss_frame > KANA_ROTATING_FINISH_AFTER) {
		boss_render_mode = 0;
		boss_frame = 0;
		boss_mode = KANA_MODE_SELECT;
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
	case KANA_MODE_INTRO:
		if(boss_frame != 0x64) {
			return;
		}
		boss_frame = 0;
		boss_mode = 1;
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
		static_cast<int16_t>(_AX) >>= 4;
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
