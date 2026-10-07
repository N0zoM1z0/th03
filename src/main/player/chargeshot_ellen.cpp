// Maintained exact natural Turbo C++ reconstruction of TH03 MAIN_08_TEXT.
#pragma codeseg MAIN_08_TEXT

#include "src/main/player/chargeshot_ellen.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"

struct ellen_chargeshot_t {
	unsigned char state;
	unsigned char phase;
	unsigned char angle;
	unsigned char length;
	PlayfieldPoint center;
	SPPoint velocity;
};

struct gauge_pattern_timing_t {
	unsigned char total_frames;
	unsigned char byte_1;
	unsigned char byte_2;
	unsigned char byte_3;
};

extern int ellen_gauge_x[PLAYER_COUNT];
extern int ellen_gauge_y[PLAYER_COUNT];
extern unsigned char ellen_gauge_frame[PLAYER_COUNT];
extern ellen_chargeshot_t ellen_chargeshots[PLAYER_COUNT][32];
extern ellen_chargeshot_t near *ellen_chargeshot_p;
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];

extern int ellen_target_x;
extern int ellen_target_y;
extern "C" void far pascal ellen_target_set(pid_t pid);
extern "C" void far pascal bomb_center_add(int x, int y, int pid);
extern "C" void far pascal palette_restore_for_pid(pid_t pid);

void far pascal chargeshots_reset_ellen(void)
{
	ellen_chargeshot_p = &ellen_chargeshots[0][0];
	for(int i = 0; i < 64; (i++, ellen_chargeshot_p++)) {
		ellen_chargeshot_p->state = 0;
	}
}

void far pascal chargeshot_add_ellen(Subpixel center_x, Subpixel center_y)
{
	ellen_chargeshot_p = &ellen_chargeshots[pid.current][0];
	for(int state = 0; state < 0x40; (state += 2, ellen_chargeshot_p++)) {
		ellen_chargeshot_p->state = state;
		ellen_chargeshot_p->phase = 0;
		ellen_chargeshot_p->center.x = center_x;
		ellen_chargeshot_p->center.y = center_y;
		ellen_chargeshot_p->angle = randring_far_next16();
		ellen_chargeshot_p->length = 0x50;
	}
}

void far pascal ellen_hyper(Subpixel center_x, Subpixel center_y)
{
	ellen_chargeshot_p = &ellen_chargeshots[pid.current][0];
	for(int i = 0; i < 32; (i++, ellen_chargeshot_p++)) {
		if(ellen_chargeshot_p->state != 0) {
			continue;
		}
		ellen_chargeshot_p->state = 1;
		ellen_chargeshot_p->phase = 0;
		ellen_chargeshot_p->center.x = center_x;
		ellen_chargeshot_p->center.y = center_y;
		ellen_chargeshot_p->angle = randring_far_next16();
		ellen_chargeshot_p->length = 0x50;
		return;
	}
}

void far pascal chargeshot_update_ellen(void)
{
	int target_x;
	int target_y;
	int player_x;
	int player_y;
	unsigned char length;

	ellen_chargeshot_p = &ellen_chargeshots[pid_current][0];
	int i;
	for(i = 0; i < 32; (i++, ellen_chargeshot_p++)) {
		if(ellen_chargeshot_p->state != 0) {
			goto active;
		}
	}
	return;

active:
	ellen_chargeshot_p = &ellen_chargeshots[pid_current][0];
	ellen_target_set(pid_current);
	target_x = ellen_target_x;
	target_y = (ellen_target_y + TO_SP(-110));
	players[pid_current].gauge_charged = 0;
	player_x = players[pid_current].center.x.v;
	player_y = players[pid_current].center.y.v;
	playfield_clip_negative_radius.x.v = TO_SP(-8);
	playfield_clip_negative_radius.y.v = TO_SP(-8);

	for(i = 0; i < 32; (i++, ellen_chargeshot_p++)) {
		if(ellen_chargeshot_p->state == 0) {
			continue;
		}
		if(ellen_chargeshot_p->state == 1) {
			ellen_chargeshot_p->center.x.v += ellen_chargeshot_p->velocity.x.v;
			ellen_chargeshot_p->center.y.v += ellen_chargeshot_p->velocity.y.v;
			if(ellen_chargeshot_p->phase == 0) {
				length = (ellen_chargeshot_p->length - 2);
				vector2(
					ellen_chargeshot_p->velocity.x.v,
					ellen_chargeshot_p->velocity.y.v,
					ellen_chargeshot_p->angle,
					length
				);
				ellen_chargeshot_p->length = length;
				if(length == 0) {
					ellen_chargeshot_p->phase = 1;
					ellen_chargeshot_p->angle = iatan2(
						(target_y - ellen_chargeshot_p->center.y.v),
						(target_x - ellen_chargeshot_p->center.x.v)
					);
					vector2(
						ellen_chargeshot_p->velocity.x.v,
						ellen_chargeshot_p->velocity.y.v,
						ellen_chargeshot_p->angle,
						160
					);
				}
			} else if(playfield_clip(
				ellen_chargeshot_p->center.x,
				ellen_chargeshot_p->center.y
			)) {
				ellen_chargeshot_p->state = 0;
			}
		} else {
			if((ellen_chargeshot_p->state = (ellen_chargeshot_p->state - 1)) == 1) {
				snd_se_play(1);
			}
			ellen_chargeshot_p->center.x.v = player_x;
			ellen_chargeshot_p->center.y.v = player_y;
		}
	}
}

void near pascal ellen_chargeshot_private(Subpixel x, Subpixel y)
{
	_SI = x.v;
	_DI = y.v;
	sprite16_offset_t sprite_offset = (pid.so_attack + 0x10);
	unsigned char cel = (ellen_chargeshot_p->angle + 0x10);
	cel >>= 5;
	cel <<= 1;
	sprite_offset += cel;

	_SI = (playfield_fg_x_to_screen(_SI, pid_current) - 8);
	_AX = _DI;
	#define _AX static_cast<int16_t>(_AX)
	_AX >>= 4;
	_AX += 8;
	_DI = _AX;
	#undef _AX
	sprite16_put(_SI, _AX, sprite_offset);
}

uint8_t far chargeshot_hittest_ellen(void)
{
	unsigned char hits = 0;
	ellen_chargeshot_p = &ellen_chargeshots[hitbox.pid][0];

	for(int i = 0; i < 32; (i++, ellen_chargeshot_p++)) {
		if(ellen_chargeshot_p->state != 1) {
			continue;
		}
		if(
			(ellen_chargeshot_p->center.x.v >= hitbox.origin.topleft.x.v) &&
			(ellen_chargeshot_p->center.x.v <= hitbox.right.v) &&
			(ellen_chargeshot_p->center.y.v >= hitbox.origin.topleft.y.v) &&
			(ellen_chargeshot_p->center.y.v <= hitbox.bottom.v)
		) {
			hitcircles_enemy_add(
				ellen_chargeshot_p->center.x.v,
				ellen_chargeshot_p->center.y.v,
				hitbox.pid
			);
			ellen_chargeshot_p->state = 0;
			hits += 2;
		}
	}
	return hits;
}

void far pascal chargeshot_render_ellen(void)
{
	ellen_chargeshot_p = &ellen_chargeshots[pid_current][0];
	sprite16_put_size.set(16, 16);
	sprite16_clip_set_for_pid(pid_current);

	for(int i = 0; i < 32; (i++, ellen_chargeshot_p++)) {
		if(ellen_chargeshot_p->state != 1) {
			continue;
		}
		ellen_chargeshot_private(
			ellen_chargeshot_p->center.x,
			ellen_chargeshot_p->center.y
		);
	}
}

void near pascal gauge_pattern_ellen(bullet_type_t type)
{
	unsigned char pid_other;
	unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
	if(type == BT_BULLET16_DEFAULT) {
		flag_expected = (flag_expected + GBAF_PELLET_TO_BULLET);
	}

	if(gba_flag_active[pid_current] == flag_expected) {
		ellen_gauge_frame[pid_current] = 0;
		gba_flag_active[pid_current]++;
		ellen_gauge_x[pid_current] = TO_SP(144);
		ellen_gauge_y[pid_current] = 0;
		gauge_pattern_timing[pid_current].total_frames = (
			gba_gauge_level[pid_current] + 0x0E
		);
		gauge_pattern_timing[pid_current].byte_1 = (
			gba_gauge_level[pid_current] + 0x1C
		);
		return;
	}
	if(gba_flag_active[pid_current] != (flag_expected + 1)) {
		return;
	}

	if((ellen_gauge_frame[pid_current] % 8) == 0) {
		bullet_template.type = type;
		bullet_template.center.y.v = TO_SP(8);
		pid_other = (1 - pid_current);
		bullet_template.pid = pid_other;

		if(ellen_gauge_x[pid_current] > 0) {
			bullet_template.angle = 0;
			bullet_template.speed.v = ((3 << 4) + 8);
			bullet_template.group = BG_RING_AIMED;
			bullet_template.count = gauge_pattern_timing[pid_current].total_frames;
			bullet_template.center.y.v = 0;
			bomb_center_add(
				(bullet_template.center.x.v = ellen_gauge_x[pid_current]),
				0,
				pid_other
			);
			bullets_add();

			_DX = (TO_SP(PLAYFIELD_W) - ellen_gauge_x[pid_current]);
			bullet_template.center.x.v = _DX;
			bomb_center_add(_DX, 0, pid_other);
			bullets_add();
			ellen_gauge_x[pid_current] -= TO_SP(24);
		} else if(ellen_gauge_y[pid_current] < TO_SP(144)) {
			bullet_template.angle = randring_far_next16();
			bullet_template.speed.v = gauge_pattern_timing[pid_current].byte_1;
			bullet_template.group = BG_16_RING;
			bullet_template.center.y.v = ellen_gauge_y[pid_current];
			bullet_template.center.x.v = 0;
			bomb_center_add(0, ellen_gauge_y[pid_current], pid_other);
			bullets_add();

			bullet_template.center.x.v = TO_SP(PLAYFIELD_W);
			bomb_center_add(
				TO_SP(PLAYFIELD_W),
				ellen_gauge_y[pid_current],
				pid_other
			);
			bullets_add();
			bullet_template.angle = randring_far_next16();
			ellen_gauge_y[pid_current] += TO_SP(24);
		} else {
			gba_flag_active[pid_current] = GBAF_NONE;
			palette_restore_for_pid(pid_other);
		}
	}
	ellen_gauge_frame[pid_current]++;
}

void far gba_gauge_pattern_pellet_ellen(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_ellen(BT_PELLET);
	}
}

void far gba_gauge_pattern_bullet_ellen(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_ellen(BT_BULLET16_DEFAULT);
	}
}
