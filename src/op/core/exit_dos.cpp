#pragma option -zCSHARED

#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/th02/core/initexit.h"

void game_exit_to_dos(void)
{
	game_exit();
	key_beep_on();
	text_systemline_show();
	text_cursor_show();
}
