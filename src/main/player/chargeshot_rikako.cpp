// Natural Turbo C++ reconstruction candidate for TH03 MAIN_11_TEXT.
// Target boundaries and semantics are checked independently against MAIN.EXE;
// exact producer acceptance requires the object-shape and full-link Oracles.
#pragma codeseg MAIN_11_TEXT

#include "src/main/player/chargeshot_rikako.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/polar.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"

struct rikako_chargeshot_t {
	PlayfieldPoint center;
	unsigned char angle;
	unsigned char unused;
};

struct gauge_pattern_timing_t {
	unsigned char total_frames;
	unsigned char byte_1;
	unsigned char byte_2;
	unsigned char byte_3;
};

extern unsigned char rikako_gauge_frame[PLAYER_COUNT];
extern rikako_chargeshot_t rikako_chargeshots[PLAYER_COUNT][4];
extern rikako_chargeshot_t near *rikako_chargeshot_p;
extern unsigned char rikako_active[PLAYER_COUNT];
extern unsigned char rikako_frame[PLAYER_COUNT];
extern int rikako_radius[PLAYER_COUNT];
extern playfield_subpixel_t rikako_center_x[PLAYER_COUNT];
extern playfield_subpixel_t rikako_center_y[PLAYER_COUNT];
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];

extern "C" void far pascal bomb_center_add(int x, int y, int pid);
extern "C" void far pascal palette_restore_for_pid(pid_t pid);

void far chargeshots_reset_rikako(void)
{
	rikako_active[0] = 0;
	rikako_active[1] = 0;
}

void far pascal chargeshot_add_rikako(Subpixel center_x, Subpixel center_y)
{
	register rikako_chargeshot_t near *p;
	register int center_x_raw;

	center_x_raw = center_x.v;
	rikako_active[pid.current] = 1;
	rikako_frame[pid.current] = 0;
	rikako_radius[pid.current] = 0x80;
	p = &rikako_chargeshots[pid.current][0];

	for(_CX = 0; ((int)_CX) < 4; (_CX++, p++)) {
		p->center.x.v = center_x_raw;
		p->center.y = center_y;
		p->angle = ((_CL << 6) + 0x20);
	}

	rikako_center_x[pid.current] = center_x_raw;
	rikako_center_y[pid.current] = center_y.v;
}

void far pascal rikako_charge_add_private(Subpixel center_x, Subpixel center_y)
{
	chargeshot_add_rikako(center_x, center_y);
	rikako_active[pid.current] = 2;
}

void far rikako_chargeshot_cancel(void)
{
	rikako_active[pid.current] = 0;
}

void far pascal chargeshot_update_rikako(void)
{
	int i;
	player_stuff_t near *player;
	unsigned char frame;
	register rikako_chargeshot_t near *p;
	register int radius;

	if(rikako_active[pid_current] == 0) {
		return;
	}

	player = &players[pid_current];
	player->gauge_charged = 0;
	frame = rikako_frame[pid_current];
	radius = rikako_radius[pid_current];
	p = &rikako_chargeshots[pid_current][0];

	if(rikako_active[pid_current] == 1) {
		rikako_center_y[pid_current] -= 0x20;
	} else {
		rikako_center_x[pid_current] = player->center.x.v;
		rikako_center_y[pid_current] = player->center.y.v;
	}

	for(i = 0; i < 4; (i++, p++)) {
		p->center.x.v = polar(
			rikako_center_x[pid_current],
			radius,
			CosTable8[p->angle]
		);
		p->center.y.v = polar(
			rikako_center_y[pid_current],
			radius,
			SinTable8[p->angle]
		);
		p->angle = (
			p->angle + ((i & 1) ? 8 : 0xF8)
		);
	}

	if(frame < 0x20) {
		radius += 0x20;
	} else if(rikako_active[pid_current] == 1) {
		if(frame > 0x80) {
			radius += 0x60;
			if(frame > 0x90) {
				rikako_active[pid_current] = 0;
			}
		}
	} else {
		rikako_frame[pid_current] = 0x20;
	}

	rikako_radius[pid_current] = radius;
	rikako_frame[pid_current]++;
}

void near rikako_chargeshot_private(void)
{
	screen_x_t left;
	screen_y_t top;
	sprite16_offset_t sprite_offset;

	sprite_offset = (pid.so_attack + 0x280);
	left = (
		playfield_fg_x_to_screen(rikako_chargeshot_p->center.x.v, pid_current) - 16
	);
	top = rikako_chargeshot_p->center.y.to_pixel();
	sprite16_put(left, top, sprite_offset);
}

uint8_t far chargeshot_hittest_rikako(void)
{
	int hit_count;
	register rikako_chargeshot_t near *p;
	register int i;

	if(rikako_active[hitbox.pid] == 0) {
		return 0;
	}

	hit_count = 0;
	p = &rikako_chargeshots[hitbox.pid][0];
	for(i = 0; i < 4; (i++, p++)) {
		if((p->center.x.v - hitbox.right.v) > TO_SP(12)) {
			continue;
		}
		if((hitbox.origin.topleft.x.v - p->center.x.v) > TO_SP(12)) {
			continue;
		}
		if((p->center.y.v - hitbox.bottom.v) > TO_SP(12)) {
			continue;
		}
		if((hitbox.origin.topleft.y.v - p->center.y.v) > TO_SP(12)) {
			continue;
		}
		hitcircles_enemy_add(p->center.x.v, p->center.y.v, hitbox.pid);
		hit_count++;
	}
	return hit_count;
}

void far pascal chargeshot_render_rikako(void)
{
	if(rikako_active[pid_current] == 0) {
		return;
	}

	rikako_chargeshot_p = &rikako_chargeshots[pid_current][0];
	sprite16_put_size.set(32, 32);
	sprite16_clip_set_for_pid(pid_current);

	for(int i = 0; i < 4; (i++, rikako_chargeshot_p++)) {
		rikako_chargeshot_private();
	}
}

void near pascal gauge_pattern_rikako(bullet_type_t type)
{
	unsigned char pid_other;
	unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
	if(type == BT_BULLET16_DEFAULT) {
		flag_expected = (flag_expected + GBAF_PELLET_TO_BULLET);
	}

	if(gba_flag_active[pid_current] == flag_expected) {
		rikako_gauge_frame[pid_current] = 0;
		gba_flag_active[pid_current]++;
		gauge_pattern_timing[pid_current].total_frames = (
			16 - (gba_gauge_level[pid_current] / 2)
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
		(rikako_gauge_frame[pid_current] %
		 gauge_pattern_timing[pid_current].total_frames) == 0
	) {
		pid_other = (1 - pid_current);
		bullet_template.type = type;
		bullet_template.pid = pid_other;
		bullet_template.center.y.v = 0;
		bullet_template.group = BG_1_AIMED;
		bullet_template.angle = (
			0x20 - (rikako_gauge_frame[pid_current] / 4)
		);
		bullet_template.speed.v = gauge_pattern_timing[pid_current].byte_1;

		bullet_template.center.x.v = 0;
		bullets_add();
		bullet_template.center.x.v = TO_SP(PLAYFIELD_W);
		bullets_add();
		bullet_template.angle = -bullet_template.angle;
		bullets_add();
		bullet_template.center.x.v = 0;
		bullets_add();

		bomb_center_add(0, 0, pid_other);
		bomb_center_add(TO_SP(PLAYFIELD_W), 0, pid_other);
	}

	if(rikako_gauge_frame[pid_current] >= 0x80) {
		gba_flag_active[pid_current] = GBAF_NONE;
		palette_restore_for_pid(1 - pid_current);
	}
	rikako_gauge_frame[pid_current]++;
}

void far gba_gauge_pattern_pellet_rikako(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_rikako(BT_PELLET);
	}
}

void far gba_gauge_pattern_bullet_rikako(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_rikako(BT_BULLET16_DEFAULT);
	}
}
