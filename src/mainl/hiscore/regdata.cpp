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

// Original score-menu character order; strings remain external owners.
extern const shiftjis_t mainl_name_none[];
extern const shiftjis_t mainl_name_reimu[];
extern const shiftjis_t mainl_name_mima[];
extern const shiftjis_t mainl_name_marisa[];
extern const shiftjis_t mainl_name_ellen[];
extern const shiftjis_t mainl_name_kotohime[];
extern const shiftjis_t mainl_name_kana[];
extern const shiftjis_t mainl_name_rikako[];
extern const shiftjis_t mainl_name_chiyuri[];
extern const shiftjis_t mainl_name_yumemi[];

const shiftjis_t* REGIST_PLAYCHARS[] = {
    mainl_name_none,
    mainl_name_reimu,
    mainl_name_mima,
    mainl_name_marisa,
    mainl_name_ellen,
    mainl_name_kotohime,
    mainl_name_kana,
    mainl_name_rikako,
    mainl_name_chiyuri,
    mainl_name_yumemi,
};
