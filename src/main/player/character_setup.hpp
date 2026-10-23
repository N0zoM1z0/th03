#ifndef TH03_MAIN_CHARACTER_SETUP_HPP
#define TH03_MAIN_CHARACTER_SETUP_HPP

// MAIN_01 near entries; Pascal arguments occupy 16-bit stack words.
extern "C" {
void near pascal character_sprite_pair_load(int slot, char far *filename);
void near character_sprites_finalize(void);
void near pascal character_resources_load(int pid, int resource);
void near pascal set_callbacks_reimu(int pid);
void near pascal set_callbacks_mima(int pid);
void near pascal set_callbacks_marisa(int pid);
void near pascal set_callbacks_ellen(int pid);
void near pascal set_callbacks_kotohime(int pid);
void near pascal set_callbacks_kana(int pid);
void near pascal set_callbacks_rikako(int pid);
void near pascal set_callbacks_chiyuri(int pid);
void near pascal set_callbacks_yumemi(int pid);
}
#endif
