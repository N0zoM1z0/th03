#ifndef TH03_MAIN_BOSS_MARISA_HPP
#define TH03_MAIN_BOSS_MARISA_HPP


extern "C" {
void far pascal boss_marisa_template_init(int player_id);
void far gba_boss_update_marisa(void);
void far gba_boss_render_marisa(void);
}

#endif
