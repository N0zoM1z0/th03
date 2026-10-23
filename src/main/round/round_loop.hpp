#ifndef TH03_MAIN_ROUND_LOOP_HPP
#define TH03_MAIN_ROUND_LOOP_HPP
// Views of existing storage; this interface allocates no DATA/BSS.
#pragma option -a-
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/resident.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "compat/rec98/th03/main/difficul.hpp"
#include "compat/rec98/th03/main/defeat.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#pragma option -a2
#include <stddef.h>
#include <dos.h>

#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

extern unsigned char stage_render_timing_flag, round_reset_flag;
extern unsigned char round_quit_requested, playfield_transition_midpoint;
extern unsigned char page_front, page_back;
extern unsigned int stage_result_wait_frames;
extern volatile unsigned int vsync_Count1;
extern void (near *stage_demo_update)(void);
extern void (near *stage_background_update)(void);

extern farfunc_t_near round_exatt_update_p1, round_exatt_update_p2;
extern farfunc_t_near round_player_hook_p1, round_player_hook_p2;
extern farfunc_t_near round_exatt_render_p1, round_exatt_render_p2;
extern farfunc_t_near round_render_hook;
extern farfunc_t_near round_bomb_p1, round_bomb_p2;
extern farfunc_t_near gba_boss_update[2], gba_boss_render[2];
extern farfunc_t_near chargeshot_update[2], chargeshot_render[2];
extern farfunc_t_near gba_gauge_pattern_pellet[2], gba_gauge_pattern_bullet[2];

// Match the maintained producers' C++ linkage and 16-bit near/far/Pascal ABI.
void far bullet_template_reset_stuff(void);
void near hitcircles_update(void);
void near shots_update(void);
void far enemy_formations_update(void);
void far bullets_update(void);
void far enemies_update(void);
void far fireballs_update(void);
void far player_effects_update(void);
void near pascal player_state_update(input_t input, player_stuff_t near *player);
void near shots_render(void);
void far enemies_render(void);
void far fireballs_hittest_and_render(void);
void near hitcircles_render(void);
void near pascal player_render(player_stuff_t near *player);
void near pascal player_overlay_render(player_stuff_t near *player);
void far player_effects_render(void);
void far bullets_render(void);
void near round_defeat_banners_render(void);
void near round_match_result_render(void);
void near pascal round_score_commit(unsigned int winner);
void far combos_update_and_render(void);
void near randring_fill(void);

extern "C" {
unsigned char near round_loop(void);
void near collmap_reset(void);
void near hud_start_anim_update(void);
void far snd_se_update(void);
void near round_pause_or_quit(void);
void far round_CA3C(void);
void far pascal round_CB81(unsigned char player);
void near stage_demo_finish(void);
void near round_C830(void);
void near round_C8C4(void);
void near score_hud_render(void);
void far pascal round_C9FE(unsigned char player);
void near hud_start_anim_render(void);
// Genuine BX register argument, no stack arguments.
void near round_playfield_clear(void);
}
#pragma samecodeseg player_effects_update
#pragma samecodeseg player_effects_render
#pragma samecodeseg round_CA3C
#pragma samecodeseg round_CB81
#pragma samecodeseg round_C9FE

#define ROUND_FIELD(T,F,O,S) typedef char loop_##T##_##F[((offsetof(T,F)==O) && (sizeof(((T near *)0)->F)==S)) ? 1 : -1]
ROUND_FIELD(player_stuff_t, rounds_won, 0x6C, 1);
ROUND_FIELD(player_stuff_t, hit_damage_next, 0x73, 1);
ROUND_FIELD(player_stuff_t, cpu_frame, 0x74, 2);
ROUND_FIELD(resident_t, pid_winner, 0x17, 1);
ROUND_FIELD(resident_t, game_mode, 0x28, 1);
ROUND_FIELD(resident_t, story_lives, 0x34, 1);
#undef ROUND_FIELD
typedef char loop_widths[(sizeof(int)==2 && sizeof(long)==4 && sizeof(player_stuff_t)==128) ? 1 : -1];
typedef char loop_pointers[(sizeof(farfunc_t_near)==4 && sizeof(stage_demo_update)==2 && sizeof(stage_background_update)==2) ? 1 : -1];
typedef char loop_round_counter[(sizeof(round_frame)==4 && sizeof(round_or_result_frame)==2) ? 1 : -1];
typedef char loop_state_widths[(sizeof(round_speed)==1 && sizeof(defeat_flag)==1 && sizeof(palette_changed)==1 && sizeof(pid)==1 && sizeof(pid_current)==1 && sizeof(input_mode)==4 && sizeof(input_t)==2) ? 1 : -1];
#endif
