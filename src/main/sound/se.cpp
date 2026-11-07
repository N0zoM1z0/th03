#pragma option -zCSHARED -k-

#include "src/main/sound/se.hpp"

// The original PMD sound-effect service is a fixed PC-98 software vector.
// Its AH operation code and AL effect number are hardware ABI fields,
// not ordinary 16-bit C++ call arguments.
enum { TH03_SE_PMD_VECTOR = 0x60 };

void far pascal snd_se_play(int new_se)
{
    register int se = new_se;
    if(!snd_se_active()) {
        return;
    }
    // Retain original priority lookup/evaluation order: reversing the
    // operands compiles a different TC4 object despite equal comparison
    // semantics (genuine negative experiment af834b).
    if(snd_se_playing == SE_NONE) {
        snd_se_playing = se;
    } else if(snd_se_priorities[snd_se_playing] <= snd_se_priorities[se]) {
        snd_se_playing = se;
        snd_se_frame = 0;
    }
}

void far snd_se_update(void)
{
    if(!snd_se_active() || (snd_se_playing == SE_NONE)) {
        return;
    }
    // This direct register-service source compiles the exact original
    // PMD INT vector; the previous tiny reference helper is unnecessary.
    if(!snd_se_frame) {
        _AH = PMD_SE_PLAY;
        _AL = snd_se_playing;
        geninterrupt(TH03_SE_PMD_VECTOR);
    }
    snd_se_frame++;
    if(snd_se_priority_frames[snd_se_playing] < snd_se_frame) {
        snd_se_frame = 0;
        snd_se_playing = SE_NONE;
    }
}
