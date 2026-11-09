#pragma option -zCSHARED -k-

#include "src/main/sound/se.hpp"

// The original PMD sound-effect service is a fixed PC-98 software vector.
// Its AH operation code and AL effect number are hardware ABI fields,
// not ordinary 16-bit C++ call arguments.
enum { TH03_SE_PMD_VECTOR = 0x60 };

void far pascal snd_se_play(int new_se)
{
    register int se = new_se;
    // A disabled sound driver returns before any priority lookup.
    if(!snd_se_active()) {
        return;
    }
    // Selecting the first effect returns before the priority comparison.
    // Keep the original priority operands for the replacement case.
    if(snd_se_playing == SE_NONE) {
        snd_se_playing = se;
        return;
    }
    if(snd_se_priorities[snd_se_playing] <= snd_se_priorities[se]) {
        snd_se_playing = se;
        snd_se_frame = 0;
    }
}

void far snd_se_update(void)
{
    // The second service only emits an interrupt while FM is active
    // and a real effect is selected; the driver-active check comes first.
    if((!snd_se_active()) || (snd_se_playing == SE_NONE)) {
        return;
    }
    // This direct register-service source compiles the exact original
    // PMD INT vector; the previous tiny reference helper is unnecessary.
    // Only the zero frame emits AH=0x0C/AL=effect at INT 60h;
    // the original two byte registers are not ordinary C++ args.
    if(!snd_se_frame) {
        _AH = PMD_SE_PLAY;
        _AL = snd_se_playing;
        geninterrupt(TH03_SE_PMD_VECTOR);
    }
    // Byte-memory postfix is codegen-visible: prefix changed TC4
    // output (af908c). The ordinary reversed duration comparison
    // below IS native-exact (af908d), unlike priority lookup above.
    snd_se_frame++;
    if(snd_se_frame > snd_se_priority_frames[snd_se_playing]) {
        snd_se_frame = 0;
        snd_se_playing = SE_NONE;
    }
}
