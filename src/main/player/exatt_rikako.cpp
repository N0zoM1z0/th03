// Complete current native-source Turbo C++ reconstruction of Rikako's
// physical Extra Attack in TH03 MAIN_06_TEXT, with original DGROUP state.
#pragma codeseg MAIN_06_TEXT

#include "src/main/player/exatt_rikako.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"

#pragma option -a2

// Shared 32-byte entity view with the original per-Rikako homing flag.
#include "src/main/player/exatt_entity.hpp"

struct exatt_player_view_t {
	PlayfieldPoint center;
	unsigned char rest[124];
};
extern exatt_player_view_t players[PLAYER_COUNT];

extern exatt_entity_t exatt_entities[PLAYER_COUNT][16];
extern exatt_entity_t near *exatt_entity_p;

extern "C" unsigned char near cdecl exatt_fly_update(void);
extern "C" void near pascal exatt_fly_init(
	int x,
	int y,
	int target_x,
	int target_y,
	unsigned char pid,
	int speed
);
extern "C" void near pascal exatt_render_state2(
	screen_x_t left,
	screen_y_t top,
	unsigned char frame
);
extern "C" void near pascal exatt_render_state_other(
	screen_x_t left,
	screen_y_t top,
	unsigned char frame
);
extern "C" void near pascal exatt_collmap_set(int x, int y);

// Rikako's Extra Attack uses 14 slots per player, of which its normal
// spawner scans the first 8. The +0x17 character-specific mode is the
// original homing-disable bit, and the 0x40..0x50 frame range is the
// only span during which motion can adjust the aimed direction.
enum rikako_exatt_limits_t {
    RIKAKO_EXATT_NORMAL_SLOTS = 8,
    RIKAKO_EXATT_ALL_SLOTS = 14,
    RIKAKO_EXATT_HOMING_START = 0x40,
    RIKAKO_EXATT_HOMING_END = 0x50,
    RIKAKO_EXATT_FLYING_STATE = 2,
    RIKAKO_EXATT_APPEARING_END = 0x1C,
    RIKAKO_EXATT_FREE = 0,
    RIKAKO_EXATT_ACTIVE = 1,
    RIKAKO_EXATT_TARGET_X_RANGE = 0x1200,
    RIKAKO_EXATT_TARGET_Y = 0x100,
    RIKAKO_EXATT_INITIAL_FLY_SPEED = 0x64,
    RIKAKO_EXATT_START_ANGLE = 0x40,
    RIKAKO_EXATT_SPEED_BASE = 0x20,
    RIKAKO_EXATT_HIT_RADIUS = TO_SP(16),
    RIKAKO_EXATT_CLIP_RADIUS = TO_SP(32),
    RIKAKO_EXATT_SPRITE_SIZE = 48,
    RIKAKO_EXATT_SPRITE_OFFSET = 0x780,
};

void far pascal exatt_add_rikako(int x, int y, unsigned char pid_)
{
	register exatt_entity_t near *p = &exatt_entities[pid_][0];
	register int i = 0;

	// Normal spawn scans eight slots; the special spawn below scans
	// fourteen. Preserve the original per-slot RNG/return ordering.
	for(; i < RIKAKO_EXATT_NORMAL_SLOTS; ++i, ++p) {
		if(!p->state) {
			exatt_entity_p = p;
			exatt_fly_init(
				x,
				y,
				randring_far_next16_mod(RIKAKO_EXATT_TARGET_X_RANGE),
				RIKAKO_EXATT_TARGET_Y,
				pid_,
				RIKAKO_EXATT_INITIAL_FLY_SPEED
			);
			p->character.rikako.homing_disabled = randring_far_next16_and(1);
			p->angle = RIKAKO_EXATT_START_ANGLE;
			p->speed = (randring_far_next16_and(0x0F) + RIKAKO_EXATT_SPEED_BASE);
			return;
		}
	}
}

void far pascal rikako_extra_add(int x, int y, unsigned char angle_)
{
	register exatt_entity_t near *p = &exatt_entities[pid_current][0];
	int i = 0;

	for(; i < RIKAKO_EXATT_ALL_SLOTS; ++i, ++p) {
		if(!p->state) {
			p->state = RIKAKO_EXATT_ACTIVE;
			p->character.rikako.homing_disabled = 1;
			p->frame = RIKAKO_EXATT_HOMING_START;
			p->x = x;
			p->y = y;
			p->angle = angle_;
			p->speed = RIKAKO_EXATT_SPEED_BASE;
			p->pid = (1 - pid_current);
			return;
		}
	}
}

void near rikako_exatt_render_one(void)
{
	screen_x_t left;
	screen_y_t top;
	unsigned char frame;
	register exatt_entity_t near *p = exatt_entity_p;
	register sprite16_offset_t sprite_offset;

	sprite16_put_size.set(RIKAKO_EXATT_SPRITE_SIZE, RIKAKO_EXATT_SPRITE_SIZE);
	left = playfield_fg_x_to_screen(p->x, p->pid);
	top = ((p->y >> 4) + 0x10);

	if(pid_current) {
		sprite16_clip.set_for_pid_0();
	} else {
		sprite16_clip.set_for_pid_1();
	}

	frame = p->frame;
	if(p->state == RIKAKO_EXATT_ACTIVE) {
		sprite_offset = (pid.so_attack + RIKAKO_EXATT_SPRITE_OFFSET);
		if(frame & 1) {
			sprite_offset += RIKAKO_EXATT_SPRITE_OFFSET;
		}
		sprite16_put((left - 24), (top - 24), sprite_offset);
		return;
	}

	if(p->state == RIKAKO_EXATT_FLYING_STATE) {
		exatt_render_state2(left, top, frame);
	} else {
		exatt_render_state_other(left, top, frame);
	}
}

void far pascal exatt_update_rikako(void)
{
	int vector_x;
	int vector_y;
	unsigned char pid_other;
	unsigned char target_angle;
	signed char angle_delta;
	register exatt_entity_t near *p = &exatt_entities[pid_current][0];

	pid_other = (1 - pid_current);
	playfield_clip_negative_radius.x.v = -RIKAKO_EXATT_CLIP_RADIUS;
	playfield_clip_negative_radius.y.v = -RIKAKO_EXATT_CLIP_RADIUS;
	hitbox_hittest_skip_explosions = true;
	hitbox.radius.x.v = RIKAKO_EXATT_HIT_RADIUS;
	hitbox.radius.y.v = RIKAKO_EXATT_HIT_RADIUS;
	hitbox.pid = pid_other;

	// Both early continue paths join the signed-index and near-pointer
	// progression at the same natural for-header boundary.
	for(register int i = 0; i < RIKAKO_EXATT_ALL_SLOTS; ++i, ++p) {
		if(!p->state) {
			continue;
		}

		if(p->state == RIKAKO_EXATT_ACTIVE) {
			vector2(vector_x, vector_y, p->angle, p->speed);
			p->x += vector_x;
			p->y += vector_y;

			if(
				(!p->character.rikako.homing_disabled) &&
				(p->frame >= RIKAKO_EXATT_HOMING_START) &&
				(p->frame <= RIKAKO_EXATT_HOMING_END)
			) {
				target_angle = iatan2(
					(players[pid_other].center.y.v - p->y),
					(players[pid_other].center.x.v - p->x)
				);
				// Original byte-memory postfix is codegen-visible. A fresh
				// native TC4 trial af874f independently rejects ++p->speed.
                p->speed++;
				angle_delta = (target_angle - p->angle);
				// Keep the literal 8 here. Replacing it with an enum of
				// equal value changes TC4's 16-bit signed-division codegen.
				// Signed division truncates toward zero, unlike arithmetic
				// right shift for negative deltas (fresh af874d failed).
                angle_delta /= 8;
				p->angle += angle_delta;
			}

			if(playfield_clip(
				*(PlayfieldSubpixel near *)&p->x,
				*(PlayfieldSubpixel near *)&p->y
			)) {
				p->state = RIKAKO_EXATT_FREE;
				continue;
			}

			hitbox.origin.center.x.v = p->x;
			hitbox.origin.center.y.v = p->y;
			hitbox_hittest();
			exatt_collmap_set(p->x, p->y);
		} else if(p->state == RIKAKO_EXATT_FLYING_STATE) {
			exatt_entity_p = p;
			exatt_fly_update();
		} else if(p->state <= RIKAKO_EXATT_APPEARING_END) {
			p->state++;
		} else {
			p->frame = 0;
			p->state = RIKAKO_EXATT_ACTIVE;
		}

		p->frame++;
	}

	hitbox_hittest_skip_explosions = false;
}

void far pascal exatt_render_rikako(void)
{
	register exatt_entity_t near *p = &exatt_entities[pid_current][0];
	register int i = 0;

	// Each real render call advances original near pointer afterwards;
	// all fourteen slots are visited in this natural while.
	for(; i < RIKAKO_EXATT_ALL_SLOTS; ++i, ++p) {
		if(p->state) {
			exatt_entity_p = p;
			rikako_exatt_render_one();
		}
	}
}
