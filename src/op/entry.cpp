// TH03 OP entry, configuration and screen dispatch in original CODE group_01.
// Reference candidate reviewed against the decoded Japanese target; exact open.

#pragma option -zPgroup_01

#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th01/rank.h"
#include "compat/rec98/th01/math/clamp.hpp"
#include "compat/rec98/th01/core/initexit.hpp"
#include "compat/rec98/th02/hardware/frmdelay.h"
#include "compat/rec98/th02/gaiji/str.hpp"
#include "compat/rec98/th02/op/menu.hpp"
#include "compat/rec98/th02/op/m_music.hpp"
#include "compat/rec98/th03/common.h"
#include "compat/rec98/th03/resident.hpp"
#include "compat/rec98/th03/hardware/input.h"
#include "compat/rec98/th03/formats/cfg_impl.hpp"
#include "compat/rec98/th03/core/initexit.h"
#include "compat/rec98/th03/gaiji/gaiji.h"
#include "compat/rec98/th03/snd/snd.h"
#include "compat/rec98/th03/shiftjis/fns.hpp"
#include "compat/rec98/th03/shiftjis/main.hpp"
#include "compat/rec98/th03/op/m_main.hpp"
#include "compat/rec98/th03/op/m_select.hpp"
#include <conio.h>
#include <stddef.h>
#include <process.h>

enum main_choice_t {
	MC_STORY,
	MC_VS,
	MC_MUSICROOM,
	MC_REGIST_VIEW,
	MC_OPTION,
	MC_QUIT,
	MC_COUNT,
};

enum option_choice_t {
	OC_RANK,
	OC_BGM,
	OC_KEY_MODE,
	OC_QUIT,
	OC_COUNT,
};

// Proportional gaiji strings
// --------------------------

enum gaiji_th03_mikoft_t {
	gp_Start = 0x30,
	gp_Start_last = ((gp_Start + 3) - 1),
	gp_VS_Start,
	gp_VS_Start_last = ((gp_VS_Start + 6) - 1),
	gp_Option = 0x3D,
	gp_Option_last = ((gp_Option + 4) - 1),
	gp_Music_room,
	gp_Music_room_last = ((gp_Music_room + 7) - 1),
	gp_Quit,
	gp_Quit_last = ((gp_Quit + 3) - 1),
	gp_Music,
	gp_Music_last = ((gp_Music + 4) - 1),
	gp_FM_86_,
	gp_FM_86__last = ((gp_FM_86_ + 4) - 1),
	gp_MIDI__SC_88_,
	gp_MIDI__SC_88__last = ((gp_MIDI__SC_88_ + 7) - 1),
	gp_off,
	gp_off_last = ((gp_off + 2) - 1),
	gp_KeyConfig,
	gp_KeyConfig_last = ((gp_KeyConfig + 6) - 1),
	gp_Type,
	gp_Type_last = ((gp_Type + 3) - 1),
	gp_1,
	gp_2,
	gp_3,
	gp_Key,
	gp_Key_last = ((gp_Key + 2) - 1),
	gp_Joy,
	gp_Joy_last = ((gp_Joy + 2) - 1),
	gp_vs,
	gp_vs_last = ((gp_vs + 2) - 1),
	gp_Rank,
	gp_Rank_last = ((gp_Rank + 3) - 1),
	gp_Easy,
	gp_Easy_last = ((gp_Easy + 3) - 1),
	gp_Normal,
	gp_Normal_last = ((gp_Normal + 4) - 1),
	gp_Hard,
	gp_Hard_last = ((gp_Hard + 3) - 1),
	gp_Lunatic,
	gp_Lunatic_last = ((gp_Lunatic + 4) - 1),

	gp_HiScore = 0x82,
	gp_HiScore_last = ((gp_HiScore + 5) - 1),
	gp_1P_vs = 0x88,
	gp_1P_vs_last = ((gp_1P_vs + 4) - 1),
	gp__CPU,
	gp__CPU_last = ((gp__CPU + 4) - 1),
	gp_CPU_vs = 0x92,
	gp_CPU_vs_last = ((gp_CPU_vs + 4) - 1),
	gp__2P,
	gp__2P_last = ((gp__2P + 4) - 1),
};

// Constructs a VS choice string out of its two halves.
#define g_str_vs(first, second) { g_str_4(first), g_str_4(second), '\0' }
// --------------------------

bool snd_sel_disabled = false; // Yes, it's just (!snd_fm_possible).

/// YUME.CFG loading and saving
/// ---------------------------

void near cfg_load(void)
{
	cfg_t cfg;

	cfg_load_and_set_resident(cfg, CFG_FN_CAPS);

	resident->bgm_mode = cfg.opts.bgm_mode;
	snd_determine_mode();
	snd_sel_disabled = false;
	if(!snd_active) {
		resident->bgm_mode = SND_BGM_OFF;
		snd_sel_disabled = true;
	} else if(cfg.opts.bgm_mode == SND_BGM_OFF) {
		snd_active = false;
	}

	resident->key_mode = cfg.opts.key_mode;
	resident->rank = cfg.opts.rank;
}

inline void cfg_save_bytes(cfg_t &cfg, size_t bytes) {
	file_append(CFG_FN_CAPS);
	file_seek(0, SEEK_SET);

	cfg.opts.bgm_mode = resident->bgm_mode;
	cfg.opts.key_mode = resident->key_mode;
	cfg.opts.rank = resident->rank;

	file_write(&cfg.opts, bytes);
	file_close();
}

void near cfg_save(void)
{
	cfg_t cfg;
	cfg_save_bytes(cfg, 4); // MODDERS: Should be `sizeof(cfg.opts)`
}

void near cfg_save_exit(void)
{
	cfg_t cfg = { 0 };
	cfg_save_bytes(cfg, sizeof(cfg));
}
/// ---------------------------

#define resident_reset_scores(i) { \
	/* ZUN bloat: Very unsafe. */ \
	for(i = 0; i < (PLAYER_COUNT * SCORE_DIGITS); i++) { \
		resident->score_last[0].digits[i] = 0; \
	} \
}

inline bool switch_to_mainl(bool opwin_free) {
	cfg_save();

	// ZUN landmine: The system's previous gaiji should be restored *after*
	// TRAM gets cleared in game_exit(), not before while we're still showing
	// menu text.
	gaiji_restore();

	snd_kaja_func(KAJA_SONG_STOP, 0);
	if(opwin_free) {
		super_free(); // ZUN bloat: Process termination will do this anyway.
	}

	// ZUN landmine: The screen clearing done in this function will almost
	// certainly not run within VBLANK.
	game_exit();

	execl(BINARY_MAINL, BINARY_MAINL, nullptr);
	return false;
}

bool near story_menu(void)
{
	enum {
		RANDOM_OPPONENT_MIN = PLAYCHAR_REIMU,
		RANDOM_OPPONENT_MAX = PLAYCHAR_RIKAKO,
		RANDOM_OPPONENT_COUNT = (
			(RANDOM_OPPONENT_MAX - RANDOM_OPPONENT_MIN) + 1
		),
	};

	static bool opponent_seen[RANDOM_OPPONENT_COUNT] = { false };

	// ACTUAL TYPE: playchar_t
	static const uint8_t STAGE7_OPPONENT_FOR[PLAYCHAR_COUNT] = {
		PLAYCHAR_MIMA, // for Reimu
		PLAYCHAR_REIMU, // for Mima
		PLAYCHAR_REIMU, // for Marisa
		PLAYCHAR_MARISA, // for Ellen
		PLAYCHAR_REIMU, // for Kotohime
		PLAYCHAR_ELLEN, // for Kana
		PLAYCHAR_KANA, // for Rikako
		PLAYCHAR_KOTOHIME, // for Chiyuri
		PLAYCHAR_RIKAKO, // for Yumemi
	};

	int stage;
	int candidate;

	resident->demo_num = 0;
	resident->pid_winner = 0;
	resident->story_stage = 0;
	resident->is_cpu[0] = false;
	resident->is_cpu[1] = true;
	resident->game_mode = GM_STORY;
	resident->story_lives = CREDIT_LIVES;
	resident->show_score_menu = false;
	resident->playchar_paletted[1].v = -1;

	if(select_story_menu()) {
		return true;
	}

retry_opponent_selection:
	// ACTUAL TYPE: playchar_t
	int stage7_opponent = STAGE7_OPPONENT_FOR[
		resident->playchar_paletted[0].char_id_16()
	];
	irand_init(resident->rand);

	for(stage = 0; stage < 6; stage++) {
		// Native first-call fixtures use the original LCG. The static seen array
		// is not reset on reentry after a failed executable handoff.
		do {
			candidate = (
				RANDOM_OPPONENT_MIN + (irand() % RANDOM_OPPONENT_COUNT)
			);
		} while(opponent_seen[candidate] || (stage7_opponent == candidate));
		opponent_seen[candidate] = true;

		// ZUN bloat: Should not change types.
		#define candidate_paletted candidate
		candidate_paletted = TO_OPTIONAL_PALETTED(candidate);
		resident->story_opponents[stage].v = candidate_paletted;

		// ZUN bloat: All of these palette swaps could have been done in a
		// single loop at the end.
		if(candidate_paletted == resident->playchar_paletted[0].v) {
			resident->story_opponents[stage].v = (candidate_paletted + 1);
		}
		#undef candidate_paletted
	}

	resident->playchar_paletted[1] = resident->story_opponents[0];
	resident->story_opponents[6].v = TO_OPTIONAL_PALETTED(stage7_opponent);

	// ZUN bloat: Palette swaps...
	resident->story_opponents[7].set(PLAYCHAR_CHIYURI);
	if(
		resident->playchar_paletted[0].v ==
		TO_OPTIONAL_PALETTED(PLAYCHAR_CHIYURI)
	) {
		resident->story_opponents[7].v++;
	}
	resident->story_opponents[8].set(PLAYCHAR_YUMEMI);
	if(
		resident->playchar_paletted[0].v ==
		TO_OPTIONAL_PALETTED(PLAYCHAR_YUMEMI)
	) {
		resident->story_opponents[8].v++;
	}

	// Keep the original retry branch; unreachable behavior is not assumed.
	for(stage = 0; stage < STAGE_COUNT; stage++) {
		if(resident->story_opponents[stage].char_id_16() >= PLAYCHAR_COUNT) {
			goto retry_opponent_selection;
		}
	}

	resident_reset_scores(stage);
	resident->rem_credits = 3;
	resident->op_animation_fast = false;
	resident->skill = (70 + (resident->rank * 25));
	return switch_to_mainl(false);
}

inline tram_y_t choice_tram_y(unsigned int line) {
	return ((BOX_TOP / GLYPH_H) + 1 + line);
}

void pascal near vs_choice_put(int sel, tram_atrb2 atrb)
{
	enum {
		W = (8 * GAIJI_W),
		TRAM_LEFT = ((BOX_SUBMENU_CENTER_X - (W / 2)) / GLYPH_HALF_W),
	};
	if(sel == VS_1P_CPU) {
		static const char STR[] = g_str_vs(gp_1P_vs, gp__CPU);
		gaiji_putsa(TRAM_LEFT, choice_tram_y(1), STR, atrb);
	} else if(sel == VS_1P_2P) {
		static const char STR[] = g_str_vs(gp_1P_vs, gp__2P);
		gaiji_putsa(TRAM_LEFT, choice_tram_y(2), STR, atrb);
	} else /* if (sel == VS_CPU_CPU) */ {
		static const char STR[] = g_str_vs(gp_CPU_vs, gp__CPU);
		gaiji_putsa(TRAM_LEFT, choice_tram_y(3), STR, atrb);
	}
}

bool near vs_menu(void)
{
	int sel;

	// ZUN quirk: This assignment causes any initially held inputs to be
	// processed immediately, just like in the Main menu at startup, but unlike
	// after a later switch between the Main and Option menu.
	input_t input_prev = INPUT_NONE;

	// After a match, we come back here, skip the menu, and launch into
	// character selection.
	if(resident->game_mode < GM_VS) {
		text_clear();
		box_main_to_submenu_animate();

		sel = VS_1P_CPU;
		vs_choice_put(VS_1P_CPU, TX_WHITE);
		vs_choice_put(VS_1P_2P, TX_BLACK);
		vs_choice_put(VS_CPU_CPU, TX_BLACK);

		while(1) {
			input_mode_interface();
			if(input_prev == INPUT_NONE) {
				if(input_sp & INPUT_UP) {
					vs_choice_put(sel, TX_BLACK);
					ring_dec(sel, VS_CPU_CPU);
					vs_choice_put(sel, TX_WHITE);
				}
				if(input_sp & INPUT_DOWN) {
					vs_choice_put(sel, TX_BLACK);
					ring_inc(sel, VS_CPU_CPU);
					vs_choice_put(sel, TX_WHITE);
				}
				if((input_sp & INPUT_SHOT) || (input_sp & INPUT_OK)) {
					break;
				}
				// ZUN bug: Should have added a INPUT_CANCEL branch to allow
				// players to quit back to the main menu once they entered this
				// one.
			}
			input_prev = input_sp;
			frame_delay(1);
		}
	} else {
		sel = (resident->game_mode - GM_VS);
	}

	resident->is_cpu[0] = ((sel == VS_CPU_CPU) ? true : false);
	resident->is_cpu[1] = ((sel != VS_1P_2P) ? true : false);
	resident->demo_num = 0;
	resident->pid_winner = 0;
	resident->story_stage = 0;
	resident->game_mode = (GM_VS + sel);
	resident->show_score_menu = false;

	// ZUN bloat: Could be compressed into a single branch.
	if(sel == VS_1P_2P) {
		if(select_1p_vs_2p_menu()) {
			resident->game_mode = GM_NONE;
			return true;
		}
	} else {
		if(select_vs_cpu_menu()) {
			resident->game_mode = GM_NONE;
			return true;
		}
	}

	resident_reset_scores(sel);
	return switch_to_mainl(false);
}

void near start_demo(void)
{
	static const int8_t PAIRINGS[DEMO_COUNT * PLAYER_COUNT] = {
		TO_OPTIONAL_PALETTED(PLAYCHAR_MIMA),
		TO_OPTIONAL_PALETTED(PLAYCHAR_REIMU),

		TO_OPTIONAL_PALETTED(PLAYCHAR_MARISA),
		TO_OPTIONAL_PALETTED(PLAYCHAR_RIKAKO),

		TO_OPTIONAL_PALETTED(PLAYCHAR_ELLEN),
		TO_OPTIONAL_PALETTED(PLAYCHAR_KANA),

		TO_OPTIONAL_PALETTED(PLAYCHAR_KOTOHIME),
		TO_OPTIONAL_PALETTED(PLAYCHAR_MARISA),
	};
	static const int32_t RAND[DEMO_COUNT] = { 600, 1000, 3200, 500 };

	resident->is_cpu[0] = true;
	resident->is_cpu[1] = true;
	ring_inc_range(resident->demo_num, 1, DEMO_COUNT);
	resident->pid_winner = 0;

	// Critically important to guarantee deterministic demos!
	resident->story_stage = 0;

	resident->game_mode = GM_DEMO;
	resident->show_score_menu = false;

	// ZUN bloat: A two-dimensional array would have been more readable and
	// would have generated better code.
	resident->playchar_paletted[0].v = (
		PAIRINGS[((resident->demo_num - 1) * PLAYER_COUNT) + 0]
	);
	resident->playchar_paletted[1].v = (
		PAIRINGS[((resident->demo_num - 1) * PLAYER_COUNT) + 1]
	);

	resident->rand = RAND[resident->demo_num - 1];
	int i;
	resident_reset_scores(i);
	palette_black_out(1);

	switch_to_mainl(false);
}

void near wait_for_input_or_start_demo_then_box_to_main_animate(void)
{
	{
		input_sp = INPUT_NONE;
		int frame = 0;
		while(input_sp == INPUT_NONE) {
			input_mode_interface();
			resident->rand++;
			frame++;
			if(frame > 520) {
				start_demo();
			}
			frame_delay(1);
		}
	}

	super_put(BOX_LEFT, BOX_TOP, OPWIN_LEFT);

	// ZUN bloat: Should maybe be merged with the two others in `m_main.cpp`.
	{for(
		screen_x_t right_left = (BOX_LEFT + OPWIN_W);
		right_left < (BOX_MAIN_RIGHT - OPWIN_STEP_W);
		right_left += OPWIN_STEP_W
	) {
		box_column16_unput(right_left);
		super_put(right_left, BOX_TOP, OPWIN_RIGHT);
		frame_delay(1);
	}}
}

bool near score_menu(void)
{
	resident->story_stage = STAGE_NONE;
	resident->show_score_menu = true;
	resident->game_mode = GM_NONE;
	int i;
	resident_reset_scores(i);
	return switch_to_mainl(true);
}

/// The menu
/// --------

#include "src/op/menu/menu_state.inl"

void main(void)
{
	graph_400line();
	text_clear();
	respal_create();

	// ZUN landmine: There are no known issues with running the game at a GDC
	// clock speed of 5 MHz, so there's no need to enforce it here.
	if(graph_VramZoom) {
		dos_puts2(ERROR_GDC_5MHZ_1);
		dos_puts2(ERROR_GDC_5MHZ_2);
		dos_puts2(ERROR_GDC_5MHZ_3);
		getch();
		return;
	}

	if(game_init_op(OP_AND_END_PF_FN)) {
		dos_puts2(ERROR_OUT_OF_MEMORY);
		getch();
		return;
	}

	gaiji_backup();
	gaiji_entry_bfnt(GAIJI_FN);
	cfg_load();
	if((resident->game_mode >= GM_VS) && (resident->demo_num == 0)) {
		select_cdg_load_part1_of_4();
		select_cdg_load_part3_of_4();
		select_cdg_load_part2_of_4();
		vs_menu();
	}

	if(!resident->op_animation_fast) {
		op_animate();
		resident->op_animation_fast = true;
	} else {
		resident->op_animation_fast = false;
		op_fadein_animate();
	}
	wait_for_input_or_start_demo_then_box_to_main_animate();

	// Showing the menu options before loading part 2 is actually a pretty nice
	// idea to better hide potentially long loading times.
	//
	// ZUN quirk: Resetting [input_sp] regardless of the actually held keys
	// means that main_update_and_render() always returns with its instance of
	// [input_allowed] set to `true`. Thus, any initially held key is processed
	// instantly on the first call to the function in the loop below – contrary
	// to what you would expect from the whole input locking system, and
	// contrary to how the game behaves after switching the active menu later
	// on, where inputs *are* locked until the player releases all keys.
	in_option = false;
	input_sp = INPUT_NONE;
	main_update_and_render();

	select_cdg_load_part2_of_4();

	while(!quit) {
		input_mode_interface();
		switch(in_option) {
		case false:	main_update_and_render();  	break;
		case true: 	option_update_and_render();	break;
		}
		resident->rand++;
		frame_delay(1);
	}
	cfg_save_exit();

	// ZUN landmine: The system's previous gaiji should be restored *after*
	// clearing TRAM, not before while we're still showing menu text. Sending
	// ((8,192 × 2) + 512) bytes of data over I/O ports one byte at a time
	// takes a short while, so this can definitely be visible for a fraction of
	// a frame on real, not infinitely fast hardware. Especially since the CRT
	// beam is most certainly in the middle of a frame after the file I/O
	// immediately above.
	// Funnily enough, TH02 got the order correct right in the one place where
	// it mattered in that game.
	//
	// ZUN bloat: Also, game_exit_to_dos() already clears TRAM.
	gaiji_restore();
	text_clear();

	game_exit_to_dos();
	respal_free();
}
/// --------
