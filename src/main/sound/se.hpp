#ifndef TH03_MAIN_SOUND_SE_HPP
#define TH03_MAIN_SOUND_SE_HPP

#include <dos.h>

static const unsigned char SE_NONE = 0xFF;
static const unsigned char PMD_SE_PLAY = 0x0C;

extern "C" {
extern unsigned char snd_fm_possible;
extern unsigned char snd_se_playing;
extern unsigned char snd_se_priorities[];
extern unsigned char snd_se_priority_frames[];
extern unsigned char snd_se_frame;
}

inline int snd_se_active(void)
{
    return snd_fm_possible;
}

inline int snd_get_param(int &param)
{
    return param;
}

extern "C" {
void far pascal snd_se_play(int new_se);
void far snd_se_update(void);
}

#endif
