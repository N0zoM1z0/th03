// Genuine CFG + win + four complete root procedures, one natural compiler TU.
#pragma option -zPgroup_01
#pragma option -zCROOTPRE_TEXT
#include "src/mainl/linked_game/cfg_resident.cpp"
// The shared CDG header declares a far provider; this TU supplies its real near one.
#define cdg_free_all mainl_foreign_cdg_free_all
#include "src/mainl/linked_game/win.cpp"
#undef cdg_free_all
#include "compat/rec98/th03/formats/pi.hpp"
#include "compat/rec98/th03/snd/snd.h"
#include "compat/rec98/th02/hardware/frmdelay.h"
#include "compat/rec98/th03/hardware/input.h"
extern const char mainl_logo_palette[];
extern char near *mainl_stage_bg;
extern const char near *mainl_stage_number;
extern const char mainl_stage_blank[];
extern "C" int near mainl_story_dispatch(void);
extern "C" void near mainl_stage_load(void);
extern "C" void near pascal cdg_free_all(void)
{
 int slot;
 for(slot = 0; slot < CDG_SLOT_COUNT; slot++) {
  cdg_free(slot);
 }
}
extern "C" void near mainl_win_animate(void)
{
 int cel;
 graph_accesspage(1);
 graph_clear();
 graph_accesspage(0);
 graph_clear();
 graph_showpage(0);
 PaletteTone = 0;
 palette_show();
 graph_show();
 cdg_put_noalpha_8(352, 300, 0);
 snd_kaja_func(KAJA_SONG_PLAY, 0);
 palette_black_in(2);
 snd_delay_until_measure(6, 16);
 for(cel = 1; cel < 5; cel++) {
  cdg_put_noalpha_8(352, 300, cel);
  frame_delay(6);
 }
 snd_delay_until_measure(10, 64);
 PaletteTone = 200;
 palette_show();
 cdg_put_noalpha_8(224, 64, 6);
 cdg_put_noalpha_8(352, 300, 5);
 palette_entry_rgb(mainl_logo_palette);
 palette_show();
 cdg_free_all();
 snd_delay_until_measure(11, 4);
 palette_white_in(1);
 frame_delay(8);
 win_text_put();
 if(!mainl_story_dispatch()) {
  mainl_stage_load();
 }
 while(1) {
  input_mode_interface();
  if(input_sp != INPUT_NONE) {
   break;
  }
  frame_delay(1);
 }
 palette_black_out(1);
}
extern "C" int near mainl_story_dispatch(void)
{
 int char_id;
 if(resident->game_mode != GM_STORY) {
  return 1;
 }
 if(resident->pid_winner != 0) {
  return 1;
 }
 resident->playchar_paletted[1].v = resident->story_opponents[resident->story_stage].v;
 if(resident->story_stage == 7) { return 3; }
 if(resident->story_stage == 8) { return 4; }
 if(resident->story_stage == 9) { return 5; }
 char_id = (resident->playchar_paletted[1].v - 1) / 2;
 if(char_id >= 7) {
  resident->playchar_paletted[1].v = TO_OPTIONAL_PALETTED(PLAYCHAR_REIMU);
 }
 return 0;
}
extern "C" void near mainl_stage_load(void)
{
 unsigned char char_id;
 graph_showpage(0);
 graph_accesspage(1);
 char_id = playchar[0].v;
 cdg_load_single(0, PIC_FN[char_id / 2], char_id & 1);
 char_id = resident->playchar_paletted[1].v - 1;
 cdg_load_single(1, PIC_FN[char_id / 2], char_id & 1);
 char_id = char_id / 2;
 do_not_show_stage_number = 1;
 if(resident->game_mode != GM_STORY) {
  mainl_stage_bg[4] = mainl_stage_bg[4] + 4;
 } else if(char_id == 7) {
  mainl_stage_bg[4] = mainl_stage_bg[4] + 2;
 } else if(char_id == 8) {
  mainl_stage_bg[4]++;
 } else if(resident->story_stage == 6) {
  mainl_stage_bg[4] = mainl_stage_bg[4] + 3;
 } else {
  cdg_load_single(2, mainl_stage_number, resident->story_stage + 1);
  do_not_show_stage_number = 0;
 }
 pi_load(0, mainl_stage_blank);
 pi_put_8(0, 0, 0);
 pi_free(0);
 pi_load(0, mainl_stage_bg);
 pi_put_8(0, 0, 0);
}

// Stage introduction, including its genuine enemy-selection switch.
extern char PLAYCHAR_BGM_FN[];
extern const char mainl_dec_bgm[];
extern const char mainl_intro_frame[];
extern const char mainl_enemy00[];
extern const char mainl_enemy01[];
extern const char mainl_enemy02[];
extern const char mainl_enemy03[];
extern const char mainl_enemy04[];
extern const char mainl_sound_effects[];
extern const unsigned char far *mainl_char_info[18];
#define mainl_char_titles mainl_char_info
#define mainl_char_names (mainl_char_info + 1)
extern "C" void near pascal mainl_shot_load(int player);
extern "C" void near mainl_stage_intro(void)
{
 char near *bgm_fn = PLAYCHAR_BGM_FN;
 const char near *dec_bgm_fn = mainl_dec_bgm;
 int char_id;
 PaletteTone = 0;
 palette_show();
 pi_palette_apply(0);
 graph_copy_page(0);
 pi_free(0);
 cdg_put_8(96, 96, 0);
 cdg_put_hflip_8(352, 96, 1);
 if(!do_not_show_stage_number) {
  cdg_put_8(384, 46, 2);
 }
 cdg_free(0);
 cdg_free(1);
 cdg_free(2);
 char_id = ((resident->playchar_paletted[0].v - 1) / 2) * 2;
 graph_putsa_fx(80, 292, (V_WHITE | FX_WEIGHT_BOLD), mainl_char_titles[char_id]);
 graph_putsa_fx(128, 308, (V_WHITE | FX_WEIGHT_BOLD), mainl_char_names[char_id]);
 char_id = ((resident->playchar_paletted[1].v - 1) / 2) * 2;
 graph_putsa_fx(336, 292, (V_WHITE | FX_WEIGHT_BOLD), mainl_char_titles[char_id]);
 graph_putsa_fx(384, 308, (V_WHITE | FX_WEIGHT_BOLD), mainl_char_names[char_id]);
 palette_black_in(1);
 vsync_Count1 = 0;
 graph_accesspage(1);
 graph_clear();
 mainl_shot_load(0);
 mainl_shot_load(1);
 pi_load(0, mainl_intro_frame);
 pi_put_interlace_8(0, 280, 0);
 pi_free(0);
 char_id = (resident->playchar_paletted[1].v - 1) / 2;
 switch(char_id) {
 case 0: case 1: case 6: pi_load(0, mainl_enemy00); break;
 case 2: case 4: pi_load(0, mainl_enemy01); break;
 case 3: case 5: pi_load(0, mainl_enemy02); break;
 case 7: pi_load(0, mainl_enemy03); break;
 case 8: pi_load(0, mainl_enemy04); break;
 }
 pi_put_interlace_8(0, 304, 0);
 char_id = (resident->playchar_paletted[1].v - 1) / 2;
 if(char_id >= 10) {
  bgm_fn[0] = char_id / 10 + bgm_fn[0];
  char_id %= 10;
 }
 bgm_fn[1] = bgm_fn[1] + char_id;
 snd_kaja_func(KAJA_SONG_STOP, 0);
 if(resident->story_stage != 6) {
  snd_load(bgm_fn, SND_LOAD_SONG);
 } else {
  snd_load(dec_bgm_fn, SND_LOAD_SONG);
 }
 snd_load(mainl_sound_effects, SND_LOAD_SE);
 input_sp = INPUT_NONE;
 while(vsync_Count1 <= 32) {}
 while(vsync_Count1 <= 96 && input_sp == INPUT_NONE) {
  input_mode_interface();
 }
 palette_white_out(1);
 graph_accesspage(0);
 graph_clear();
 palette_white_in(1);
 text_fillca(' ', TX_BLACK | TX_REVERSE);
 pi_palette_apply(0);
 pi_free(0);
 respal_set_palettes();
}

// Two complete shot helpers. The original template is seven characters plus five NULs.
extern char SHOT_FN[12];
extern "C" void near pascal mainl_shot_pair(int player, char far *fn)
{
 pi_load(0, fn);
 pi_put_interlace_8(player * 320, 200, 0);
 pi_free(0);
 fn[2] = 'e';
 fn[3] = 'x';
 pi_load(0, fn);
 pi_put_interlace_8(player * 320, 208, 0);
 pi_free(0);
}
extern "C" void near pascal mainl_shot_load(int player)
{
 char fn[sizeof(SHOT_FN)];
 int char_id;
 int i;
 for(i = 0; i < (int)sizeof(SHOT_FN); i++) {
  fn[i] = SHOT_FN[i];
 }
 char_id = resident->playchar_paletted[player].v - 1;
 if(char_id >= 10) {
  fn[0] = char_id / 10 + fn[0];
  char_id %= 10;
 }
 fn[1] = fn[1] + char_id;
 mainl_shot_pair(player, fn);
}

// Genuine MAINL entry. Failed exec calls retain their original fall-through paths.
#include <process.h>
#include "compat/rec98/th03/core/initexit.h"
extern "C" {
#include "compat/rec98/th03/formats/hfliplut.h"
}
#include "src/mainl/cutscene/cutscene.hpp"
#include "src/mainl/hiscore/regist.hpp"
extern const unsigned char mainl_archive_name[];
extern const char mainl_gaiji_font[];
extern const char mainl_win_bgm[];
extern char mainl_root_op_name[];
extern char mainl_main_name[];
extern unsigned char far *mainl_story_script;
extern "C" void near mainl_ending(void);
extern "C" int near mainl_continue_menu(void);
extern "C" void near mainl_reg_music(void);
// Documented slight jump pass, confined to the genuine main function.
#pragma option -O- -y
void far cdecl main(void)
{
 unsigned char outcome;
 unsigned char char_id;
 // A successful resident lookup owns this entire body; failure returns naturally.
 if(cfg_load_resident_ptr()) {
 game_init_main(mainl_archive_name);
 respal_exist();
 snd_midi_active = 0;
 if(resident->bgm_mode != SND_BGM_OFF) {
  snd_determine_mode();
 }
 gaiji_backup();
 gaiji_entry_bfnt(mainl_gaiji_font);
 snd_load(mainl_sound_effects, SND_LOAD_SE);
 snd_se_reset();
 hflip_lut_generate();
 if(resident->show_score_menu) {
  regist_menu();
  text_clear();
  gaiji_restore();
  game_exit();
  execl(mainl_root_op_name, mainl_root_op_name, (char far *)0);
 }
 playchar[0].v = resident->playchar_paletted[0].v - 1;
 playchar[1].v = resident->playchar_paletted[1].v - 1;
 if(resident->story_stage != 0) {
 if(resident->game_mode == GM_STORY) {
  outcome = mainl_story_dispatch();
  asm {
   cmp outcome, 4
   je story_cutscene
  }
  if(outcome == 5) {
   mainl_ending();
  }
 }
 snd_load(mainl_win_bgm, SND_LOAD_SONG);
 win_load();
 mainl_win_animate();
 snd_kaja_func(KAJA_SONG_STOP, 0);
 if(resident->game_mode == GM_STORY) {
  outcome = mainl_story_dispatch();
  if(outcome == 0) {
intro:
   mainl_stage_intro();
   goto launch_main;
  }
  if(outcome == 3 || outcome == 4) {
story_cutscene:
   cdg_free_all();
   pi_free(0);
   char_id = playchar[0].v / 2;
   if(char_id >= 10) {
    mainl_story_script[1] += char_id / 10;
    char_id %= 10;
   }
   mainl_story_script[2] += char_id;
   if(outcome == 4) {
    mainl_story_script[5]++;
   }
   graph_accesspage(0);
   graph_showpage(0);
   graph_clear();
   graph_show();
   cutscene_script_load((const char far *)mainl_story_script);
   cutscene_animate();
   cutscene_script_free();
   mainl_stage_load();
   mainl_stage_intro();
   gaiji_restore();
launch_main:
   game_exit_from_mainl_to_main();
   execl(mainl_main_name, mainl_main_name, (char far *)0);
exec_return:
   return;
  }
  cdg_free_all();
  pi_free(0);
  regist_menu();
  // The near cdecl integer result is in AX.
  mainl_continue_menu();
  _AX |= _AX;
  asm {
   jnz load_stage
  }
  mainl_reg_music();
 } else {
  cdg_free_all();
  pi_free(0);
 }
 text_clear();
 gaiji_restore();
 game_exit();
 execl(mainl_root_op_name, mainl_root_op_name, (char far *)0);
 goto exec_return;
 }
load_stage:
 mainl_stage_load();
 goto intro;
 }
 return;
}

#pragma option -O. -y.

// Genuine contiguous pointer storage in original logical order.
extern const char mainl_script_0[];
extern const char mainl_script_1[];
extern const char mainl_script_2[];
extern const char mainl_script_3[];
extern const char mainl_script_4[];
extern const char mainl_script_5[];
extern const char mainl_script_6[];
extern const char mainl_script_7[];
extern const char mainl_script_8[];
extern unsigned char mainl_story_template[];
extern const unsigned char mainl_title_0[];
extern const unsigned char mainl_name_0[];
extern const unsigned char mainl_title_1[];
extern const unsigned char mainl_name_1[];
extern const unsigned char mainl_title_2[];
extern const unsigned char mainl_name_2[];
extern const unsigned char mainl_title_3[];
extern const unsigned char mainl_name_3[];
extern const unsigned char mainl_title_4[];
extern const unsigned char mainl_name_4[];
extern const unsigned char mainl_title_5[];
extern const unsigned char mainl_name_5[];
extern const unsigned char mainl_title_6[];
extern const unsigned char mainl_name_6[];
extern const unsigned char mainl_title_7[];
extern const unsigned char mainl_name_7[];
extern const unsigned char mainl_title_8[];
extern const unsigned char mainl_name_8[];
const char far *WIN_MESSAGE_FN[9] = {
 mainl_script_0, mainl_script_1, mainl_script_2, mainl_script_3, mainl_script_4, mainl_script_5, mainl_script_6, mainl_script_7, mainl_script_8
};
unsigned char far *mainl_story_script = mainl_story_template;
const unsigned char far *mainl_char_info[18] = {
 mainl_title_0, mainl_name_0,
 mainl_title_1, mainl_name_1,
 mainl_title_2, mainl_name_2,
 mainl_title_3, mainl_name_3,
 mainl_title_4, mainl_name_4,
 mainl_title_5, mainl_name_5,
 mainl_title_6, mainl_name_6,
 mainl_title_7, mainl_name_7,
 mainl_title_8, mainl_name_8
};
