// TH03 OP Music Room bounded include; complete carrier reviewed separately.
#include <mem.h>
#include "compat/rec98/planar.h"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/game/coords.hpp"
#include "compat/rec98/th02/v_colors.hpp"
#include "compat/rec98/th02/hardware/frmdelay.h"
#include "compat/rec98/th02/formats/musiccmt.hpp"
#include "compat/rec98/th03/hardware/input.h"
#include "compat/rec98/th01/hardware/grppsafx.h"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/th03/formats/cdg.h"
#include "compat/rec98/th03/math/polar.hpp"
#include "compat/rec98/th02/op/m_music.hpp"
#include "compat/rec98/th02/formats/pi.h"
#include "compat/rec98/th03/shiftjis/music.hpp"
static const size_t TRACK_COUNT = (
	sizeof(MUSIC_FILES) / sizeof(MUSIC_FILES[0])
);

// Colors
// ------
// The native caller draws track text on both pages. Comment refreshes also
// recapture the B plane; actual graphics callbacks remain separate evidence.

static const vc_t COL_TRACKLIST_SELECTED = ((GAME >= 4) ? 3 : V_WHITE);
static const vc_t COL_TRACKLIST          = ((GAME >= 4) ? 5 : 3);
static const vc_t COL_CMT_TRACK          = ((GAME >= 4) ? 7 : V_WHITE);
static const vc_t COL_CMT_COMMENT        = ((GAME >= 4) ? 7 : 13);
// ------

// Coordinates
// -----------

static const screen_x_t TRACKLIST_LEFT = ((GAME == 5) ? 12 : 16);
inline screen_y_t track_top(uint8_t sel) {
	return (40 + (sel * GLYPH_H));
}

inline int16_t track_fx(vc_t col) {
	if(GAME >= 4) {
		return col;
	} else {
		return (col | FX_WEIGHT_BOLD);
	}
}

static const pixel_t CMT_LINE_W = (CMT_LINE_LENGTH * GLYPH_HALF_W);
static const vram_byte_amount_t CMT_LINE_VRAM_W = (CMT_LINE_W / BYTE_DOTS);
static const pixel_t CMT_COMMENT_H = (CMT_COMMENT_LINES * GLYPH_H);

static const screen_x_t CMT_TITLE_LEFT = (
	/**/ (GAME >= 3)  ? (RES_X - GLYPH_FULL_W - CMT_LINE_W) :
	/*   (GAME == 2) */ ((RES_X / 2) - (CMT_LINE_W / 2))
);
static const screen_y_t CMT_TITLE_TOP = ((GAME == 5) ? 32 : 64);
static const screen_x_t CMT_TITLE_RIGHT = (CMT_TITLE_LEFT + CMT_LINE_W);
static const screen_y_t CMT_TITLE_BOTTOM = (CMT_TITLE_TOP + GLYPH_H);

static const screen_x_t CMT_COMMENT_LEFT = (RES_X - GLYPH_FULL_W - CMT_LINE_W);
static const screen_y_t CMT_COMMENT_TOP = CMT_TITLE_BOTTOM;
static const screen_x_t CMT_COMMENT_RIGHT = (CMT_COMMENT_LEFT + CMT_LINE_W);
static const screen_x_t CMT_COMMENT_BOTTOM = (CMT_COMMENT_TOP + CMT_COMMENT_H);
// -----------

// ZUN bloat

// Polygon state
// -------------

struct polygon_point_t {
	pixel_t x;
	Subpixel y;
};

static const unsigned int POLYGON_COUNT = 16;

// Native caller visits all sixteen entries in TH03.
static const unsigned int POLYGONS_RENDERED = (
	(GAME == 5) ? (POLYGON_COUNT - 2) : POLYGON_COUNT
);

bool polygons_initialized = false;

// ZUN bloat: Could have been local to polygons_update_and_render().
static screen_point_t points[10];

static polygon_point_t center[POLYGON_COUNT];
static polygon_point_t velocity[POLYGON_COUNT];
static unsigned char angle[POLYGON_COUNT];
static unsigned char angle_speed[POLYGON_COUNT];
// -------------

// Selection state
// ---------------

uint8_t track_playing = 0;
uint8_t music_sel;
page_t music_page_accessed;
// ---------------

// Backgrounds
// -----------

// Persistent intended contents of the B plane, without any polygons drawn on
// top of it.
dots8_t __seg* nopoly_B;

// ZUN bloat: Unused in TH04 and TH05 which use the bgimage system for that,
// but still present in the binary.
Planar<dots8_t far *> cmt_bg;
// -----------

struct cmt_line_t {
	shiftjis_t c[CMT_LINE_SIZE];
};
cmt_line_t cmt[CMT_LINES];

void pascal near track_put_both(uint8_t i, vc_t col)
{
	page_t other_page = (1 - music_page_accessed);
	graph_accesspage(other_page);
	graph_putsa_fx(
		TRACKLIST_LEFT, track_top(i), track_fx(col), MUSIC_CHOICES[i]
	);
	graph_accesspage(music_page_accessed);
	graph_putsa_fx(
		TRACKLIST_LEFT, track_top(i), track_fx(col), MUSIC_CHOICES[i]
	);
}

void pascal near tracklist_put_both(uint8_t sel)
{
	int i;
	for(i = 0; i < sizeof(MUSIC_CHOICES) / sizeof(MUSIC_CHOICES[0]); i++) {
		track_put_both(
			i, ((i == sel) ? COL_TRACKLIST_SELECTED : COL_TRACKLIST)
		);
	}
}

void near nopoly_B_snap(void)
{
	nopoly_B = HMem<dots8_t>::alloc(PLANE_SIZE);
	for(vram_offset_t p = 0; p < PLANE_SIZE; p += int(sizeof(dots32_t))) {
		*reinterpret_cast<dots32_t far *>(nopoly_B + p) = VRAM_CHUNK(B, p, 32);
	}
}

void near nopoly_B_free(void)
{
	HMem<dots8_t>::free(nopoly_B);
}
