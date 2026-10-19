#ifndef TH03_MAIN_PLAYER_CPU_PROPOSAL_HPP
#define TH03_MAIN_PLAYER_CPU_PROPOSAL_HPP

#include <stddef.h>
#pragma option -a1
#include "src/main/player/stuff.hpp"
#pragma option -a2
#include "src/main/player/move.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/round.hpp"

// Existing storage only. The first array's outer bound is deliberately open:
// row stride is proved, but this proposal does not claim the whole DATA owner.
enum { CPU_DIRECTIONS = 9, CPU_RETRY_REGIONS = 3 };
extern input_t cpu_dodge_patterns[][CPU_DIRECTIONS];
extern input_t cpu_retry_directions[CPU_RETRY_REGIONS][CPU_DIRECTIONS];
extern input_t near *cpu_dodge_pattern;
extern int ellen_target_x;
extern int ellen_target_y;

extern "C" {
void far pascal ellen_target_set(pid_t player);
void near pascal player_bomb(player_stuff_t near *player);
}

input_t near pascal player_cpu_direction_for_collision(
    subpixel_t collision_y_relative, subpixel_t player_x, subpixel_t player_y
);
void near pascal player_cpu_approach_target(player_stuff_t near *player);
void near pascal player_cpu_update(player_stuff_t near *player);
void near pascal player_cpu_dodge_and_aim(player_stuff_t near *player);

#define CPU_FIELD(field, offset, bytes) \
    typedef char cpu_field_##field[ \
        (offsetof(player_stuff_t, field) == offset && \
         sizeof(((player_stuff_t near *)0)->field) == bytes) ? 1 : -1]
CPU_FIELD(center, 0x00, 4);
CPU_FIELD(is_hit, 0x04, 1);
CPU_FIELD(cpu_dodge_strategy, 0x16, 1);
CPU_FIELD(gauge_charged, 0x18, 2);
CPU_FIELD(cpu_safety_frames, 0x6E, 2);
CPU_FIELD(cpu_frame, 0x74, 2);
#undef CPU_FIELD

typedef char cpu_record_size[(sizeof(player_stuff_t) == 0x80) ? 1 : -1];
typedef char cpu_point_y[(offsetof(PlayfieldPoint, y) == 2) ? 1 : -1];
typedef char cpu_word_widths[(sizeof(input_t) == 2 && sizeof(subpixel_t) == 2 &&
    sizeof(int) == 2 && sizeof(cpu_dodge_pattern) == 2) ? 1 : -1];
typedef char cpu_byte_pid[(sizeof(pid.current) == 1) ? 1 : -1];
typedef char cpu_signed_byte[(sizeof(int8_t) == 1 && int8_t(-1) < 0) ? 1 : -1];
#endif
