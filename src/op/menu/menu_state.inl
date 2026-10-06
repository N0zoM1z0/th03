// Bounded OP menu include. The original OP entry carrier provides the enums,
// choice_tram_y(), declarations and explicitly forwarded reference context.

// Must be non-`const` for data ordering reasons. Declared at global scope
// because
// 1) the same [COMMAND_QUIT] string is used in both the main and Option menu,
//    and
// 2) some of those are unused, which points toward ZUN having declared them at
//    global scope as well.
char COMMAND_STORY[] = { g_str_3(gp_Start), '\0' };
char COMMAND_VS[] = { g_str_6(gp_VS_Start), '\0' };
char COMMAND_MUSICROOM[] = { g_str_7(gp_Music_room), '\0' };
char COMMAND_REGIST_VIEW[] = { g_str_5(gp_HiScore), '\0' };
char COMMAND_OPTION[] = { g_str_4(gp_Option), '\0' };
char COMMAND_QUIT[] = { g_str_3(gp_Quit), '\0' };

char LABEL_RANK[] = { g_str_3(gp_Rank), '\0' };
char LABEL_MUSIC[] = { g_str_4(gp_Music), '\0' };
char LABEL_KEYCONFIG[] = { g_str_6(gp_KeyConfig), '\0' };

// ZUN bloat: Unused, but looks like a gaiji version of the space string below.
// Since that is the only call to text_putsa() in this binary, using this one
// would have also removed the need to link in that function.
char UNUSED_SPACES[5] = { g_SP, g_SP, g_SP, g_SP, '\0' };

char VALUE_EASY[] = { g_str_3(gp_Easy), '\0' };
char VALUE_NORMAL[] = { g_str_4(gp_Normal), '\0' };
char VALUE_HARD[] = { g_str_3(gp_Hard), '\0' };
char VALUE_LUNATIC[] = { g_str_4(gp_Lunatic), '\0' };

char VALUE_OFF[8] = { g_SP, g_SP, g_str_2(gp_off), g_SP, g_SP, g_SP };
char VALUE_FM[8] = { g_SP, g_str_4(gp_FM_86_), g_SP, g_SP };
char VALUE_MIDI[8] = { g_str_7(gp_MIDI__SC_88_) };

// The initial names for the three input modes? Unused in the final game.
char VALUE_TYPE_1[] = { g_str_3(gp_Type), gp_1, '\0' };
char VALUE_TYPE_2[] = { g_str_3(gp_Type), gp_2, '\0' };
char VALUE_TYPE_3[] = { g_str_3(gp_Type), gp_3, '\0' };

char VALUE_KEY_KEY[] = {
	g_str_2(gp_Key), g_str_2(gp_vs), g_str_2(gp_Key), '\0',
};
char VALUE_JOY_KEY[] = {
	g_str_2(gp_Joy), g_str_2(gp_vs), g_str_2(gp_Key), '\0',
};
char VALUE_KEY_JOY[] = {
	g_str_2(gp_Key), g_str_2(gp_vs), g_str_2(gp_Joy), '\0',
};

// Globals
// -------

int8_t menu_sel = 0;
bool quit = false;
bool in_main = true;

// ZUN bloat: Should be function-level statics.
bool main_input_allowed;
bool option_input_allowed;

int8_t in_option; // ACTUAL TYPE: bool
static int8_t padding; // ZUN bloat
menu_put_func_t menu_put;
// -------

// These menus want to display centered strings. However, the underlying gaiji
// of all of these (except "Start", which exactly fits into the 48 pixels
// covered by its 3 gaiji) are left-aligned and leave anywhere from 6 to 14
// pixels of trailing blank space in their last gaiji. Hence, ZUN shifts the
// mathematically correct center a bit to get as close as possible to visual
// centering, but still fails to perfectly center three of these labels; only
// "Music room" and "Option" are. Would be a ZUN bug, but a fix would also have
// to change assets. We'll probably only do that once we translate the game.
#define gaiji_w_shifted(str, shift_x) ( \
	((sizeof(str) - 1) + shift_x) * GAIJI_W \
)

#define choice_put_centered(center_x, line, shift_x, str, atrb) { \
	gaiji_putsa( \
		((center_x - (gaiji_w_shifted(str, shift_x) / 2)) / GLYPH_HALF_W), \
		choice_tram_y(line), \
		str, \
		atrb \
	); \
}

void pascal near main_choice_put(int sel, tram_atrb2 atrb)
{
	if(sel == MC_STORY) {
		choice_put_centered(BOX_MAIN_CENTER_X, 0, 0, COMMAND_STORY, atrb);
	} else if(sel == MC_VS) {
		choice_put_centered(BOX_MAIN_CENTER_X, 1, -1, COMMAND_VS, atrb);
	} else if(sel == MC_MUSICROOM) {
		choice_put_centered(BOX_MAIN_CENTER_X, 2, -1, COMMAND_MUSICROOM, atrb);
	} else if(sel == MC_REGIST_VIEW) {
		choice_put_centered(
			BOX_MAIN_CENTER_X, 3, -1, COMMAND_REGIST_VIEW, atrb
		);
	} else if(sel == MC_OPTION) {
		choice_put_centered(BOX_MAIN_CENTER_X, 4, -1, COMMAND_OPTION, atrb);
	} else if(sel == MC_QUIT) {
		choice_put_centered(BOX_MAIN_CENTER_X, 5, -1, COMMAND_QUIT, atrb);
	}
}

#pragma option -a2

void pascal near option_choice_put(int sel, tram_atrb2 atrb)
{
	enum {
		// ZUN quirk: Not the center of the left column.
		LABEL_CENTER_X = BOX_MAIN_CENTER_X,

		VALUE_LEFT = BOX_SUBMENU_CENTER_X,
		VALUE_W = (BOX_SUBMENU_RIGHT - VALUE_LEFT),
		VALUE_TRAM_LEFT = (VALUE_LEFT / GLYPH_HALF_W),
		VALUE_CENTER_X = (VALUE_LEFT + (VALUE_W / 2)),
	};

	if(sel == OC_RANK) {
		choice_put_centered(LABEL_CENTER_X, 0, 0, LABEL_RANK, atrb);
		text_putsa(
			(VALUE_TRAM_LEFT + 2), // This is bloat anyway, who cares
			choice_tram_y(0),
			"        ",
			TX_WHITE
		);
		switch(resident->rank) {
		case RANK_EASY:
			choice_put_centered(VALUE_CENTER_X, 0, 1, VALUE_EASY, atrb);
			break;
		case RANK_NORMAL:
			choice_put_centered(VALUE_CENTER_X, 0, 1, VALUE_NORMAL, atrb);
			break;
		case RANK_HARD:
			choice_put_centered(VALUE_CENTER_X, 0, 1, VALUE_HARD, atrb);
			break;
		case RANK_LUNATIC:
			choice_put_centered(VALUE_CENTER_X, 0, 1, VALUE_LUNATIC, atrb);
			break;
		}
	} else if(sel == OC_BGM) {
		choice_put_centered(LABEL_CENTER_X, 2, -1, LABEL_MUSIC, atrb);
		switch(resident->bgm_mode) {
		case SND_BGM_OFF:
			gaiji_putsa(VALUE_TRAM_LEFT, choice_tram_y(2), VALUE_OFF, atrb);
			break;
		case SND_BGM_FM:
			gaiji_putsa(VALUE_TRAM_LEFT, choice_tram_y(2), VALUE_FM, atrb);
			break;
		case SND_BGM_MIDI:
			gaiji_putsa(VALUE_TRAM_LEFT, choice_tram_y(2), VALUE_MIDI, atrb);
			break;
		}
	} else if(sel == OC_KEY_MODE) {
		choice_put_centered(LABEL_CENTER_X, 4, -1, LABEL_KEYCONFIG, atrb);
		switch(resident->key_mode) {
		case KM_KEY_KEY:
			choice_put_centered(VALUE_CENTER_X, 4, -1, VALUE_KEY_KEY, atrb);
			break;
		case KM_JOY_KEY:
			choice_put_centered(VALUE_CENTER_X, 4, -1, VALUE_JOY_KEY, atrb);
			break;
		case KM_KEY_JOY:
			choice_put_centered(VALUE_CENTER_X, 4, -1, VALUE_KEY_JOY, atrb);
			break;
		}
	} else if(sel == OC_QUIT) {
		choice_put_centered(BOX_SUBMENU_CENTER_X, 5, 0, COMMAND_QUIT, atrb);
	}
}

void pascal near menu_sel_update_and_render(int8_t max, int8_t direction)
{
	menu_put(menu_sel, TX_BLACK);
	menu_sel += direction;
	if(menu_sel < ring_min()) {
		menu_sel = max;
	}
	if(menu_sel > max) {
		menu_sel = 0;
	}
	menu_put(menu_sel, TX_WHITE);
}

#define menu_init(in_this_menu, input_allowed, choice_count, put) { \
	input_allowed = false; /* ZUN bloat: Redundant */ \
	for(int i = 0; i < choice_count; i++) { \
		put(i, ((menu_sel == i) ? TX_WHITE : TX_BLACK)); \
	} \
	menu_put = put; \
	in_this_menu = true; \
	input_allowed = false; \
}

inline void return_from_other_screen_to_main(
	bool& in_this_menu, bool& main_input_allowed
) {
	op_fadein_animate();
	wait_for_input_or_start_demo_then_box_to_main_animate();
	select_cdg_load_part2_of_4();
	in_this_menu = false;
	main_input_allowed = false;
	in_main = true;
}

// Sure, *maybe* these names should point out the possibility of a blocking
// box transition animation, but main_update_and_render() also directly enters
// the even more blocking character selection and Music Room screens.
void near main_update_and_render(void)
{
	#define input_allowed	main_input_allowed
	static bool in_this_menu = false;

	if(!in_this_menu) {
		text_clear();
		if(!in_main) {
			box_submenu_to_main_animate();
		}
		in_main = false; // ZUN bloat: Why is this set here, and now?
		menu_init(in_this_menu, input_allowed, MC_COUNT, main_choice_put);
	}

	if(input_sp == INPUT_NONE) {
		input_allowed = true;
	}
	if(!input_allowed) {
		return;
	}
	menu_update_vertical(input_sp, MC_COUNT);
	if((input_sp & INPUT_OK) || (input_sp & INPUT_SHOT)) {
		switch(menu_sel) {
		case MC_STORY:
			story_menu();
			return_from_other_screen_to_main(in_this_menu, input_allowed);
			return;
		case MC_VS:
			resident->playchar_paletted[0].set(PLAYCHAR_REIMU);
			resident->playchar_paletted[1].set(PLAYCHAR_REIMU);
			vs_menu();
			return_from_other_screen_to_main(in_this_menu, input_allowed);
			return;
		case MC_MUSICROOM:
			/* TODO: Replace with the decompiled call
			* 	musicroom_menu();
			* once the segmentation allows us to, if ever */
			_asm { nop; push cs; call near ptr musicroom_menu; }

			return_from_other_screen_to_main(in_this_menu, input_allowed);
			return;
		case MC_REGIST_VIEW:
			score_menu();
			break; // launches into MAINL.EXE
		case MC_OPTION:
			in_this_menu = false;
			in_option = true;
			menu_sel = OC_RANK;
			break;
		case MC_QUIT:
			in_this_menu = false; // We're quitting anyway...
			quit = true;
			break;
		}
	}
	if(input_sp & INPUT_CANCEL) {
		quit = true;
	}
	if(input_sp != INPUT_NONE) { // Covers all previous input cases too! Good!
		input_allowed = false;
	}

	#undef input_allowed
}

#define snd_flip() { \
	if(!snd_sel_disabled) { \
		if(resident->bgm_mode == SND_BGM_OFF) { \
			resident->bgm_mode = SND_BGM_FM; \
			snd_kaja_func(KAJA_SONG_STOP, 0); \
			snd_determine_mode(); \
			snd_kaja_func(KAJA_SONG_PLAY, 0); \
		} else { \
			resident->bgm_mode = SND_BGM_OFF; \
			snd_kaja_func(KAJA_SONG_STOP, 0); \
			snd_active = false; \
		} \
		/* ZUN bloat: Already done at the call site. */ \
		option_choice_put(menu_sel, TX_WHITE); \
	} \
}

inline void return_from_option_to_main(bool& option_initialized) {
	option_initialized = false;
	menu_sel = MC_OPTION;
	in_option = false;
}

void near option_update_and_render(void)
{
	#define input_allowed	option_input_allowed
	static bool in_this_menu = false;

	if(!in_this_menu) {
		text_clear();
		box_main_to_submenu_animate();
		menu_init(in_this_menu, input_allowed, OC_COUNT, option_choice_put);
	}

	if(input_sp == INPUT_NONE) {
		input_allowed = true;
	}
	if(!input_allowed) {
		return;
	}
	menu_update_vertical(input_sp, OC_COUNT);

	// ZUN bloat: Could have been deduplicated.
	if(input_sp & INPUT_RIGHT) {
		switch(menu_sel) {
		case OC_RANK:
			ring_inc_range(resident->rank, RANK_EASY, RANK_LUNATIC);
			break;
		case OC_BGM:
			snd_flip();
			break;
		case OC_KEY_MODE:
			ring_inc_range(resident->key_mode, KM_KEY_KEY, KM_KEY_JOY);
			break;
		}
		option_choice_put(menu_sel, TX_WHITE);
	}
	if(input_sp & INPUT_LEFT) {
		switch(menu_sel) {
		case OC_RANK:
			ring_dec_range(resident->rank, RANK_EASY, RANK_LUNATIC);
			break;
		case OC_BGM:
			snd_flip();
			break;
		case OC_KEY_MODE:
			ring_dec_range(resident->key_mode, KM_KEY_KEY, KM_KEY_JOY);
			break;
		}
		option_choice_put(menu_sel, TX_WHITE);
	}

	if((input_sp & INPUT_OK) || (input_sp & INPUT_SHOT)) {
		if(menu_sel == OC_QUIT) {
			return_from_option_to_main(in_this_menu);
		}
	}
	if(input_sp & INPUT_CANCEL) {
		return_from_option_to_main(in_this_menu);
	}
	if(input_sp != INPUT_NONE) { // Covers all previous input cases too! Good!
		input_allowed = false;
	}

	#undef input_allowed
}
