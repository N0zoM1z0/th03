// Maintained exact natural Turbo C++ reconstruction of TH03 MAIN_10_TEXT.
#pragma codeseg MAIN_10_TEXT

#include "src/main/player/chargeshot_kotohime.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/enemy/efe.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"

struct kotohime_chargeshot_t {
	unsigned char active;
	unsigned char anim;
	PlayfieldPoint center;
	int velocity_y;
};

struct gauge_pattern_timing_t {
	unsigned char total_frames;
	unsigned char byte_1;
	unsigned char byte_2;
	unsigned char byte_3;
};

extern unsigned char kotohime_gauge_frame[PLAYER_COUNT];
extern kotohime_chargeshot_t kotohime_chargeshots[PLAYER_COUNT];
extern kotohime_chargeshot_t near *kotohime_chargeshot_p;
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];

extern "C" void far pascal kotohime_extra_add(int x, int y);
extern "C" void far pascal palette_restore_for_pid(pid_t pid);

void far chargeshots_reset_kotohime(void)
{
	kotohime_chargeshots[0].active = 0;
	kotohime_chargeshots[1].active = 0;
}

void far pascal chargeshot_add_kotohime(Subpixel center_x, Subpixel center_y)
{
	kotohime_chargeshot_p = &kotohime_chargeshots[pid.current];
	kotohime_chargeshot_p->active = 1;
	kotohime_chargeshot_p->anim = 0;
	kotohime_chargeshot_p->center.x = center_x;
	kotohime_chargeshot_p->center.y = center_y;
	kotohime_chargeshot_p->velocity_y = -16;
	snd_se_play(6);
}

void far pascal chargeshot_update_kotohime(void)
{
	kotohime_chargeshot_p = &kotohime_chargeshots[pid_current];
	if(kotohime_chargeshot_p->active == 0) {
		return;
	}
	players[pid_current].gauge_charged = 0;
	kotohime_chargeshot_p->center.y.v += kotohime_chargeshot_p->velocity_y;
	if(kotohime_chargeshot_p->center.y.v <= TO_SP(-16)) {
		kotohime_chargeshot_p->active = 0;
		return;
	}
	kotohime_chargeshot_p->velocity_y -= 2;
}

void near kotohime_chargeshot_private(void)
{
	// TC4 allocates these locals in declaration order from BP-2 downward.
	// The target layout is left=-2, top=-4, sprite_offset=-6.
	screen_x_t left;
	screen_y_t top;
	sprite16_offset_t sprite_offset;

	sprite_offset = (pid.so_attack + 0x1188);
	left = (
		playfield_fg_x_to_screen(kotohime_chargeshot_p->center.x.v, pid_current) - 48
	);
	top = (kotohime_chargeshot_p->center.y.to_pixel() + 8);
	sprite16_put(left, top, sprite_offset);
}

uint8_t far chargeshot_hittest_kotohime(void)
{
	kotohime_chargeshot_p = &kotohime_chargeshots[hitbox.pid];
	if(kotohime_chargeshot_p->active != 0) {
		_BX = (unsigned int)kotohime_chargeshot_p;
		#define p (*(kotohime_chargeshot_t near *)_BX)
		if(
			((p.center.x.v - hitbox.right.v) <= TO_SP(40)) &&
			((hitbox.origin.topleft.x.v - p.center.x.v) <= TO_SP(40)) &&
			(p.center.y.v >= hitbox.origin.topleft.y.v) &&
			(p.center.y.v <= hitbox.bottom.v)
		) {
			ef_onehit = true;
			hitcircles_enemy_add(
				(hitbox.origin.topleft.x.v + hitbox.radius.x.v),
				p.center.y.v,
				hitbox.pid
			);
			#undef p
			return 3;
		}
		#undef p
	}
	return 0;
}

void far pascal chargeshot_render_kotohime(void)
{
	kotohime_chargeshot_p = &kotohime_chargeshots[pid_current];
	if(kotohime_chargeshot_p->active == 0) {
		return;
	}
	sprite16_put_size.set(96, 32);
	sprite16_clip_set_for_pid(pid_current);
	kotohime_chargeshot_private();
}

void near pascal gauge_pattern_kotohime(bullet_type_t type)
{
	unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
	if(type == BT_BULLET16_DEFAULT) {
		flag_expected = (flag_expected + GBAF_PELLET_TO_BULLET);
	}

	if(gba_flag_active[pid_current] == flag_expected) {
		kotohime_gauge_frame[pid_current] = 0;
		gba_flag_active[pid_current]++;
		gauge_pattern_timing[pid_current].total_frames = (
			(gba_gauge_level[pid_current] / 2) + 4
		);
		gauge_pattern_timing[pid_current].byte_1 = randring_far_next16_and(1);
		gauge_pattern_timing[pid_current].byte_2 = type;
		return;
	}

	if(gba_flag_active[pid_current] != (flag_expected + 1)) {
		return;
	}

	if(kotohime_gauge_frame[pid_current] == 0) {
		kotohime_extra_add(
			(randring_far_next16_mod(0xA00) + 0x400),
			0
		);
	} else if(kotohime_gauge_frame[pid_current] >= 0x80) {
		gba_flag_active[pid_current] = GBAF_NONE;
		palette_restore_for_pid(1 - pid_current);
	}
	kotohime_gauge_frame[pid_current]++;
}

void far gba_gauge_pattern_pellet_kotohime(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_kotohime(BT_PELLET);
	}
}

void far gba_gauge_pattern_bullet_kotohime(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_kotohime(BT_BULLET16_DEFAULT);
	}
}
