// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#pragma option -zCSHARED -WX -k-

#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/th02/snd/impl.hpp"

void snd_se_reset(void)
{
	snd_se_frame = 0;
	snd_se_playing = SE_NONE;
}
#pragma codestring "\x90"
