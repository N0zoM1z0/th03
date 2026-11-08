// Complete current source-native reconstruction of the original Chiyuri
// BOSS in MAIN_03_TEXT. Shared BOSS helpers and state stay in their own
// physical objects: the complete Japanese normal MAIN link is exact,
// while canonical Factory packed-unit ownership is a separate open gate.
#pragma codeseg MAIN_03_TEXT

#include "src/main/boss/chiyuri.hpp"
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
#include "compat/rec98/th03/main/v_colors.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/libs/sprite16/sprite16.h"

#pragma option -a2

// Shares the physical 32-byte BOSS layout; trailing bytes are per-character.
#include "src/main/boss/template_state.hpp"

extern boss_template_state_t boss_character_template[PLAYER_COUNT];

extern int boss_center_x;
extern int boss_center_y;
extern int boss_hp;
extern sprite16_offset_t boss_sprite_offset;
extern unsigned char boss_hit;
extern unsigned char boss_mode;
extern unsigned char boss_angle;
extern unsigned char boss_pattern_i;
extern unsigned char boss_pattern_count;
extern unsigned char boss_render_mode;
extern unsigned char boss_render_frame;
extern unsigned char boss_move_phase;
extern int boss_effect_radius;
extern unsigned int boss_frame;

// Chiyuri's seven level-derived parameters, all mapped onto the historical
// shared parameter scratch bytes.
extern unsigned char chiyuri_cardinal_speed;
extern unsigned char chiyuri_cardinal_interval;
extern unsigned char chiyuri_ring_speed;
extern unsigned char chiyuri_ring_interval;
extern unsigned char chiyuri_trail_speed;
extern unsigned char chiyuri_fan_speed;
extern unsigned char chiyuri_fan_count;

// Chiyuri-private direction state in the historical player-state tail.
extern unsigned char chiyuri_cardinal_angle;
extern unsigned char chiyuri_cardinal_reverse;

// Two overlapping word views of five historical x/y pairs at DATA
// 1D56:08D6 and 1D56:08D8. The original code doubles the 0..4 random index
// before using it as a word-array index, yielding a four-byte pair stride.
extern int chiyuri_boss_x_words[];
extern int chiyuri_boss_y_words[];

extern int SinTable8[256];
extern int CosTable8[256];

extern "C" {
void far pascal bomb_palette_step(int level, pid_t pid);
void far pascal palette_restore_for_pid(pid_t pid);
void far pascal bomb_center_add(int x, int y, int pid);
void far pascal bomb_axis_add(int x, int y, int pid);
}

// The shared BOSS scheduler draws byte modes 2..17; Chiyuri's
// pattern grouping and the intro/descend behavior are character-specific.
enum chiyuri_boss_mode_t {
    CHIYURI_MODE_INTRO = 0x00,
    CHIYURI_MODE_SELECT = 0x01,
    CHIYURI_MODE_CARDINAL_0 = 0x02,
    CHIYURI_MODE_CARDINAL_1 = 0x03,
    CHIYURI_MODE_CARDINAL_2 = 0x04,
    CHIYURI_MODE_CARDINAL_3 = 0x05,
    CHIYURI_MODE_RINGS_0 = 0x06,
    CHIYURI_MODE_RINGS_1 = 0x07,
    CHIYURI_MODE_RINGS_2 = 0x08,
    CHIYURI_MODE_RINGS_3 = 0x09,
    CHIYURI_MODE_TRAIL_0 = 0x0A,
    CHIYURI_MODE_TRAIL_1 = 0x0B,
    CHIYURI_MODE_TRAIL_2 = 0x0C,
    CHIYURI_MODE_TRAIL_3 = 0x0D,
    CHIYURI_MODE_FANS_0 = 0x0E,
    CHIYURI_MODE_FANS_1 = 0x0F,
    CHIYURI_MODE_FANS_2 = 0x10,
    CHIYURI_MODE_FANS_3 = 0x11,
    CHIYURI_MODE_DESCEND = 0x80,
    CHIYURI_MODE_EXPLODE = 0xFF,
};

// The 16-bit frame and 8-bit render-state gates describe one whole
// Chiyuri BOSS lifecycle, not a shared timer for all nine characters.
enum chiyuri_lifecycle_t {
    CHIYURI_PATTERN_END_AT = 0x80,
    CHIYURI_INTRO_CROSS_EFFECT_FRAME = 0x50,
    CHIYURI_INTRO_DONE_FRAME = 0x60,
    CHIYURI_SELECT_TIME_AT = 0x30,
    CHIYURI_PALETTE_CYCLE_START = 0x10,
    CHIYURI_POST_ATTACK_PALETTE = 0x20,
    CHIYURI_INTRO_RENDER_FIRST_END = 0x20,
    CHIYURI_INTRO_RENDER_SECOND_END = 0x40,
    CHIYURI_INTRO_RENDER_LAST_END = 0x40,
    CHIYURI_MONO_WHITE_STEP = 4,
    CHIYURI_MONO_COLOR5_STEP = 8,
    CHIYURI_MONO_COLOR2_STEP = 0x0C,
    CHIYURI_MONO_COLOR5_LATE_STEP = 0x14,
    CHIYURI_MONO_COLOR6_LATE_STEP = 0x18,
};

// The original 16-bit frame uses natural %8 trail warnings and %4 sprite
// animation clocks. The mutable byte render frame still needs its original
// &=3 instructions, proven distinct from byte-memory %=4 in TC4.
enum chiyuri_boss_cadence_t {
    CHIYURI_RENDER_ANIM_PERIOD = 4,
    CHIYURI_RING_SPRITES = 16,
    CHIYURI_RING_SPRITE_ANGLE_STEP = 0x10,
    CHIYURI_COLLISION_STRIPE_WIDTH = 64,
    CHIYURI_COLLISION_TILE_HEIGHT = 48,
    CHIYURI_COLLISION_HALF_RADIUS = TO_SP(32),
    CHIYURI_RENDER_MAIN_WIDTH = 128,
    CHIYURI_RENDER_MAIN_HEIGHT = 64,
    CHIYURI_RENDER_HIT_WIDTH = 48,
    CHIYURI_RENDER_HIT_HEIGHT = 40,
    CHIYURI_RENDER_ANIM_WIDTH = 32,
    CHIYURI_RENDER_ANIM_HEIGHT = 24,
    CHIYURI_RENDER_HIT_SPRITE_DELTA = 0x778,
    CHIYURI_RENDER_ANIM_SPRITE_BASE = 0x0C,
    CHIYURI_CARDINAL_FIRST_FRAME = 1,
    CHIYURI_CARDINAL_FORWARD_END = 0x20,
    CHIYURI_CARDINAL_REVERSE_END = 0xE4,
    CHIYURI_CARDINAL_QUARTER_TURN = 0x40,
    CHIYURI_CARDINAL_STEP = 8,
    CHIYURI_RING_RADIUS_SCALE = 16,
    CHIYURI_INTRO_RADIUS_SHIFT = 3,
    CHIYURI_RING_SPRITE_WIDTH = 32,
    CHIYURI_RING_SPRITE_HEIGHT = 16,
    CHIYURI_RING_SPRITE_OFFSET = 0x790,
    CHIYURI_RING_SPRITE_ANIM_SCALE = 4,
    CHIYURI_INTRO_RADIUS_FIRST = 0x100,
    CHIYURI_INTRO_RADIUS_SECOND = 0x200,
    CHIYURI_INTRO_RADIUS_FINAL = 0x300,
};

enum chiyuri_template_layout_t {
    CHIYURI_TEMPLATE_CENTER_X = 0x900,
    CHIYURI_TEMPLATE_CENTER_Y = 0x500,
    CHIYURI_TEMPLATE_VELOCITY_X = -0x20,
    CHIYURI_TEMPLATE_HP = 0x8C,
    CHIYURI_TEMPLATE_SPRITE_OFF = 0x288,
    CHIYURI_TEMPLATE_PLAYER2_OFF = 0x28,
};

enum chiyuri_render_mode_t {
    CHIYURI_RENDER_MODE_NORMAL = 0,
};

enum chiyuri_render_placement_t {
    CHIYURI_RENDER_MAIN_LEFT_HALF = 64,
    CHIYURI_RENDER_MAIN_TOP_OFF = 48,
    CHIYURI_RENDER_HIT_LEFT_OFF = 48,
    CHIYURI_RENDER_HIT_TOP_OFF = 32,
};

void far pascal boss_chiyuri_template_init(int player_id)
{
	boss_template_state_t near *p =
		&boss_character_template[player_id];

	p->center_x = CHIYURI_TEMPLATE_CENTER_X;
	p->center_y = CHIYURI_TEMPLATE_CENTER_Y;
	p->velocity_x = CHIYURI_TEMPLATE_VELOCITY_X;
	p->velocity_y = 0;
	p->angle = 0;
	p->hit = 0;
	p->mode = CHIYURI_MODE_INTRO;
	p->hp = CHIYURI_TEMPLATE_HP;
	p->pattern_i = 0;
	p->move_phase = 0;
	p->effect_radius = 0;
	p->sprite_offset = CHIYURI_TEMPLATE_SPRITE_OFF;
	if(player_id != 0) {
		p->sprite_offset += CHIYURI_TEMPLATE_PLAYER2_OFF;
	}
	p->render_mode = CHIYURI_RENDER_MODE_NORMAL;
}

void near chiyuri_pattern_cardinal(void)
{
	// The unsigned-word frame remainder comparison is native-exact with
	// the natural remainder-first spelling as well (af1013e).
	if((boss_frame % chiyuri_cardinal_interval) == 1) {

	if(boss_frame == CHIYURI_CARDINAL_FIRST_FRAME) {
		pid_t pid_other;

		chiyuri_cardinal_angle = 0xE0;
		chiyuri_cardinal_reverse = 0;
		pid_other = (1 - pid_current);

		bomb_axis_add(
			(boss_center_x - TO_SP(56)), boss_center_y, pid_other
		);
		bomb_axis_add(
			(boss_center_x + TO_SP(56)), boss_center_y, pid_other
		);
		bomb_axis_add(
			boss_center_x, (boss_center_y - TO_SP(56)), pid_other
		);
		bomb_axis_add(
			boss_center_x, (boss_center_y + TO_SP(56)), pid_other
		);
	}

	else if(CHIYURI_PATTERN_END_AT <= boss_frame) {
		boss_mode = CHIYURI_MODE_SELECT;
		boss_frame = 0;
		boss_render_mode = CHIYURI_POST_ATTACK_PALETTE;
	}

	bullet_template.type = BT_PELLET;
	bullet_template.group = BG_1;
	bullet_template.speed.v = chiyuri_cardinal_speed;

	if(!chiyuri_cardinal_reverse) {
		// Named compound byte-angle steps preserve the original CODE
		// in both directions (af1013a).
		chiyuri_cardinal_angle += CHIYURI_CARDINAL_STEP;
		if(chiyuri_cardinal_angle == CHIYURI_CARDINAL_FORWARD_END) {
			chiyuri_cardinal_reverse = 1;
			chiyuri_cardinal_angle = 0x24;
		}
	} else {
		chiyuri_cardinal_angle -= CHIYURI_CARDINAL_STEP;
		if(chiyuri_cardinal_angle == CHIYURI_CARDINAL_REVERSE_END) {
			chiyuri_cardinal_reverse = 0;
			chiyuri_cardinal_angle = 0xE0;
		}
	}

	bullet_template.center.x.v = (boss_center_x + TO_SP(56));
	bullet_template.center.y.v = boss_center_y;
	bullet_template.angle = chiyuri_cardinal_angle;
	bullets_add();

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = (boss_center_y + TO_SP(56));
	// Each 90-degree compound rotation stays after the previous bullet
	// call; all three named updates are TC4-exact (af1013b).
	bullet_template.angle += CHIYURI_CARDINAL_QUARTER_TURN;
	bullets_add();

	bullet_template.center.x.v = (boss_center_x - TO_SP(56));
	bullet_template.center.y.v = boss_center_y;
	bullet_template.angle += CHIYURI_CARDINAL_QUARTER_TURN;
	bullets_add();

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = (boss_center_y - TO_SP(56));
	bullet_template.angle += CHIYURI_CARDINAL_QUARTER_TURN;
	bullets_add();
	}
}

void near chiyuri_pattern_rings(void)
{
	// This distinct ring cadence also allows natural comparison order.
	if((boss_frame % chiyuri_ring_interval) == 1) {

	bomb_axis_add(
		boss_center_x, boss_center_y, (1 - pid_current)
	);

	if(CHIYURI_PATTERN_END_AT <= boss_frame) {
		boss_mode = CHIYURI_MODE_SELECT;
		boss_frame = 0;
		boss_render_mode = CHIYURI_POST_ATTACK_PALETTE;
	}

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = boss_center_y;
	bullet_template.angle = randring_far_next16();
	bullet_template.type = BT_BULLET16_DEFAULT;
	bullet_template.group = BG_32_RING;
	bullet_template.speed.v = chiyuri_ring_speed;
	bullets_add();

	if(gba_boss_level < 8) {
		return;
	}

	bullet_template.type = BT_PELLET;
	bullet_template.group = BG_8_RING;
	bullet_template.speed.v = (chiyuri_ring_speed / 4);

	bullet_template.center.x.v = (boss_center_x + TO_SP(56));
	bullets_add();
	bullet_template.center.x.v = (boss_center_x - TO_SP(56));
	bullets_add();

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = (boss_center_y + TO_SP(56));
	bullets_add();
	bullet_template.center.y.v = (boss_center_y - TO_SP(56));
	bullets_add();
	}
}

// Bomb warnings repeat every eight ticks before the single 48-shot
// trailing ring is released at the original 0x30 frame.
enum chiyuri_trail_phase_t {
    CHIYURI_TRAIL_BOMB_PERIOD = 8,
    CHIYURI_TRAIL_FIRE_FRAME = 0x30,
};

void near chiyuri_pattern_trail_ring(void)
{
	// The unsigned 16-bit eight-frame cadence is a natural low-bit test.
	// This does not generalize to byte %=4 on the mutable render frame.
	if((boss_frame & (CHIYURI_TRAIL_BOMB_PERIOD - 1)) == 0) {
		bomb_axis_add(
			boss_center_x, boss_center_y, (1 - pid_current)
		);
	}

	if(CHIYURI_TRAIL_FIRE_FRAME == boss_frame) {

	bullet_template.center.x.v = boss_center_x;
	bullet_template.center.y.v = boss_center_y;
	bullet_template.angle = randring_far_next16();
	bullet_template.type = BT_BULLET16_DEFAULT;
	bullet_template.group = BG_RING;
	bullet_template.count = 48;
	bullet_template.speed.v = chiyuri_trail_speed;
	bullet_template.has_trail = true;
	bullets_add();
	bullet_template.has_trail = false;

	boss_mode = CHIYURI_MODE_SELECT;
	boss_frame = 0;
	boss_render_mode = CHIYURI_POST_ATTACK_PALETTE;
	}
}

// The horizontal fans fire at 0x20 and vertical fans at 0x40;
// both retain separate ascending/descending bullet velocity passes.
enum chiyuri_fan_phase_t {
    CHIYURI_FAN_HORIZONTAL_FRAME = 0x20,
    CHIYURI_FAN_VERTICAL_FRAME = 0x40,
    CHIYURI_FAN_SPAN_PIXELS = 0x70,
    CHIYURI_FAN_ANGLE_UNITS = 64,
    CHIYURI_FAN_HORIZ_ANGLE_BASE = 0x60,
    CHIYURI_FAN_VERT_ANGLE_OFFSET = 0x20,
    CHIYURI_FAN_SPEED_STEP = 2,
    CHIYURI_FAN_SPAN_TO_SUBPIXELS = 16,
};

// The fan coordinates divide the 16-bit polar range BEFORE scaling
// to subpixels. Natural C++ multiplication is original-native here;
// changing the division order would change trajectory rounding.
// All four fan passes now use native-exact natural C++ for loops;
// original signed 16-bit count, division-before-scale, RNG and dual
// bullets_add call ordering are preserved (af872a). The earlier native
// `speed += enum` trial failed; fresh af922h proves that explicit
// `speed = speed +/- NAMED_STEP` is byte exact for all four fan passes.
void near chiyuri_pattern_fans(void)
{
	pid_t pid_other = (1 - pid_current);
	register int i;

	if(CHIYURI_FAN_HORIZONTAL_FRAME == boss_frame) {
		bomb_axis_add(
			(boss_center_x - TO_SP(56)), boss_center_y, pid_other
		);
		bomb_axis_add(
			(boss_center_x + TO_SP(56)), boss_center_y, pid_other
		);

		bullet_template.center.y.v = boss_center_y;
		bullet_template.group = BG_1;
		bullet_template.type = BT_PELLET;
		bullet_template.speed.v = chiyuri_fan_speed;

		for(i = 0; i < chiyuri_fan_count; i++) {
			bullet_template.center.x.v = (
				boss_center_x -
				TO_SP(56) +
				(((i * CHIYURI_FAN_SPAN_PIXELS) / chiyuri_fan_count) * CHIYURI_FAN_SPAN_TO_SUBPIXELS)
			);
			bullet_template.angle = (
				CHIYURI_FAN_HORIZ_ANGLE_BASE - ((i * CHIYURI_FAN_ANGLE_UNITS) / chiyuri_fan_count)
			);
			bullets_add();

			bullet_template.angle = (0 - bullet_template.angle);
			bullets_add();

			// Explicit byte speed assignment + named step is exact (af922h).
			bullet_template.speed.v = bullet_template.speed.v + CHIYURI_FAN_SPEED_STEP;
		}

		for(i = 0; i < chiyuri_fan_count; i++) {
			bullet_template.center.x.v = (
				boss_center_x -
				TO_SP(56) +
				(((i * CHIYURI_FAN_SPAN_PIXELS) / chiyuri_fan_count) * CHIYURI_FAN_SPAN_TO_SUBPIXELS)
			);
			bullet_template.angle = (
				CHIYURI_FAN_HORIZ_ANGLE_BASE - ((i * CHIYURI_FAN_ANGLE_UNITS) / chiyuri_fan_count)
			);
			bullets_add();

			bullet_template.angle = (0 - bullet_template.angle);
			bullets_add();

			bullet_template.speed.v = bullet_template.speed.v - CHIYURI_FAN_SPEED_STEP;
		}
		return;
	}

	if(CHIYURI_FAN_VERTICAL_FRAME == boss_frame) {
	bomb_axis_add(
		boss_center_x, (boss_center_y - TO_SP(56)), pid_other
	);
	bomb_axis_add(
		boss_center_x, (boss_center_y + TO_SP(56)), pid_other
	);

	bullet_template.center.x.v = boss_center_x;
	bullet_template.type = BT_PELLET;
	bullet_template.group = BG_2_SPREAD_HORIZONTALLY_SYMMETRIC;
	bullet_template.speed.v = chiyuri_fan_speed;

	for(i = 0; i < chiyuri_fan_count; i++) {
		bullet_template.center.y.v = (
			boss_center_y -
			TO_SP(56) +
			(((i * CHIYURI_FAN_SPAN_PIXELS) / chiyuri_fan_count) * CHIYURI_FAN_SPAN_TO_SUBPIXELS)
		);
		bullet_template.angle = (
			((i * CHIYURI_FAN_ANGLE_UNITS) / chiyuri_fan_count) - CHIYURI_FAN_VERT_ANGLE_OFFSET
		);
		bullets_add();

		bullet_template.speed.v = bullet_template.speed.v + CHIYURI_FAN_SPEED_STEP;
	}

	for(i = 0; i < chiyuri_fan_count; i++) {
		bullet_template.center.y.v = (
			boss_center_y -
			TO_SP(56) +
			(((i * CHIYURI_FAN_SPAN_PIXELS) / chiyuri_fan_count) * CHIYURI_FAN_SPAN_TO_SUBPIXELS)
		);
		bullet_template.angle = (
			((i * CHIYURI_FAN_ANGLE_UNITS) / chiyuri_fan_count) - CHIYURI_FAN_VERT_ANGLE_OFFSET
		);
		bullets_add();

		bullet_template.speed.v = bullet_template.speed.v - CHIYURI_FAN_SPEED_STEP;
	}

	boss_mode = CHIYURI_MODE_SELECT;
	boss_frame = 0;
	boss_render_mode = CHIYURI_POST_ATTACK_PALETTE;
	}
}

void far gba_boss_update_chiyuri(void)
{
	pid_t pid_other;
	register unsigned char random_i;

	if(boss_update_start()) {
		chiyuri_cardinal_speed = (gba_boss_level + 0x30);
		chiyuri_cardinal_interval = (6 - (gba_boss_level / 4));
		chiyuri_ring_speed = (gba_boss_level + 0x34);
		chiyuri_ring_interval = (0x20 - gba_boss_level);
		chiyuri_trail_speed = ((gba_boss_level * 2) + 0x38);
		chiyuri_fan_speed = (gba_boss_level + 0x10);
		chiyuri_fan_count = ((gba_boss_level / 2) + 0x0C);
	}

	if(pid_current != gba_boss_launched_by) {
		return;
	}

	pid_other = (1 - pid_current);
	boss_target_update();
	bullet_template.is_animated = false;
	bullet_template.pid = pid_other;
	// The original unsigned-word BOSS frame admits natural prefix;
	// byte-valued movement state below does not (af922j/k).
	++boss_frame;

	switch(boss_mode) {
	case CHIYURI_MODE_INTRO:
		if(boss_frame == CHIYURI_INTRO_DONE_FRAME) {
			boss_frame = 0;
			boss_mode = CHIYURI_MODE_SELECT;
			bomb_palette_step(0xFF, pid_other);
			boss_move_phase = CHIYURI_PALETTE_CYCLE_START;
			boss_render_mode = CHIYURI_PALETTE_CYCLE_START;
			break;
		} else if(boss_frame == CHIYURI_INTRO_CROSS_EFFECT_FRAME) {
			bomb_center_add(
				(boss_center_x - TO_SP(56)), boss_center_y, pid_other
			);
			bomb_center_add(
				(boss_center_x + TO_SP(56)), boss_center_y, pid_other
			);
			bomb_center_add(
				boss_center_x, (boss_center_y - TO_SP(56)), pid_other
			);
			bomb_center_add(
				boss_center_x, (boss_center_y + TO_SP(56)), pid_other
			);
			break;
		} else {
			bullet_template.is_animated = true;
			return;
		}

	case CHIYURI_MODE_SELECT:
		if(CHIYURI_PALETTE_CYCLE_START == boss_render_mode) {
			random_i = (randring_far_next16_mod(5) * 2);
			boss_center_x = chiyuri_boss_x_words[random_i];
			boss_center_y = chiyuri_boss_y_words[random_i];
			boss_move_phase = CHIYURI_PALETTE_CYCLE_START;
		}
		if(CHIYURI_SELECT_TIME_AT <= boss_frame) {
			boss_frame = 0;
			boss_mode = (randring_far_next16_and(0x0F) + 2);
			boss_pattern_i++;
			if(boss_pattern_i > boss_pattern_count) {
				boss_mode = CHIYURI_MODE_DESCEND;
			}
		}
		break;

	case CHIYURI_MODE_CARDINAL_0:
	case CHIYURI_MODE_CARDINAL_1:
	case CHIYURI_MODE_CARDINAL_2:
	case CHIYURI_MODE_CARDINAL_3:
		chiyuri_pattern_cardinal();
		break;

	case CHIYURI_MODE_RINGS_0:
	case CHIYURI_MODE_RINGS_1:
	case CHIYURI_MODE_RINGS_2:
	case CHIYURI_MODE_RINGS_3:
		chiyuri_pattern_rings();
		break;

	case CHIYURI_MODE_TRAIL_0:
	case CHIYURI_MODE_TRAIL_1:
	case CHIYURI_MODE_TRAIL_2:
	case CHIYURI_MODE_TRAIL_3:
		chiyuri_pattern_trail_ring();
		break;

	case CHIYURI_MODE_FANS_0:
	case CHIYURI_MODE_FANS_1:
	case CHIYURI_MODE_FANS_2:
	case CHIYURI_MODE_FANS_3:
		chiyuri_pattern_fans();
		break;

	case CHIYURI_MODE_DESCEND:
		boss_fall();
		palette_restore_for_pid(pid_other);
		break;

	case CHIYURI_MODE_EXPLODE:
		bullet_template.is_animated = true;
		return;
	}

	bullet_template.is_animated = true;

	boss_render_frame += (
        (round_or_result_frame & (CHIYURI_RENDER_ANIM_PERIOD - 1)) == 0
    );
	// This mutable byte field needs the original bitmask instruction:
	// boss_render_frame %= 4 emitted different TC4 CODE (af702a).
	// Preserve the original byte-memory mask, NOT %=4 (af922i).
	boss_render_frame &= (CHIYURI_RENDER_ANIM_PERIOD - 1);

	if(boss_move_phase) {
		// The original postfix byte decrement is CODE-visible; prefix
		// --boss_move_phase was native-unequal (af702d).
		// Preserve the byte postfix: prefix changed TC4 CODE (af922k).
		boss_move_phase--;
		if(boss_move_phase) {
			bomb_palette_step((boss_move_phase * 16), pid_other);
		}
	}

	if(boss_render_mode) {
		boss_render_mode--;
	}

	collmap_center.x.v = boss_center_x;
	collmap_center.y.v = boss_center_y;
	collmap_stripe_tile_w.set(CHIYURI_COLLISION_STRIPE_WIDTH);
	collmap_tile_h.set(CHIYURI_COLLISION_TILE_HEIGHT);
	collmap_pid = pid_other;
	collmap_set_rect_striped();

	hitbox_hittest_skip_explosions = true;
	hitbox.radius.x.v = CHIYURI_COLLISION_HALF_RADIUS;
	hitbox.radius.y.v = CHIYURI_COLLISION_HALF_RADIUS;
	hitbox.pid = pid_other;
	hitbox.origin.center.x.v = boss_center_x;
	hitbox.origin.center.y.v = boss_center_y;
	boss_hit = hitbox_hittest();
	boss_hp -= boss_hit;
	hitbox_hittest_skip_explosions = false;
	boss_hittest_end();
}

// Natural signed 16-bit radius and sprite-frame shifts remain exact.
// The original two-carrier 16-sprite ring now uses a natural for-header.
// Its update advances the signed index before the byte-angle assignment;
// enum-valued compound += still shortens the original byte-reg update.
void near chiyuri_render_ring(void)
{
	screen_y_t top;
	sprite16_offset_t sprite_offset;
	int pid_other;
	int radius;
	unsigned char angle;
	register int i;

	pid_other = (1 - pid_current);
	radius = (boss_effect_radius * CHIYURI_RING_RADIUS_SCALE);

	sprite16_put_size.w = CHIYURI_RING_SPRITE_WIDTH;
	sprite16_put_size.h = CHIYURI_RING_SPRITE_HEIGHT;

	sprite_offset = (boss_sprite_offset + CHIYURI_RING_SPRITE_OFFSET);
	sprite_offset += (boss_render_frame * CHIYURI_RING_SPRITE_ANIM_SCALE);

	for(
		i = 0, angle = boss_move_phase;
		i < CHIYURI_RING_SPRITES;
		++i, angle = angle + CHIYURI_RING_SPRITE_ANGLE_STEP
	) {
		register screen_x_t left;
		left = polar(
			boss_center_x, radius, CosTable8[angle]
		);
		top = polar(
			boss_center_y, radius, SinTable8[angle]
		);
		left = (playfield_fg_x_to_screen(left, pid_other) - 16);
		// Natural signed coordinate conversion replaces manual _AX
		// loading/shifting/storing. A compound >>= on top generated
		// different TC4 CODE (native negative trial af759b).
		top = static_cast<screen_y_t>(top >> 4);
		sprite16_put(left, top, sprite_offset);
	}
}

void near pascal chiyuri_render_mono(int color);

void near chiyuri_render_main(void)
{
	screen_y_t top;
	register sprite16_offset_t sprite_offset;
	register screen_x_t left;

	if(!boss_render_mode) {
		sprite16_put_size.w = CHIYURI_RENDER_MAIN_WIDTH;
		sprite16_put_size.h = CHIYURI_RENDER_MAIN_HEIGHT;

		left = (
			playfield_fg_x_to_screen(
				boss_center_x, (1 - pid_current)
			) - CHIYURI_RENDER_MAIN_LEFT_HALF
		);
		top = ((boss_center_y >> 4) - CHIYURI_RENDER_MAIN_TOP_OFF);
		sprite_offset = boss_sprite_offset;
		sprite16_put(left, top, sprite_offset);

		left += CHIYURI_RENDER_HIT_LEFT_OFF;
		top += CHIYURI_RENDER_HIT_TOP_OFF;

		if(boss_hit) {
			sprite16_put_size.w = CHIYURI_RENDER_HIT_WIDTH;
			sprite16_put_size.h = CHIYURI_RENDER_HIT_HEIGHT;
			sprite_offset += CHIYURI_RENDER_HIT_SPRITE_DELTA;
			sprite16_put(left, top, sprite_offset);
			return;
		}

		if(!boss_render_frame) {
			return;
		}

		sprite16_put_size.w = CHIYURI_RENDER_ANIM_WIDTH;
		sprite16_put_size.h = CHIYURI_RENDER_ANIM_HEIGHT;
		sprite_offset += ((boss_render_frame * CHIYURI_RENDER_ANIM_PERIOD) + CHIYURI_RENDER_ANIM_SPRITE_BASE);
		sprite16_put(left, top, sprite_offset);
		return;
	}

	else if(boss_render_mode >= CHIYURI_MONO_COLOR6_LATE_STEP) {
		chiyuri_render_mono(6);
	} else if(boss_render_mode >= CHIYURI_MONO_COLOR5_LATE_STEP) {
		chiyuri_render_mono(5);
	} else if(boss_render_mode >= CHIYURI_MONO_COLOR2_STEP) {
		chiyuri_render_mono(2);
	} else if(boss_render_mode >= CHIYURI_MONO_COLOR5_STEP) {
		chiyuri_render_mono(5);
	} else if(boss_render_mode >= CHIYURI_MONO_WHITE_STEP) {
		chiyuri_render_mono(6);
	} else {
		chiyuri_render_mono(V_WHITE);
	}
}

void near chiyuri_render_intro(void)
{
	register int frame;

	if(round_frame_mod2 && (boss_frame < CHIYURI_INTRO_RENDER_LAST_END)) {
		return;
	}

	// TC4 compiles the signed frame << 3 to the original shift. The
	// adjacent byte phase updates still require their AL expression:
	// direct +=4, =phase+4 and -=4 changed original native code.
	frame = boss_frame;
	// The three raster phases are separate signed 16-bit origin radii;
	// keep each original byte phase update in the original AL carrier.
	if(frame < CHIYURI_INTRO_RENDER_FIRST_END) {
		boss_effect_radius = (
            CHIYURI_INTRO_RADIUS_FIRST -
            (frame << CHIYURI_INTRO_RADIUS_SHIFT)
        );
		_AL = boss_move_phase;
		_AL += 4;
		boss_move_phase = _AL;
	} else if(frame < CHIYURI_INTRO_RENDER_SECOND_END) {
		boss_effect_radius = (
            CHIYURI_INTRO_RADIUS_SECOND -
            (frame << CHIYURI_INTRO_RADIUS_SHIFT)
        );
		_AL = boss_move_phase;
		_AL += (unsigned char)0xFC;
		boss_move_phase = _AL;
	} else {
		boss_effect_radius = (
            CHIYURI_INTRO_RADIUS_FINAL -
            (frame << CHIYURI_INTRO_RADIUS_SHIFT)
        );
		_AL = boss_move_phase;
		_AL += 4;
		boss_move_phase = _AL;
	}

	chiyuri_render_ring();
}

void near pascal chiyuri_render_mono(int color)
{
	screen_x_t left;
	screen_y_t top;
	sprite16_offset_t sprite_offset;

	sprite16_put_size.w = CHIYURI_RENDER_MAIN_WIDTH;
	sprite16_put_size.h = CHIYURI_RENDER_MAIN_HEIGHT;

	left = (
		playfield_fg_x_to_screen(
			boss_center_x, (1 - pid_current)
		) - 64
	);
	top = ((boss_center_y >> 4) - 48);
	sprite_offset = boss_sprite_offset;

	_AH = SPRITE16_SET_MONO;
	_DX = 1;
	geninterrupt(SPRITE16);
	_AH = SPRITE16_SET_COLOR;
	_DX = color;
	geninterrupt(SPRITE16);
	sprite16_put(left, top, sprite_offset);
	_AH = SPRITE16_SET_MONO;
	asm { xor dx, dx }
	geninterrupt(SPRITE16);
}

void far gba_boss_render_chiyuri(void)
{
	if(pid_current != gba_boss_launched_by) {
		return;
	}

	sprite16_clip_set_for_pid(1 - pid_current);

	if(boss_mode == CHIYURI_MODE_INTRO) {
		chiyuri_render_intro();
		return;
	}
	if(boss_mode != CHIYURI_MODE_EXPLODE) {
		chiyuri_render_main();
		return;
	}

	boss_explosion_render();
	if(gba_boss_launched_by == PID_NONE) {
		palette_restore_for_pid(1 - pid_current);
	}
}
