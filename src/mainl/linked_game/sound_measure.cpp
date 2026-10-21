// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#pragma option -zCSHARED

#include "compat/rec98/th02/hardware/frmdelay.h"
#include "compat/rec98/th02/snd/measure.hpp"

void pascal snd_delay_until_measure(int measure, unsigned int frames_if_no_bgm)
{
	if(!snd_bgm_active()) {
		frame_delay(frames_if_no_bgm);
		return;
	}
	while(snd_get_song_measure() < measure) {
	}
}
