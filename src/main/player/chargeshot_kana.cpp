// Maintained exact natural Turbo C++ reconstruction of TH03 MAIN_09_TEXT.
#pragma codeseg MAIN_09_TEXT

#include <stddef.h>
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

// Four independently animated trails of thirteen two-byte X/Y samples,
// giving the original fixed 54-byte per-trail DGROUP layout.
enum kana_charge_layout_t {
    KANA_CHARGE_TRAILS = 4,
    KANA_CHARGE_SAMPLES = 13,
    KANA_CHARGE_LAST = 12,
    KANA_CHARGE_RENDER_STEP = 4,
    KANA_CHARGE_INITIAL_LENGTH = 0x30,
    KANA_CHARGE_RELEASE_LENGTH = 0x80,
    KANA_CHARGE_RELEASE_AFTER = 0x28,
    KANA_CHARGE_END_Y = TO_SP(-16),
    KANA_CHARGE_SWIRLING = 1,
    KANA_CHARGE_RELEASED = 2,
};

struct kana_chargeshot_t {
	playfield_subpixel_t x[KANA_CHARGE_SAMPLES];
	playfield_subpixel_t y[KANA_CHARGE_SAMPLES];
	unsigned char angle;
	unsigned char length;
};

typedef char kana_charge_stride_is_54[
    (sizeof(kana_chargeshot_t) == 54) ? 1 : -1
];
typedef char kana_charge_y_at_1a[
    (offsetof(kana_chargeshot_t, y) == 0x1A) ? 1 : -1
];
typedef char kana_charge_angle_at_34[
    (offsetof(kana_chargeshot_t, angle) == 0x34) ? 1 : -1
];
typedef char kana_charge_length_at_35[
    (offsetof(kana_chargeshot_t, length) == 0x35) ? 1 : -1
];

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

	for(int group = 0; group < KANA_CHARGE_TRAILS; (++group, p++)) {
		for(int i = 0; i <= KANA_CHARGE_LAST; ++i) {
			p->x[i] = center_x.v;
			p->y[i] = center_y.v;
		}
		p->length = KANA_CHARGE_INITIAL_LENGTH;
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

	if(!kana_active[pid_current]) {
		return;
	}
	players[pid_current].gauge_charged = 0;
	state = kana_active[pid_current];

	p = &kana_chargeshots[pid_current][0];
	for(group = 0; group < KANA_CHARGE_TRAILS; (++group, p++)) {
		vector2(vector_x, vector_y, p->angle, p->length);

		for(point = KANA_CHARGE_LAST; point > 0; --point) {
			p->x[point] = p->x[point - 1];
			p->y[point] = p->y[point - 1];
		}
		p->x[0] += vector_x;
		p->y[0] += vector_y;
		if(state == KANA_CHARGE_SWIRLING) {
			p->length--;
		}
	}

	if(state == KANA_CHARGE_SWIRLING) {
		p--;
		p->angle -= 2;
		p -= 3;
		p->angle += 2;

		if(kana_frame[pid_current] > KANA_CHARGE_RELEASE_AFTER) {
			kana_active[pid_current] = KANA_CHARGE_RELEASED;
			for(group = 0; group < KANA_CHARGE_TRAILS; (++group, p++)) {
				p->length = KANA_CHARGE_RELEASE_LENGTH;
			}
		}
	}

	p = &kana_chargeshots[pid_current][0];
	if(p->y[KANA_CHARGE_LAST] <= KANA_CHARGE_END_Y) {
		kana_active[pid_current] = 0;
	}
	kana_frame[pid_current]++;
}

void near kana_chargeshot_private(void)
{
	sprite16_offset_t sprite_offset = (pid.so_attack + 0x1180);
	for(int i = KANA_CHARGE_LAST; i >= 0; (i -= KANA_CHARGE_RENDER_STEP, sprite_offset -= 0x500)) {
		screen_x_t left = (
			playfield_fg_x_to_screen(kana_chargeshot_p->x[i], pid_current) - 16
		);
		screen_y_t top = (kana_chargeshot_p->y[i] >> 4);
		sprite16_put(left, top, sprite_offset);
	}
}

uint8_t far chargeshot_hittest_kana(void)
{
	if(!kana_active[hitbox.pid]) {
		return 0;
	}

	kana_chargeshot_t near *p = &kana_chargeshots[hitbox.pid][0];
	for(int group = 0; group < KANA_CHARGE_TRAILS; (++group, p++)) {
		for(int i = 0; i <= KANA_CHARGE_LAST; i += 4) {
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
	if(!kana_active[pid_current]) {
		return;
	}
	kana_chargeshot_p = &kana_chargeshots[pid_current][0];
	sprite16_put_size.set(32, 32);
	sprite16_clip_set_for_pid(pid_current);

	// Original XOR DX,DX encodes the overlap mask zero setup;
	// _DX=0 changed native CODE (negative original TC4 af773c).
	asm xor dx, dx;
	_AH = SPRITE16_SET_OVERLAP;
	geninterrupt(SPRITE16);

	for(int i = 0; i < KANA_CHARGE_TRAILS; (++i, kana_chargeshot_p++)) {
		kana_chargeshot_private();
	}

	_DX = OVERLAP_CLEAR;
	_AH = SPRITE16_SET_OVERLAP;
	geninterrupt(SPRITE16);
}

// 64-frame left-right Gauge sweep: 32 frames per direction,
// then the original Gauge state expires after 128 frames.
enum kana_gauge_phase_t {
    KANA_GAUGE_SWEEP_PERIOD = 0x40,
    KANA_GAUGE_SWEEP_HALF = 0x20,
    KANA_GAUGE_MOVE_SUBPIXELS = 0x80,
    KANA_GAUGE_END_FRAME = 0x80,
};

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

		bullet_template.center.x.v = (
			TO_SP(PLAYFIELD_W) - kana_gauge_x[pid_current]
		);
		bullets_add();
		bomb_center_add(bullet_template.center.x.v, 0, pid_other);
	}

	// The original unsigned byte %64 differs from an equivalent &63
	// in TC4 machine code (actual native negative trial af773b).
	if((kana_gauge_frame[pid_current] % KANA_GAUGE_SWEEP_PERIOD) < KANA_GAUGE_SWEEP_HALF) {
		kana_gauge_x[pid_current] += KANA_GAUGE_MOVE_SUBPIXELS;
	} else {
		kana_gauge_x[pid_current] -= KANA_GAUGE_MOVE_SUBPIXELS;
	}

	if(kana_gauge_frame[pid_current] >= KANA_GAUGE_END_FRAME) {
		gba_flag_active[pid_current] = GBAF_NONE;
		palette_restore_for_pid(1 - pid_current);
	}
	kana_gauge_frame[pid_current]++;
}

void far gba_gauge_pattern_pellet_kana(void)
{
	if(gba_flag_active[pid_current]) {
		gauge_pattern_kana(BT_PELLET);
	}
}

void far gba_gauge_pattern_bullet_kana(void)
{
	if(gba_flag_active[pid_current]) {
		gauge_pattern_kana(BT_BULLET16_DEFAULT);
	}
}
