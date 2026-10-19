#ifndef TH03_TAIL_WARNING_RESEARCH_HPP
#define TH03_TAIL_WARNING_RESEARCH_HPP
// Research-only complete-function source. Historical storage remains external.
#pragma option -a1
#include "compat/rec98/th03/main/player/stuff.hpp"
#include "compat/rec98/th03/resident.hpp"
#include "compat/rec98/th03/main/hud/warning.hpp"
#include "compat/rec98/th03/main/player/gba.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "compat/rec98/th03/hardware/palette.hpp"
#pragma option -a2
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th03/formats/mrs.hpp"
#include "compat/rec98/th02/snd/snd.h"
#include "src/main/hud/static.hpp"
#include "src/main/hardware/frame_delay.hpp"
#include <stddef.h>

extern unsigned char round_quit_requested;
extern unsigned char warning_brightness[PLAYER_COUNT];
extern unsigned char warning_fading_out[PLAYER_COUNT];
extern const char near warning_title_top[], warning_title_middle[];
extern const char near warning_title_bottom[], warning_forced_to_evade[];
extern const char near warning_gauge_level[], warning_boss_level[];
extern const char near warning_life_in_peril[], warning_clear_line[];
// Input constants/input_sp already arrive through the packed player header.
extern "C" {
void near round_pause_or_quit(void);
void near round_C830(void);
void near round_C8C4(void);
void far pascal round_C9FE(pid_t player);
void far round_CA3C(void);
void near pascal warning_text_put(pid_t player, unsigned int attribute);
void far pascal round_CB81(pid_t player);
void far pascal palette_restore_for_pid(pid_t player);
// Private historical entries: assembly calls ONLY. These are not stack APIs.
void near hud_gauge_highlight_fill(void); // B398: BX=VRAM offset; shared B37F tail.
void near hud_gauge_highlights_restore(void); // B3A2: EGC copy; restores DS/SI/DI.
void near hud_gauge_bar_fill(void); // B3F6: DX=pixel x, BX=width; preserves SI/DI.
}
#define CHECK_FIELD(F,O,S) typedef char warning_##F[((offsetof(player_stuff_t,F)==O)&&(sizeof(((player_stuff_t near *)0)->F)==S))?1:-1]
CHECK_FIELD(gauge_charged,0x18,2);
CHECK_FIELD(gauge_avail,0x1A,2);
CHECK_FIELD(hyper_active,0x1E,1);
#undef CHECK_FIELD
typedef char warning_player_layout[(sizeof(player_stuff_t)==128 && sizeof(pid_t)==1 && sizeof(pid2)==2)?1:-1];
typedef char warning_flag_width[(sizeof(warning_flag_t)==1 && sizeof(gba_flag_t)==1)?1:-1];
#endif
