// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#pragma option -zCSHARED -k-

#include "compat/rec98/th02/snd/impl.hpp"
#if (GAME >= 4)
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/th04/snd/snd.h"

// MODDERS: Just replace with [snd_se_playing].
inline uint16_t for_current(void) {
	_BL = snd_se_playing;
	_BH ^= _BH;
	return _BX;
}

inline void driver_play(unsigned char &se) {
	_AL = snd_se_playing;
	if(snd_se_mode != SND_SE_BEEP) {
		_AH = PMD_SE_PLAY;
		geninterrupt(PMD);
	} else {
		_AH ^= _AH;
		bgm_sound(_AX);
	}
}
#else
#include "compat/rec98/th02/snd/snd.h"

// MODDERS: Just replace with [snd_se_playing].
inline uint16_t for_current(void) {
	return snd_se_playing;
}

inline void driver_play(unsigned char &se) {
	_AH = PMD_SE_PLAY;
	_AL = se;
	geninterrupt(PMD);
}
#endif

void DEFCONV snd_se_play(int new_se)
{
	register int se = snd_get_param(new_se);
	if(!snd_se_active()) {
		return;
	}
	if(snd_se_playing == SE_NONE) {
		snd_se_playing = se;
	} else if(snd_se_priorities[for_current()] <= snd_se_priorities[se]) {
		snd_se_playing = se;
		snd_se_frame = 0;
	}
}
#if (GAME >= 4)
#pragma codestring "\x90"
#endif

void snd_se_update(void)
{
	if(!snd_se_active() || (snd_se_playing == SE_NONE)) {
		return;
	}
	if(snd_se_frame == 0) {
		driver_play(snd_se_playing);
	}
	snd_se_frame++;
	if(snd_se_priority_frames[for_current()] < snd_se_frame) {
		snd_se_frame = 0;
		snd_se_playing = SE_NONE;
	}
}
