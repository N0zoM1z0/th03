#ifndef TH03_MAIN_PLAYER_SHOTROOT_HPP
#define TH03_MAIN_PLAYER_SHOTROOT_HPP

// Candidate declarations for the complete P_SHOT contribution. These refer to
// existing DGROUP storage; their original storage ownership is still open.
#include "src/main/sound/se.hpp"
#pragma option -a-
#include "src/main/player/stuff.hpp"
#include "compat/rec98/th03/main/enemy/efe.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "src/main/core/resident.hpp"
#pragma option -a2
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th03/gaiji/gaiji.h"
#include "compat/rec98/th03/main/hud/dynamic.hpp"
#include "src/main/player/score_add.hpp"

extern unsigned char round_reset_flag, round_reset_clear_flag;
extern unsigned char round_defeated_player;
extern unsigned char defeat_combo_hits_max, defeat_gauge_attacks_fired;
extern unsigned char defeat_boss_attacks_fired, defeat_boss_attacks_reversed;
extern unsigned char defeat_boss_panics_fired, result_lives_remaining;
extern unsigned char extends_gained;
extern unsigned int result_bonus_step, result_bonus_low, result_bonus_high;
extern long result_bonus_remaining;

extern char near result_label_combo[], result_label_gauge[];
extern char near result_label_boss[], result_label_reversal[];
extern char near result_label_panic[], result_label_total[];
extern char near result_label_winner[], result_label_clear[], result_label_lives[];

void near stage_prepare_shot_sprites(void);
void near round_objects_and_counters_reset(void);
void near pascal round_result_number_put(int x, int y, int value);
void near round_match_result_render(void);
void near player_shots_add(void);
void far pascal round_result_high_digits_put(
    screen_x_t left, vram_y_t top, unsigned int points, vc_t color
);
// Same typed API as the accepted src/main/player/reimu_gameplay.hpp provider.
extern "C" void far pascal reimu_hyper_shot_add(Subpixel center_x, Subpixel center_y);

typedef char shotroot_scalar_widths[(sizeof(int) == 2 && sizeof(long) == 4
    && sizeof(bool) == 1 && sizeof(pid.current) == 1
    && sizeof(pid.so_attack) == 1) ? 1 : -1];
typedef char shotroot_record_sizes[(sizeof(shotpair_t) == 14
    && sizeof(efe_t) == 48 && sizeof(player_stuff_t) == 128
    && sizeof(resident_t) == 256) ? 1 : -1];
typedef char shotroot_pointer_widths[(sizeof(shotpair_t near *) == 2
    && sizeof(resident_t far *) == 4) ? 1 : -1];
typedef char shotroot_resident_fields[(offsetof(resident_t, story_stage) == 0x33
    && offsetof(resident_t, story_lives) == 0x34) ? 1 : -1];

#endif
