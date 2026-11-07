// One native producer for MAIN load 96E6..A2D0.
// Initial declarations retain the packed views used by the round loop.
#pragma codeseg PLAYFLD_TEXT main_01
#include "src/main/round/round_loop.hpp"

// The main executable's exit codes are an inter-function contract: 1
// repeats a round, 2 dispatches to MAINL, 0 returns to OP. The original
// distinct return sites in round_loop() must not be collapsed.
enum round_loop_exit_t {
    ROUND_LOOP_RETURN_TO_OP = 0,
    ROUND_LOOP_PLAY_NEXT = 1,
    ROUND_LOOP_END_MATCH = 2,
};

// The large frame scheduler's original 16-bit timing gates. Keep the
// comparisons and all RNG draws in the original execution order.
enum round_loop_timing_t {
    ROUND_RESULT_FINISH_BACKGROUND_AT = 160,
    ROUND_VICTORY_ROUNDS = 2,
    ROUND_ENTRY_SPEED_MAX = 127,
    ROUND_SPEED_UPDATE_MASK = 63,
    ROUND_RANDOM_REFILL_MASK = 1023,
    ROUND_CPU_RESET_WINDOW_END = 2000,
};
#include "src/main/core/entry.inl"
#include "src/main/round/round_loop.inl"
#include "src/main/round/stage_round.inl"
#include "src/main/core/roundfin.inl"
