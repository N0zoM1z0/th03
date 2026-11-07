// Natural Turbo C++ reconstruction candidate for the complete Chiyuri
// contribution inside TH03 MAIN_03_TEXT. Shared boss helpers and historical
// state remain external until full-link ownership is proved.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/chiyuri.hpp"
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
#include "compat/rec98/th03/main/v_colors.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/sprite16/sprite16.h"

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
extern unsigned char boss_angle;
extern unsigned char boss_pattern_i;
extern unsigned char boss_pattern_count;
extern unsigned char boss_render_mode;
extern unsigned char boss_render_frame;
extern unsigned char boss_move_phase;
extern int boss_effect_radius;
extern unsigned int boss_frame;

// Chiyuri's seven level-derived parameters, all mapped onto the historical
// shared parameter scratch bytes.
extern unsigned char chiyuri_cardinal_speed;
extern unsigned char chiyuri_cardinal_interval;
extern unsigned char chiyuri_ring_speed;
extern unsigned char chiyuri_ring_interval;
extern unsigned char chiyuri_trail_speed;
extern unsigned char chiyuri_fan_speed;
extern unsigned char chiyuri_fan_count;

// Chiyuri-private direction state in the historical player-state tail.
extern unsigned char chiyuri_cardinal_angle;
extern unsigned char chiyuri_cardinal_reverse;

// Two overlapping word views of five historical x/y pairs at DATA
// 1D56:08D6 and 1D56:08D8. The original code doubles the 0..4 random index
// before using it as a word-array index, yielding a four-byte pair stride.
extern int chiyuri_boss_x_words[];
extern int chiyuri_boss_y_words[];

extern int SinTable8[256];
extern int CosTable8[256];

extern "C" {
void far pascal bomb_palette_step(int level, pid_t pid);
void far pascal palette_restore_for_pid(pid_t pid);
void far pascal bomb_center_add(int x, int y, int pid);
void far pascal bomb_axis_add(int x, int y, int pid);
}

// The shared BOSS scheduler draws byte modes 2..17; Chiyuri's
// pattern grouping and the intro/descend behavior are character-specific.
enum chiyuri_boss_mode_t {
    CHIYURI_MODE_INTRO = 0x00,
    CHIYURI_MODE_SELECT = 0x01,
    CHIYURI_MODE_CARDINAL_0 = 0x02,
    CHIYURI_MODE_CARDINAL_1 = 0x03,
    CHIYURI_MODE_CARDINAL_2 = 0x04,
    CHIYURI_MODE_CARDINAL_3 = 0x05,
    CHIYURI_MODE_RINGS_0 = 0x06,
    CHIYURI_MODE_RINGS_1 = 0x07,
    CHIYURI_MODE_RINGS_2 = 0x08,
    CHIYURI_MODE_RINGS_3 = 0x09,
    CHIYURI_MODE_TRAIL_0 = 0x0A,
    CHIYURI_MODE_TRAIL_1 = 0x0B,
    CHIYURI_MODE_TRAIL_2 = 0x0C,
    CHIYURI_MODE_TRAIL_3 = 0x0D,
    CHIYURI_MODE_FANS_0 = 0x0E,
    CHIYURI_MODE_FANS_1 = 0x0F,
    CHIYURI_MODE_FANS_2 = 0x10,
    CHIYURI_MODE_FANS_3 = 0x11,
    CHIYURI_MODE_DESCEND = 0x80,
    CHIYURI_MODE_EXPLODE = 0xFF,
};

void far pascal boss_chiyuri_template_init(int player_id)
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
	p->hp = 0x8C;
	p->pattern_i = 0;
	p->move_phase = 0;
	p->effect_radius = 0;
	p->sprite_offset = 0x288;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->render_mode = 0;
}

void near chiyuri_pattern_cardinal(void)
{
	pid_t pid_other;

	if((boss_frame % chiyuri_cardinal_interval) != 1) {
		return;
	}

	if(boss_frame == 1) {
		chiyuri_cardinal_angle = 0xE0;
		chiyuri_cardinal_reverse = 0;
		pid_other = (1 - pid_current);

		bomb_axis_add(
			(boss_center_x - TO_SP(56)), boss_center_y, pid_other
		);
		bomb_axis_add(
			(boss_center_x + TO_SP(56)), boss_center_y, pid_other
		);
		bomb_axis_add(
			boss_center_x, (boss_center_y - TO_SP(56)), pid_other
		);
		bomb_axis_add(
			boss_center_x, (boss_center_y + TO_SP(56)), pid_other
		);
	}

	else if(boss_frame >= 0x80) {
		boss_mode = 1;
		boss_frame = 0;
		boss_render_mode = 0x20;
	}

	bullet_template.type = BT_PELLET;
	bullet_template.group = BG_1;
	bullet_template.speed.v = chiyuri_cardinal_speed;

	if(chiyuri_cardinal_reverse == 0) {
		chiyuri_cardinal_angle += 8;
		if(chiyuri_cardinal_angle == 0x20) {
			chiyuri_cardinal_reverse = 1;
			chiyuri_cardinal_angle = 0x24;
		}
	} else {
		chiyuri_cardinal_angle -= 8;
		if(chiyuri_cardinal_angle == 0xE4) {
			chiyuri_cardinal_reverse = 0;
			chiyuri_cardinal_angle = 0xE0;
		}
	}

	bullet_template.center.x.v = (boss_center_x + TO_SP(56));
	bullet_template.center.y.v = boss_center_y;
	bullet_template.angle = chiyuri_cardinal_angle;
	bullets_add();

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = (boss_center_y + TO_SP(56));
	bullet_template.angle += 0x40;
	bullets_add();

	bullet_template.center.x.v = (boss_center_x - TO_SP(56));
	bullet_template.center.y.v = boss_center_y;
	bullet_template.angle += 0x40;
	bullets_add();

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = (boss_center_y - TO_SP(56));
	bullet_template.angle += 0x40;
	bullets_add();
}

void near chiyuri_pattern_rings(void)
{
	if((boss_frame % chiyuri_ring_interval) != 1) {
		return;
	}

	bomb_axis_add(
		boss_center_x, boss_center_y, (1 - pid_current)
	);

	if(boss_frame >= 0x80) {
		boss_mode = 1;
		boss_frame = 0;
		boss_render_mode = 0x20;
	}

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = boss_center_y;
	bullet_template.angle = randring_far_next16();
	bullet_template.type = BT_BULLET16_DEFAULT;
	bullet_template.group = BG_32_RING;
	bullet_template.speed.v = chiyuri_ring_speed;
	bullets_add();

	if(gba_boss_level < 8) {
		return;
	}

	bullet_template.type = BT_PELLET;
	bullet_template.group = BG_8_RING;
	bullet_template.speed.v = (chiyuri_ring_speed / 4);

	bullet_template.center.x.v = (boss_center_x + TO_SP(56));
	bullets_add();
	bullet_template.center.x.v = (boss_center_x - TO_SP(56));
	bullets_add();

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = (boss_center_y + TO_SP(56));
	bullets_add();
	bullet_template.center.y.v = (boss_center_y - TO_SP(56));
	bullets_add();
}

// Bomb warnings repeat every eight ticks before the single 48-shot
// trailing ring is released at the original 0x30 frame.
enum chiyuri_trail_phase_t {
    CHIYURI_TRAIL_BOMB_PERIOD = 8,
    CHIYURI_TRAIL_FIRE_FRAME = 0x30,
};

void near chiyuri_pattern_trail_ring(void)
{
	if((boss_frame % CHIYURI_TRAIL_BOMB_PERIOD) == 0) {
		bomb_axis_add(
			boss_center_x, boss_center_y, (1 - pid_current)
		);
	}

	if(boss_frame != CHIYURI_TRAIL_FIRE_FRAME) {
		return;
	}

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = boss_center_y;
	bullet_template.angle = randring_far_next16();
	bullet_template.type = BT_BULLET16_DEFAULT;
	bullet_template.group = BG_RING;
	bullet_template.count = 48;
	bullet_template.speed.v = chiyuri_trail_speed;
	bullet_template.has_trail = true;
	bullets_add();
	bullet_template.has_trail = false;

	boss_mode = 1;
	boss_frame = 0;
	boss_render_mode = 0x20;
}

// The horizontal fans fire at 0x20 and vertical fans at 0x40;
// both retain separate ascending/descending bullet velocity passes.
enum chiyuri_fan_phase_t {
    CHIYURI_FAN_HORIZONTAL_FRAME = 0x20,
    CHIYURI_FAN_VERTICAL_FRAME = 0x40,
};

void near chiyuri_pattern_fans(void)
{
	pid_t pid_other = (1 - pid_current);
	register int i;

	if(boss_frame == CHIYURI_FAN_HORIZONTAL_FRAME) {
		bomb_axis_add(
			(boss_center_x - TO_SP(56)), boss_center_y, pid_other
		);
		bomb_axis_add(
			(boss_center_x + TO_SP(56)), boss_center_y, pid_other
		);

		bullet_template.center.y.v = boss_center_y;
		bullet_template.group = BG_1;
		bullet_template.type = BT_PELLET;
		bullet_template.speed.v = chiyuri_fan_speed;

		for(i = 0; i < chiyuri_fan_count; i++) {
			bullet_template.center.x.v = (
				boss_center_x -
				TO_SP(56) +
				(((i * 0x70) / chiyuri_fan_count) << 4)
			);
			bullet_template.angle = (
				0x60 - ((i << 6) / chiyuri_fan_count)
			);
			bullets_add();

			bullet_template.angle = (0 - bullet_template.angle);
			bullets_add();

			bullet_template.speed.v += 2;
		}

		for(i = 0; i < chiyuri_fan_count; i++) {
			bullet_template.center.x.v = (
				boss_center_x -
				TO_SP(56) +
				(((i * 0x70) / chiyuri_fan_count) << 4)
			);
			bullet_template.angle = (
				0x60 - ((i << 6) / chiyuri_fan_count)
			);
			bullets_add();

			bullet_template.angle = (0 - bullet_template.angle);
			bullets_add();

			bullet_template.speed.v -= 2;
		}
		return;
	}

	if(boss_frame != CHIYURI_FAN_VERTICAL_FRAME) {
		return;
	}

	bomb_axis_add(
		boss_center_x, (boss_center_y - TO_SP(56)), pid_other
	);
	bomb_axis_add(
		boss_center_x, (boss_center_y + TO_SP(56)), pid_other
	);

	bullet_template.center.x.v = boss_center_x;
	bullet_template.type = BT_PELLET;
	bullet_template.group = BG_2_SPREAD_HORIZONTALLY_SYMMETRIC;
	bullet_template.speed.v = chiyuri_fan_speed;

	for(i = 0; i < chiyuri_fan_count; i++) {
		bullet_template.center.y.v = (
			boss_center_y -
			TO_SP(56) +
			(((i * 0x70) / chiyuri_fan_count) << 4)
		);
		bullet_template.angle = (
			((i << 6) / chiyuri_fan_count) - 0x20
		);
		bullets_add();

		bullet_template.speed.v += 2;
	}

	for(i = 0; i < chiyuri_fan_count; i++) {
		bullet_template.center.y.v = (
			boss_center_y -
			TO_SP(56) +
			(((i * 0x70) / chiyuri_fan_count) << 4)
		);
		bullet_template.angle = (
			((i << 6) / chiyuri_fan_count) - 0x20
		);
		bullets_add();

		bullet_template.speed.v -= 2;
	}

	boss_mode = 1;
	boss_frame = 0;
	boss_render_mode = 0x20;
}

void far gba_boss_update_chiyuri(void)
{
	pid_t pid_other;
	unsigned char random_i;

	if(boss_update_start()) {
		chiyuri_cardinal_speed = (gba_boss_level + 0x30);
		chiyuri_cardinal_interval = (6 - (gba_boss_level / 4));
		chiyuri_ring_speed = (gba_boss_level + 0x34);
		chiyuri_ring_interval = (0x20 - gba_boss_level);
		chiyuri_trail_speed = ((gba_boss_level * 2) + 0x38);
		chiyuri_fan_speed = (gba_boss_level + 0x10);
		chiyuri_fan_count = ((gba_boss_level / 2) + 0x0C);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	boss_target_update();
	bullet_template.is_animated = false;
	bullet_template.pid = pid_other;
	boss_frame++;

	switch(boss_mode) {
	case CHIYURI_MODE_INTRO:
		if(boss_frame == 0x60) {
			boss_frame = 0;
			boss_mode = 1;
			bomb_palette_step(0xFF, pid_other);
			boss_move_phase = 0x10;
			boss_render_mode = 0x10;
			break;
		}
		if(boss_frame == 0x50) {
			bomb_center_add(
				(boss_center_x - TO_SP(56)), boss_center_y, pid_other
			);
			bomb_center_add(
				(boss_center_x + TO_SP(56)), boss_center_y, pid_other
			);
			bomb_center_add(
				boss_center_x, (boss_center_y - TO_SP(56)), pid_other
			);
			bomb_center_add(
				boss_center_x, (boss_center_y + TO_SP(56)), pid_other
			);
			break;
		}
		bullet_template.is_animated = true;
		return;

	case CHIYURI_MODE_SELECT:
		if(boss_render_mode == 0x10) {
			random_i = (randring_far_next16_mod(5) * 2);
			boss_center_x = chiyuri_boss_x_words[random_i];
			boss_center_y = chiyuri_boss_y_words[random_i];
			boss_move_phase = 0x10;
		}
		if(boss_frame >= 0x30) {
			boss_frame = 0;
			boss_mode = (randring_far_next16_and(0x0F) + 2);
			boss_pattern_i++;
			if(boss_pattern_i > boss_pattern_count) {
				boss_mode = 0x80;
			}
		}
		break;

	case CHIYURI_MODE_CARDINAL_0:
	case CHIYURI_MODE_CARDINAL_1:
	case CHIYURI_MODE_CARDINAL_2:
	case CHIYURI_MODE_CARDINAL_3:
		chiyuri_pattern_cardinal();
		break;

	case CHIYURI_MODE_RINGS_0:
	case CHIYURI_MODE_RINGS_1:
	case CHIYURI_MODE_RINGS_2:
	case CHIYURI_MODE_RINGS_3:
		chiyuri_pattern_rings();
		break;

	case CHIYURI_MODE_TRAIL_0:
	case CHIYURI_MODE_TRAIL_1:
	case CHIYURI_MODE_TRAIL_2:
	case CHIYURI_MODE_TRAIL_3:
		chiyuri_pattern_trail_ring();
		break;

	case CHIYURI_MODE_FANS_0:
	case CHIYURI_MODE_FANS_1:
	case CHIYURI_MODE_FANS_2:
	case CHIYURI_MODE_FANS_3:
		chiyuri_pattern_fans();
		break;

	case CHIYURI_MODE_DESCEND:
		boss_fall();
		palette_restore_for_pid(pid_other);
		break;

	case CHIYURI_MODE_EXPLODE:
		bullet_template.is_animated = true;
		return;
	}

	bullet_template.is_animated = true;

	boss_render_frame += ((round_or_result_frame % 4) == 0);
	boss_render_frame &= 3;

	if(boss_move_phase != 0) {
		boss_move_phase--;
		if(boss_move_phase != 0) {
			bomb_palette_step((boss_move_phase << 4), pid_other);
		}
	}

	if(boss_render_mode != 0) {
		boss_render_mode--;
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

void near chiyuri_render_ring(void)
{
	screen_y_t top;
	sprite16_offset_t sprite_offset;
	int pid_other;
	int radius;
	unsigned char angle;
	register int i;
	register screen_x_t left;

	pid_other = (1 - pid_current);
	radius = (boss_effect_radius << 4);

	sprite16_put_size.w = 32;
	sprite16_put_size.h = 16;

	sprite_offset = (boss_sprite_offset + 0x790);
	sprite_offset += (boss_render_frame << 2);

	for(
		i = 0, angle = boss_move_phase;
		i < 16;
		(i++, angle += 0x10)
	) {
		left = polar(
			boss_center_x, radius, CosTable8[angle]
		);
		top = polar(
			boss_center_y, radius, SinTable8[angle]
		);
		left = (playfield_fg_x_to_screen(left, pid_other) - 16);
		_AX = top;
		static_cast<int16_t>(_AX) >>= 4;
		top = _AX;
		sprite16_put(left, _AX, sprite_offset);
	}
}

void near pascal chiyuri_render_mono(int color);

void near chiyuri_render_main(void)
{
	screen_y_t top;
	register sprite16_offset_t sprite_offset;
	register screen_x_t left;

	if(boss_render_mode == 0) {
		sprite16_put_size.w = 128;
		sprite16_put_size.h = 64;

		left = (
			playfield_fg_x_to_screen(
				boss_center_x, (1 - pid_current)
			) - 64
		);
		top = ((boss_center_y >> 4) - 48);
		sprite_offset = boss_sprite_offset;
		sprite16_put(left, top, sprite_offset);

		left += 48;
		top += 32;

		if(boss_hit != 0) {
			sprite16_put_size.w = 48;
			sprite16_put_size.h = 40;
			sprite_offset += 0x778;
			sprite16_put(left, top, sprite_offset);
			return;
		}

		if(boss_render_frame == 0) {
			return;
		}

		sprite16_put_size.w = 32;
		sprite16_put_size.h = 24;
		sprite_offset += ((boss_render_frame << 2) + 0x0C);
		sprite16_put(left, top, sprite_offset);
		return;
	}

	if(boss_render_mode >= 0x18) {
		chiyuri_render_mono(6);
	} else if(boss_render_mode >= 0x14) {
		chiyuri_render_mono(5);
	} else if(boss_render_mode >= 0x0C) {
		chiyuri_render_mono(2);
	} else if(boss_render_mode >= 8) {
		chiyuri_render_mono(5);
	} else if(boss_render_mode >= 4) {
		chiyuri_render_mono(6);
	} else {
		chiyuri_render_mono(V_WHITE);
	}
}

void near chiyuri_render_intro(void)
{
	register int frame;

	if((round_frame_mod2 != 0) && (boss_frame < 0x40)) {
		return;
	}

	// TC4 compiles signed frame*8 to the original left shift. The
	// adjacent byte phase updates still require their AL expression:
	// direct +=4, =phase+4 and -=4 changed original native code.
	frame = boss_frame;
	if(frame < 0x20) {
		boss_effect_radius = (0x100 - (frame * 8));
		_AL = boss_move_phase;
		_AL += 4;
		boss_move_phase = _AL;
	} else if(frame < 0x40) {
		boss_effect_radius = (0x200 - (frame * 8));
		_AL = boss_move_phase;
		_AL += (unsigned char)0xFC;
		boss_move_phase = _AL;
	} else {
		boss_effect_radius = (0x300 - (frame * 8));
		_AL = boss_move_phase;
		_AL += 4;
		boss_move_phase = _AL;
	}

	chiyuri_render_ring();
}

void near pascal chiyuri_render_mono(int color)
{
	screen_x_t left;
	screen_y_t top;
	sprite16_offset_t sprite_offset;

	sprite16_put_size.w = 128;
	sprite16_put_size.h = 64;

	left = (
		playfield_fg_x_to_screen(
			boss_center_x, (1 - pid_current)
		) - 64
	);
	top = ((boss_center_y >> 4) - 48);
	sprite_offset = boss_sprite_offset;

	_AH = SPRITE16_SET_MONO;
	_DX = 1;
	geninterrupt(SPRITE16);
	_AH = SPRITE16_SET_COLOR;
	_DX = color;
	geninterrupt(SPRITE16);
	sprite16_put(left, top, sprite_offset);
	_AH = SPRITE16_SET_MONO;
	asm { xor dx, dx }
	geninterrupt(SPRITE16);
}

void far gba_boss_render_chiyuri(void)
{
	if(pid_current != gba_boss_launched_by) {
		return;
	}

	sprite16_clip_set_for_pid(1 - pid_current);

	if(boss_mode == 0) {
		chiyuri_render_intro();
		return;
	}
	if(boss_mode != 0xFF) {
		chiyuri_render_main();
		return;
	}

	boss_explosion_render();
	if(gba_boss_launched_by == PID_NONE) {
		palette_restore_for_pid(1 - pid_current);
	}
}
