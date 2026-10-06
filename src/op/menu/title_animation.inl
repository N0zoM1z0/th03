// ZUN bloat: Only contains animations, the rest is in `op_01.cpp`.

#include "compat/rec98/th03/op/m_main.hpp"
#include "compat/rec98/th02/hardware/frmdelay.h"
#include "compat/rec98/th02/formats/pi.h"
#include "compat/rec98/th03/snd/snd.h"
#include "compat/rec98/th03/op/m_select.hpp"
#include "compat/rec98/th03/shiftjis/fns.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/platform/x86real/pc98/page.hpp"
#include "compat/rec98/platform/x86real/flags.hpp"
#include "compat/rec98/planar.h"

inline void title_load_opwin_and_bgm(void) {
	super_entry_bfnt("opwin.bft");
	snd_kaja_func(KAJA_SONG_STOP, 0);
	snd_load(BGM_MENU_MAIN_FN, SND_LOAD_SONG);
}

void near op_animate(void)
{
	enum {
		COL_SHADOW = 11, // Shadow behind the 東方夢時空 kanji. Faded to #888.
		COL_BG = 15, // Background
		SHIFT_DELTA = 2,
	};

	int i;
	int brightness = 0;
	page_t page = 0;

	title_load_opwin_and_bgm();
	pi_load(0, "TL01.PI");

	// TODO: Investigate whether this is a landmine once MAINL.EXE has reached
	// 100% RE and we know all possible VRAM and palette states at this point.
	palette_settone(0);

	graph_accesspage(1);
	pi_put_8(0, 0, 0);

	graph_accesspage(0);
	pi_palette_apply(0);
	pi_put_8(0, 0, 0);

	// Pre-shift only VRAM page 0 by 2 pixels. With this initial displacement,
	// each iteration of the page-flipped loop below only has to shift the
	// single respectively next page by a consistent 4 pixels to end up with an
	// animation at a smooth 2 pixels per frame.
	egc_shift_left_all(SHIFT_DELTA);

	Palettes[COL_BG].set(0x00, 0x00, 0x00);
	palette_show(); // ZUN bloat: Redundant
	Palettes[COL_SHADOW].set(0x00, 0x00, 0x00);
	palette_show();
	pi_free(0);

	pi_load(0, MENU_MAIN_BG_FN);
	graph_showpage(1);

	// Fade in and move. These values do actually represent the X position of
	// the 東方夢時空 kanji in TL01.PI (160) and TL02.PI, respectively. That 17
	// is still awkward though.
	for(i = 160; i > 17; i -= SHIFT_DELTA) {
		frame_delay(1);

		Palettes[COL_BG].c.r = brightness;
		Palettes[COL_BG].c.g = brightness;
		Palettes[COL_BG].c.b = brightness;
		palette_show(); // ZUN bloat: Redundant
		if(brightness <= 0x80) {
			Palettes[COL_SHADOW].c.r = brightness;
			Palettes[COL_SHADOW].c.g = brightness;
			Palettes[COL_SHADOW].c.b = brightness;
		}
		palette_show();
		if(brightness <= 100) {
			palette_settone(brightness);
		}
		brightness += 2;
		graph_showpage(page);
		page = (1 - page);
		graph_accesspage(page);
		egc_shift_left_all(SHIFT_DELTA * 2);
	}

	// Complete fade-in
	while(brightness < 0xFF) {
		Palettes[COL_BG].c.r = brightness;
		Palettes[COL_BG].c.g = brightness;
		Palettes[COL_BG].c.b = brightness;
		palette_show();
		brightness += 2;
		frame_delay(1);
	}

	vsync_Count1 = 0;
	select_cdg_load_part3_of_4();
	while(vsync_Count1 < 16) {
	}

	// Flash
	for(i = 0; i < 8; i++) {
		palette_settone(200);
		frame_delay(1);
		palette_settone(100);
		frame_delay(1);
	}

	palette_settone(200);
	snd_kaja_func(KAJA_SONG_PLAY, 0);
	graph_showpage(0);
	graph_accesspage(0);
	pi_palette_apply(0);
	pi_put_8(0, 0, 0);
	frame_delay(1);

	palette_settone(100);
	frame_delay(1);

	// Flash again
	for(i = 0; i < 8; i++) {
		palette_settone(200);
		frame_delay(1);
		palette_settone(100);
		frame_delay(1);
	}

	graph_accesspage(1);
	pi_put_8(0, 0, 0);
	graph_accesspage(0);
	pi_free(0);

	select_cdg_load_part1_of_4();
}

void near op_fadein_animate(void)
{
	title_load_opwin_and_bgm();

	// ZUN landmine: Will cause tearing if we return from the Music Room, which
	// leaves with VRAM cleared to color 0 but still keeps its purple color in
	// palette slot 0.
	palette_settone(0);

	pi_load(0, MENU_MAIN_BG_FN);
	graph_showpage(0);

	// This function is called either on startup (where we haven't loaded any
	// of these), or when leaving the character selection menu or the Music
	// Room (both of which free all .CDG sprites).
	select_cdg_load_part3_of_4();

	graph_accesspage(1);
	pi_put_8(0, 0, 0);

	graph_accesspage(0);
	pi_palette_apply(0);
	pi_put_8(0, 0, 0);
	graph_accesspage(0); // ZUN bloat: Redundant
	pi_free(0);

	select_cdg_load_part1_of_4();

	snd_kaja_func(KAJA_SONG_PLAY, 0);
	for(int i = 0; i <= 100; i += 4) {
		// At least this one doesn't constitute an additional landmine because
		// the `palette_settone(0)` call on the first iteration matches the
		// call at the beginning of the function.
		palette_settone(i);
		frame_delay(1);
	}
}

void near box_main_to_submenu_animate(void)
{
	for(
		screen_x_t right_left = (BOX_MAIN_RIGHT - OPWIN_STEP_W);
		right_left < (BOX_SUBMENU_RIGHT - OPWIN_STEP_W);
		right_left += OPWIN_STEP_W
	) {
		box_column16_unput(right_left);
		super_put(right_left, BOX_TOP, OPWIN_RIGHT);
		frame_delay(1);
	}
}

void near box_submenu_to_main_animate(void)
{
	for(
		screen_x_t right_left = (BOX_SUBMENU_RIGHT - OPWIN_W);
		right_left >= (BOX_MAIN_RIGHT - OPWIN_W);
		right_left -= OPWIN_STEP_W
	) {
		box_column16_unput(right_left + OPWIN_STEP_W);
		super_put(right_left, BOX_TOP, OPWIN_RIGHT);
		frame_delay(1);
	}
}

