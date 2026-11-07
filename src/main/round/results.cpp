// Round reset and result rendering: E313..E737.
#pragma codeseg P_SHOT_TEXT main_01
#include "src/main/player/shotroot.hpp"
#pragma samecodeseg hud_dynamic_5_digit_points_put
#pragma samecodeseg round_result_high_digits_put
#pragma samecodeseg score_add
// The result panel samples its statistics once at the first frame, then
// refreshes the labels every eighth frame. Bonus accumulation is amortized
// over 192 updates while retaining the original signed 32-bit arithmetic.
enum round_results_clock_t {
    RESULTS_DISPLAY_PERIOD = 8,
    RESULTS_FIRST_FRAME = 1,
    RESULTS_FINAL_STORY_STAGE = 8,
    RESULTS_BONUS_DURATION = 192,
    RESULTS_DIGIT_BASE = 10,
    RESULTS_HUNDREDS = 100,
    RESULTS_DECIMAL_GROUP = 10000,
    RESULTS_COMBO_POINTS = 1000,
    RESULTS_GAUGE_POINTS = 10000,
    RESULTS_BOSS_POINTS = 15000,
    RESULTS_REVERSAL_POINTS = 20000,
    RESULTS_PANIC_POINTS = 30000,
};
#include "src/main/round/objects_reset.inl"
#include "src/main/round/results.inl"
