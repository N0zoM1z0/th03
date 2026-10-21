// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#pragma option -zCSHARED

#include "x86real.h"
#include "compat/rec98/th02/snd/snd.h"

void snd_delay_until_volume(uint8_t volume)
{
	while(1) {
		_AH = KAJA_GET_VOLUME;
		if(snd_midi_active != true) {
			geninterrupt(PMD);
		} else {
			geninterrupt(MMD);
		}
		_asm { cmp	al, volume; }
		_asm { jz 	end; }
	}
end:
}
#pragma codestring "\x90"
