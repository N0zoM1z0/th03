// Compiler-only producer grouping probe. No DATA ownership is moved.
#pragma option -zCREGIST_TEXT
#include "src/mainl/regist.cpp"

extern const char mainl_over_music[];

extern "C" void near mainl_reg_music(void)
{
    snd_kaja_func(KAJA_SONG_STOP, 0);
    snd_load(mainl_over_music, SND_LOAD_SONG);
    snd_kaja_func(KAJA_SONG_PLAY, 0);
    palette_black_in(1);
    snd_delay_until_measure(3, 64);
    palette_black_out(1);
    snd_kaja_func(KAJA_SONG_STOP, 0);
}
