// Natural Turbo C++ reconstruction candidate for the complete Yumemi
// Extra Attack contribution in TH03 MAIN_06_TEXT.
//
// The historical entity pool and shared Extra Attack helpers remain external.
// This translation unit intentionally owns CODE only until full-link ownership
// is proved against the immutable TH03 target.
#pragma codeseg MAIN_06_TEXT

#include "src/main/player/exatt_yumemi.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/libs/sprite16/sprite16.h"

#pragma option -a2

// The same 32-byte live entity view used by the shared flight/Reimu code.
#include "src/main/player/exatt_entity.hpp"

extern exatt_entity_t exatt_entities[PLAYER_COUNT][16];
extern exatt_entity_t near *exatt_entity_p;

// Shared MAIN_06_TEXT helpers reconstructed separately.
extern "C" unsigned char near cdecl exatt_fly_update(void);
extern "C" void near pascal exatt_fly_init(
	int x,
	int y,
	int target_x,
	int target_y,
	unsigned char pid,
	int speed
);
extern "C" void near pascal exatt_render_state2(
	screen_x_t left,
	screen_y_t top,
	unsigned int state_frame
);
extern "C" void near pascal exatt_render_state_other(
	screen_x_t left,
	screen_y_t top,
	unsigned int state_frame
);

// Each player owns sixteen 32-byte Extra Attack slots, partitioned
// into eight ordinary flying entities and eight explicitly spawned
// on-field warnings. The active beam changes width through its frame.
enum yumemi_exatt_limits_t {
    YUME_EXATT_ORDINARY_SLOTS = 8,
    YUME_EXATT_SPECIAL_FIRST_SLOT = 8,
    YUME_EXATT_ALL_SLOTS = 16,
    YUME_EXATT_FRAME_GROW_END = 8,
    YUME_EXATT_BEAM_WARNING_END = 0x10,
    YUME_EXATT_CORNER_MIN_RADIUS = 0x18,
    YUME_EXATT_APPEAR_END_STATE = 0x28,
    YUME_EXATT_SPECIAL_DURATION = 0x20,
    YUME_EXATT_ORDINARY_DURATION = 0x60,
};

// All sixteen Extra Attack slots share an original byte-valued lifecycle.
// Keep the original transition through the 3..0x28 appearance states, and
// keep frame/state memory postincrement semantics even for inactive slots.
enum yumemi_exatt_state_t {
    YUME_EXATT_FREE = 0,
    YUME_EXATT_BEAM = 1,
    YUME_EXATT_FLYING = 2,
    YUME_EXATT_APPEARING_FIRST = 3,
};

void far pascal exatt_add_yumemi(int x, int y, unsigned char pid_)
{
	register exatt_entity_t near *p = &exatt_entities[pid_][0];
	register int i = 0;

	for(; i < YUME_EXATT_ORDINARY_SLOTS; ++i, p++) {
		if(!p->state) {
			exatt_entity_p = p;
			exatt_fly_init(
				x,
				y,
				randring_far_next16_mod(0x1200),
				(randring_far_next16_mod(0x1000) + 0x600),
				pid_,
				0x46
			);
			p->radius = 0;
			p->duration = YUME_EXATT_ORDINARY_DURATION;
			return;
		}
	}
}

void far pascal yumemi_extra_add(int x, int y)
{
	register exatt_entity_t near *p = &exatt_entities[pid_current][YUME_EXATT_SPECIAL_FIRST_SLOT];
	int i = YUME_EXATT_SPECIAL_FIRST_SLOT;

	for(; i < YUME_EXATT_ALL_SLOTS; ++i, p++) {
		if(!p->state) {
			p->state = YUME_EXATT_APPEARING_FIRST;
			p->frame = 0;
			p->x = x;
			p->y = y;
			p->pid = (1 - pid_current);
			p->radius = 0;
			p->duration = YUME_EXATT_SPECIAL_DURATION;
			return;
		}
	}
}

void near yumemi_exatt_render_one(void)
{
	sprite16_offset_t sprite_offset;
	screen_x_t edge_x;
	screen_y_t top;
	signed char extent;
	signed char extent_half;
	exatt_entity_t near *p;

	register screen_y_t mid_y;
	register screen_x_t left;

	p = exatt_entity_p;
	left = playfield_fg_x_to_screen(p->x, p->pid);
	top = ((p->y >> 4) + 0x10);

	if(pid_current == 1) {
		sprite16_clip.set_for_pid_0();
	} else {
		sprite16_clip.set_for_pid_1();
	}

	if(p->state == YUME_EXATT_BEAM) {
		if(pid_current == 1) {
			grc_setclip(16, 8, 303, 191);
		} else {
			grc_setclip(336, 8, 623, 191);
		}

		if(p->frame <= YUME_EXATT_BEAM_WARNING_END) {
			egc_off();
			grcg_setcolor(GC_RMW, 6);
			extent = p->frame;
			mid_y = (top / 2);
			extent_half = (extent / 2);

			grcg_hline(
				(left + extent - 32),
				(left + 32 - extent),
				(mid_y + extent_half - 40)
			);
			grcg_hline(
				(left + extent - 32),
				(left + 32 - extent),
				(mid_y + 52 - extent_half)
			);
			grcg_vline(
				(left + extent - 32),
				(mid_y + extent_half - 40),
				(mid_y + 52 - extent_half)
			);
			grcg_vline(
				(left + 32 - extent),
				(mid_y + extent_half - 40),
				(mid_y + 52 - extent_half)
			);

			grcg_hline(
				(left + extent - 80),
				(left + 80 - extent),
				(mid_y + extent_half - 16)
			);
			grcg_hline(
				(left + extent - 80),
				(left + 80 - extent),
				(mid_y + 16 - extent_half)
			);
			grcg_vline(
				(left + extent - 80),
				(mid_y + extent_half - 16),
				(mid_y + 16 - extent_half)
			);
			grcg_vline(
				(left + 80 - extent),
				(mid_y + extent_half - 16),
				(mid_y + 16 - extent_half)
			);
		} else {
			egc_off();
			extent = static_cast<signed char>(p->duration - 8 - p->frame);
			if(extent > 0x10) {
				grcg_setcolor(GC_RMW, 5);
			} else {
				grcg_setcolor(GC_RMW, 6);
			}
			mid_y = (top / 2);
			extent_half = (extent / 2);

			grcg_hline(
				(left + extent - 16),
				(left + 16 - extent),
				(mid_y + extent_half - 32)
			);
			grcg_hline(
				(left + extent - 16),
				(left + 16 - extent),
				(mid_y + 44 - extent_half)
			);
			grcg_vline(
				(left + extent - 16),
				(mid_y + extent_half - 32),
				(mid_y + 44 - extent_half)
			);
			grcg_vline(
				(left + 16 - extent),
				(mid_y + extent_half - 32),
				(mid_y + 44 - extent_half)
			);

			grcg_hline(
				(left + extent - 64),
				(left + 64 - extent),
				(mid_y + extent_half - 8)
			);
			grcg_hline(
				(left + extent - 64),
				(left + 64 - extent),
				(mid_y + 8 - extent_half)
			);
			grcg_vline(
				(left + extent - 64),
				(mid_y + extent_half - 8),
				(mid_y + 8 - extent_half)
			);
			grcg_vline(
				(left + 64 - extent),
				(mid_y + extent_half - 8),
				(mid_y + 8 - extent_half)
			);
		}

		grcg_off();
		egc_on();
		grc_setclip(0, 0, (RES_X - 1), (SPRITE16_RES_Y - 1));

		left -= 16;
		sprite16_put_size.set(32, 16);
		sprite_offset = (pid.so_attack + 0x280);

		mid_y = (top - p->radius);
		sprite16_put(left, mid_y, sprite_offset);
		for(mid_y += 16; mid_y < (top - 16); mid_y += 16) {
			sprite16_put(left, mid_y, (sprite_offset + 0x502));
		}

		mid_y = (
			(p->radius / 2) +
			(p->radius + top) -
			16
		);
		sprite16_put(left, mid_y, (sprite_offset + 0x280));
		for(mid_y -= 16; mid_y > top; mid_y -= 16) {
			sprite16_put(left, mid_y, (sprite_offset + 0x502));
		}

		sprite16_put_size.set(16, 32);
		top -= 16;

		edge_x = (left - p->radius + 16);
		sprite16_put(edge_x, top, sprite_offset);
		for(edge_x += 16; edge_x < left; edge_x += 16) {
			sprite16_put(edge_x, top, (sprite_offset + 0x500));
		}

		edge_x = (p->radius + left);
		sprite16_put(edge_x, top, (sprite_offset + 2));
		for(edge_x -= 16; edge_x > (left + 16); edge_x -= 16) {
			sprite16_put(edge_x, top, (sprite_offset + 0x500));
		}

		if(p->radius > YUME_EXATT_CORNER_MIN_RADIUS) {
			sprite16_put_size.set(32, 32);
			sprite16_put(left, top, (sprite_offset + 4));
		}
		return;
	}

	if(p->state == YUME_EXATT_FLYING) {
		exatt_render_state2(left, top, *((unsigned int near *)&p->frame));
	} else {
		exatt_render_state_other(left, top, *((unsigned int near *)&p->frame));
	}
}

void far pascal exatt_update_yumemi(void)
{
	unsigned char pid_other;
	register exatt_entity_t near *p = &exatt_entities[pid_current][0];
	register int i;

	pid_other = (1 - pid_current);
	collmap_pid = pid_other;
	i = 0;

	for(; i < YUME_EXATT_ALL_SLOTS; ++i, p++) {
		if(!p->state) {
			continue;
		}

		if(p->state == YUME_EXATT_BEAM) {
			if(p->frame <= YUME_EXATT_FRAME_GROW_END) {
				p->radius += 6;
			} else if(
				(p->frame >= p->duration) &&
				(p->frame < (p->duration + 8))
			) {
				p->radius -= 6;
			} else if(p->frame >= (p->duration + 8)) {
				p->state = YUME_EXATT_FREE;
			}

			hitbox_hittest_skip_explosions = true;
			hitbox.pid = pid_other;
			hitbox.radius.x.v = (p->radius << 3);
			hitbox.radius.y.v = TO_SP(4);
			hitbox.origin.center.x.v = p->x;
			hitbox.origin.center.y.v = p->y;
			hitbox_hittest();

			hitbox.radius.x.v = TO_SP(4);
			hitbox.radius.y.v = (p->radius << 3);
			hitbox.origin.center.x.v = p->x;
			hitbox.origin.center.y.v = p->y;
			hitbox_hittest();
			hitbox_hittest_skip_explosions = false;

			collmap_stripe_tile_w.v = p->radius;
			collmap_tile_h.v = (16 / COLLMAP_TILE_H);
			collmap_center.x.v = p->x;
			collmap_center.y.v = p->y;
			collmap_set_rect_striped();

			collmap_center.y.v = (p->y + (p->radius << 2));
			collmap_stripe_tile_w.v = (16 / COLLMAP_TILE_W);
			collmap_tile_h.v = ((p->radius / 4) + p->radius);
			collmap_set_rect_striped();
		} else if(p->state == YUME_EXATT_FLYING) {
			exatt_entity_p = p;
			if(exatt_fly_update()) {
				continue;
			}
		} else if(p->state <= YUME_EXATT_APPEAR_END_STATE) {
			p->state++;
		} else {
			p->radius = 0x10;
			p->frame = 0;
			p->state = YUME_EXATT_BEAM;
			snd_se_play(7);
		}

		p->frame++;
	}
}

void far pascal exatt_render_yumemi(void)
{
	register int i;

	exatt_entity_p = &exatt_entities[pid_current][0];
	for(i = 0; i < YUME_EXATT_ALL_SLOTS; ++i, exatt_entity_p++) {
		if(exatt_entity_p->state) {
			yumemi_exatt_render_one();
		}
	}
}
