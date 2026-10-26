// Candidate for the five retained P_SHOT procedures. The following maintained
// update/render translation unit remains a separate producer. No exact credit.
#pragma codeseg P_SHOT_TEXT main_01
#include "src/main/player/shotroot.hpp"
// Far providers in the same MAIN_01 code frame.
#pragma samecodeseg hud_dynamic_5_digit_points_put
#pragma samecodeseg round_result_high_digits_put
#pragma samecodeseg score_add

#include "src/main/player/shot_sprites.inl"
#include "src/main/round/objects_reset.inl"
#include "src/main/round/results.inl"
#include "src/main/player/shots_add.inl"
