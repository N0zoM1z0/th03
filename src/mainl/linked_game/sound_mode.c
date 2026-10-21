// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#pragma option -WX -zCSHARED -k-

#include "x86real.h"
#include "compat/rec98/th02/snd/snd.h"

bool16 snd_determine_mode(void)
{
	_AH = PMD_GET_DRIVER_TYPE_AND_VERSION;
	geninterrupt(PMD);
	_BX = false;
	if(_AL != 0xFF) {
		_BX++;
		snd_fm_possible = true;
	} else {
		_BL = snd_midi_active;
	}
	snd_active = _BL;
	return _BX;
}
#pragma codestring "\x90"
