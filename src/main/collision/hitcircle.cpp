#include "compat/rec98/libs/sprite16/sprite16.h"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "src/main/collision/hitcircle.hpp"
#include "compat/rec98/th03/main/v_colors.hpp"
#include "compat/rec98/th03/sprites/main_s16.hpp"

enum hitcircle_layout_t {
	HITCIRCLE_W = 48,
	HITCIRCLE_H = 48,
	HITCIRCLE_VRAM_W = (HITCIRCLE_W / BYTE_DOTS),
	HITCIRCLE_VRAM_W_PER_CEL_TERM = (HITCIRCLE_VRAM_W / 3),
	HITCIRCLE_CELS = 4,
	HITCIRCLE_FRAMES_PER_CEL = 4,
	HITCIRCLE_FRAMES = (HITCIRCLE_FRAMES_PER_CEL * HITCIRCLE_CELS),
};

// ZUN quirk: Should *maybe* be [PLAYER_COUNT]? If both players get hit within
// [HITCIRCLE_FRAMES], the earlier animation is cut off. It's too obvious of an
// oversight to classify it as a bug, though. The sudden stop of the animation
// could also be supposed to telegraph that the other player got hit, without
// having to peek over to the other playfield.
enum hitcircle_capacity_t {
	HITCIRCLE_ENEMY_COUNT = 12,
	HITCIRCLE_PLAYER_COUNT = 1,
	HITCIRCLE_COUNT = (HITCIRCLE_ENEMY_COUNT + HITCIRCLE_PLAYER_COUNT),
};


struct HitCircle {
	uint8_t age; // Alive if ≥1.
	pid_t pid;
	screen_point_t topleft;

	void spawn(const pid2& pid_) {
		age = 1;
		pid = pid_;
	}

	sprite16_offset_t cel(void) const {
		// ZUN bloat: (SO_HITCIRCLE + (
		// 	((age - 1) / HITCIRCLE_FRAMES_PER_CEL) * HITCIRCLE_VRAM_W)
		// ). 1 SHR, 1 IMUL. This compiles to both those *and* a bunch of MOVs
		// and ADDs in between...
		static_assert(HITCIRCLE_VRAM_W == 6);
		_BX = (age - 1);
		_BX = (_BX / HITCIRCLE_FRAMES_PER_CEL);
		_BX *= HITCIRCLE_VRAM_W_PER_CEL_TERM;
		return (SO_HITCIRCLE + _BX + _BX + _BX);
	}
};

extern HitCircle hitcircles[HITCIRCLE_COUNT];

void pascal hitcircles_enemy_add(
	subpixel_t center_x, subpixel_t center_y, pid2 pid
)
{
	#define last_id hitcircles_enemy_last_id
	extern uint8_t last_id;
	// This byte ring index must stay postfix: prefix changed actual
	// original TC4 CODE in the independent af919c negative trial.
	last_id++;
	if(HITCIRCLE_ENEMY_COUNT <= last_id) {
		last_id = 0;
	}

	HitCircle near& p = hitcircles[last_id];
	p.spawn(pid);

	if(!hitcircles_enemy_add_do_not_randomly_center_within_hitbox) {
		center_x = (
			hitbox.origin.topleft.x.v +
			randring_far_next16_mod(hitbox.radius.x * 2)
		);
		center_y = (
			hitbox.origin.topleft.y.v +
			randring_far_next16_mod(hitbox.radius.y * 2)
		);
	}
	// Keep the original near-record stores directly at each spawn site.
	p.topleft.x = (
		playfield_fg_x_to_screen(center_x, pid) - (HITCIRCLE_W / 2)
	);
	p.topleft.y = (TO_PIXEL(center_y) + PLAYFIELD_TOP - (HITCIRCLE_H / 2));

	#undef last_id
}

void pascal hitcircles_player_add(
	subpixel_t center_x, subpixel_t center_y, pid2 pid
)
{
	HitCircle near& p = hitcircles[HITCIRCLE_ENEMY_COUNT];
	p.spawn(pid);
	// Keep the original near-record stores directly at each spawn site.
	p.topleft.x = (
		playfield_fg_x_to_screen(center_x, pid) - (HITCIRCLE_W / 2)
	);
	p.topleft.y = (TO_PIXEL(center_y) + PLAYFIELD_TOP - (HITCIRCLE_H / 2));
}

void near hitcircles_update(void)
{
	register HitCircle near* p = hitcircles;
	register int i;
	// The thirteen-record age walk keeps its signed index and near-pointer
	// increments together in the for header after each byte-state update.
	for(i = 0; i < HITCIRCLE_COUNT; (++i, ++p)) {
		if(p->age) {
			p->age++;
			if(HITCIRCLE_FRAMES < p->age) {
				p->age = 0;
			}
		}
	}
}

void near hitcircles_render(void)
{
	register const HitCircle near* p = hitcircles;

	sprite16_mono_(true);

	// ZUN bloat
	_DX = round_or_result_frame;
	// Original 81 E2 01 00 (AND DX,imm16) is four CODE bytes.
	// Natural _DX &= 1 again selected the nonoriginal shorter imm8
	// instruction (fresh af919f), not the original imm16 AND.
	asm { and dx, 1 };
	_DX += V_YELLOW_DARK;
	sprite16_mono_color(_DX);

	sprite16_put_size.set(HITCIRCLE_W, HITCIRCLE_H);

	register int i;
	// Only twelve enemy slots draw in this pass. The thirteenth player
	// hit circle uses its own monochrome palette after the signed-index
	// and near-pointer for loop.
	for(i = 0; i < HITCIRCLE_ENEMY_COUNT; (++i, ++p)) {
		if(p->age) {
			sprite16_clip_set_for_pid(p->pid);
			sprite16_offset_t so = p->cel();
			sprite16_put(p->topleft.x, p->topleft.y, so);
		}
	}

	// Player circle
	static_assert(HITCIRCLE_PLAYER_COUNT == 1);
	_DX = V_WHITE;
	sprite16_mono_color(_DX);
	if(p->age) {
		sprite16_clip_set_for_pid(p->pid);
		sprite16_offset_t so = p->cel();
		sprite16_put(p->topleft.x, p->topleft.y, so);
	}

	asm { xor dx, dx; }
	_AH = SPRITE16_SET_MONO;
	geninterrupt(SPRITE16);
}
