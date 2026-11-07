// Maintained exact natural Turbo C++ reconstruction of Ellen's contribution
// to TH03 MAIN_05_TEXT. Historical private state remains at frozen carrier
// offsets and is bound through semantic extern names by the accepted manifest.
#pragma codeseg MAIN_05_TEXT

#include <stddef.h>
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

// Physical Ellen Bomb particle slots: 8 per player and 8 bytes each.
// The original native CODE producer refers to an external 132-byte carrier.
enum ellen_bomb_layout_t {
    ELLEN_BOMB_PARTICLES_PER_PLAYER = 8,
    ELLEN_BOMB_SPAWN_X = 19999,
    ELLEN_BOMB_RESPAWN_X = 9999,
    ELLEN_BOMB_FLASH_END = 64,
    ELLEN_BOMB_SHAKE_END = 128,
    ELLEN_BOMB_EXPLOSION_PERIOD = 4,
};

struct ellen_bomb_particle_t {
	SPPoint center;
	SPPoint velocity;
};

typedef char ellen_bomb_particle_stride_is_8[
    (sizeof(ellen_bomb_particle_t) == 8) ? 1 : -1
];
typedef char ellen_bomb_particle_velocity_at_4[
    (offsetof(ellen_bomb_particle_t, velocity) == 4) ? 1 : -1
];

// The target places these three private objects consecutively at DGROUP
// 25DC, 25DE..265D, and 265E. Object-level probes keep them local; aggregate
// reconstruction binds the same semantic names to the frozen carrier storage.
#ifdef TH03_BOMB_EXTERNAL_STORAGE
extern int ellen_bomb_particle_spawn_count;
extern ellen_bomb_particle_t ellen_bomb_particles[PLAYER_COUNT][ELLEN_BOMB_PARTICLES_PER_PLAYER];
extern ellen_bomb_particle_t near *ellen_bomb_particle_p;
#else
static int ellen_bomb_particle_spawn_count;
static ellen_bomb_particle_t ellen_bomb_particles[PLAYER_COUNT][ELLEN_BOMB_PARTICLES_PER_PLAYER];
static ellen_bomb_particle_t near *ellen_bomb_particle_p;
#endif
typedef char ellen_bomb_physical_pool_is_128[
    (sizeof(ellen_bomb_particles) == 128) ? 1 : -1
];

// Semantic names for three still-unreconstructed helpers. The current
// monolithic scaffold labels the corresponding entries sub_B39E, sub_CDBD,
// and sub_A3A8 respectively.
extern "C" void far bomb_bg_fill(void);
extern "C" void far pascal bomb_explosion_add(int x, int y, int pid);
extern "C" void far pascal palette_restore_for_pid(pid_t pid);

void far ellen_bomb_update(void)
{
	int i;

	if(bomb_flag[pid_current] == BF_INACTIVE) {
		return;
	}
	if(bomb_flag[pid_current] == BF_PREPARING) {
		bomb_flag[pid_current] = BF_ACTIVE;
		bomb_frame[pid_current] = 0;
		for(i = 0; i < ELLEN_BOMB_PARTICLES_PER_PLAYER; i++) {
			ellen_bomb_particles[pid_current][i].center.x.v = ELLEN_BOMB_SPAWN_X;
		}
		snd_se_play(17);
	}

	bomb_frame[pid_current]++;
	playfield_clip_negative_radius.x.v = TO_SP(-32);
	playfield_clip_negative_radius.y.v = TO_SP(-32);
	ellen_bomb_particle_p = &ellen_bomb_particles[pid_current][0];

	for(
        i = 0;
        i < ELLEN_BOMB_PARTICLES_PER_PLAYER;
        (i++, ellen_bomb_particle_p++)
    ) {
		// The original goto to the common respawn block is codegen-visible:
		// a falling-through C++ branch changed native CODE.
		if(ellen_bomb_particle_p->center.x.v == ELLEN_BOMB_RESPAWN_X) {
			goto respawn;
		}
		if(ellen_bomb_particle_p->center.x.v == ELLEN_BOMB_SPAWN_X) {
			continue;
		}
		ellen_bomb_particle_p->center.x.v += ellen_bomb_particle_p->velocity.x.v;
		ellen_bomb_particle_p->center.y.v += ellen_bomb_particle_p->velocity.y.v;
		if(!playfield_clip(ellen_bomb_particle_p->center.x, ellen_bomb_particle_p->center.y)) {
			continue;
		}

	respawn:
		ellen_bomb_particle_p->center.x.v = TO_SP(144);
		ellen_bomb_particle_p->center.y.v = TO_SP(184);
		vector2(
			ellen_bomb_particle_p->velocity.x.v,
			ellen_bomb_particle_p->velocity.y.v,
			randring_far_next16(),
			224
		);
	}

	if(bomb_frame[pid_current] >= BOMB_FRAMES) {
		bomb_flag[pid_current] = BF_INACTIVE;
		palette_restore_for_pid(pid_current);
	}
}

void near ellen_bomb_render(void)
{
	ellen_bomb_particle_p = &ellen_bomb_particles[pid_current][0];
	sprite16_put_size.set(64, 64);
	sprite16_clip_set_for_pid(pid_current);

	screen_x_t left;
	screen_y_t top;
	sprite16_offset_t sprite_offset = (pid.so_attack + 0x29C);

	for(
        int i = 0;
        i < ELLEN_BOMB_PARTICLES_PER_PLAYER;
        (i++, ellen_bomb_particle_p++)
    ) {
		// Keeping these as two source-level conditions is material: TC4J
		// reloads [ellen_bomb_particle_p] for the second comparison, as in the target.
		if(ellen_bomb_particle_p->center.x.v == ELLEN_BOMB_SPAWN_X) {
			continue;
		}
		if(ellen_bomb_particle_p->center.x.v == ELLEN_BOMB_RESPAWN_X) {
			continue;
		}
		left = (
			playfield_fg_x_to_screen(ellen_bomb_particle_p->center.x.v, pid_current) - 32
		);
		top = (ellen_bomb_particle_p->center.y.to_pixel() - 16);
		sprite16_put(left, top, sprite_offset);
	}
}

void far ellen_bomb(void)
{
	int fg_shift;
	unsigned char frame;
	unsigned char color;

	if(bomb_flag[pid_current] == BF_INACTIVE) {
		return;
	}
	egc_off();
	frame = bomb_frame[pid_current];

	if(frame < ELLEN_BOMB_FLASH_END) {
		grcg_setcolor(GC_RMW, pid_current);
		_BX = 0x3932;
		if(pid_current != 0) {
			_BX += 40;
		}
		bomb_bg_fill();
		grcg_off();

		color = (frame * 2);
		Palettes[pid_current].c.r = (color * 2);
		Palettes[pid_current].c.g = color;
		Palettes[pid_current].c.b = color;
		palette_changed = true;
		ellen_bomb_particle_spawn_count = 0;
	} else if(frame < ELLEN_BOMB_SHAKE_END) {
		if((static_cast<unsigned int>(frame) % 2) != 0) {
			snd_se_play(10);
			Palettes[pid_current].c.r = 255;
			Palettes[pid_current].c.g = 128;
			Palettes[pid_current].c.b = 128;
		} else {
			Palettes[pid_current].c.r = 0;
			Palettes[pid_current].c.g = 0;
			Palettes[pid_current].c.b = 32;
		}
		palette_changed = true;

		if((frame & 3) < 2) {
			playfield_fg_shift_x[pid_current] = 4;
		} else {
			playfield_fg_shift_x[pid_current] = -4;
		}

		int left = PLAYFIELD_LEFT;
		if(pid_current != 0) {
			left += PLAYFIELD_W_BORDERED;
		}
		mrs_put_noalpha_8(
			left,
			PLAYFIELD_TOP,
			(pid_current + 2),
			// This preserves the target's integer promotion sequence
			// (MOV AL / MOV AH,0 / PUSH AX) without creating a stack local.
			(_AX = pid_current)
		);

		if((frame % ELLEN_BOMB_EXPLOSION_PERIOD) == 0) {
			bomb_explosion_add(TO_SP(144), TO_SP(184), pid_current);
			if(ellen_bomb_particle_spawn_count < ELLEN_BOMB_PARTICLES_PER_PLAYER) {
				ellen_bomb_particles[pid_current][ellen_bomb_particle_spawn_count].center.x.v = ELLEN_BOMB_RESPAWN_X;
				ellen_bomb_particle_spawn_count++;
			}
		}
	} else {
		playfield_fg_shift_x[pid_current] = 0;
		color = (255 - (frame << 3));
		Palettes[pid_current].c.r = ((color * 2) & 0xFF);
		Palettes[pid_current].c.g = color;
		Palettes[pid_current].c.b = color;
		palette_changed = true;
	}
	egc_on();

	if((frame >= ELLEN_BOMB_FLASH_END) && (frame < ELLEN_BOMB_SHAKE_END)) {
		fg_shift = playfield_fg_shift_x[pid_current];
		playfield_fg_shift_x[pid_current] = 0;
		ellen_bomb_render();
		playfield_fg_shift_x[pid_current] = fg_shift;
	}
}
