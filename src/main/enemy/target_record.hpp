#ifndef TH03_TARGET_ENEMY_RECORD_PROPOSAL_HPP
#define TH03_TARGET_ENEMY_RECORD_PROPOSAL_HPP
#include "compat/rec98/th03/main/enemy/efe.hpp"

// Position flags
// --------------

typedef uint8_t enemy_pos_type_t;

// Clips the enemy at the left and right edges of the playfield.
static const enemy_pos_type_t EPT_CLIP_X = 0x01;

// Clips the enemy at the bottom edge of the playfield.
static const enemy_pos_type_t EPT_CLIP_BOTTOM = 0x02;

// If set, horizontal spawn positions and movement velocities are applied as
// given in the script. If not set, they are horizontally mirrored. (Yes, this
// would have been easier to describe if it were the other way round.)
static const enemy_pos_type_t EPT_DO_NOT_MIRROR_X = 0x80;
// --------------

// Entity flags
// ------------

// Script is running and has spawned its enemy
static const efe_flag_t EF_RUNNING_SPAWNED = 1;

// Script is running and hasn't spawned its enemy
static const efe_flag_t EF_RUNNING_UNSPAWNED = 3;
// ------------

struct enemy_t {
	efe_flag_t flag;
	uint8_t frame;
	PlayfieldPoint center;
	uint8_t explosion_max_enemy_hits_half;
	uint8_t hp;
	pid_t pid;
	pixel_length_8_t size_pixels; // Also controls the hitbox size
	uint16_t script_ip; // Offset from [script_base]
	uint16_t script_op_frame;
	uint8_t near *script_base; // Pointer to first script instruction
	SPPoint velocity;
	int8_t unused_1[4];

	// 16-bit angles!
	// ZUN landmine: Should be a single 16-bit variable instead of a `union`
	// to not break on big-endian systems.
	union {
		uint16_t wide;
		struct {
			unsigned char fine;
			unsigned char coarse;
		} split;
	} angle;

	int8_t angle_speed;
	int8_t unused_2;
	uint8_t chain_slot;
	uint8_t formation_type;
	uint8_t formation_i; // ID of this enemy within its formation
	subpixel_length_8_t speed;

	// Current loop counter for the (broken) [EO_LOOP_*] instructions.
	uint8_t loop_i;

	enemy_pos_type_t pos_type;
	int8_t padding[14];

	// Sprite size in 16-pixel units. 0 = invalid.
	// ZUN bloat: Fully redundant with [size_pixels]. The code should
	// explicitly assign [explosion_max_enemy_hits_half] in the [EO_SPAWN]
	// handler and then use [size_pixels] everywhere else.
	uvram_word_amount_8_t& size_words(void) {
		return static_cast<uvram_word_amount_8_t>(
			explosion_max_enemy_hits_half
		);
	}
};

inline void enemy_t_verify(void) {
	efe_subclass_verify(reinterpret_cast<enemy_t *>(nullptr));
}


typedef char target_enemy_size_check[(sizeof(enemy_t) == 0x30) ? 1 : -1];
typedef char target_enemy_formation_check[(offsetof(enemy_t, formation_i) == 0x1E) ? 1 : -1];
typedef char target_enemy_center_check[(offsetof(enemy_t, center) == 2) ? 1 : -1];
typedef char target_enemy_pid_check[(offsetof(enemy_t, pid) == 8) ? 1 : -1];
static const int TARGET_ENEMY_COUNT = 40;
#endif
