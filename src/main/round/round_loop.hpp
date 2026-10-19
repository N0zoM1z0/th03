#ifndef TH03_ROUND_LOOP_PROPOSAL_HPP
#define TH03_ROUND_LOOP_PROPOSAL_HPP
// Proposed names only. No storage is allocated here.
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

extern unsigned char stage_render_timing_flag, stage_vsync_wait_frames;
extern unsigned char round_quit_requested, round_background_complete;
extern unsigned char page_front, page_back;
extern unsigned int stage_result_wait_frames;
extern volatile unsigned int round_vsync_count;
extern void (near *stage_demo_update)(void);
extern void (near *stage_background_update)(void);

extern farfunc_t_near round_exatt_update_p1, round_exatt_update_p2;
extern farfunc_t_near round_boss_update_p1, round_boss_update_p2;
extern farfunc_t_near round_player_hook_p1, round_player_hook_p2;
extern farfunc_t_near round_chargeshot_update_p1, round_chargeshot_update_p2;
extern farfunc_t_near round_gauge_pellet_p1, round_gauge_pellet_p2;
extern farfunc_t_near round_gauge_bullet_p1, round_gauge_bullet_p2;
extern farfunc_t_near round_render_hook;
extern farfunc_t_near round_bomb_p1, round_bomb_p2;
extern farfunc_t_near round_boss_render_p1, round_boss_render_p2;
extern farfunc_t_near round_exatt_render_p1, round_exatt_render_p2;
extern farfunc_t_near round_chargeshot_render_p1, round_chargeshot_render_p2;

// Existing calls; aliases must be resolved against actual owned producers.
extern "C" {
unsigned char near round_loop(void);
void near collmap_reset(void);
void far round_bullet_template_reset(void);
void near round_hitcircles_update(void);
void near round_shots_update(void);
void near hud_start_anim_update(void);
void far round_formations_update(void);
void far round_bullets_update(void);
void far round_enemies_update(void);
void far round_fireballs_update(void);
void far round_CEB2(void);
void near pascal round_player_update(input_t input, player_stuff_t near *player);
void far round_sound_update(void);
void near round_pause_or_quit(void);
void far round_CA3C(void);
void far pascal round_CB81(unsigned char player);
void far round_egc_on(void);
void far round_egc_off(void);
void near round_shots_render(void);
void far round_enemies_render(void);
void far round_fireballs_hittest_and_render(void);
void near round_hitcircles_render(void);
void near pascal round_player_render(player_stuff_t near *player);
void near pascal round_DF18(player_stuff_t near *player);
void far round_CEE0(void);
void far round_bullets_render(void);
void near round_defeat_banner_render(void);
void near round_match_result_render(void);
void near pascal round_score_store_winner(int winner);
void near round_background_finish(void);
void near round_C830(void);
void near round_C8C4(void);
void near round_D52E(void);
void far pascal round_C9FE(unsigned char player);
void near hud_start_anim_render(void);
void far round_combos_update_and_render(void);
void far round_palette_show(void);
void far pascal round_grcg_setcolor(int mode, int color);
void far round_grcg_off(void);
void near round_playfield_clear(void); // Genuine BX register argument, NOT stack.
void near round_randring_fill(void);
}

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
