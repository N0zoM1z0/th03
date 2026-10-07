// Natural Turbo C++ reconstruction candidate for TH03 MAIN_09_TEXT.
#pragma codeseg MAIN_09_TEXT

#include "src/main/player/chargeshot_kana.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/libs/sprite16/sprite16.h"

struct kana_chargeshot_t {
	playfield_subpixel_t x[13];
	playfield_subpixel_t y[13];
	unsigned char angle;
	unsigned char length;
};

struct gauge_pattern_timing_t {
	unsigned char total_frames;
	unsigned char byte_1;
	unsigned char byte_2;
	unsigned char byte_3;
};

extern int kana_gauge_x[PLAYER_COUNT];
extern unsigned char kana_gauge_frame[PLAYER_COUNT];
extern kana_chargeshot_t kana_chargeshots[PLAYER_COUNT][4];
extern kana_chargeshot_t near *kana_chargeshot_p;
extern unsigned char kana_active[PLAYER_COUNT];
extern unsigned char kana_frame[PLAYER_COUNT];
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];

extern "C" void far pascal bomb_center_add(int x, int y, int pid);
extern "C" void far pascal palette_restore_for_pid(pid_t pid);

void far pascal chargeshots_reset_kana(void)
{
	kana_active[0] = 0;
	kana_active[1] = 0;
}

void far pascal chargeshot_add_kana(Subpixel center_x, Subpixel center_y)
{
	kana_active[pid.current] = 1;
	kana_frame[pid.current] = 0;
	kana_chargeshot_t near *p = &kana_chargeshots[pid.current][0];

	for(int group = 0; group < 4; (group++, p++)) {
		for(int i = 0; i <= 12; i++) {
			p->x[i] = center_x.v;
			p->y[i] = center_y.v;
		}
		p->length = 0x30;
	}

	p--;
	p->angle = 0xF0;
	p--;
	p->angle = 0xC8;
	p--;
	p->angle = 0xB8;
	p--;
	p->angle = 0x90;
}

void far pascal chargeshot_update_kana(void)
{
	int vector_x;
	int vector_y;
	int point;
	unsigned char state;
	register kana_chargeshot_t near *p;
	register int group;

	if(kana_active[pid_current] == 0) {
		return;
	}
	players[pid_current].gauge_charged = 0;
	state = kana_active[pid_current];

	p = &kana_chargeshots[pid_current][0];
	for(group = 0; group < 4; (group++, p++)) {
		vector2(vector_x, vector_y, p->angle, p->length);

		point = 12;
		while(point > 0) {
			p->x[point] = p->x[point - 1];
			p->y[point] = p->y[point - 1];
			point--;
		}
		p->x[0] += vector_x;
		p->y[0] += vector_y;
		if(state == 1) {
			p->length--;
		}
	}

	if(state == 1) {
		p--;
		p->angle -= 2;
		p -= 3;
		p->angle += 2;

		if(kana_frame[pid_current] > 0x28) {
			kana_active[pid_current] = 2;
			for(group = 0; group < 4; (group++, p++)) {
				p->length = 0x80;
			}
		}
	}

	p = &kana_chargeshots[pid_current][0];
	if(p->y[12] <= TO_SP(-16)) {
		kana_active[pid_current] = 0;
	}
	kana_frame[pid_current]++;
}

void near kana_chargeshot_private(void)
{
	sprite16_offset_t sprite_offset = (pid.so_attack + 0x1180);
	for(int i = 12; i >= 0; (i -= 4, sprite_offset -= 0x500)) {
		screen_x_t left = (
			playfield_fg_x_to_screen(kana_chargeshot_p->x[i], pid_current) - 16
		);
		screen_y_t top = (kana_chargeshot_p->y[i] >> 4);
		sprite16_put(left, top, sprite_offset);
	}
}

uint8_t far chargeshot_hittest_kana(void)
{
	if(kana_active[hitbox.pid] == 0) {
		return 0;
	}

	kana_chargeshot_t near *p = &kana_chargeshots[hitbox.pid][0];
	for(int group = 0; group < 4; (group++, p++)) {
		for(int i = 0; i <= 12; i += 4) {
			if((p->x[i] - hitbox.right.v) > TO_SP(12)) {
				continue;
			}
			if((hitbox.origin.topleft.x.v - p->x[i]) > TO_SP(12)) {
				continue;
			}
			if((p->y[i] - hitbox.bottom.v) > TO_SP(12)) {
				continue;
			}
			if((hitbox.origin.topleft.y.v - p->y[i]) > TO_SP(12)) {
				continue;
			}
			hitcircles_enemy_add(p->x[i], p->y[i], hitbox.pid);
			return 1;
		}
	}
	return 0;
}

void far pascal chargeshot_render_kana(void)
{
	if(kana_active[pid_current] == 0) {
		return;
	}
	kana_chargeshot_p = &kana_chargeshots[pid_current][0];
	sprite16_put_size.set(32, 32);
	sprite16_clip_set_for_pid(pid_current);

	asm xor dx, dx;
	_AH = SPRITE16_SET_OVERLAP;
	geninterrupt(SPRITE16);

	for(int i = 0; i < 4; (i++, kana_chargeshot_p++)) {
		kana_chargeshot_private();
	}

	_DX = OVERLAP_CLEAR;
	_AH = SPRITE16_SET_OVERLAP;
	geninterrupt(SPRITE16);
}

void near pascal gauge_pattern_kana(bullet_type_t type)
{
	unsigned char pid_other;
	unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
	if(type == BT_BULLET16_DEFAULT) {
		flag_expected = (flag_expected + GBAF_PELLET_TO_BULLET);
	}

	if(gba_flag_active[pid_current] == flag_expected) {
		kana_gauge_frame[pid_current] = 0;
		gba_flag_active[pid_current]++;
		kana_gauge_x[pid_current] = 0;
		gauge_pattern_timing[pid_current].total_frames = (
			8 - (gba_gauge_level[pid_current] / 4)
		);
		gauge_pattern_timing[pid_current].byte_1 = (
			gba_gauge_level[pid_current] + 0x30
		);
		return;
	}
	if(gba_flag_active[pid_current] != (flag_expected + 1)) {
		return;
	}

	if(
		(kana_gauge_frame[pid_current] %
		 gauge_pattern_timing[pid_current].total_frames) == 0
	) {
		pid_other = (1 - pid_current);
		bullet_template.type = type;
		bullet_template.pid = pid_other;
		bullet_template.center.y.v = 0;
		bullet_template.center.x.v = kana_gauge_x[pid_current];
		bullet_template.group = BG_1;
		bullet_template.angle = 0x40;
		bullet_template.speed.v = gauge_pattern_timing[pid_current].byte_1;
		bullets_add();
		bomb_center_add(bullet_template.center.x.v, 0, pid_other);

		_DX = (TO_SP(PLAYFIELD_W) - kana_gauge_x[pid_current]);
		bullet_template.center.x.v = _DX;
		bullets_add();
		bomb_center_add(bullet_template.center.x.v, 0, pid_other);
	}

	if((kana_gauge_frame[pid_current] % 0x40) < 0x20) {
		kana_gauge_x[pid_current] += 0x80;
	} else {
		kana_gauge_x[pid_current] -= 0x80;
	}

	if(kana_gauge_frame[pid_current] >= 0x80) {
		gba_flag_active[pid_current] = GBAF_NONE;
		palette_restore_for_pid(1 - pid_current);
	}
	kana_gauge_frame[pid_current]++;
}

void far gba_gauge_pattern_pellet_kana(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_kana(BT_PELLET);
	}
}

void far gba_gauge_pattern_bullet_kana(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_kana(BT_BULLET16_DEFAULT);
	}
}
