// Complete native-source Turbo C++ of the original Chiyuri Chargeshot/
// Gauge owner in MAIN_07_TEXT, including eight-slot reverse physics,
// five-continue hit testing and real 16-byte frame/Gauge semantics.
#pragma codeseg MAIN_07_TEXT

#include <stddef.h>
#include "src/main/player/chargeshot_chiyuri.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th02/snd/snd.h"

// Eight 6-byte staggered projectiles per player; the game checks
// collision and draws in reverse storage order (slot 7 down to slot 0).
enum chiyuri_charge_limits_t {
    CHIYURI_CHARGE_SLOTS_PER_PLAYER = 8,
    CHIYURI_CHARGE_TOTAL_SLOTS = 16,
    CHIYURI_CHARGE_LAST_SLOT = 7,
    CHIYURI_CHARGE_INACTIVE_AGE = 0,
    CHIYURI_CHARGE_ACTIVE_AGE = 1,
    CHIYURI_GAUGE_BOMB_PERIOD = 16,
    CHIYURI_CHARGE_INITIAL_AGE_STEP = 4,
    CHIYURI_CHARGE_INITIAL_AGE_BASE = 2,
    CHIYURI_CHARGE_FLY_SPEED = 0xE0,
    CHIYURI_CHARGE_CLIP_TOP = TO_SP(-48),
    CHIYURI_CHARGE_HIT_MARGIN_X = TO_SP(14),
    CHIYURI_CHARGE_HIT_MARGIN_BOTTOM = TO_SP(32),
    CHIYURI_CHARGE_HIT_MARGIN_TOP = TO_SP(-16),
    CHIYURI_CHARGE_RENDER_WIDTH = 32,
    CHIYURI_CHARGE_RENDER_HEIGHT = 48,
    CHIYURI_GAUGE_WARNING_X_STEP = TO_SP(24),
};

struct chiyuri_chargeshot_t {
	unsigned char age;
	unsigned char anim;
	PlayfieldPoint center;
};

typedef char chiyuri_charge_stride_is_6[
    (sizeof(chiyuri_chargeshot_t) == 6) ? 1 : -1
];
typedef char chiyuri_charge_center_at_02[
    (offsetof(chiyuri_chargeshot_t, center) == 2) ? 1 : -1
];

struct gauge_pattern_timing_t {
	unsigned char total_frames;
	unsigned char byte_1;
	unsigned char byte_2;
	unsigned char byte_3;
};

typedef char chiyuri_gauge_timing_is_4[
    (sizeof(gauge_pattern_timing_t) == 4) ? 1 : -1
];

// These names describe target state inferred from indexing shape. The aggregate
// owner will later bind them to the historical carrier storage after the TC4J
// code producer has been proved independently.
extern int chiyuri_gauge_x[PLAYER_COUNT];
extern unsigned char chiyuri_gauge_frame[PLAYER_COUNT];
extern chiyuri_chargeshot_t chiyuri_chargeshots[PLAYER_COUNT][CHIYURI_CHARGE_SLOTS_PER_PLAYER];
extern chiyuri_chargeshot_t near *chiyuri_chargeshot_p;
extern gauge_pattern_timing_t gauge_pattern_timing[PLAYER_COUNT];

extern "C" void far pascal bomb_center_add(int x, int y, int pid);
extern "C" void far pascal palette_restore_for_pid(pid_t pid);

void far chargeshots_reset_chiyuri(void)
{
	chiyuri_chargeshot_t near *p = &chiyuri_chargeshots[0][0];
	for(int i = 0; i < CHIYURI_CHARGE_TOTAL_SLOTS; ++i) {
		// Original-game quirk: this loop clears only the first physical
		// slot 16 times. A fresh genuine TC4 trial af875g adding p++
		// changed original CODE: do NOT silently repair this behavior.
		p->age = CHIYURI_CHARGE_INACTIVE_AGE;
	}
}

void far pascal chargeshot_add_chiyuri(Subpixel center_x, Subpixel center_y)
{
	chiyuri_chargeshot_t near *p = &chiyuri_chargeshots[pid.current][0];
	p->anim = 0;
	p->center.x.v = center_x.v;
	p->center.y.v = center_y.v;
	players[pid.current].shot_active = SA_DISABLED;

	for(int i = 0; i < CHIYURI_CHARGE_SLOTS_PER_PLAYER; ++i, ++p) {
		p->age = ((i * CHIYURI_CHARGE_INITIAL_AGE_STEP) + CHIYURI_CHARGE_INITIAL_AGE_BASE);
	}
}

void far pascal chargeshot_update_chiyuri(void)
{
	chiyuri_chargeshot_t near *p = &chiyuri_chargeshots[pid_current][CHIYURI_CHARGE_LAST_SLOT];
	if(p->age == CHIYURI_CHARGE_INACTIVE_AGE) {
		return;
	}
	players[pid_current].gauge_charged = 0;

	// Both clip/continue and animation paths advance the signed index
	// and descending near pointer through the same for header.
	for(int i = 0; i < CHIYURI_CHARGE_SLOTS_PER_PLAYER; ++i, --p) {
		// The exact original byte-value state 0 permits a natural FREE
		// equality check under real TC4 (af925a); do not fix the
		// separate reset-loop's original first-slot-only behavior.
		if(p->age == CHIYURI_CHARGE_INACTIVE_AGE) {
			return;
		}
		if(p->age != CHIYURI_CHARGE_ACTIVE_AGE) {
			// Keep byte-memory postfix decrement: prefix changed
			// native CODE in fresh af925h, despite behavior equivalence.
			p->age--;
			if(p->age == CHIYURI_CHARGE_ACTIVE_AGE) {
				p->center.x = players[pid_current].center.x;
				p->center.y = players[pid_current].center.y;
				snd_se_play(15);
			}
		} else {
			p->center.y.v -= CHIYURI_CHARGE_FLY_SPEED;
			if(p->center.y.v < CHIYURI_CHARGE_CLIP_TOP) {
				if(i == 0) {
					players[pid_current].shot_active = SA_ENABLED;
				}
				p->age = CHIYURI_CHARGE_INACTIVE_AGE;
				continue;
			}
		}
		p->anim++;
	}
}

void near chiyuri_chargeshot_private(void)
{
	sprite16_offset_t so = (pid.so_attack + 0x280);
	// Byte-valued animation must retain this bit mask: replacing it
	// with natural byte %2 generated non-original CODE in af875d.
	// The animation is a byte and its original &1 test must stay:
	// `%2` selected nonoriginal TC4 instructions (af925b).
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
	chiyuri_chargeshot_t near *p = &chiyuri_chargeshots[hitbox.pid][CHIYURI_CHARGE_LAST_SLOT];
	int i = 0;
	unsigned char hits = 0;

	// Five short-circuit rejects share one signed-index and reverse
	// near-pointer advancement at the for header.
	for(; i < CHIYURI_CHARGE_SLOTS_PER_PLAYER; ++i, --p) {
		if(p->age == CHIYURI_CHARGE_INACTIVE_AGE) {
			return hits;
		}
		if(p->age != CHIYURI_CHARGE_ACTIVE_AGE) {
			continue;
		}
		if((p->center.x.v - hitbox.right.v) > CHIYURI_CHARGE_HIT_MARGIN_X) {
			continue;
		}
		if((hitbox.origin.topleft.x.v - p->center.x.v) > CHIYURI_CHARGE_HIT_MARGIN_X) {
			continue;
		}
		if((p->center.y.v - hitbox.bottom.v) > CHIYURI_CHARGE_HIT_MARGIN_BOTTOM) {
			continue;
		}
		if((hitbox.origin.topleft.y.v - p->center.y.v) > CHIYURI_CHARGE_HIT_MARGIN_TOP) {
			continue;
		}
		hitcircles_enemy_add(p->center.x.v, p->center.y.v, hitbox.pid);
		// Original byte hit-count postfix, not prefix: af925c failed.
		hits++;
	}
	return hits;
}

void far pascal chargeshot_render_chiyuri(void)
{
	chiyuri_chargeshot_p = &chiyuri_chargeshots[pid_current][CHIYURI_CHARGE_LAST_SLOT];
	sprite16_put_size.set(CHIYURI_CHARGE_RENDER_WIDTH, CHIYURI_CHARGE_RENDER_HEIGHT);
	sprite16_clip_set_for_pid(pid_current);

	for(int i = 0; i < CHIYURI_CHARGE_SLOTS_PER_PLAYER; ++i, --chiyuri_chargeshot_p) {
		if(chiyuri_chargeshot_p->age == CHIYURI_CHARGE_INACTIVE_AGE) {
			return;
		}
		if(chiyuri_chargeshot_p->age == CHIYURI_CHARGE_ACTIVE_AGE) {
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

	// The original initial Gauge enum equality allows the natural
	// constant-first form, still native exact (af925g).
	if(flag_expected == gba_flag_active[pid_current]) {
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

	// The historical unsigned-byte %16 condition is codegen-visible:
	// a direct &15 mask changed original TC4 CODE (af771c).
	// This *different* byte-valued Gauge `%16` condition safely uses
	// natural `if(!(frame %16))` under original TC4 (af875e).
	if(!(chiyuri_gauge_frame[pid_current] % CHIYURI_GAUGE_BOMB_PERIOD)) {
		// The 16-bit word storage allows a named +24-pixel compound
		// update, while direct `word = word + enum` changed native
		// CODE (af925d/e). The local x uses the same named compound step.
		chiyuri_gauge_x[pid_current] += CHIYURI_GAUGE_WARNING_X_STEP;
		x += CHIYURI_GAUGE_WARNING_X_STEP;
		bomb_center_add(x, 0, pid_other);
		bomb_center_add((TO_SP(PLAYFIELD_W) - x), 0, pid_other);
	}

	// In contrast, the odd-tick gauge volley is byte-exact with &1.
	if((chiyuri_gauge_frame[pid_current] & 1)) {
		bullet_template.type = type;
		bullet_template.pid = pid_other;
		bullet_template.speed.v = (
			((chiyuri_gauge_frame[pid_current] % CHIYURI_GAUGE_BOMB_PERIOD) << 2) + 0x18
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
