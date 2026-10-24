#ifndef TH03_MAIN_ENTRY_HPP
#define TH03_MAIN_ENTRY_HPP
#pragma option -a1
#include "src/main/core/resident.hpp"
#pragma option -a2
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "compat/rec98/th03/snd/snd.h"
#include "compat/rec98/th03/gaiji/gaiji.h"
#include "src/main/core/initmain.hpp"
#include "src/main/enemy/enemy.hpp"
resident_t __seg* near cfg_load_resident_ptr(void);
extern const unsigned char main_archive_name[];
extern const char main_gaiji_font[];
extern const char main_op_name[], main_ending_name[];
extern void (far *main_background_init)(void);
#include "src/main/core/execl.hpp"
extern "C" {
void near stage_setup(void);
unsigned char near round_loop(void);
void near round_start_next(void);
}
#endif
