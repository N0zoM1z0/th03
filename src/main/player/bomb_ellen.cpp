// Natural Turbo C++ reconstruction candidate for the Ellen contribution to
// TH03 MAIN_05_TEXT. This file is kept out of the accepted build graph until
// its physical producer placement, private BSS placement, and final linked
// relocations are proven exact by the full-owner Oracle.

#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

struct ellen_bomb_particle_t {
	SPPoint center;
	SPPoint velocity;
};

// The target places these three private objects consecutively at DGROUP
// 25DC, 25DE..265D, and 265E. Their order is therefore significant.
static int particle_spawn_count;
static ellen_bomb_particle_t particles[PLAYER_COUNT][8];
static ellen_bomb_particle_t near *particle_p;

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
		for(i = 0; i < 8; i++) {
			particles[pid_current][i].center.x.v = 19999;
		}
		snd_se_play(17);
	}

	bomb_frame[pid_current]++;
	playfield_clip_negative_radius.x.v = TO_SP(-32);
	playfield_clip_negative_radius.y.v = TO_SP(-32);
	particle_p = &particles[pid_current][0];

	for(i = 0; i < 8; (i++, particle_p++)) {
		if(particle_p->center.x.v == 9999) {
			goto respawn;
		}
		if(particle_p->center.x.v == 19999) {
			continue;
		}
		particle_p->center.x.v += particle_p->velocity.x.v;
		particle_p->center.y.v += particle_p->velocity.y.v;
		if(!playfield_clip(particle_p->center.x, particle_p->center.y)) {
			continue;
		}

	respawn:
		particle_p->center.x.v = TO_SP(144);
		particle_p->center.y.v = TO_SP(184);
		vector2(
			particle_p->velocity.x.v,
			particle_p->velocity.y.v,
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
	particle_p = &particles[pid_current][0];
	sprite16_put_size.set(64, 64);
	sprite16_clip_set_for_pid(pid_current);

	screen_x_t left;
	screen_y_t top;
	sprite16_offset_t sprite_offset = (pid.so_attack + 0x29C);

	for(int i = 0; i < 8; (i++, particle_p++)) {
		// Keeping these as two source-level conditions is material: TC4J
		// reloads [particle_p] for the second comparison, as in the target.
		if(particle_p->center.x.v == 19999) {
			continue;
		}
		if(particle_p->center.x.v == 9999) {
			continue;
		}
		left = (
			playfield_fg_x_to_screen(particle_p->center.x.v, pid_current) - 32
		);
		top = (particle_p->center.y.to_pixel() - 16);
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

	if(frame < 64) {
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
		particle_spawn_count = 0;
	} else if(frame < 128) {
		if(frame & 1) {
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

		if((frame % 4) == 0) {
			bomb_explosion_add(TO_SP(144), TO_SP(184), pid_current);
			if(particle_spawn_count < 8) {
				particles[pid_current][particle_spawn_count].center.x.v = 9999;
				particle_spawn_count++;
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

	if((frame >= 64) && (frame < 128)) {
		fg_shift = playfield_fg_shift_x[pid_current];
		playfield_fg_shift_x[pid_current] = 0;
		ellen_bomb_render();
		playfield_fg_shift_x[pid_current] = fg_shift;
	}
}
