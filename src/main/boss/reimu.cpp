// Complete current source-native original Reimu major BOSS in MAIN_03_TEXT.
// Shared boss helpers and physical state remain in their historical slots;
// full normal MAIN linking is exact, canonical packed Factory is separate.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/reimu.hpp"
#include "src/main/boss/shared.hpp"
#include "src/main/math/polar.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/bullet/bullet.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/math/vector.hpp"

#pragma option -a2

// Shares the physical 32-byte BOSS layout; trailing bytes are per-character.
#include "src/main/boss/template_state.hpp"

extern boss_template_state_t boss_character_template[PLAYER_COUNT];

extern int boss_center_x;
extern int boss_center_y;
extern PlayfieldPoint boss_aux_point;
extern int boss_hp;
extern sprite16_offset_t boss_sprite_offset;
extern unsigned char boss_hit;
extern unsigned char boss_mode;
extern unsigned char boss_render_mode;
extern unsigned int boss_frame;

// Reimu's six level-derived pattern parameters.
extern unsigned char reimu_cloud_interval;
extern unsigned char reimu_unused_param;
extern unsigned char reimu_bullet_speed;
extern unsigned char reimu_orbit_count;
extern unsigned char reimu_ring_speed;
extern unsigned char reimu_ring_count;

// Reimu-private state and point arrays in the historical player-state tail.
extern unsigned char reimu_direction;
extern unsigned char reimu_cloud_speed;
extern unsigned char reimu_orbit_angle;
extern int reimu_orbit_x[6];
extern int reimu_orbit_y[6];

extern int SinTable8[256];
extern int CosTable8[256];

extern "C" void far pascal reimu_extra_add(int x, int y, unsigned char angle);

// Reimu's actual byte-valued attack scheduler. Unlike other characters,
// the update checks intro and selection before the switch.
enum reimu_boss_mode_t {
    REIMU_MODE_INTRO = 0x00,
    REIMU_MODE_SELECT = 0x01,
    REIMU_MODE_CLOUD_0 = 0x02,
    REIMU_MODE_CLOUD_1 = 0x03,
    REIMU_MODE_CLOUD_2 = 0x04,
    REIMU_MODE_CLOUD_3 = 0x05,
    REIMU_MODE_CLOUD_4 = 0x06,
    REIMU_MODE_MIRROR_0 = 0x07,
    REIMU_MODE_SPREAD_0 = 0x08,
    REIMU_MODE_SPREAD_1 = 0x09,
    REIMU_MODE_SPREAD_2 = 0x0A,
    REIMU_MODE_MIRROR_1 = 0x0B,
    REIMU_MODE_MIRROR_2 = 0x0C,
    REIMU_MODE_SPREAD_3 = 0x0D,
    REIMU_MODE_MIRROR_3 = 0x0E,
    REIMU_MODE_ORBIT_BURST_0 = 0x0F,
    REIMU_MODE_ORBIT_BURST_1 = 0x10,
    REIMU_MODE_ORBIT_BURST_2 = 0x11,
    REIMU_MODE_DESCEND = 0x80,
    REIMU_MODE_EXPLODE = 0xFF,
};

// The full BOSS update and both eight-sprite character renderers share
// their own start/flicker gates, independent of bullet-wave intervals.
enum reimu_render_timing_t {
    REIMU_INTRO_END_FRAME = 0x64,
    REIMU_INTRO_FLASH_END_FRAME = 0x40,
    REIMU_INTRO_SPRITE_COUNT = 8,
    REIMU_INTRO_ANGLE_STEP = 0x20,
    REIMU_RENDER_CEL_PERIOD = 4,
    REIMU_INTRO_START_RADIUS = 0xC80,
    REIMU_INTRO_RADIUS_STEP = 32,
    REIMU_COLLISION_TILE_SIZE = 56,
    REIMU_COLLISION_HALF_RADIUS = TO_SP(32),
    REIMU_RENDER_MAIN_SIZE = 96,
    REIMU_RENDER_ORBIT_SIZE = 48,
    REIMU_RENDER_MAIN_LEFT_MARGIN = 48,
    REIMU_RENDER_MAIN_TOP_MARGIN = 32,
    REIMU_RENDER_ORBIT_LEFT_MARGIN = 24,
    REIMU_RENDER_ORBIT_TOP_MARGIN = 8,
};

enum reimu_template_layout_t {
    REIMU_TEMPLATE_CENTER_X = 0x900,
    REIMU_TEMPLATE_CENTER_Y = 0x500,
    REIMU_TEMPLATE_VELOCITY_X = -0x20,
    REIMU_TEMPLATE_HP = 0x6E,
    REIMU_TEMPLATE_SPRITE_OFFSET = 0x28C,
    REIMU_SECOND_PLAYER_SPRITE_OFFSET = 0x28,
};

enum reimu_render_mode_t {
    REIMU_RENDER_MODE_NONE = 0,
    REIMU_RENDER_MODE_ORBIT = 1,
};

void far pascal boss_reimu_template_init(int player_id)
{
	boss_template_state_t near *p =
		&boss_character_template[player_id];

	p->center_x = REIMU_TEMPLATE_CENTER_X;
	p->center_y = REIMU_TEMPLATE_CENTER_Y;
	p->velocity_x = REIMU_TEMPLATE_VELOCITY_X;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = REIMU_MODE_INTRO;
	p->hp = REIMU_TEMPLATE_HP;
	p->pattern_i = 0;
	p->render_mode = REIMU_RENDER_MODE_NONE;
	p->sprite_offset = REIMU_TEMPLATE_SPRITE_OFFSET;
	if(player_id != 0) {
		p->sprite_offset += REIMU_SECOND_PLAYER_SPRITE_OFFSET;
	}
}

// The orbiting cloud gradually accelerates until the original 0x80
// frame cutoff. Timer wrap and angle sign remain 8-bit operations.
enum reimu_cloud_phase_t {
    REIMU_CLOUD_START_FRAME = 0,
    REIMU_CLOUD_FINISH_FRAME = 0x80,
    REIMU_CLOUD_ACCEL_PERIOD = 2,
    REIMU_CLOUD_ANGLE_FRAME_STEP = 2,
    REIMU_CLOUD_ORBIT_RADIUS = TO_SP(32),
    REIMU_CLOUD_CENTER_ORBIT_RADIUS = TO_SP(48),
    REIMU_CLOUD_INITIAL_SPEED = 0x10,
    REIMU_CLOUD_OPPOSITE_ANGLE = 0x80,
    REIMU_CLOUD_ANGLE_ROTATION = -0x40,
};

void near reimu_pattern_orbit_cloud(void)
{
	unsigned char angle;

	if(REIMU_CLOUD_START_FRAME == boss_frame) {
		boss_aux_point.x.v = boss_center_x;
		boss_aux_point.y.v = (REIMU_CLOUD_CENTER_ORBIT_RADIUS + boss_center_y);
		reimu_direction = randring_far_next16_and(1);
		reimu_cloud_speed = REIMU_CLOUD_INITIAL_SPEED;
	}

	angle = (REIMU_CLOUD_ANGLE_FRAME_STEP * static_cast<unsigned char>(boss_frame));
	if(reimu_direction) {
		angle = static_cast<unsigned char>(0 - angle);
	}

	// The variable unsigned-word interval compares its remainder with
	// zero; both projectile emissions and RNG order remain unchanged.
	if(!(boss_frame % reimu_cloud_interval)) {
		bullet_template.type = BT_PELLET_CLOUD;
		bullet_template.group = BG_1;
		bullet_template.pid = (1 - pid_current);
		bullet_template.angle = (angle * 2);
		bullet_template.speed.v = reimu_cloud_speed;
		bullet_template.center.x.v = polar(
			boss_center_x, REIMU_CLOUD_ORBIT_RADIUS, CosTable8[angle]
		);
		bullet_template.center.y.v = polar(
			boss_center_y, REIMU_CLOUD_ORBIT_RADIUS, SinTable8[angle]
		);
		bullets_add();

		bullet_template.angle = ((angle * 2) + REIMU_CLOUD_OPPOSITE_ANGLE);
		angle += REIMU_CLOUD_OPPOSITE_ANGLE;
		bullet_template.center.x.v = polar(
			boss_center_x, REIMU_CLOUD_ORBIT_RADIUS, CosTable8[angle]
		);
		bullet_template.center.y.v = polar(
			boss_center_y, REIMU_CLOUD_ORBIT_RADIUS, SinTable8[angle]
		);
		bullets_add();
	}

	if(!(boss_frame % REIMU_CLOUD_ACCEL_PERIOD)) {
		// Preserve postfix here: prefix ++reimu_cloud_speed changed
		// the original TC4 byte-field codegen (af691b).
		reimu_cloud_speed++;
	}

	angle = (REIMU_CLOUD_ANGLE_FRAME_STEP * static_cast<unsigned char>(boss_frame));
	angle += REIMU_CLOUD_ANGLE_ROTATION;
	boss_center_y = polar(
		boss_aux_point.y.v, REIMU_CLOUD_CENTER_ORBIT_RADIUS, SinTable8[angle]
	);

	if(REIMU_CLOUD_FINISH_FRAME <= boss_frame) {
		boss_mode = REIMU_MODE_SELECT;
		boss_frame = 0;
	}
}

// Two timed spreads: narrow paired arcs, then the five-way medium
// volley, with the same global 16-frame synchronization check.
enum reimu_spread_phase_t {
    REIMU_SPREAD_NARROW_END = 0x40,
    REIMU_SPREAD_MEDIUM_END = 0x64,
};

void near reimu_pattern_spreads(void)
{
	boss_move_sine();

	bullet_template.type = BT_BULLET16_DEFAULT;
	bullet_template.speed.v = reimu_bullet_speed;
	bullet_template.pid = (1 - pid_current);
	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = boss_center_y;

	if(boss_frame < REIMU_SPREAD_NARROW_END) {
		if(round_frame_mod16) {
			return;
		}
		bullet_template.angle = 0x20;
		bullet_template.group = BG_3_SPREAD_NARROW;
		bullets_add();
		bullet_template.angle = 0x60;
		bullets_add();
		return;
	} else if(boss_frame < REIMU_SPREAD_MEDIUM_END) {
		if(round_frame_mod16) {
			return;
		}
		bullet_template.group = BG_5_SPREAD_MEDIUM;
		bullet_template.angle = 0x40;
		bullets_add();
		return;
	}

	boss_mode = REIMU_MODE_SELECT;
	boss_frame = 0;
}

// This controller first expands the ring, then holds the exact
// original radius until its Extra Attack release frame.
enum reimu_orbit_phase_t {
    REIMU_ORBIT_INIT_FRAME = 0,
    REIMU_ORBIT_EXPAND_END = 0x18,
    REIMU_ORBIT_RELEASE_FRAME = 0x50,
    // One full turn has 256 native byte-angle units, distributed by
    // the *signed* integer quotient before truncation to byte angle.
    REIMU_ORBIT_ANGLE_UNITS = 256,
    REIMU_ORBIT_ANGLE_STEP = 8,
};

// The four radial loops use natural signed i*256 BEFORE the original
// integer division; collapsing or reordering would change ring angles.
void near reimu_pattern_orbit_burst(void)
{
	register unsigned char angle;
	register int i;

	boss_move_sine();

	if(REIMU_ORBIT_INIT_FRAME == boss_frame) {
		boss_render_mode = REIMU_RENDER_MODE_ORBIT;
		reimu_orbit_angle = randring_far_next16();
	}

	if(REIMU_ORBIT_EXPAND_END > boss_frame) {
		// Keep the subpixel conversion before doubling: TO_SP(frame) * 2
		// is exact, while a single frame * 32 expression changes TC4 CODE.
		// Three orbit phases retain signed i*256 before division and byte
		// angle truncation. Postfix for-header increments preserve each
		// phase's polar and Extra Attack call order.
		for(i = 0; i < reimu_orbit_count; i++) {
			angle = reimu_orbit_angle + (REIMU_ORBIT_ANGLE_UNITS * i) / reimu_orbit_count;
			reimu_orbit_x[i] = polar(
				boss_center_x,
				(TO_SP(boss_frame) * 2),
				CosTable8[angle]
			);
			reimu_orbit_y[i] = polar(
				boss_center_y,
				(TO_SP(boss_frame) * 2),
				SinTable8[angle]
			);
		}
		// This unsigned-byte orbit angle accepts compound += in both
		// phases; signed-byte fields in other BOSS owners can differ.
		reimu_orbit_angle += REIMU_ORBIT_ANGLE_STEP;
		return;
	}

	if(REIMU_ORBIT_RELEASE_FRAME > boss_frame) {
		for(i = 0; i < reimu_orbit_count; i++) {
			angle = reimu_orbit_angle + (REIMU_ORBIT_ANGLE_UNITS * i) / reimu_orbit_count;
			reimu_orbit_x[i] = polar(
				boss_center_x, TO_SP(48), CosTable8[angle]
			);
			reimu_orbit_y[i] = polar(
				boss_center_y, TO_SP(48), SinTable8[angle]
			);
		}
		reimu_orbit_angle += REIMU_ORBIT_ANGLE_STEP;

		if(!round_frame_mod16) {
			bullet_template.type = BT_BULLET16_DEFAULT;
			bullet_template.speed.v = reimu_ring_speed;
			bullet_template.pid = (1 - pid_current);
			bullet_template.center.x.v = boss_center_x;
			bullet_template.center.y.v = boss_center_y;
			bullet_template.angle = randring_far_next16();
			bullet_template.group = BG_RING;
			bullet_template.count = reimu_ring_count;
			bullets_add();
		}
		return;
	}

	if(REIMU_ORBIT_RELEASE_FRAME == boss_frame) {
		for(i = 0; i < reimu_orbit_count; i++) {
			angle = reimu_orbit_angle + (REIMU_ORBIT_ANGLE_UNITS * i) / reimu_orbit_count;
			reimu_extra_add(reimu_orbit_x[i], reimu_orbit_y[i], angle);
		}
		boss_mode = REIMU_MODE_SELECT;
		boss_frame = 0;
		boss_render_mode = REIMU_RENDER_MODE_NONE;
	}
}

// Mirrored four-way spread completes on the original 0x80 frame;
// the boss dispatcher then returns to its shared pattern selector.
enum reimu_mirror_phase_t {
    REIMU_MIRROR_FINISH_FRAME = 0x80,
    REIMU_MIRROR_FIRE_PERIOD = 16,
    REIMU_MIRROR_OPPOSITE_ANGLE = 0x78,
};

void near reimu_pattern_mirrored_spread(void)
{
	boss_move_sine();

	// The sixteen-frame mirrored spread uses the unsigned-word low bits.
	if(boss_frame < REIMU_MIRROR_FINISH_FRAME) {
		if((boss_frame & (REIMU_MIRROR_FIRE_PERIOD - 1)) != 0) {
			return;
		}
		bullet_template.type = BT_BULLET16_DEFAULT;
		bullet_template.speed.v = reimu_bullet_speed;
		bullet_template.pid = (1 - pid_current);
		bullet_template.center.x.v = boss_center_x;
		bullet_template.center.y.v = boss_center_y;
		bullet_template.angle = (unsigned char)boss_frame;
		bullet_template.group = BG_4_SPREAD_NARROW;
		bullets_add();

		bullet_template.angle = (REIMU_MIRROR_OPPOSITE_ANGLE - (unsigned char)boss_frame);
		bullets_add();
		return;
	}

	boss_mode = REIMU_MODE_SELECT;
	boss_frame = 0;
}

void far gba_boss_update_reimu(void)
{
	register pid_t pid_other;

	if(boss_update_start()) {
		reimu_cloud_interval = (5 - (gba_boss_level / 5));
		reimu_unused_param = (0x18 + gba_boss_level);
		reimu_bullet_speed = (0x28 + (2 * gba_boss_level));
		reimu_orbit_count = (4 + (gba_boss_level / 8));
		reimu_ring_speed = (0x10 + gba_boss_level);
		reimu_ring_count = (0x10 + gba_boss_level);
	}

	if(pid_current == gba_boss_launched_by) {
		pid_other = (1 - pid_current);
		boss_target_update();
		boss_frame++;

		if(REIMU_MODE_INTRO == boss_mode) {
			if(REIMU_INTRO_END_FRAME == boss_frame) {
				boss_frame = 0;
				boss_mode = REIMU_MODE_SELECT;
			} else {
				return;
			}
		}

		if(REIMU_MODE_SELECT == boss_mode) {
			boss_pattern_next();
		}

		switch(boss_mode) {
		case REIMU_MODE_CLOUD_0:
		case REIMU_MODE_CLOUD_1:
		case REIMU_MODE_CLOUD_2:
		case REIMU_MODE_CLOUD_3:
		case REIMU_MODE_CLOUD_4:
			reimu_pattern_orbit_cloud();
			break;

		case REIMU_MODE_SPREAD_0:
		case REIMU_MODE_SPREAD_1:
		case REIMU_MODE_SPREAD_2:
		case REIMU_MODE_SPREAD_3:
			reimu_pattern_spreads();
			break;

		case REIMU_MODE_ORBIT_BURST_0:
		case REIMU_MODE_ORBIT_BURST_1:
		case REIMU_MODE_ORBIT_BURST_2:
			reimu_pattern_orbit_burst();
			break;

		case REIMU_MODE_MIRROR_0:
		case REIMU_MODE_MIRROR_1:
		case REIMU_MODE_MIRROR_2:
		case REIMU_MODE_MIRROR_3:
			reimu_pattern_mirrored_spread();
			break;

		case REIMU_MODE_DESCEND:
			boss_fall();
			break;

		case REIMU_MODE_EXPLODE:
			return;
		}

		collmap_center.x.v = boss_center_x;
		collmap_center.y.v = boss_center_y;
		collmap_stripe_tile_w.set(REIMU_COLLISION_TILE_SIZE);
		collmap_tile_h.set(REIMU_COLLISION_TILE_SIZE);
		collmap_pid = pid_other;
		collmap_set_rect_striped();

		hitbox_hittest_skip_explosions = true;
		hitbox.radius.x.v = REIMU_COLLISION_HALF_RADIUS;
		hitbox.radius.y.v = REIMU_COLLISION_HALF_RADIUS;
		hitbox.pid = pid_other;
		hitbox.origin.center.x.v = boss_center_x;
		hitbox.origin.center.y.v = boss_center_y;
		boss_hit = hitbox_hittest();
		boss_hp -= boss_hit;
		hitbox_hittest_skip_explosions = false;
		boss_hittest_end();	}

}

void near reimu_render_main(void)
{
	screen_x_t left;
	screen_y_t top;
	pid_t pid_other;
	unsigned char anim;
	register sprite16_offset_t sprite_offset;
	register int i;

	pid_other = (1 - pid_current);
	sprite16_put_size.set(REIMU_RENDER_MAIN_SIZE, REIMU_RENDER_MAIN_SIZE);

	if(!pid_other) {
		sprite16_clip.set_for_pid_0();
	} else {
		sprite16_clip.set_for_pid_1();
	}

	sprite_offset = boss_sprite_offset;
	if(boss_hit != 0) {
		sprite_offset += 0x0C;
	}

	left = (playfield_fg_x_to_screen(boss_center_x, pid_other) - REIMU_RENDER_MAIN_LEFT_MARGIN);
	top = ((boss_center_y >> 4) - REIMU_RENDER_MAIN_TOP_MARGIN);
	sprite16_put(left, top, sprite_offset);

	if(boss_render_mode != REIMU_RENDER_MODE_ORBIT) {
		return;
	}

	sprite16_put_size.set(REIMU_RENDER_ORBIT_SIZE, REIMU_RENDER_ORBIT_SIZE);
	sprite_offset = (boss_sprite_offset + 0xFFF4);
	anim = (boss_frame / REIMU_RENDER_CEL_PERIOD);
	// Do not write `%4` for this *byte* animation carrier: it changed
	// original TC4 CODE in af892g, unlike the 16-bit attack clock.
	if((anim & 3) == 1) {
		sprite_offset += 6;
	} else if(anim & 3) {
		sprite_offset += (((anim & 1) * 6) + 0x780);
	}

	// All live orbit sprites draw in signed-index order; the prefix
	// for-header increment preserves the original register sequence.
	for(i = 0; i < reimu_orbit_count; ++i) {
		left = (
			playfield_fg_x_to_screen(reimu_orbit_x[i], pid_other) - REIMU_RENDER_ORBIT_LEFT_MARGIN
		);
		top = ((reimu_orbit_y[i] >> 4) - REIMU_RENDER_ORBIT_TOP_MARGIN);
		sprite16_put(left, top, sprite_offset);
	}
}

// Both renderers take a 16-bit global frame division before truncating
// the result to a byte-valued animation cel. The later byte &3 checks
// must stay masks: changing all four to byte %4 expands original CODE
// (negative native af845b). Word-sized attack clocks *can* use %2/%16.
void near pascal reimu_render_intro(unsigned char angle, int length)
{
	screen_y_t top;
	int i;
	unsigned char anim;
	pid_t pid_other;
	register sprite16_offset_t sprite_offset;
	register screen_x_t left;

	pid_other = (1 - pid_current);

	if(round_frame_mod2 && (boss_frame < REIMU_INTRO_FLASH_END_FRAME)) {
		return;
	}

	sprite16_put_size.set(REIMU_RENDER_ORBIT_SIZE, REIMU_RENDER_ORBIT_SIZE);
	if(pid_current) {
		sprite16_clip.set_for_pid_0();
	} else {
		sprite16_clip.set_for_pid_1();
	}

	sprite_offset = (pid.so_attack + 0x280);
	anim = (boss_frame / REIMU_RENDER_CEL_PERIOD);
	if((anim & 3) == 1) {
		sprite_offset += 6;
	} else if(anim & 3) {
		sprite_offset += (((anim & 1) * 6) + 0x780);
	}

	// Eight original polar-sprite calls with byte-angle advancement
	// after rendering. The comma-expression increments the signed index
	// first and the byte angle second (af985d).
	for(i = 0; i < REIMU_INTRO_SPRITE_COUNT; ++i, angle += REIMU_INTRO_ANGLE_STEP) {
		left = polar(boss_center_x, length, CosTable8[angle]);
		top = polar(boss_center_y, length, SinTable8[angle]);
		left = (playfield_fg_x_to_screen(left, pid_other) - REIMU_RENDER_ORBIT_LEFT_MARGIN);
		top = ((top >> 4) - REIMU_RENDER_ORBIT_TOP_MARGIN);
		sprite16_put(left, top, sprite_offset);
	}
}

// The arrival render radius's single <<5 has native-exact natural
// C++ *32 codegen; unlike the orbit pattern's two-stage scale.
void far gba_boss_render_reimu(void)
{
	if(pid_current != gba_boss_launched_by) {
		return;
	}

	if(boss_mode == REIMU_MODE_INTRO) {
		reimu_render_intro(
			(unsigned char)boss_frame,
			(REIMU_INTRO_START_RADIUS - (boss_frame * REIMU_INTRO_RADIUS_STEP))
		);
		return;
	}

	if(boss_mode != REIMU_MODE_EXPLODE) {
		reimu_render_main();
		return;
	}

	boss_explosion_render();
}
