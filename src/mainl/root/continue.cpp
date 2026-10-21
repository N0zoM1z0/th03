// Genuine MAINL continue menu. Compiler owns the frame and register saves.
#pragma option -zPgroup_01
#pragma option -zCCONTINUE_TEXT
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th01/hardware/grppsafx.h"
#include "compat/rec98/th03/resident.hpp"
#include "compat/rec98/th03/formats/cdg.h"
#include "compat/rec98/th03/formats/pi.hpp"
#include "compat/rec98/th02/hardware/frmdelay.h"
#include "compat/rec98/th02/snd/snd.h"
#include "compat/rec98/th03/hardware/input.h"
extern shiftjis_t mainl_continue_digit[];
extern const char mainl_continue_over[];
extern "C" int near mainl_continue_menu(void)
{
 int selected = 1;
 int held = 0;
 shiftjis_t far *credits = mainl_continue_digit;
 int i;
 for(i = 0; i < (PLAYER_COUNT * SCORE_DIGITS); i++) {
  ((unsigned char far *)resident->score_last)[i] = 0;
 }
 if(resident->rem_credits == 0) {
  return 0;
 }
 cdg_put_noalpha_8(192, 272, 0);
 cdg_put_noalpha_8(352, 272, 3);
 credits[0] = resident->rem_credits + credits[0];
 graph_putsa_fx(576, 371, 0x2F, credits);
 palette_black_in(1);
 while(1) {
  input_mode_interface();
  if((input_sp & INPUT_LEFT) || (input_sp & INPUT_RIGHT)) {
   if(!held) {
    selected = 1 - selected;
    cdg_put_noalpha_8(192, 272, 2 - (selected * 2));
    cdg_put_noalpha_8(352, 272, (selected * 2) + 1);
    held = 1;
   }
  } else {
   held = 0;
  }
  if((input_sp & INPUT_OK) || (input_sp & INPUT_SHOT)) {
   if(selected == 1) {
    grcg_setcolor(GC_RMW, 0);
    grcg_boxfill(576, 371, 592, 387);
    grcg_off();
    resident->rem_credits--;
    credits[0]--;
    graph_putsa_fx(576, 371, 0x2F, credits);
   }
   break;
  }
  if(input_sp & INPUT_CANCEL) {
   selected = 0;
   break;
  }
  frame_delay(1);
 }
 snd_kaja_func(KAJA_SONG_FADE, 3);
 palette_black_out(1);
 graph_accesspage(0);
 graph_showpage(0);
 PaletteTone = 0;
 palette_show();
 pi_load(0, mainl_continue_over);
 pi_palette_apply(0);
 pi_put_8(0, 0, 0);
 pi_free(0);
 snd_kaja_func(KAJA_SONG_STOP, 0);
 resident->story_stage--;
 resident->story_lives = CREDIT_LIVES;
 return selected;
}
