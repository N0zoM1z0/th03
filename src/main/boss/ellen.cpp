// Complete current native-source Turbo C++ reconstruction of Ellen's
// original major BOSS in MAIN_03_TEXT. Shared BOSS helpers and state
// remain in their own historical original physical project objects.
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

// Shares the physical 32-byte BOSS layout; trailing bytes are per-character.
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

// Real shared scheduler values, with Ellen's distinct BOSS patterns.
// The modes are byte values; no extra state or dispatch table is emitted.
enum ellen_boss_mode_t {
    ELLEN_MODE_INTRO = 0x00,
    ELLEN_MODE_SELECT = 0x01,
    ELLEN_MODE_SPREAD_0 = 0x02,
    ELLEN_MODE_SPREAD_1 = 0x03,
    ELLEN_MODE_SPREAD_2 = 0x04,
    ELLEN_MODE_SPREAD_3 = 0x05,
    ELLEN_MODE_EXTRA_0 = 0x06,
    ELLEN_MODE_EXTRA_1 = 0x07,
    ELLEN_MODE_EXTRA_2 = 0x08,
    ELLEN_MODE_EXTRA_3 = 0x09,
    ELLEN_MODE_EXTRA_4 = 0x0A,
    ELLEN_MODE_PELLETS_0 = 0x0B,
    ELLEN_MODE_PELLETS_1 = 0x0C,
    ELLEN_MODE_PELLETS_2 = 0x0D,
    ELLEN_MODE_PELLETS_3 = 0x0E,
    ELLEN_MODE_PELLETS_4 = 0x0F,
    ELLEN_MODE_PELLETS_5 = 0x10,
    ELLEN_MODE_PELLETS_6 = 0x11,
    ELLEN_MODE_DESCEND = 0x80,
    ELLEN_MODE_EXPLODE = 0xFF,
};

enum ellen_template_layout_t {
    ELLEN_TEMPLATE_CENTER_X = 0x900,
    ELLEN_TEMPLATE_CENTER_Y = 0x500,
    ELLEN_TEMPLATE_VELOCITY_X = -0x20,
    ELLEN_TEMPLATE_HP = 0x64,
    ELLEN_TEMPLATE_SPRITE_OFF = 0x780,
    ELLEN_TEMPLATE_PLAYER2_OFF = 0x28,
};

enum ellen_render_layout_t {
    ELLEN_RENDER_MODE_NORMAL = 0,
    ELLEN_RENDER_STRIP_Y_SCALE = 0x28,
    ELLEN_RENDER_STRIP_BASE = 0xFB10,
    ELLEN_RENDER_STRIP_LEFT = 48,
    ELLEN_RENDER_STRIP_TOP = 40,
    ELLEN_RENDER_HIT_SPRITE_OFF = 8,
    ELLEN_RENDER_INTRO_SPRITE_OFF = 0x28C,
    ELLEN_RENDER_INTRO_HALF = 16,
};

enum ellen_level_scaling_t {
    ELLEN_BULLET_SPEED_SCALE = 2,
    ELLEN_BULLET_SPEED_BASE = 0x32,
    ELLEN_EXTRA_COUNT_DIVISOR = 10,
    ELLEN_EXTRA_COUNT_BASE = 4,
    ELLEN_PELLET_SPEED_BASE = 0x30,
    ELLEN_PELLET_INTERVAL_BASE = 10,
    ELLEN_PELLET_INTERVAL_DIVISOR = 3,
    ELLEN_EXTRA_RENDER_STEP = 3,
    ELLEN_SPREAD_PERIOD = 2,
    ELLEN_SPREAD_VOLLEY_COUNT = 8,
    ELLEN_STRIP_HEIGHT_DIVISOR = 2,
};

enum ellen_attack_sound_t {
    ELLEN_SOUND_SPREAD = 3,
    ELLEN_SOUND_PELLET = 10,
};

enum ellen_angle_t {
    ELLEN_PELLET_OPPOSITE_ANGLE = 0x80,
};

void far pascal boss_ellen_template_init(int player_id)
{
	boss_template_state_t near *p =
		&boss_character_template[player_id];

	p->center_x = ELLEN_TEMPLATE_CENTER_X;
	p->center_y = ELLEN_TEMPLATE_CENTER_Y;
	p->velocity_x = ELLEN_TEMPLATE_VELOCITY_X;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = 0;
	p->hp = ELLEN_TEMPLATE_HP;
	p->pattern_i = 0;
	p->render_frame = 0;
	p->move_phase = 0;
	p->sprite_offset = ELLEN_TEMPLATE_SPRITE_OFF;
	if(player_id != 0) {
		p->sprite_offset += ELLEN_TEMPLATE_PLAYER2_OFF;
	}
	p->render_mode = 0;
}

// Collision warning, ring firing and termination are distinct timed
// phases of Ellen's full spread attack. Numeric equality is intentional.
enum ellen_spread_phase_t {
    ELLEN_SPREAD_WARNING_0 = 0x10,
    ELLEN_SPREAD_WARNING_1 = 0x14,
    ELLEN_SPREAD_START_ANGLE = 0x18,
    ELLEN_SPREAD_WARMUP_END = 0x1C,
    ELLEN_SPREAD_SINGLE_END = 0x24,
    ELLEN_SPREAD_FINISH = 0x2C,
    ELLEN_SPREAD_ANGLE_STEP = 8,
};

// The two low-bit checks compile from natural unsigned C++ %2.
// The original fire_single/done labels still preserve native branch
// layout; merging the decrement and negative test in strip rendering
// changed original CODE (af678b).
void near ellen_pattern_spread(void)
{
	pid_t pid_other = (1 - pid_current);
	register int i;

	if((boss_frame == ELLEN_SPREAD_WARNING_0) || (boss_frame == ELLEN_SPREAD_WARNING_1)) {
		bomb_center_add(boss_center_x, boss_center_y, pid_other);
		return;
	}
	if(boss_frame == ELLEN_SPREAD_START_ANGLE) {
		bomb_center_add(boss_center_x, boss_center_y, pid_other);
		ellen_spread_angle = 0x40;
		return;
	}
	if(boss_frame < ELLEN_SPREAD_WARMUP_END) {
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

	// Both two-frame spread gates use the unsigned-word low bit.
	if(boss_frame < ELLEN_SPREAD_SINGLE_END) {
		if((boss_frame & (ELLEN_SPREAD_PERIOD - 1)) == 0) {
			goto fire_single;
		}
		goto done;
	}
	if(boss_frame == ELLEN_SPREAD_SINGLE_END) {
		snd_se_play(ELLEN_SOUND_SPREAD);
		// Eight native spread calls in original sound/angle order.
		// A named mutable byte step is exact as C++ `angle=angle+enum`
		// (af893k), unlike replacing literal `angle +=8` with enum.
		i = 0;
		while(i < ELLEN_SPREAD_VOLLEY_COUNT) {
			bullets_add();
			ellen_spread_angle = ellen_spread_angle + ELLEN_SPREAD_ANGLE_STEP;
			bullet_template.angle = ellen_spread_angle;
			++i;
		}
		goto done;
	}
	if(boss_frame > ELLEN_SPREAD_FINISH) {
		goto done;
	}
	if((boss_frame & (ELLEN_SPREAD_PERIOD - 1)) != 0) {
		goto done;
	}

fire_single:
	snd_se_play(ELLEN_SOUND_SPREAD);
	bullets_add();
	ellen_spread_angle = ellen_spread_angle + ELLEN_SPREAD_ANGLE_STEP;

done:
	if(boss_frame >= ELLEN_SPREAD_FINISH) {
		boss_render_mode = ELLEN_RENDER_MODE_NORMAL;
		boss_mode = ELLEN_MODE_SELECT;
		boss_frame = 0;
	}
}

// Warning pulses and radial Extra Attack bursts happen at these
// historical frames, with different final arguments for two volleys.
enum ellen_extra_phase_t {
    ELLEN_EXTRA_WARN_START = 0x20,
    ELLEN_EXTRA_WARN_NEXT = 0x24,
    ELLEN_EXTRA_WARN_LAST = 0x28,
    ELLEN_EXTRA_FIRST_BURST = 0x30,
    ELLEN_EXTRA_LAST_BURST = 0x60,
    ELLEN_EXTRA_FULL_TURN_UNITS = 256,
    ELLEN_EXTRA_FIRST_MODE = 2,
    ELLEN_EXTRA_LAST_MODE = -2,
};

void near ellen_pattern_extra(void)
{
	pid_t pid_other = (1 - pid_current);
	unsigned char angle;
	register int i;

	boss_render_frame = boss_render_frame + ELLEN_EXTRA_RENDER_STEP;

	if(boss_frame < ELLEN_EXTRA_WARN_START) {
		return;
	}
	else if(
		(boss_frame == ELLEN_EXTRA_WARN_START) ||
		(boss_frame == ELLEN_EXTRA_WARN_NEXT) ||
		(boss_frame == ELLEN_EXTRA_WARN_LAST)
	) {
		bomb_center_add(boss_center_x, boss_center_y, pid_other);
		return;
	}

	else if(boss_frame == ELLEN_EXTRA_FIRST_BURST) {
		// Each independent original radial burst draws its own RNG angle,
		// divides 256 by the byte count at each native iteration, then
		// updates the byte angle AFTER the far Extra Attack spawn.
		i = 0;
		angle = randring_far_next16();
		while(i < ellen_extra_count) {
			ellen_extra_add(
				boss_center_x,
				boss_center_y,
				angle,
				ELLEN_EXTRA_FIRST_MODE
			);
			++i;
			angle = angle + (ELLEN_EXTRA_FULL_TURN_UNITS / ellen_extra_count);
		}
		return;
	}

	// Byte-valued 0xFE is a signed -2 offset in this final volley.
	else if(boss_frame == ELLEN_EXTRA_LAST_BURST) {
		i = 0;
		angle = randring_far_next16();
		while(i < ellen_extra_count) {
			ellen_extra_add(
				boss_center_x,
				boss_center_y,
				angle,
				ELLEN_EXTRA_LAST_MODE
			);
			++i;
			angle = angle + (ELLEN_EXTRA_FULL_TURN_UNITS / ellen_extra_count);
		}
		boss_mode = ELLEN_MODE_SELECT;
		boss_frame = 0;
	}
}

// These three independent sprite strips share one original signed
// nine-entry table cycle but have three separate physical call sites.
enum ellen_native_renderer_timing_t {
    ELLEN_STRIP_TABLE_ENTRIES = 9,
    ELLEN_STRIP_WRAP_LAST = ELLEN_STRIP_TABLE_ENTRIES - 1,
    ELLEN_STRIP_ANIM_PERIOD = 4,
    ELLEN_INTRO_FLICKER_END = 0x40,
    ELLEN_INTRO_FINISH_FRAME = 0x64,
    ELLEN_INTRO_RADIUS_START = 0xC8,
    ELLEN_INTRO_RADIAL_FAMILIES = 4,
    ELLEN_INTRO_ARC_SPRITES = 8,
    ELLEN_INTRO_ARC_ANGLE_STEP = 0x20,
    ELLEN_INTRO_GROUP_ANGLE_STEP = 3,
    ELLEN_PELLET_FINISH_FRAME = 0x60,
    ELLEN_PELLET_ANGLE_STEP = 0x10,
    ELLEN_COLLISION_TILE_WIDTH = 40,
    ELLEN_COLLISION_TILE_HEIGHT = 48,
    ELLEN_COLLISION_HALF_RADIUS = TO_SP(24),
    ELLEN_RENDER_STRIP_WIDTH = 96,
    ELLEN_RENDER_MAIN_WIDTH = 64,
    ELLEN_RENDER_MAIN_HEIGHT = 48,
    ELLEN_RENDER_MAIN_LEFT = 32,
    ELLEN_RENDER_MAIN_TOP = 32,
    ELLEN_RENDER_INTRO_WIDTH = 32,
    ELLEN_RENDER_INTRO_HEIGHT = 16,
};

void near ellen_pattern_pellets(void)
{
	boss_move_sine();

	if((boss_frame % ellen_pellet_interval) == 1) {
		snd_se_play(ELLEN_SOUND_PELLET);
		bullet_template.group = BG_4_SPREAD_NARROW;
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.angle = ellen_pellet_angle;
		bullet_template.speed.v = ellen_pellet_speed;
		bullet_template.type = BT_PELLET;
		bullet_template.pid = (1 - pid_current);
		bullets_add();

		bullet_template.angle = (ellen_pellet_angle + ELLEN_PELLET_OPPOSITE_ANGLE);
		bullets_add();

		bullet_template.speed.v = (ellen_pellet_speed / 2);
		bullets_add();

		bullet_template.angle = ellen_pellet_angle;
		bullets_add();

		// Natural assignment with named +0x10 keeps the original
		// mutable byte-angle codegen (af893l).
		ellen_pellet_angle = ellen_pellet_angle + ELLEN_PELLET_ANGLE_STEP;
	}

	if(boss_frame >= ELLEN_PELLET_FINISH_FRAME) {
		boss_mode = ELLEN_MODE_SELECT;
		boss_frame = 0;
	}
}

void far gba_boss_update_ellen(void)
{
	pid_t pid_other;

	if(boss_update_start()) {
		ellen_bullet_speed = ((gba_boss_level * ELLEN_BULLET_SPEED_SCALE) + ELLEN_BULLET_SPEED_BASE);
		ellen_extra_count = ((gba_boss_level / ELLEN_EXTRA_COUNT_DIVISOR) + ELLEN_EXTRA_COUNT_BASE);
		ellen_pellet_speed = (gba_boss_level + ELLEN_PELLET_SPEED_BASE);
		ellen_pellet_interval = (ELLEN_PELLET_INTERVAL_BASE - (gba_boss_level / ELLEN_PELLET_INTERVAL_DIVISOR));
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	boss_target_update();
	boss_render_frame++;
	++boss_frame;

	switch(boss_mode) {
	case ELLEN_MODE_INTRO:
		if(boss_frame != ELLEN_INTRO_FINISH_FRAME) {
			return;
		}
		boss_frame = 0;
		boss_mode = ELLEN_MODE_SELECT;
		break;

	case ELLEN_MODE_SELECT:
		boss_pattern_next();
		break;

	case ELLEN_MODE_SPREAD_0:
	case ELLEN_MODE_SPREAD_1:
	case ELLEN_MODE_SPREAD_2:
	case ELLEN_MODE_SPREAD_3:
		ellen_pattern_spread();
		break;

	case ELLEN_MODE_EXTRA_0:
	case ELLEN_MODE_EXTRA_1:
	case ELLEN_MODE_EXTRA_2:
	case ELLEN_MODE_EXTRA_3:
	case ELLEN_MODE_EXTRA_4:
		ellen_pattern_extra();
		break;

	case ELLEN_MODE_PELLETS_0:
	case ELLEN_MODE_PELLETS_1:
	case ELLEN_MODE_PELLETS_2:
	case ELLEN_MODE_PELLETS_3:
	case ELLEN_MODE_PELLETS_4:
	case ELLEN_MODE_PELLETS_5:
	case ELLEN_MODE_PELLETS_6:
		ellen_pattern_pellets();
		break;

	case ELLEN_MODE_DESCEND:
		boss_fall();
		break;

	case ELLEN_MODE_EXPLODE:
		return;
	}

	collmap_center.x.v = boss_center_x;
	collmap_center.y.v = boss_center_y;
	collmap_stripe_tile_w.set(ELLEN_COLLISION_TILE_WIDTH);
	collmap_tile_h.set(ELLEN_COLLISION_TILE_HEIGHT);
	collmap_pid = pid_other;
	collmap_set_rect_striped();

	hitbox_hittest_skip_explosions = true;
	hitbox.radius.x.v = ELLEN_COLLISION_HALF_RADIUS;
	hitbox.radius.y.v = ELLEN_COLLISION_HALF_RADIUS;
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
		(ellen_render_y_offsets[i] * ELLEN_RENDER_STRIP_Y_SCALE) +
		boss_sprite_offset +
		ELLEN_RENDER_STRIP_BASE
	);
	sprite16_put_size.w = ELLEN_RENDER_STRIP_WIDTH;
	sprite16_put_size.h = (ellen_render_heights[i] / ELLEN_STRIP_HEIGHT_DIVISOR);

	left = (
		playfield_fg_x_to_screen(
			boss_center_x,
			(1 - pid_current)
		) - ELLEN_RENDER_STRIP_LEFT
	);
	top = (
		(boss_center_y >> 4) +
		ellen_render_y_offsets[i] -
		ELLEN_RENDER_STRIP_TOP
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

	sprite16_put_size.w = ELLEN_RENDER_MAIN_WIDTH;
	sprite16_put_size.h = ELLEN_RENDER_MAIN_HEIGHT;
	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - ELLEN_RENDER_MAIN_LEFT);
	top = ((boss_center_y >> 4) - ELLEN_RENDER_MAIN_TOP);

	sprite_offset = boss_sprite_offset;
	if(boss_hit) {
		sprite_offset += ELLEN_RENDER_HIT_SPRITE_OFF;
	}
	sprite16_put(left, top, sprite_offset);

	i = ((boss_render_frame / ELLEN_STRIP_ANIM_PERIOD) % ELLEN_STRIP_TABLE_ENTRIES);
	ellen_render_strip(i);
	--i;
	if(i < 0) {
		i = ELLEN_STRIP_WRAP_LAST;
	}
	ellen_render_strip(i);
	--i;
	if(i < 0) {
		i = ELLEN_STRIP_WRAP_LAST;
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

	i = (frame % ELLEN_STRIP_TABLE_ENTRIES);
	ellen_render_strip(i);
	--i;
	if(i < 0) {
		i = ELLEN_STRIP_WRAP_LAST;
	}
	ellen_render_strip(i);
	--i;
	if(i < 0) {
		i = ELLEN_STRIP_WRAP_LAST;
	}
	ellen_render_strip(i);

	if(round_frame_mod2 && (boss_frame < ELLEN_INTRO_FLICKER_END)) {
		return;
	}

	sprite16_put_size.w = ELLEN_RENDER_INTRO_WIDTH;
	sprite16_put_size.h = ELLEN_RENDER_INTRO_HEIGHT;
	sprite_offset = (pid.so_attack + ELLEN_RENDER_INTRO_SPRITE_OFF);

	// Four families of eight genuine sprites. Two nested natural
	// while loops keep both byte-angle steps and sprite-offset updates
	// in the original post-render order (native af893c).
	i = 0;
	while(i < ELLEN_INTRO_RADIAL_FAMILIES) {
		j = 0;
		while(j < ELLEN_INTRO_ARC_SPRITES) {
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
				playfield_fg_x_to_screen(left, pid_other) - ELLEN_RENDER_INTRO_HALF
			);
			// TC4 naturally emits the original signed AX shift with a
			// separate C++ assignment to top. Inlining this into
			// sprite16_put changes the whole BOSS CODE (af760b).
			top = static_cast<screen_y_t>(top >> 4);
			sprite16_put(left, top, sprite_offset);
			// Enum-valued `+=` changed code; ordinary byte assignment
			// with named +0x20 restores original TC4 instructions (af893j).
			angle = angle + ELLEN_INTRO_ARC_ANGLE_STEP;
			++j;
		}
		// The next family's +3 byte angle has the same native-exact
		// C++ assignment pattern (af893i), without changing wraparound.
		angle = angle + ELLEN_INTRO_GROUP_ANGLE_STEP;
		sprite_offset -= 4;
		++i;
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

	if(boss_mode == ELLEN_MODE_INTRO) {
		ellen_render_intro(
			TO_SP(ELLEN_INTRO_RADIUS_START - (boss_frame * 2)),
			(unsigned char)boss_frame,
			(unsigned char)(boss_frame * 3)
		);
		return;
	}
	if(boss_mode != ELLEN_MODE_EXPLODE) {
		ellen_render_main();
		return;
	}
	boss_explosion_render();
}
