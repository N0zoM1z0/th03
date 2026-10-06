// Natural Turbo C++ reconstruction candidate for TH03 MAIN_07_TEXT.
#pragma codeseg MAIN_07_TEXT

#include "src/main/player/chargeshot_chiyuri.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th02/snd/snd.h"

struct chiyuri_chargeshot_t {
	unsigned char age;
	unsigned char anim;
	PlayfieldPoint center;
};

struct gauge_pattern_timing_t {
	unsigned char total_frames;
	unsigned char byte_1;
	unsigned char byte_2;
	unsigned char byte_3;
};

// These names describe target state inferred from indexing shape. The aggregate
// owner will later bind them to the historical carrier storage after the TC4J
// code producer has been proved independently.
extern int chiyuri_gauge_x[PLAYER_COUNT];
extern unsigned char chiyuri_gauge_frame[PLAYER_COUNT];
extern chiyuri_chargeshot_t chiyuri_chargeshots[PLAYER_COUNT][8];
extern chiyuri_chargeshot_t near *chiyuri_chargeshot_p;
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];

extern "C" void far pascal bomb_center_add(int x, int y, int pid);
extern "C" void far pascal palette_restore_for_pid(pid_t pid);

void far chargeshots_reset_chiyuri(void)
{
	chiyuri_chargeshot_t near *p = &chiyuri_chargeshots[0][0];
	for(int i = 0; i < 16; i++) {
		// Target quirk: [p] is deliberately not advanced.
		p->age = 0;
	}
}

void far pascal chargeshot_add_chiyuri(Subpixel center_x, Subpixel center_y)
{
	chiyuri_chargeshot_t near *p = &chiyuri_chargeshots[pid.current][0];
	p->anim = 0;
	p->center.x = center_x;
	p->center.y = center_y;
	players[pid.current].shot_active = SA_DISABLED;

	for(int i = 0; i < 8; (i++, p++)) {
		p->age = ((i << 2) + 2);
	}
}

void far pascal chargeshot_update_chiyuri(void)
{
	chiyuri_chargeshot_t near *p = &chiyuri_chargeshots[pid_current][7];
	if(p->age == 0) {
		return;
	}
	players[pid_current].gauge_charged = 0;

	for(int i = 0; i < 8; (i++, p--)) {
		if(p->age == 0) {
			return;
		}
		if(p->age != 1) {
			p->age--;
			if(p->age == 1) {
				p->center.x = players[pid_current].center.x;
				p->center.y = players[pid_current].center.y;
				snd_se_play(15);
			}
		} else {
			p->center.y.v -= 0xE0;
			if(p->center.y.v < TO_SP(-48)) {
				if(i == 0) {
					players[pid_current].shot_active = SA_ENABLED;
				}
				p->age = 0;
				continue;
			}
		}
		p->anim++;
	}
}

void near chiyuri_chargeshot_private(void)
{
	sprite16_offset_t so = (pid.so_attack + 0x280);
	if(chiyuri_chargeshot_p->anim & 1) {
		so += 4;
	}
	screen_x_t left = (
		playfield_fg_x_to_screen(
			chiyuri_chargeshot_p->center.x.v, pid_current
		) - 16
	);
	screen_y_t top = (chiyuri_chargeshot_p->center.y.to_pixel() - 8);
	sprite16_put(left, top, so);
}

uint8_t far chargeshot_hittest_chiyuri(void)
{
	chiyuri_chargeshot_t near *p = &chiyuri_chargeshots[hitbox.pid][7];
	int i = 0;
	unsigned char hits = 0;

	for(; i < 8; (i++, p--)) {
		if(p->age == 0) {
			return hits;
		}
		if(p->age != 1) {
			continue;
		}
		if((p->center.x.v - hitbox.right.v) > TO_SP(14)) {
			continue;
		}
		if((hitbox.origin.topleft.x.v - p->center.x.v) > TO_SP(14)) {
			continue;
		}
		if((p->center.y.v - hitbox.bottom.v) > TO_SP(32)) {
			continue;
		}
		if((hitbox.origin.topleft.y.v - p->center.y.v) > TO_SP(-16)) {
			continue;
		}
		hitcircles_enemy_add(p->center.x.v, p->center.y.v, hitbox.pid);
		hits++;
	}
	return hits;
}

void far pascal chargeshot_render_chiyuri(void)
{
	chiyuri_chargeshot_p = &chiyuri_chargeshots[pid_current][7];
	sprite16_put_size.set(32, 48);
	sprite16_clip_set_for_pid(pid_current);

	for(int i = 0; i < 8; (i++, chiyuri_chargeshot_p--)) {
		if(chiyuri_chargeshot_p->age == 0) {
			return;
		}
		if(chiyuri_chargeshot_p->age == 1) {
			chiyuri_chargeshot_private();
		}
	}
}

void near pascal gauge_pattern_chiyuri(bullet_type_t type)
{
	unsigned char pid_other;
	unsigned char flag_expected = GBAF_GAUGE_PELLET_INIT;
	if(type == BT_BULLET16_DEFAULT) {
		flag_expected = (flag_expected + GBAF_PELLET_TO_BULLET);
	}

	if(gba_flag_active[pid_current] == flag_expected) {
		chiyuri_gauge_frame[pid_current] = 0;
		gba_flag_active[pid_current]++;
		gauge_pattern_timing[pid_current].total_frames = (
			((gba_gauge_level[pid_current] / 2) << 4) + 0x20
		);
		chiyuri_gauge_x[pid_current] = TO_SP(-24);
		return;
	}

	if(gba_flag_active[pid_current] != (flag_expected + 1)) {
		return;
	}

	int x = chiyuri_gauge_x[pid_current];
	pid_other = (1 - pid_current);

	if((chiyuri_gauge_frame[pid_current] % 16) == 0) {
		chiyuri_gauge_x[pid_current] += TO_SP(24);
		x += TO_SP(24);
		bomb_center_add(x, 0, pid_other);
		bomb_center_add((TO_SP(PLAYFIELD_W) - x), 0, pid_other);
	}

	if(chiyuri_gauge_frame[pid_current] & 1) {
		bullet_template.type = type;
		bullet_template.pid = pid_other;
		bullet_template.speed.v = (
			((chiyuri_gauge_frame[pid_current] % 16) << 2) + 0x18
		);
		bullet_template.group = BG_1_AIMED;
		bullet_template.angle = 0;
		bullet_template.center.y.v = 0;
		bullet_template.center.x.v = x;
		bullet_template.is_animated = false;
		bullets_add();

		bullet_template.center.x.v = (TO_SP(PLAYFIELD_W) - x);
		bullets_add();
		bullet_template.is_animated = true;
	}

	chiyuri_gauge_frame[pid_current]++;
	if(
		chiyuri_gauge_frame[pid_current] >=
		gauge_pattern_timing[pid_current].total_frames
	) {
		gba_flag_active[pid_current] = GBAF_NONE;
		palette_restore_for_pid(pid_other);
	}
}

void far gba_gauge_pattern_pellet_chiyuri(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_chiyuri(BT_PELLET);
	}
}

void far gba_gauge_pattern_bullet_chiyuri(void)
{
	if(gba_flag_active[pid_current] != GBAF_NONE) {
		gauge_pattern_chiyuri(BT_BULLET16_DEFAULT);
	}
}
