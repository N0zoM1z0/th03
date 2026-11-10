#pragma option -zCSHARED -k-

#include "src/main/sound/se.hpp"

// The original PMD sound-effect service is a fixed PC-98 software vector.
// Its AH operation code and AL effect number are hardware ABI fields,
// not ordinary 16-bit C++ call arguments.
enum { TH03_SE_PMD_VECTOR = 0x60 };

void far pascal snd_se_play(int new_se)
{
    register int se = new_se;
    // The driver-active gate is positive: a disabled PMD driver never
    // reads the priority table or alters the selected effect.
    if(snd_se_active()) {
        // No predecessor is selected immediately; otherwise compare
        // the original two priority slots in their native read order.
        if(snd_se_playing == SE_NONE) {
            snd_se_playing = se;
        } else if(snd_se_priorities[snd_se_playing] <= snd_se_priorities[se]) {
            snd_se_playing = se;
            snd_se_frame = 0;
        }
    }
}

void far snd_se_update(void)
{
    // Driver availability is tested before the selected-effect slot.
    // Neither the PMD interrupt nor the frame counter changes otherwise.
    if(snd_se_active() && snd_se_playing != SE_NONE) {
        // Exactly frame zero issues the fixed 16-bit PMD register service:
        // AH is the operation, AL the effect, and INT 60h is not a C++ call.
        if(snd_se_frame == 0) {
            _AH = PMD_SE_PLAY;
            _AL = snd_se_playing;
            geninterrupt(TH03_SE_PMD_VECTOR);
        }
        // This is the original byte-memory postfix update, not prefix.
        // Priority-indexed expiration resets the frame *after* its update.
        snd_se_frame++;
        if(snd_se_frame > snd_se_priority_frames[snd_se_playing]) {
            snd_se_frame = 0;
            snd_se_playing = SE_NONE;
        }
    }
}
