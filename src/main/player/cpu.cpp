// Target-derived CPU strategies; retained native proof is source-present only.
#pragma codeseg PLAYER_M_TEXT main_01
#pragma option -G
#include "src/main/player/cpu.hpp"
#include "src/main/math/randring_getters.hpp"

enum cpu_target_flags_t {
    CPU_TARGET_LEFT = 1,
    CPU_TARGET_RIGHT = 2,
    CPU_TARGET_UP = 4,
    CPU_TARGET_DOWN = 8,
};

// Collision avoidance samples a real 3x3 direction lookup: the
// first row is an approaching obstacle above the player, not a
// target-location coordinate. Indices are row-major in the original.
enum cpu_dodge_lookup_t {
    CPU_DODGE_ABOVE_RIGHT = 0,
    CPU_DODGE_ABOVE_MIDDLE = 1,
    CPU_DODGE_ABOVE_LEFT = 2,
    CPU_DODGE_NEAR_RIGHT = 3,
    CPU_DODGE_NEAR_MIDDLE = 4,
    CPU_DODGE_NEAR_LEFT = 5,
    CPU_DODGE_BELOW_RIGHT = 6,
    CPU_DODGE_BELOW_MIDDLE = 7,
    CPU_DODGE_BELOW_LEFT = 8,
};
enum cpu_retry_column_t {
    CPU_RETRY_LEFT_COLUMN = 0,
    CPU_RETRY_MIDDLE_COLUMN = 1,
    CPU_RETRY_RIGHT_COLUMN = 2,
};

// CPU movement geometry and reaction thresholds are in original 16-bit
// subpixels, not screen pixels. Keep the branch sequence and RNG draws.
enum cpu_response_threshold_t {
    CPU_DODGE_RIGHT_EDGE = TO_SP(240),
    CPU_DODGE_LEFT_EDGE = TO_SP(16),
    CPU_DODGE_LOW_FIELD = TO_SP(128),
    CPU_DODGE_FLOOR = TO_SP(304),
    CPU_COLLISION_ABOVE_BOUNDARY = -TO_SP(16),
    CPU_COLLISION_NEAR_BOUNDARY = TO_SP(32),
    CPU_TARGET_X_MARGIN = TO_SP(16),
    CPU_TARGET_Y_MARGIN = TO_SP(80),
    CPU_RETRY_LEFT_LIMIT = TO_SP(80),
    CPU_RETRY_MIDDLE_LIMIT = TO_SP(176),
    CPU_HITTEST_CLOSE_RADIUS = 8 / 2,
    CPU_HITTEST_RETRY_RADIUS = 40 / 2,
    CPU_HIT_BOMB_CHARGE_LIMIT = 0x500,
    CPU_STUCK_BOMB_CHARGE_LIMIT = 0x400,
    CPU_DODGE_ALTERNATIVES = 2,
    CPU_TARGET_RANDOM_REGIONS = 3,
    CPU_HIT_BOMB_RANDOM_PERIOD = 4,
    CPU_COLLISION_SCAN_PERIOD = 4,
    CPU_COLLISION_SIDE_LEFT = -TO_SP(16),
    CPU_COLLISION_SIDE_RIGHT = TO_SP(16),
    CPU_COLLISION_SIDE_COUNT = 3,
    CPU_BOTTOM_ESCAPE_X = TO_SP(128),
};

input_t near pascal player_cpu_direction_for_collision(
    subpixel_t collision_y_relative, subpixel_t player_x, subpixel_t player_y
)
{
    input_t direction;
    if(collision_y_relative < CPU_COLLISION_ABOVE_BOUNDARY) {
        if(player_x >= CPU_DODGE_RIGHT_EDGE) {
            if(player_y >= CPU_DODGE_LOW_FIELD) {
                direction = cpu_dodge_pattern[CPU_DODGE_ABOVE_RIGHT];
            } else {
                direction = INPUT_LEFT;
            }
        } else if(player_x >= CPU_DODGE_LEFT_EDGE) {
            direction = cpu_dodge_pattern[CPU_DODGE_ABOVE_MIDDLE];
        } else if(player_y >= CPU_DODGE_LOW_FIELD) {
            direction = cpu_dodge_pattern[CPU_DODGE_ABOVE_LEFT];
        } else {
            direction = INPUT_RIGHT;
        }
    } else if(collision_y_relative < CPU_COLLISION_NEAR_BOUNDARY) {
        if(player_x >= CPU_DODGE_RIGHT_EDGE) {
            direction = cpu_dodge_pattern[CPU_DODGE_NEAR_RIGHT];
        } else if(player_x >= CPU_DODGE_LEFT_EDGE) {
            direction = cpu_dodge_pattern[CPU_DODGE_NEAR_MIDDLE];
        } else {
            direction = cpu_dodge_pattern[CPU_DODGE_NEAR_LEFT];
        }
    } else {
        if(player_x >= CPU_DODGE_RIGHT_EDGE) {
            direction = cpu_dodge_pattern[CPU_DODGE_BELOW_RIGHT];
        } else if(player_x >= CPU_DODGE_LEFT_EDGE) {
            direction = cpu_dodge_pattern[CPU_DODGE_BELOW_MIDDLE];
        } else {
            direction = cpu_dodge_pattern[CPU_DODGE_BELOW_LEFT];
        }
    }
    if(player_y >= CPU_DODGE_FLOOR && direction == INPUT_DOWN) {
        if(player_x >= CPU_BOTTOM_ESCAPE_X) {
            direction = INPUT_LEFT;
        } else {
            direction = INPUT_RIGHT;
        }
    }
    return direction;
}

void near pascal player_cpu_approach_target(player_stuff_t near *player)
{
    subpixel_t x = player->center.x.v;
    subpixel_t y = player->center.y.v;
    unsigned int random_region;
    unsigned char attempt;
    input_t direction = INPUT_NONE;

    ellen_target_set(pid.current);
    attempt = ((ellen_target_x + CPU_TARGET_X_MARGIN) < x);
    // Preserve the original Boolean shift and OR sequence: an equivalent
    // flag-valued conditional changed TC4 CODE (af838d).
    attempt |= (((ellen_target_x - CPU_TARGET_X_MARGIN) > x) << 1);
    attempt |= (((ellen_target_y + CPU_TARGET_Y_MARGIN) < y) << 2);
    attempt |= ((y < ellen_target_y) << 3);
    switch(attempt) {
    case CPU_TARGET_LEFT: direction = INPUT_LEFT; break;
    case CPU_TARGET_RIGHT: direction = INPUT_RIGHT; break;
    case CPU_TARGET_UP: direction = INPUT_UP; break;
    case CPU_TARGET_DOWN: direction = INPUT_DOWN; break;
    case (CPU_TARGET_UP | CPU_TARGET_LEFT):
        direction = (INPUT_UP | INPUT_LEFT); break;
    case (CPU_TARGET_DOWN | CPU_TARGET_LEFT):
        direction = (INPUT_DOWN | INPUT_LEFT); break;
    case (CPU_TARGET_UP | CPU_TARGET_RIGHT):
        direction = (INPUT_UP | INPUT_RIGHT); break;
    case (CPU_TARGET_DOWN | CPU_TARGET_RIGHT):
        direction = (INPUT_DOWN | INPUT_RIGHT); break;
    }

    // The original consumes a random word and calculates its remainder even
    // though it never reads this local afterward. Keep that observable draw.
    attempt = 0;
    random_region = (randring1_next16() % CPU_TARGET_RANDOM_REGIONS);
    if(player_move(direction) == MOVE_VALID) {
        player_pos_update_and_clamp(player->center);
    }
    player_hittest(CPU_HITTEST_CLOSE_RADIUS);
    if(player->is_hit) {
        player->is_hit = false;
        attempt++;
        if(player->gauge_charged <= CPU_HIT_BOMB_CHARGE_LIMIT && ((randring1_next16() % CPU_HIT_BOMB_RANDOM_PERIOD) == 0)) {
            player_bomb(player);
        } else {
            player->is_hit = true;
        }
    }
}

void near pascal player_cpu_update(player_stuff_t near *player)
{
    // Equality still takes the careful branch; these counters are unsigned.
    if(player->cpu_frame <= player->cpu_safety_frames) {
        player_cpu_dodge_and_aim(player);
    } else {
        player_cpu_approach_target(player);
    }
}

void near pascal player_cpu_dodge_and_aim(player_stuff_t near *player)
{
    subpixel_t collision_x_relative;
    subpixel_t collision_y_relative;
    subpixel_t x = player->center.x.v;
    subpixel_t y = player->center.y.v;
    unsigned char attempt;
    unsigned char retry_region;
    int8_t radius_or_retry;
    input_t direction;

    if((round_or_result_frame % CPU_COLLISION_SCAN_PERIOD) == 0) {
        // Keep the original signed-byte probe loop literals: equivalent
        // enum bounds changed native TC4 output (after646e).
        for(radius_or_retry = (64 / 2); radius_or_retry <= (160 / 2);
            radius_or_retry += (32 / 2)) {
            player_hittest(radius_or_retry);
            if(player->is_hit) {
                break;
            }
        }
    }
    if(!player->is_hit) {
        direction = INPUT_NONE;
        ellen_target_set(pid.current);
        attempt = ((ellen_target_x + CPU_TARGET_X_MARGIN) < x);
        attempt |= (((ellen_target_x - CPU_TARGET_X_MARGIN) > x) << 1);
        attempt |= (((ellen_target_y + CPU_TARGET_Y_MARGIN) < y) << 2);
        attempt |= ((y < ellen_target_y) << 3);
        switch(attempt) {
        case CPU_TARGET_LEFT: direction = INPUT_LEFT; break;
        case CPU_TARGET_RIGHT: direction = INPUT_RIGHT; break;
        case CPU_TARGET_UP: direction = INPUT_UP; break;
        case CPU_TARGET_DOWN: direction = INPUT_DOWN; break;
        case (CPU_TARGET_UP | CPU_TARGET_LEFT):
            direction = (INPUT_UP | INPUT_LEFT); break;
        case (CPU_TARGET_DOWN | CPU_TARGET_LEFT):
            direction = (INPUT_DOWN | INPUT_LEFT); break;
        case (CPU_TARGET_UP | CPU_TARGET_RIGHT):
            direction = (INPUT_UP | INPUT_RIGHT); break;
        case (CPU_TARGET_DOWN | CPU_TARGET_RIGHT):
            direction = (INPUT_DOWN | INPUT_RIGHT); break;
        }
    } else {
        collision_x_relative = (player_hittest_collision_top.x.v - x);
        collision_y_relative = (player_hittest_collision_top.y.v - y);
        player->is_hit = false;
        if(collision_x_relative <= CPU_COLLISION_SIDE_LEFT) {
            attempt = 0;
        } else if(collision_x_relative <= CPU_COLLISION_SIDE_RIGHT) {
            attempt = 1;
        } else {
            attempt = 2;
        }
        if(player->cpu_dodge_strategy) {
            attempt += (player->cpu_dodge_strategy * CPU_COLLISION_SIDE_COUNT);
        }
        cpu_dodge_pattern = cpu_dodge_patterns[attempt];
        direction = player_cpu_direction_for_collision(collision_y_relative, x, y);
    }

    // The real collision retry strategy has an unbounded control loop,
    // bounded internally by the original nine-direction lattice. A
    // natural C++ for(;;) retains the original TC4 branches (af838a).
    attempt = 0;
    radius_or_retry = 0;
    for(;;) {
        if(player_move(direction) == MOVE_VALID) {
            player_pos_update_and_clamp(player->center);
        }
        // Keep the distinct original hit-test call paths. Collapsing
        // these into a ternary argument changed native CODE (af838b).
        if(radius_or_retry == 0) {
            player_hittest(CPU_HITTEST_RETRY_RADIUS);
        } else {
            player_hittest(CPU_HITTEST_CLOSE_RADIUS);
        }
        if(!player->is_hit) {
            break;
        }
        player->is_hit = false;
        player->center.x.v = x;
        player->center.y.v = y;
        attempt++;
        if(attempt < CPU_DIRECTIONS) {
            retry_region = (
                (player_hittest_collision_top.x.v < CPU_RETRY_LEFT_LIMIT)
                ? CPU_RETRY_LEFT_COLUMN
                : ((player_hittest_collision_top.x.v < CPU_RETRY_MIDDLE_LIMIT)
                    ? CPU_RETRY_MIDDLE_COLUMN
                    : CPU_RETRY_RIGHT_COLUMN)
            );
            direction = cpu_retry_directions[retry_region][attempt];
        } else if(radius_or_retry < CPU_DIRECTIONS) {
            // Retained target branch, although attempt cannot wrap to zero
            // before this bounded retry loop finishes with ordinary state.
            if(!attempt) {
                player->cpu_dodge_strategy++;
                if(player->cpu_dodge_strategy >= CPU_DODGE_ALTERNATIVES) {
                    player->cpu_dodge_strategy = 0;
                }
                retry_region = (randring1_next16() % CPU_RETRY_REGIONS);
            }
            direction = cpu_retry_directions[retry_region][radius_or_retry];
            radius_or_retry++;
        } else {
            if(player->gauge_charged <= CPU_STUCK_BOMB_CHARGE_LIMIT) {
                player_bomb(player);
            } else {
                player->is_hit = true;
            }
            break;
        }
    }
}
