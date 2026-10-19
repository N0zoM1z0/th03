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

input_t near pascal player_cpu_direction_for_collision(
    subpixel_t collision_y_relative, subpixel_t player_x, subpixel_t player_y
)
{
    input_t direction;
    if(collision_y_relative < -TO_SP(16)) {
        if(player_x >= TO_SP(240)) {
            if(player_y >= TO_SP(128)) {
                direction = cpu_dodge_pattern[0];
            } else {
                direction = INPUT_LEFT;
            }
        } else if(player_x >= TO_SP(16)) {
            direction = cpu_dodge_pattern[1];
        } else if(player_y >= TO_SP(128)) {
            direction = cpu_dodge_pattern[2];
        } else {
            direction = INPUT_RIGHT;
        }
    } else if(collision_y_relative < TO_SP(32)) {
        if(player_x >= TO_SP(240)) {
            direction = cpu_dodge_pattern[3];
        } else if(player_x >= TO_SP(16)) {
            direction = cpu_dodge_pattern[4];
        } else {
            direction = cpu_dodge_pattern[5];
        }
    } else {
        if(player_x >= TO_SP(240)) {
            direction = cpu_dodge_pattern[6];
        } else if(player_x >= TO_SP(16)) {
            direction = cpu_dodge_pattern[7];
        } else {
            direction = cpu_dodge_pattern[8];
        }
    }
    if(player_y >= TO_SP(304) && direction == INPUT_DOWN) {
        if(player_x >= TO_SP(128)) {
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
    attempt = ((ellen_target_x + TO_SP(16)) < x);
    attempt |= (((ellen_target_x - TO_SP(16)) > x) << 1);
    attempt |= (((ellen_target_y + TO_SP(80)) < y) << 2);
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
    random_region = (randring1_next16() % 3);
    if(player_move(direction) == MOVE_VALID) {
        player_pos_update_and_clamp(player->center);
    }
    player_hittest(8 / 2);
    if(player->is_hit) {
        player->is_hit = false;
        attempt++;
        if(player->gauge_charged <= 0x500 && !(randring1_next16() & 3)) {
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

    if((round_or_result_frame & 3) == 0) {
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
        attempt = ((ellen_target_x + TO_SP(16)) < x);
        attempt |= (((ellen_target_x - TO_SP(16)) > x) << 1);
        attempt |= (((ellen_target_y + TO_SP(80)) < y) << 2);
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
        if(collision_x_relative <= -TO_SP(16)) {
            attempt = 0;
        } else if(collision_x_relative <= TO_SP(16)) {
            attempt = 1;
        } else {
            attempt = 2;
        }
        if(player->cpu_dodge_strategy != 0) {
            attempt += (player->cpu_dodge_strategy * 3);
        }
        cpu_dodge_pattern = cpu_dodge_patterns[attempt];
        direction = player_cpu_direction_for_collision(collision_y_relative, x, y);
    }

    attempt = 0;
    radius_or_retry = 0;
    while(true) {
        if(player_move(direction) == MOVE_VALID) {
            player_pos_update_and_clamp(player->center);
        }
        if(radius_or_retry == 0) {
            player_hittest(40 / 2);
        } else {
            player_hittest(8 / 2);
        }
        if(!player->is_hit) {
            break;
        }
        player->is_hit = false;
        player->center.x.v = x;
        player->center.y.v = y;
        attempt++;
        if(attempt < CPU_DIRECTIONS) {
            retry_region = (player_hittest_collision_top.x.v < TO_SP(80)) ? 0 :
                ((player_hittest_collision_top.x.v < TO_SP(176)) ? 1 : 2);
            direction = cpu_retry_directions[retry_region][attempt];
        } else if(radius_or_retry < CPU_DIRECTIONS) {
            // Retained target branch, although attempt cannot wrap to zero
            // before this bounded retry loop finishes with ordinary state.
            if(attempt == 0) {
                player->cpu_dodge_strategy++;
                if(player->cpu_dodge_strategy >= 2) {
                    player->cpu_dodge_strategy = 0;
                }
                retry_region = (randring1_next16() % CPU_RETRY_REGIONS);
            }
            direction = cpu_retry_directions[retry_region][radius_or_retry];
            radius_or_retry++;
        } else {
            if(player->gauge_charged <= 0x400) {
                player_bomb(player);
            } else {
                player->is_hit = true;
            }
            break;
        }
    }
}
