// The complete original HUD_STAT_TEXT physical owner: all static HUD
// character routines and the full two-player dispatcher. Every typed
// C++ loop below is source-native byte-exact under original TC4 4.02.
#pragma option -zCHUD_STAT_TEXT

#include "src/main/hud/static.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/gaiji/gaiji.h"
#include "compat/rec98/th03/resident.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

void hud_wipe(void)
{
	text_fillca(' ', (TX_BLACK | TX_REVERSE));

	// Include the bottom row of TRAM, which contains the gauge.
	text_boxfilla(
		playfield_tram_x(0, 0),
		PLAYFIELD_TRAM_TOP,
		(playfield_tram_x(0, PLAYFIELD_W) - 1),
		((RES_Y / GLYPH_H) - 1),
		TX_WHITE
	);
	text_boxfilla(
		playfield_tram_x(1, 0),
		PLAYFIELD_TRAM_TOP,
		(playfield_tram_x(1, PLAYFIELD_W) - 1),
		((RES_Y / GLYPH_H) - 1),
		TX_WHITE
	);
}

void pascal hud_static_halfhearts_put(pid_t pid)
{
	enum {
		HALFHEARTS_W = ((HALFHEARTS_MAX / 2) * GAIJI_W),
	};

	tram_x_t x;
	int halfheart_i = 0;
	if(!pid) {
		x = (playfield_tram_x(0, ((PLAYFIELD_W / 2) - (HALFHEARTS_W / 2))));
	} else {
		x = (playfield_tram_x(1, ((PLAYFIELD_W / 2) - (HALFHEARTS_W / 2))));
	}
	int halfhearts;
	tram_y_t y = PLAYFIELD_TRAM_TOP;

	halfhearts = players[pid].halfhearts;
	// The original full-/half-heart renderer is exact as a natural for,
	// with the signed two-halfheart step after the individual gaiji call.
	for(; halfheart_i < halfhearts; halfheart_i += 2) {
		if((halfhearts - halfheart_i) >= 2) {
			gaiji_putca(x, y, gs_HEART_FULL, TX_WHITE);
		} else {
			gaiji_putca(x, y, gs_HEART_HALF, TX_WHITE);
		}
		x += GAIJI_TRAM_W;
	}

	// Fill remaining space with empty hearts, not a second independent
	// counter: the same signed index continues from the prior loop.
	for(; halfheart_i < HALFHEARTS_MAX; halfheart_i += 2) {
		gaiji_putca(x, y, gs_HEART_EMPTY, TX_WHITE);
		x += GAIJI_TRAM_W;
	}
}

// ZUN bloat: The simple horizontal gaiji_putca() loop in all of the functions
// below could have been moved out into a separate function.

void pascal hud_static_bombs_put(pid_t pid)
{
	tram_x_t x;
	int i = 0;
	int bombs;
	tram_y_t y;
	tram_cell_amount_t step;
	if(!pid) {
		x = playfield_tram_x(0, (PLAYFIELD_W - GAIJI_W));
		step = -GAIJI_TRAM_W;
	} else {
		x = playfield_tram_x(1, 0);
		step = +GAIJI_TRAM_W;
	}
	y = ((PLAYFIELD_BOTTOM - GLYPH_H) / GLYPH_H);

	bombs = players[pid].bombs;
	// Bomb glyphs traverse in opposite directions for the two players;
	// this native for preserves step sign and one final clear-cell write.
	for(; i < bombs; ++i) {
		gaiji_putca(x, y, gs_BOMB, TX_WHITE);
		x += step;
	}

	// In case we lost a single bomb on this frame… Very clever!
	gaiji_putca(x, y, g_SP, TX_WHITE);
}

void pascal near hud_static_rounds_won_put(pid_t pid)
{
	tram_x_t x;
	int i = 0;
	if(!pid) {
		x = playfield_tram_x(0, 0);
	} else {
		x = playfield_tram_x(1, 0);
	}

	int rounds_won = players[pid].rounds_won;
	for(; i < rounds_won; ++i) {
		gaiji_putca(x, PLAYFIELD_TRAM_TOP, gs_THALIA, TX_WHITE);
		x += GAIJI_TRAM_W;
	}
}

void near hud_static_story_lives_put(void)
{
	int i = 0;
	tram_x_t x = playfield_tram_x(0, (PLAYFIELD_W - GAIJI_W));
	int lives = resident->story_lives;
	for(; i < lives; ++i) {
		gaiji_putca(x, (PLAYFIELD_TRAM_TOP + 1), gs_YINYANG, TX_WHITE);
		x -= GAIJI_TRAM_W;
	}
}

void pascal hud_static_gauge_levels_put(pid2 pid)
{
	int level;
	tram_x_t x = playfield_tram_x(0, 0);
	if(pid) {
		x += (PLAYFIELD_W_BORDERED / GLYPH_HALF_W);
	}

	level = gba_gauge_level[pid];
	gaiji_putca(x, (PLAYFIELD_BOTTOM / GLYPH_H), (gpd_1 - 1 + level), TX_GREEN);
	x += ((PLAYFIELD_W / GLYPH_HALF_W) - GAIJI_TRAM_W);

	// This branch seems to confirm the interpretation that these digits
	// display the *next* Boss Attack level, not the current one. If the level
	// is already at the maximum, additional attacks won't increase it further.
	level = gba_boss_level;
	// Preserve >=MAX (TC4 machine code differs from >MAX-1 even though
	// ordinary integer comparisons are equivalent, negative af887f).
	if(level >= GBA_BOSS_LEVEL_MAX) {
		// A bit brave to assume that [level] will never be greater than
		// [GBA_BOSS_LEVEL_MAX]. On the other hand, it's great for debugging as
		// any invalid state would render as a non-proportional-digit gaiji.
		level--;
	}
	gaiji_putca(x, (PLAYFIELD_BOTTOM / GLYPH_H), (gpd_1 + level), TX_RED);
}

void hud_static_put(void)
{
	// Native two-player HUD dispatcher, with all four per-player calls
	// and their exact original order before incrementing the index.
	// Draw both complete player HUDs in the native call order before
	// advancing the signed player index in the for header.
	for(int i = 0; i < PLAYER_COUNT; ++i) {
		hud_static_halfhearts_put(i);
		hud_static_bombs_put(i);
		hud_static_rounds_won_put(i);
		hud_static_gauge_levels_put(i);
	}
	if(resident->game_mode == GM_STORY) {
		hud_static_story_lives_put();
	}
}
