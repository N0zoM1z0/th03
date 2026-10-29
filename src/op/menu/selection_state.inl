// Declarations for the character-selection tail TU. Functions remain in
// character_selection.inl; its unlock helper is compiled in the preceding TU.
#pragma option -zPgroup_01

#include "compat/rec98/th03/op/m_select.hpp"
#include "compat/rec98/decomp.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th01/math/clamp.hpp"
#include "compat/rec98/th02/v_colors.hpp"
#include "compat/rec98/th02/hardware/frmdelay.h"
#include "compat/rec98/th02/formats/bfnt.h"
#include "compat/rec98/th03/common.h"
#include "compat/rec98/th03/resident.hpp"
#include "compat/rec98/th03/formats/cdg.h"
extern "C" {
#include "compat/rec98/th03/formats/hfliplut.h"
}
#include "compat/rec98/th03/formats/scoredat.hpp"
#include "compat/rec98/th03/gaiji/gaiji.h"
#include "compat/rec98/th03/hardware/input.h"
#include "compat/rec98/th03/math/polar.hpp"
#include "compat/rec98/th03/shiftjis/fns.hpp"
#include "compat/rec98/th03/snd/snd.h"
#include "compat/rec98/th03/sprites/op_cdg.hpp"

static const char* PLAYCHAR_PIC_FN[PLAYCHAR_COUNT] = PLAYCHAR_PIC_FN_DEF;

static const int STAT_COUNT = 3;
static const uint8_t PLAYCHAR_STATS[PLAYCHAR_COUNT][STAT_COUNT] = {
	{ 3, 1, 5 },
	{ 4, 4, 2 },
	{ 3, 4, 3 },
	{ 2, 3, 1 },
	{ 4, 1, 4 },
	{ 2, 2, 5 },
	{ 4, 5, 1 },
	{ 5, 2, 4 },
	{ 5, 5, 3 },
};
static const unsigned char g_CURSOR_TOP[PLAYER_COUNT][gc_GAIJI_W + 1] = {
	{ gc_P1_TOP_1, gc_P1_TOP_2 },
	{ gc_P2_TOP_1, gc_P2_TOP_2 },
};
static const unsigned char g_CURSOR_BOTTOM[PLAYER_COUNT][gc_GAIJI_W + 1] = {
	{ gc_P1_BOTTOM_1, gc_P1_BOTTOM_2 },
	{ gc_P2_BOTTOM_1, gc_P2_BOTTOM_2 },
};

static const pixel_t PIC_W = 192;
static const pixel_t PIC_H = 192;
static const pixel_t PIC_MARGIN_X = 32;

static const pixel_t NAME_W = 128;
static const pixel_t NAME_H = 16;
static const pixel_t NAME_PADDING_Y = 4;
static const pixel_t NAME_PADDED_H = (NAME_H + NAME_PADDING_Y);

static const pixel_t STATS_W = 128;
static const pixel_t EXTRA_W = 64;
static const pixel_t EXTRA_FOR_PLAYCHAR_W = 32;

static const pixel_t STAT_STAR_W = 9;
static const pixel_t STAT_STAR_PADDED_W = (STAT_STAR_W + 2);
static const pixel_t STAT_STAR_H = 16;

static const screen_x_t P1_LEFT = PIC_MARGIN_X;
static const screen_x_t P2_LEFT = (RES_X - PIC_MARGIN_X - PIC_W);
static const screen_y_t PIC_TOP = 96;

static const screen_x_t NAMES_LEFT = ((RES_X / 2) - (NAME_W / 2));
static const screen_y_t NAMES_TOP = 136;
static const screen_y_t STATS_TOP = (PIC_TOP + PIC_H + 16);

static bool input_locked[PLAYER_COUNT] = { false, false };

// Native state has WORD-aligned pointer/WORD objects. The gaps after the
// cycle and page BYTEs are compiler alignment, not dummy source variables.
#pragma option -a2
static unsigned char curve_cycle;
resident_t far* resident;
static playchar_t sel[PLAYER_COUNT];
static bool sel_confirmed[PLAYER_COUNT];
static page_t page_shown;
func_t_near input_mode;
static unsigned int fadeout_frame_third;
static int16_t curve_unused; // Written as200 by select_init_and_load().
static int curve_trail_count;
static unsigned char playchars_available;
// Keep the actual BYTE-aligned function layout in the following include.
#pragma option -a-
