// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#pragma option -zCSHARED -Z

#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th03/core/initexit.h"

void game_exit_from_mainl_to_main()
{
	pfend();
	graph_accesspage(0);
	graph_showpage(0);
	vsync_end();
	mem_unassign();
	js_end();
	egc_start();
}
