// Complete current source-native Turbo C++ reconstruction for the
// original Marisa major BOSS physical owner inside TH03 MAIN_03_TEXT.
// The full original normal Japanese MAIN link is exact. Shared BOSS
// helpers/storage and canonical Factory acceptance are separate gates.
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

// Reuse the same physical 32-byte shared BOSS template, with semantic
// names for the historical +10..+15 state bytes.
#include "src/main/boss/template_state.hpp"

extern boss_template_state_t boss_character_template[PLAYER_COUNT];

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

// The original shared scheduler uses these Marisa-specific attack IDs.
enum marisa_boss_mode_t {
    MARISA_MODE_INTRO = 0x00,
    MARISA_MODE_SELECT = 0x01,
    MARISA_MODE_SPREAD_0 = 0x02,
    MARISA_MODE_SPREAD_1 = 0x03,
    MARISA_MODE_SPREAD_2 = 0x04,
    MARISA_MODE_SPREAD_3 = 0x05,
    MARISA_MODE_NARROW_0 = 0x06,
    MARISA_MODE_NARROW_1 = 0x07,
    MARISA_MODE_WIDE_0 = 0x08,
    MARISA_MODE_WIDE_1 = 0x09,
    MARISA_MODE_WIDE_2 = 0x0A,
    MARISA_MODE_RING_0 = 0x0B,
    MARISA_MODE_RING_1 = 0x0C,
    MARISA_MODE_RING_2 = 0x0D,
    MARISA_MODE_RING_3 = 0x0E,
    MARISA_MODE_RING_4 = 0x0F,
    MARISA_MODE_RING_5 = 0x10,
    MARISA_MODE_NARROW_2 = 0x11,
    MARISA_MODE_DESCEND = 0x80,
    MARISA_MODE_EXPLODE = 0xFF,
};

void far pascal boss_marisa_template_init(int player_id)
{
	boss_template_state_t near *p = &boss_character_template[player_id];

	p->center_x = 0x900;
	p->center_y = 0x500;
	p->velocity_x = -0x20;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = 0;
	p->hp = 0x6E;
	p->pattern_i = 0;
	p->sprite_offset = 0x280;
	if(player_id != 0) {
		p->sprite_offset += 0x28;
	}
	p->render_mode = 0;
}

enum marisa_spread_phase_t {
    MARISA_SPREAD_START = 0x20,
    MARISA_SPREAD_FINISH = 0x50,
    MARISA_SPREAD_PERIOD = 4,
    MARISA_SPREAD_ANGLE_STEP = 7,
};

// The full BOSS update owns spread/ring clocks and main/split renderers.
// Original unsigned 16-bit periods admit natural %4 and %32 C++ clocks;
// division by the *byte* ring count and by two in projectile speed
// remain independent operations with the original TC4 signedness.
enum marisa_native_frame_timing_t {
    MARISA_BOSS_INTRO_END = 0x64,
    MARISA_MAIN_FLICKER_PERIOD = 4,
    MARISA_MAIN_FLICKER_FIRST_HALF = 2,
    MARISA_SPLIT_START_RADIUS = 0xC8,
    MARISA_RING_FULL_TURN = 256,
    MARISA_COLLISION_TILE_SIZE = 56,
    MARISA_COLLISION_HALF_RADIUS = TO_SP(32),
    MARISA_RENDER_MAIN_WIDTH = 176,
    MARISA_RENDER_MAIN_HEIGHT = 96,
    MARISA_RENDER_MAIN_LEFT_OFFSET = 88,
    MARISA_RENDER_MAIN_TOP_OFFSET = 32,
    MARISA_RENDER_DAMAGE_WIDTH = 48,
    MARISA_RENDER_DAMAGE_HEIGHT = 80,
    MARISA_RENDER_STRIP_WIDTH = 112,
    MARISA_RENDER_STRIP_HEIGHT = 16,
    MARISA_RENDER_HIT_SPRITE_OFFSET = 0x16,
    MARISA_RENDER_FLICKER_SPRITE_OFFSET = 0x1C,
    MARISA_RENDER_FLICKER_STRIP_OFFSET = 0xF00,
    MARISA_RENDER_ALTERNATE_STRIP_OFFSET = 0x1180,
    MARISA_RING_DENSE_LEVEL = 8,
    MARISA_RENDER_MASK_FIRST = 0xAAAA,
    MARISA_RENDER_MASK_SECOND = 0x5555,
    MARISA_RENDER_MASK_RESET = 0xFFFF,
};

void near marisa_pattern_spread(void)
{
	boss_render_mode = 1;
	if(boss_frame < MARISA_SPREAD_START) {
		return;
	}
	if(boss_frame == MARISA_SPREAD_START) {
		marisa_bullet_angle = 0;
	}
	if(boss_frame < MARISA_SPREAD_FINISH) {
		// Natural unsigned word-frame remainder truth check emits the
	// original spread gate (fresh native TC4 af881a).
	if(boss_frame % MARISA_SPREAD_PERIOD) {
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

		// Original TC4 rejects `angle += ENUM` (historical af830b)
		// but DOES compile the natural `angle = angle + ENUM` to exactly
		// the original byte-memory instructions (fresh af881e/f/g).
		marisa_bullet_angle = marisa_bullet_angle + MARISA_SPREAD_ANGLE_STEP;
		return;
	}
	boss_render_mode = 0;
	boss_mode = 1;
	boss_frame = 0;
}

// The wide and narrow vertical-column attacks share the first three
// emissions, but intentionally have different terminal frames.
enum marisa_column_phase_t {
    MARISA_COLUMN_WARMUP_END = 0x38,
    MARISA_COLUMN_FIRST = 0x40,
    MARISA_COLUMN_SECOND = MARISA_SPREAD_FINISH,
    MARISA_COLUMN_THIRD = 0x60,
    MARISA_COLUMN_FOURTH = 0x70,
    MARISA_COLUMN_WIDE_FINISH = 0x84,
    MARISA_COLUMN_SPAWN_Y = 0x1700,
    MARISA_COLUMN_PAIR_0_LEFT = 0x80,
    MARISA_COLUMN_PAIR_0_RIGHT = 0x1180,
    MARISA_COLUMN_PAIR_1_LEFT = 0x380,
    MARISA_COLUMN_PAIR_1_RIGHT = 0xE80,
    MARISA_COLUMN_PAIR_2_LEFT = 0x680,
    MARISA_COLUMN_PAIR_2_RIGHT = 0xB80,
    MARISA_COLUMN_PAIR_3_LEFT = 0x980,
    MARISA_COLUMN_PAIR_3_RIGHT = 0x880,
};

enum marisa_narrow_column_x_t {
    MARISA_NARROW_PAIR_0_LEFT = 0x200,
    MARISA_NARROW_PAIR_0_RIGHT = 0x1000,
    MARISA_NARROW_PAIR_1_LEFT = 0x500,
    MARISA_NARROW_PAIR_1_RIGHT = 0xD00,
    MARISA_NARROW_PAIR_2_LEFT = 0x800,
    MARISA_NARROW_PAIR_2_RIGHT = 0xA00,
};

void near marisa_pattern_columns_wide(void)
{
	pid_t pid_other = (1 - pid_current);
	boss_render_mode = 1;

	if(boss_frame < MARISA_COLUMN_WARMUP_END) {
		return;
	}
	if(boss_frame == MARISA_COLUMN_FIRST) {
		marisa_exatt_add(MARISA_COLUMN_PAIR_0_LEFT, MARISA_COLUMN_SPAWN_Y, pid_other);
		marisa_exatt_add(MARISA_COLUMN_PAIR_0_RIGHT, MARISA_COLUMN_SPAWN_Y, pid_other);
		return;
	}
	if(boss_frame == MARISA_COLUMN_SECOND) {
		marisa_exatt_add(MARISA_COLUMN_PAIR_1_LEFT, MARISA_COLUMN_SPAWN_Y, pid_other);
		marisa_exatt_add(MARISA_COLUMN_PAIR_1_RIGHT, MARISA_COLUMN_SPAWN_Y, pid_other);
		return;
	}
	if(boss_frame == MARISA_COLUMN_THIRD) {
		marisa_exatt_add(MARISA_COLUMN_PAIR_2_LEFT, MARISA_COLUMN_SPAWN_Y, pid_other);
		marisa_exatt_add(MARISA_COLUMN_PAIR_2_RIGHT, MARISA_COLUMN_SPAWN_Y, pid_other);
		return;
	}
	if(boss_frame == MARISA_COLUMN_FOURTH) {
		marisa_exatt_add(MARISA_COLUMN_PAIR_3_LEFT, MARISA_COLUMN_SPAWN_Y, pid_other);
		marisa_exatt_add(MARISA_COLUMN_PAIR_3_RIGHT, MARISA_COLUMN_SPAWN_Y, pid_other);
		return;
	}
	if(boss_frame == MARISA_COLUMN_WIDE_FINISH) {
		boss_render_mode = 0;
		boss_mode = 1;
		boss_frame = 0;
	}
}

// Regular 32-frame volley, ending at the original 0x82 timer.
enum marisa_ring_phase_t {
    MARISA_RING_PERIOD = 0x20,
    MARISA_RING_FINISH = 0x82,
};

void near marisa_pattern_ring(void)
{
	boss_move_sine();

	// Same original unsigned-word period uses a natural zero remainder
	// truth check, independent of the mutable byte angle (af881b).
	if(!(boss_frame % MARISA_RING_PERIOD)) {
		bullet_template.angle = randring_far_next16();
		bullet_template.group = BG_RING;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.pid = (1 - pid_current);

		if(gba_boss_level < MARISA_RING_DENSE_LEVEL) {
			bullet_template.count = marisa_cloud_count_low;
		} else {
			bullet_template.speed.v = marisa_ring_speed;
			bullet_template.count = marisa_ring_count;
			bullet_template.type = BT_BULLET16_DEFAULT;
			bullets_add();

			// Preserve the signed 16-bit promotion/division of the byte
			// ring count. Explicit unsigned widening changed CODE (af881h).
			bullet_template.angle += (MARISA_RING_FULL_TURN / marisa_ring_count);
			bullet_template.count = marisa_cloud_count_high;
		}
		bullet_template.speed.v = marisa_cloud_speed;
		bullet_template.type = BT_PELLET_CLOUD;
		bullets_add();
	}

	if(boss_frame >= MARISA_RING_FINISH) {
		boss_mode = 1;
		boss_frame = 0;
	}
}

void near marisa_pattern_columns_narrow(void)
{
	pid_t pid_other = (1 - pid_current);
	boss_render_mode = 1;

	if(boss_frame < MARISA_COLUMN_WARMUP_END) {
		return;
	}
	if(boss_frame == MARISA_COLUMN_FIRST) {
		marisa_exatt_add(MARISA_NARROW_PAIR_0_LEFT, MARISA_COLUMN_SPAWN_Y, pid_other);
		marisa_exatt_add(MARISA_NARROW_PAIR_0_RIGHT, MARISA_COLUMN_SPAWN_Y, pid_other);
		return;
	}
	if(boss_frame == MARISA_COLUMN_SECOND) {
		marisa_exatt_add(MARISA_NARROW_PAIR_1_LEFT, MARISA_COLUMN_SPAWN_Y, pid_other);
		marisa_exatt_add(MARISA_NARROW_PAIR_1_RIGHT, MARISA_COLUMN_SPAWN_Y, pid_other);
		return;
	}
	if(boss_frame == MARISA_COLUMN_THIRD) {
		marisa_exatt_add(MARISA_NARROW_PAIR_2_LEFT, MARISA_COLUMN_SPAWN_Y, pid_other);
		marisa_exatt_add(MARISA_NARROW_PAIR_2_RIGHT, MARISA_COLUMN_SPAWN_Y, pid_other);
		return;
	}
	if(boss_frame == MARISA_COLUMN_FOURTH) {
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
	case MARISA_MODE_INTRO:
		if(boss_frame != MARISA_BOSS_INTRO_END) {
			return;
		}
		boss_frame = 0;
		boss_mode = 1;
		break;

	case MARISA_MODE_SELECT:
		boss_pattern_next();
		break;

	case MARISA_MODE_SPREAD_0:
	case MARISA_MODE_SPREAD_1:
	case MARISA_MODE_SPREAD_2:
	case MARISA_MODE_SPREAD_3:
		marisa_pattern_spread();
		break;

	case MARISA_MODE_WIDE_0:
	case MARISA_MODE_WIDE_1:
	case MARISA_MODE_WIDE_2:
		marisa_pattern_columns_wide();
		break;

	case MARISA_MODE_RING_0:
	case MARISA_MODE_RING_1:
	case MARISA_MODE_RING_2:
	case MARISA_MODE_RING_3:
	case MARISA_MODE_RING_4:
	case MARISA_MODE_RING_5:
		marisa_pattern_ring();
		break;

	case MARISA_MODE_NARROW_0:
	case MARISA_MODE_NARROW_1:
	case MARISA_MODE_NARROW_2:
		marisa_pattern_columns_narrow();
		break;

	case MARISA_MODE_DESCEND:
		boss_fall();
		break;

	case MARISA_MODE_EXPLODE:
		return;
	}

	collmap_center.x.v = boss_center_x;
	collmap_center.y.v = boss_center_y;
	collmap_stripe_tile_w.set(MARISA_COLLISION_TILE_SIZE);
	collmap_tile_h.set(MARISA_COLLISION_TILE_SIZE);
	collmap_pid = pid_other;
	collmap_set_rect_striped();

	hitbox_hittest_skip_explosions = true;
	hitbox.radius.x.v = MARISA_COLLISION_HALF_RADIUS;
	hitbox.radius.y.v = MARISA_COLLISION_HALF_RADIUS;
	hitbox.pid = pid_other;
	hitbox.origin.center.x.v = boss_center_x;
	hitbox.origin.center.y.v = boss_center_y;
	boss_hit = hitbox_hittest();
	boss_hp -= boss_hit;
	hitbox_hittest_skip_explosions = false;
	boss_hittest_end();
}

// Unsigned global four-frame flicker lowers from natural %4
// to the original masked native comparison in this renderer.
void near marisa_render_main(void)
{
	sprite16_offset_t sprite_offset;
	pid_t pid_other;
	register screen_x_t left;
	register screen_y_t top;

	pid_other = (1 - pid_current);
	sprite16_put_size.set(MARISA_RENDER_MAIN_WIDTH, MARISA_RENDER_MAIN_HEIGHT);
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - MARISA_RENDER_MAIN_LEFT_OFFSET);
	top = ((boss_center_y >> 4) - MARISA_RENDER_MAIN_TOP_OFFSET);
	sprite16_put(left, top, boss_sprite_offset);

	if(boss_hit) {
		sprite16_put_size.set(MARISA_RENDER_DAMAGE_WIDTH, MARISA_RENDER_DAMAGE_HEIGHT);
		left += 64;
		top += 16;
		sprite16_put(left, top, (boss_sprite_offset + MARISA_RENDER_HIT_SPRITE_OFFSET));
		return;
	}
	if(boss_render_mode != 1) {
		return;
	}
	if(
		(round_or_result_frame % MARISA_MAIN_FLICKER_PERIOD) <
		MARISA_MAIN_FLICKER_FIRST_HALF
	) {
		sprite16_put_size.set(MARISA_RENDER_DAMAGE_WIDTH, MARISA_RENDER_DAMAGE_HEIGHT);
		left += 64;
		top += 16;
		sprite16_put(left, top, (boss_sprite_offset + MARISA_RENDER_FLICKER_SPRITE_OFFSET));
		left -= 32;
		top += 32;
		sprite_offset = (boss_sprite_offset + MARISA_RENDER_FLICKER_STRIP_OFFSET);
	} else {
		left += 32;
		top += 48;
		sprite_offset = (boss_sprite_offset + MARISA_RENDER_ALTERNATE_STRIP_OFFSET);
	}
	sprite16_put_size.set(MARISA_RENDER_STRIP_WIDTH, MARISA_RENDER_STRIP_HEIGHT);
	sprite16_put(left, top, sprite_offset);
}

void near pascal marisa_render_split(int offset)
{
	screen_y_t top;
	pid_t pid_other;
	// Allocation order is essential to original TC4: the first register
	// local takes SI for the two split offsets, then left takes DI.
	// This is source-native C++ without manually assigning _SI.
	register int signed_offset = offset;
	register screen_x_t left;

	pid_other = (1 - pid_current);
	sprite16_put_size.set(MARISA_RENDER_MAIN_WIDTH, MARISA_RENDER_MAIN_HEIGHT);
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - MARISA_RENDER_MAIN_LEFT_OFFSET);
	top = ((boss_center_y >> 4) - MARISA_RENDER_MAIN_TOP_OFFSET);

	// Two distinct original alternating VRAM mask planes and the final
	// all-bits restore stay explicit, not collapsed into generic draw calls.
	_AH = SPRITE16_SET_MASK;
	_DX = MARISA_RENDER_MASK_FIRST;
	geninterrupt(SPRITE16);
	sprite16_put((left - signed_offset), top, boss_sprite_offset);

	_AH = SPRITE16_SET_MASK;
	_DX = MARISA_RENDER_MASK_SECOND;
	geninterrupt(SPRITE16);
	sprite16_put((left + signed_offset), top, boss_sprite_offset);

	_AH = SPRITE16_SET_MASK;
	_DX = MARISA_RENDER_MASK_RESET;
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

	if(boss_mode == MARISA_MODE_INTRO) {
		marisa_render_split(MARISA_SPLIT_START_RADIUS - (boss_frame << 1));
		return;
	}
	if(boss_mode != MARISA_MODE_EXPLODE) {
		marisa_render_main();
		return;
	}
	boss_explosion_render();
}
