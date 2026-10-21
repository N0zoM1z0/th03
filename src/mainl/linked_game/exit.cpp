// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#pragma option -zCSHARED

#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th02/core/initexit.h"

void game_exit(void)
{
	pfend();
	graph_clear_both();

#if (GAME >= 4)
	mem_unassign();
	vsync_end();
#else
	vsync_end();
	mem_unassign();
#endif

	text_clear();

#if (GAME >= 3)
	js_end();
#endif

	egc_start();

#if (GAME >= 4)
	bgm_finish();
#endif
}
