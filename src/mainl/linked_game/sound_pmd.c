// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#pragma option -zCSHARED -k-

#include "x86real.h"
#include "compat/rec98/th02/snd/snd.h"

bool16 snd_pmd_resident(void)
{
	snd_interrupt_if_midi = PMD;
	snd_midi_active = false;
	snd_fm_possible = false;
	snd_midi_possible = false;

	_ES = 0;
	_asm { les bx, dword ptr es:[PMD * 4] };
	if(kaja_isr_magic_matches(MK_FP(_ES, _BX), 'P', 'M', 'D')) {
		return true;
	}
	return false;
}
#pragma codestring "\x90"
