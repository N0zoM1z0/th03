#pragma option -zCSHARED -k-

#include "src/main/sound/se.hpp"

inline void driver_play(unsigned char &se)
{
    _AH = PMD_SE_PLAY;
    _AL = se;
    geninterrupt(0x60);
}

void far pascal snd_se_play(int new_se)
{
    register int se = new_se;
    if(!snd_se_active()) {
        return;
    }
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
    if(!snd_se_frame) {
        driver_play(snd_se_playing);
    }
    snd_se_frame++;
    if(snd_se_priority_frames[snd_se_playing] < snd_se_frame) {
        snd_se_frame = 0;
        snd_se_playing = SE_NONE;
    }
}
