// Genuine MAINL ending transition. Compiler owns its frame and local storage.
#pragma option -zPgroup_01
#pragma option -zCSTAFFP_TEXT
#include <process.h>
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th03/resident.hpp"
extern "C" void far pascal cdg_free(int slot);
#include "compat/rec98/th03/formats/pi.hpp"
#include "compat/rec98/th02/hardware/frmdelay.h"
#include "compat/rec98/th02/core/initexit.h"
#include "src/mainl/cutscene/cutscene.hpp"
#include "src/mainl/hiscore/regist.hpp"

extern char far *mainl_ending_script;
extern const char mainl_bonus_script[];
extern char mainl_op_name[];
extern "C" void near mainl_staff_roll(void);

extern "C" void near mainl_ending(void)
{
 signed char playchar;
 cdg_free(0);
 cdg_free(1);
 cdg_free(2);
 pi_free(0);
 playchar = (resident->playchar_paletted[0].v - 1) / 2;
 if(playchar >= 10) {
  mainl_ending_script[1] += playchar / 10;
  playchar %= 10;
 }
 mainl_ending_script[2] += playchar;
 PaletteTone = 0;
 palette_show();
 frame_delay(96);
 graph_accesspage(0);
 graph_showpage(0);
 graph_clear();
 graph_show();
 cutscene_script_load(mainl_ending_script);
 cutscene_animate();
 cutscene_script_free();
 mainl_staff_roll();
 resident->story_stage = STAGE_ALL;
 regist_menu();
 if(resident->rem_credits == 3 && resident->playchar_paletted[0].v < (1 + (PLAYCHAR_CHIYURI * 2))) {
  graph_accesspage(1);
  graph_clear();
  graph_accesspage(0);
  graph_clear();
  graph_showpage(0);
  cutscene_script_load(mainl_bonus_script);
  cutscene_animate();
  cutscene_script_free();
 }
 text_clear();
 gaiji_restore();
 game_exit();
 execl(mainl_op_name, mainl_op_name, (char far *)0);
}

// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#include "compat/rec98/th03/sprites/flake.h"
#include "compat/rec98/th03/score.hpp"
#include "compat/rec98/th01/math/subpixel.hpp"
#include "compat/rec98/platform/x86real/flags.hpp"
#include "x86real.h"
#include <stdlib.h>

// State
// -----

struct flake_t {
	bool alive;
	int8_t padding_1; // ZUN bloat: Could have squeezed [cel] in there.
	Subpixel left;
	Subpixel top;
	SPPoint velocity;
	uint16_t cel;
	int8_t padding_2[4]; // ZUN bloat
};

static const unsigned int FLAKE_COUNT = 80;

extern flake_t flakes[FLAKE_COUNT];

extern page_t page_back;

// Oh look, it's the TH02 approach!
extern screen_y_t stf_center_y_on_page[PAGE_COUNT];

extern score9_lebcd_t score;
// -----

void pascal near flake_put(screen_x_t left, screen_y_t top, int cel)
{
	#define src      	reinterpret_cast<flake_dots_t near *>(_SI)
	#define first_bit	static_cast<int16_t>(_CX)
	#define rows_left	static_cast<pixel_t>(_BX)

	dots16_t __es *dst = reinterpret_cast<dots16_t __es *>(
		vram_offset_shift(left, top)
	);

	// ZUN bloat: src = &sFLAKE[cel].row[0];`
	#define src_bloat reinterpret_cast<uint16_t>(src)
	src_bloat = cel;
	src_bloat <<= 4;
	src_bloat += FP_OFF(sFLAKE[0].row);
	#undef src_bloat

	_ES = SEG_PLANE_B;

	// ZUN bloat: `first_bit = (left & BYTE_MASK);`. Using a 16-bit-immediate
	// for some reason.
	first_bit = left;
	asm { and cx, BYTE_MASK; }

	rows_left = FLAKE_H;
	do {
		*dst |= __rotr__(*src, first_bit);
		dst += (ROW_SIZE / sizeof(dots16_t));
		src++;
		rows_left--;
	} while(!FLAGS_ZERO);

	#undef rows_left
	#undef first_bit
	#undef src
}

// MAINL CDG effects. Native 16-bit TC4 arithmetic and inline assembler.
// The generated carrier supplies storage and library imports; no assets here.
struct mainl_cdg_slot_t {
 unsigned int bitplane_size;
 int pixel_w;
 int pixel_h;
 int offset_at_bottom_left;
 unsigned int vram_dword_w;
 unsigned char image_count;
 signed char plane_layout;
 unsigned int seg_alpha;
 unsigned int seg_colors;
};
typedef char mainl_cdg_slot_must_be_16[(sizeof(mainl_cdg_slot_t)==16)?1:-1];
extern mainl_cdg_slot_t mainl_staff_cdg_slots[32];
extern unsigned char mainl_dissolve_alpha_enabled;
extern unsigned char mainl_dissolve_alpha_requested;
extern unsigned int mainl_dissolve_pattern[8][4];
extern "C" {
 void far pascal cdg_put_noalpha_8(int left, int top, int slot);
 void far pascal cdg_put_8(int left, int top, int slot);
}

// Explicit near Pascal ABI, unlike the underspecified reference declaration.
// Three rows are cleared. Width truncates to whole words; DF is inherited.
extern "C" void near pascal cdg_unput_for_upwards_motion_e_8(
 int center_x, int center_y, int slot)
{
 int w, h;
 w = mainl_staff_cdg_slots[slot].pixel_w;
 h = mainl_staff_cdg_slots[slot].pixel_h;
 center_x -= w / 2;
 center_y += (h / 2) - 2;
 _DI = (center_x >> 3) + (center_y << 6) + (center_y << 4);
 _ES = 0xE000;
 _DX = w;
 _DX >>= 4;
 asm {
  mov si, 80
  sub si, dx
  sub si, dx
  xor ax, ax
  mov cx, dx
  rep stosw
  add di, si
  mov cx, dx
  rep stosw
  add di, si
  mov cx, dx
  rep stosw
 }
}

// Clear 32000 bytes of the blue plane, with the incoming direction flag.
extern "C" void near mainl_clear_blue(void)
{
 asm {
  mov ax, 0A800h
  mov es, ax
  xor ax, ax
  mov di, ax
  mov cx, 3E80h
  rep stosw
 }
}

// Strength is modulo eight. No zero-size guard or clipping is invented.

// Semantic alternative, compiler-owned ABI. Uncompiled diagnostic candidate.
// Complete maintained snow spawn behavior; no manual frame/save/return sequence.
struct mainl_spawn_flake_t {
 unsigned char alive;
 unsigned char alignment;
 int left;
 int top;
 int velocity_x;
 int velocity_y;
 int cel;
 unsigned char reserved[4];
};
typedef char mainl_spawn_flake_size[(sizeof(mainl_spawn_flake_t)==16)?1:-1];
extern mainl_spawn_flake_t mainl_spawn_flakes[80];
extern int mainl_snow_frame;
extern unsigned char mainl_snow_slot_limit;
extern "C" {
 int far pascal IRand(void);
 void far pascal vector2(int &ret_x, int &ret_y, unsigned char angle, int length);
}
void near flakes_reset(void)
{
 register mainl_spawn_flake_t near *flake;
 int i;
 flake = mainl_spawn_flakes;
 for(i = 0; i < 80; i++, flake++) {
  flake->alive = 0;
 }
}

extern "C" void near mainl_snow_spawn(void)
{
 unsigned char angle;
 unsigned char length;
 register mainl_spawn_flake_t near *flake;
 register int i;
 flake = mainl_spawn_flakes;
 for(i = 0; i < mainl_snow_slot_limit; i++, flake++) {
  if(flake->alive == 0 && (i << 3) <= mainl_snow_frame) {
   flake->alive = 1;
   if(i & 3) {
    flake->left = IRand() % ((640 - 8) * 16);
    flake->top = 0;
   } else {
    flake->left = ((640 - 8) * 16);
    flake->top = IRand() % ((400 - 8) * 16);
   }
   angle = (IRand() % 32) + 80;
   length = (IRand() % (4 * 16)) + (3 * 16);
   flake->cel = IRand() & 3;
   vector2(flake->velocity_x, flake->velocity_y, angle, length);
  }
 }
}

// Genuine snow update/render/gate/frame, following the maintained snow provider.
// Compiler owns frames and register saves. No byte or instruction padding.
#include "compat/rec98/th02/snd/snd.h"
extern unsigned char mainl_snow_auto_adjust;

extern "C" void near mainl_snow_update(void)
{
 register mainl_spawn_flake_t near *flake;
 int i;
 flake = mainl_spawn_flakes;
 for(i = 0; i < mainl_snow_slot_limit; i++, flake++) {
  if(flake->alive) {
   flake->alive = 1;
   flake->left += flake->velocity_x;
   flake->top += flake->velocity_y;
   if(flake->left <= 0) {
    flake->left += ((640 - FLAKE_W) * 16);
   }
   if(flake->top >= ((400 - FLAKE_H) * 16)) {
    flake->top -= ((400 - FLAKE_H) * 16);
   }
  }
 }
}

extern "C" void near mainl_snow_render(void)
{
 register mainl_spawn_flake_t near *flake;
 register int i;
 flake = mainl_spawn_flakes;
 for(i = 0; i < mainl_snow_slot_limit; i++, flake++) {
  if(flake->alive) {
   flake_put(flake->left >> 4, flake->top >> 4, flake->cel);
  }
 }
}

extern "C" int near pascal mainl_snow_gate(unsigned int measure, int frames)
{
 if(!snd_active) {
  return mainl_snow_frame > frames;
 } else {
  _AH = KAJA_GET_SONG_MEASURE;
  geninterrupt(PMD);
  return (_AX >= measure && mainl_snow_frame > 192);
 }
}

extern "C" void near mainl_snow_tick(void)
{
 mainl_snow_spawn();
 mainl_snow_update();
 mainl_snow_render();
 if(mainl_snow_auto_adjust && vsync_Count1 > 1) {
  mainl_dissolve_alpha_requested = 0;
  mainl_snow_slot_limit = 50;
  mainl_snow_auto_adjust = 0;
 }
 while(vsync_Count1 == 0) {}
 vsync_Count1 = 0;
 graph_showpage(page_back);
 page_back = 1 - page_back;
 graph_accesspage(page_back);
}

extern "C" void near pascal cdg_put_dissolve_e_8(
 int center_x, int center_y, int slot, int strength)
{
 unsigned int p_offset;
 int w, h;
 w = mainl_staff_cdg_slots[slot].pixel_w;
 h = mainl_staff_cdg_slots[slot].pixel_h;
 center_x -= w / 2;
 center_y -= h / 2;
 if(!mainl_dissolve_alpha_enabled || !mainl_dissolve_alpha_requested) {
  cdg_put_noalpha_8(center_x, center_y, slot);
 } else {
  cdg_put_8(center_x, center_y, slot);
 }
 strength &= 7;
 if(strength != 0) {
  w /= 16;
  h += center_y;
  p_offset = (center_x >> 3) + (center_y << 6) + (center_y << 4);
  _ES = 0xE000;
  _BX = strength;
  _BX <<= 3;
  _BX += (unsigned int)(unsigned int near *)mainl_dissolve_pattern;
  _DX = center_y;
  asm {
 next_row:
   mov si, dx
   and si, 3
   shl si, 1
   mov ax, [bx+si]
   not ax
   mov di, p_offset
   mov cx, w
 next_word:
   and es:[di], ax
   add di, 2
   loop next_word
   add p_offset, 80
   inc dx
   cmp dx, h
   jb next_row
  }
 }
}

// Genuine first four STAFF transitions, preserving original state and ABI.
extern int mainl_staff_speed;
extern int mainl_staff_duration;
extern int mainl_staff_center_limit;
extern int mainl_staff_height_offset;
extern unsigned char mainl_staff_secondary_slot;

extern "C" void near pascal mainl_staff_enter(int slot)
{
 register int strength;
 register int selected_slot = slot;
 mainl_clear_blue();
 if(mainl_snow_frame <= mainl_staff_duration) {
  cdg_unput_for_upwards_motion_e_8(320, stf_center_y_on_page[page_back], selected_slot);
  if(stf_center_y_on_page[page_back] > mainl_staff_center_limit) {
   stf_center_y_on_page[page_back] -= mainl_staff_speed;
   if(stf_center_y_on_page[page_back] < mainl_staff_center_limit) {
    stf_center_y_on_page[page_back] = mainl_staff_center_limit;
   }
  }
  strength = 7 - mainl_snow_frame / (mainl_staff_duration / 8);
  if(strength < 0) { strength = 0; }
  if(mainl_dissolve_alpha_requested && mainl_staff_secondary_slot) {
   cdg_put_dissolve_e_8(504, 200, mainl_staff_secondary_slot, strength);
   mainl_dissolve_alpha_enabled = 1;
  }
  cdg_put_dissolve_e_8(320, stf_center_y_on_page[page_back], selected_slot, strength);
  mainl_dissolve_alpha_enabled = 0;
 }
}

extern "C" void near pascal mainl_staff_leave(int slot)
{
 register int strength;
 register int selected_slot = slot;
 mainl_clear_blue();
 if(mainl_snow_frame <= 161) {
  if(mainl_snow_frame < 160) {
   cdg_unput_for_upwards_motion_e_8(320, stf_center_y_on_page[page_back], selected_slot);
   stf_center_y_on_page[page_back]--;
   strength = mainl_snow_frame / 20;
   if(strength > 7) { strength = 7; }
   if(mainl_dissolve_alpha_requested && mainl_staff_secondary_slot) {
    cdg_put_dissolve_e_8(504, 200, mainl_staff_secondary_slot, strength);
    mainl_dissolve_alpha_enabled = 1;
   }
   cdg_put_dissolve_e_8(320, stf_center_y_on_page[page_back], selected_slot, strength);
   mainl_dissolve_alpha_enabled = 0;
  } else {
   grcg_setcolor(GC_RMW, 0);
   grcg_byteboxfill_x(1, 8, 78, 391);
   grcg_off();
  }
 }
}

extern "C" void near pascal mainl_staff_gallery(int x_center, int y_center, int slot)
{
 register int strength;
 if(mainl_snow_frame <= 160) {
  strength = 7 - mainl_snow_frame / 20;
  if(strength < 0) { strength = 0; }
  cdg_put_dissolve_e_8(x_center, y_center, slot, strength);
 }
}

extern "C" void near pascal mainl_staff_single(int slot, unsigned int enter_measure, unsigned int leave_measure)
{
 register int selected_slot = slot;
 if(mainl_staff_speed == 2) {
  stf_center_y_on_page[page_back] = 264;
  stf_center_y_on_page[page_back ^ 1] = 263;
 } else {
  stf_center_y_on_page[page_back] = 280 - mainl_staff_height_offset;
  stf_center_y_on_page[page_back ^ 1] = 280 - mainl_staff_height_offset;
 }
 mainl_snow_frame = 0;
 do {
  mainl_staff_enter(selected_slot);
  mainl_snow_tick();
  mainl_snow_frame++;
 } while(!mainl_snow_gate(enter_measure, 256));
 mainl_snow_frame = 0;
 do {
  mainl_staff_leave(selected_slot);
  mainl_snow_tick();
  mainl_snow_frame++;
 } while(!mainl_snow_gate(leave_measure, 256));
 grcg_setcolor(GC_RMW, 0);
 grcg_byteboxfill_x(1, 8, 78, 391);
 grcg_off();
 mainl_snow_tick();
 grcg_setcolor(GC_RMW, 0);
 grcg_byteboxfill_x(1, 8, 78, 391);
 grcg_off();
 mainl_snow_tick();
}

// Paired entrance/exit and entrance/hold, with original alpha/page sequencing.
extern int mainl_staff_secondary_y;

extern "C" void near pascal mainl_staff_pair(int slot, unsigned int enter_measure, unsigned int leave_measure)
{
 register int selected_slot = slot;
 register int strength;
 if(mainl_staff_speed == 2) {
  stf_center_y_on_page[page_back] = 264;
  stf_center_y_on_page[page_back ^ 1] = 263;
 } else {
  stf_center_y_on_page[1] = stf_center_y_on_page[0] = 280 - mainl_staff_height_offset;
 }
 mainl_snow_frame = 0;
 do {
  mainl_staff_enter(selected_slot);
  mainl_dissolve_alpha_enabled = 1;
  cdg_put_dissolve_e_8(320, mainl_staff_secondary_y, selected_slot - 1, 0);
  mainl_dissolve_alpha_enabled = 0;
  mainl_snow_tick();
  mainl_snow_frame++;
 } while(!mainl_snow_gate(enter_measure, 256));
 mainl_snow_frame = 0;
 do {
  if(mainl_snow_frame <= 161) {
   cdg_unput_for_upwards_motion_e_8(320, mainl_staff_secondary_y, selected_slot - 1);
  }
  mainl_staff_leave(selected_slot);
  if(mainl_snow_frame <= 161) {
   strength = (mainl_snow_frame - 1) / 20;
   if(strength > 7) { strength = 7; }
   if(page_back == 0) { mainl_staff_secondary_y--; }
   mainl_dissolve_alpha_enabled = 1;
   if(mainl_snow_frame < 160) {
    cdg_put_dissolve_e_8(320, mainl_staff_secondary_y, selected_slot - 1, strength);
   } else {
    grcg_setcolor(GC_RMW, 0);
    grcg_byteboxfill_x(1, 8, 78, 391);
    grcg_off();
   }
   mainl_dissolve_alpha_enabled = 0;
  }
  mainl_snow_tick();
  mainl_snow_frame++;
 } while(!mainl_snow_gate(leave_measure, 256));
 grcg_setcolor(GC_RMW, 0);
 grcg_byteboxfill_x(1, 8, 78, 391);
 grcg_off();
 mainl_snow_tick();
 grcg_setcolor(GC_RMW, 0);
 grcg_byteboxfill_x(1, 8, 78, 391);
 grcg_off();
 mainl_snow_tick();
}

extern "C" void near pascal mainl_staff_hold(int slot, unsigned int enter_measure, unsigned int hold_measure)
{
 if(mainl_staff_speed == 2) {
  stf_center_y_on_page[page_back] = 264;
  stf_center_y_on_page[page_back ^ 1] = 263;
 } else {
  stf_center_y_on_page[1] = stf_center_y_on_page[0] = 280 - mainl_staff_height_offset;
 }
 mainl_snow_frame = 0;
 do {
  mainl_staff_enter(slot);
  mainl_snow_tick();
  mainl_snow_frame++;
 } while(!mainl_snow_gate(enter_measure, 256));
 mainl_snow_frame = 0;
 do {
  mainl_clear_blue();
  mainl_snow_tick();
  mainl_snow_frame++;
 } while(!mainl_snow_gate(hold_measure, 256));
 mainl_staff_secondary_y = stf_center_y_on_page[page_back];
}

// Genuine verdict rendering, reusing existing pointer tables and score storage.
#include "compat/rec98/th02/v_colors.hpp"
#include "compat/rec98/th01/hardware/grppsafx.h"
extern const shiftjis_t *mainl_verdict_playchars[];
extern const shiftjis_t *mainl_verdict_ranks[];
extern const shiftjis_t *mainl_verdict_numbers[];
extern const shiftjis_t mainl_verdict_unit[];
extern unsigned char mainl_verdict_playchar;
extern unsigned char mainl_verdict_rank;
extern unsigned char mainl_verdict_skill;

extern "C" void near mainl_staff_verdict(void)
{
 int digits;
 int seen;
 register int x;
 register int digit;
 graph_putsa_fx(352, 174, V_WHITE | FX_WEIGHT_BOLD, mainl_verdict_playchars[mainl_verdict_playchar]);
 graph_putsa_fx(360, 199, V_WHITE | FX_WEIGHT_BOLD, mainl_verdict_ranks[mainl_verdict_rank]);
 x = 408;
 seen = 0;
 for(digits = SCORE_DIGITS; digits > 0; digits--) {
  digit = score.digits[digits];
  if(!seen && digit) {
   x -= digits * 8;
   seen = 1;
  }
  if(seen) {
   graph_putsa_fx(x, 224, V_WHITE | FX_WEIGHT_BOLD, mainl_verdict_numbers[digit]);
   x += 16;
  }
 }
 digit = score.continues_used;
 graph_putsa_fx(x, 224, V_WHITE | FX_WEIGHT_BOLD, mainl_verdict_numbers[digit]);
 graph_putsa_fx(408, 248, V_WHITE | FX_WEIGHT_BOLD, mainl_verdict_numbers[digit]);
 digit = mainl_verdict_skill / 100;
 x = 408;
 seen = 0;
 if(digit) {
  x -= 16;
  seen = 1;
  graph_putsa_fx(x, 291, V_WHITE | FX_WEIGHT_BOLD, mainl_verdict_numbers[digit]);
  x += 16;
 }
 digit = (mainl_verdict_skill % 100) / 10;
 if(digit && !seen) {
  seen = 1;
  x -= 8;
 }
 if(seen) {
  graph_putsa_fx(x, 291, V_WHITE | FX_WEIGHT_BOLD, mainl_verdict_numbers[digit]);
  x += 16;
 }
 digit = mainl_verdict_skill % 10;
 graph_putsa_fx(x, 291, V_WHITE | FX_WEIGHT_BOLD, mainl_verdict_numbers[digit]);
 graph_putsa_fx(x + 16, 291, V_WHITE | FX_WEIGHT_BOLD, mainl_verdict_unit);
}

// Genuine staff-roll orchestration. Asset names remain existing symbolic storage.
#include "compat/rec98/th03/hardware/input.h"
extern "C" {
 void far pascal cdg_load_single(int slot, const char *fn, int n);
 void far pascal cdg_load_single_noalpha(int slot, const char *fn, int n);
}
extern const char mainl_staff_music[];
extern const char mainl_staff_palette[];
extern const char mainl_stf1[], mainl_stf11[], mainl_stf3[], mainl_stf4[];
extern const char mainl_stf5[], mainl_stf6[], mainl_stf7[], mainl_stf8[];
extern const char mainl_stf9[], mainl_stf10[], mainl_stf2[], mainl_stf12[];

extern "C" void near mainl_staff_roll(void)
{
 register int i;
 register int tone;
 snd_kaja_func(KAJA_SONG_FADE, 16);
 palette_black_out(4);
 snd_delay_until_volume(255);
 snd_kaja_func(KAJA_SONG_STOP, 0);
 mainl_snow_slot_limit = 80;
 for(i = 1; i < 9; i++) {
  score.digits[i] = resident->score_last[0].digits[i - 1];
 }
 score.continues_used = 3 - resident->rem_credits;
 mainl_verdict_playchar = (resident->playchar_paletted[0].v - 1) / 2;
 mainl_verdict_rank = resident->rank;
 mainl_verdict_skill = resident->skill;
 switch(score.digits[7]) {
 case 3:
  mainl_verdict_skill += score.digits[6] / 2 + 2;
  // Original case3 deliberately falls through to case4.
 case 4:
  mainl_verdict_skill += score.digits[6] / 2 + 7;
 }
 if(score.digits[7] >= 5) { mainl_verdict_skill += 15; }
 if(score.digits[8]) { mainl_verdict_skill = 100; }
 if(mainl_verdict_skill > 100) { mainl_verdict_skill = 100; }
 snd_load(mainl_staff_music, SND_LOAD_SONG);
 PaletteTone = 0;
 palette_show();
 palette_entry_rgb(mainl_staff_palette);
 palette_show();
 grcg_setcolor(GC_RMW, 8);
 graph_accesspage(1);
 grcg_byteboxfill_x(0, 0, 79, 399);
 graph_accesspage(0);
 grcg_byteboxfill_x(0, 0, 79, 399);
 grcg_setcolor(GC_RMW, 0);
 graph_accesspage(1);
 grcg_byteboxfill_x(1, 8, 78, 391);
 graph_accesspage(0);
 grcg_byteboxfill_x(1, 8, 78, 391);
 grcg_off();
 graph_showpage(1);
 cdg_load_single_noalpha(0, mainl_stf1, 0);
 cdg_load_single_noalpha(1, mainl_stf11, 0);
 cdg_load_single(2, mainl_stf3, 0);
 cdg_load_single(3, mainl_stf4, 0);
 cdg_load_single_noalpha(4, mainl_stf5, 0);
 cdg_load_single_noalpha(5, mainl_stf6, 0);
 cdg_load_single_noalpha(6, mainl_stf7, 0);
 cdg_load_single_noalpha(7, mainl_stf8, 0);
 cdg_load_single_noalpha(8, mainl_stf9, 0);
 cdg_load_single_noalpha(9, mainl_stf10, 0);
 cdg_load_single_noalpha(10, mainl_stf2, 0);
 cdg_load_single_noalpha(11, mainl_stf12, 0);
 flakes_reset();
 mainl_snow_frame = 0;
 random_seed = resident->rand;
 page_back = 0;
 PaletteTone = 100;
 palette_show();
 snd_kaja_func(KAJA_SONG_PLAY, 0);
 mainl_snow_auto_adjust = 1;
 mainl_dissolve_alpha_requested = 1;
 frame_delay(1);
 vsync_Count1 = 0;
 do {
  mainl_clear_blue();
  mainl_snow_tick();
  mainl_snow_frame++;
 } while(!mainl_snow_gate(4, 256));
 mainl_dissolve_alpha_enabled = 0;
 mainl_staff_height_offset = 0;
 mainl_staff_center_limit = 200;
 mainl_staff_speed = 2;
 mainl_staff_duration = 65;
 mainl_staff_secondary_slot = 0;
 mainl_staff_single(0, 8, 10);
 mainl_staff_speed = 1;
 mainl_staff_duration = 161;
 mainl_snow_auto_adjust = 0;
 mainl_staff_single(1, 16, 20);
 mainl_staff_height_offset = 32;
 mainl_staff_center_limit = 168;
 mainl_staff_hold(2, 22, 24);
 mainl_staff_secondary_slot = 7;
 mainl_staff_center_limit = 216;
 mainl_staff_height_offset = -16;
 mainl_staff_pair(3, 32, 34);
 mainl_staff_secondary_slot = 0;
 mainl_staff_center_limit = 200;
 mainl_staff_height_offset = 0;
 mainl_staff_single(4, 36, 38);
 mainl_staff_single(11, 42, 44);
 mainl_staff_single(5, 48, 50);
 mainl_staff_single(6, 54, 56);
 mainl_staff_single(10, 60, 62);
 mainl_snow_frame = 0;
 do {
  mainl_clear_blue();
  mainl_staff_gallery(320, 128, 8);
  mainl_staff_gallery(192, 240, 9);
  mainl_snow_tick();
  mainl_snow_frame++;
 } while(!mainl_snow_gate(66, 256));
 graph_accesspage(1 - page_back);
 mainl_staff_verdict();
 graph_accesspage(page_back);
 mainl_staff_verdict();
 mainl_snow_frame = 0;
 tone = 0;
 for(;;) {
  input_mode_interface();
  mainl_clear_blue();
  mainl_snow_tick();
  mainl_snow_frame++;
  if(tone) {
   PaletteTone = tone;
   palette_show();
   if(mainl_snow_frame & 1) {
    tone--;
    if(!tone) { break; }
   }
  } else if(input_sp != INPUT_NONE && mainl_snow_frame > 256) {
   snd_kaja_func(KAJA_SONG_FADE, 8);
   tone = 100;
   mainl_snow_frame = 0;
  }
 }
 for(i = 0; i < 32; i++) { cdg_free(i); }
}

// Real STAFF-owned initialized data; values come from maintained sprite/mask source.
extern char mainl_ending_template[];
extern const shiftjis_t mainl_vname_0[];
extern const shiftjis_t mainl_vname_1[];
extern const shiftjis_t mainl_vname_2[];
extern const shiftjis_t mainl_vname_3[];
extern const shiftjis_t mainl_vname_4[];
extern const shiftjis_t mainl_vname_5[];
extern const shiftjis_t mainl_vname_6[];
extern const shiftjis_t mainl_vname_7[];
extern const shiftjis_t mainl_vname_8[];
extern const shiftjis_t mainl_vrank_0[];
extern const shiftjis_t mainl_vrank_1[];
extern const shiftjis_t mainl_vrank_2[];
extern const shiftjis_t mainl_vrank_3[];
extern const shiftjis_t mainl_vdigit_0[];
extern const shiftjis_t mainl_vdigit_1[];
extern const shiftjis_t mainl_vdigit_2[];
extern const shiftjis_t mainl_vdigit_3[];
extern const shiftjis_t mainl_vdigit_4[];
extern const shiftjis_t mainl_vdigit_5[];
extern const shiftjis_t mainl_vdigit_6[];
extern const shiftjis_t mainl_vdigit_7[];
extern const shiftjis_t mainl_vdigit_8[];
extern const shiftjis_t mainl_vdigit_9[];
char far *mainl_ending_script = mainl_ending_template;
const DotRect<flake_dots_t, FLAKE_H> near sFLAKE[FLAKE_CELS] = {
 {{0x003C, 0x007E, 0x00FF, 0x00FF, 0x00FF, 0x00FF, 0x007E, 0x003C}},
 {{0x0000, 0x0018, 0x003C, 0x007E, 0x007E, 0x003C, 0x0018, 0x0000}},
 {{0x0000, 0x0000, 0x0018, 0x003C, 0x003C, 0x0018, 0x0000, 0x0000}},
 {{0x0000, 0x0000, 0x0000, 0x0018, 0x0018, 0x0000, 0x0000, 0x0000}},
};
unsigned int mainl_dissolve_pattern[8][4] = {
 {0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF},
 {0x2222, 0x5555, 0x8888, 0x5555},
 {0xAAAA, 0x5555, 0xAAAA, 0x5555},
 {0xEEEE, 0x5555, 0xBBBB, 0x5555},
 {0xEEEE, 0x7777, 0xBBBB, 0xDDDD},
 {0xFFFF, 0x5555, 0xFFFF, 0x5555},
 {0xFFFF, 0xEEEE, 0xFFFF, 0xBBBB},
 {0xFFFF, 0x7777, 0xFFFF, 0xFFFF},
};
const shiftjis_t *mainl_verdict_playchars[9] = {
 mainl_vname_0, mainl_vname_1, mainl_vname_2, mainl_vname_3, mainl_vname_4, mainl_vname_5, mainl_vname_6, mainl_vname_7, mainl_vname_8
};
const shiftjis_t *mainl_verdict_ranks[4] = {
 mainl_vrank_0, mainl_vrank_1, mainl_vrank_2, mainl_vrank_3
};
const shiftjis_t *mainl_verdict_numbers[10] = {
 mainl_vdigit_0, mainl_vdigit_1, mainl_vdigit_2, mainl_vdigit_3, mainl_vdigit_4, mainl_vdigit_5, mainl_vdigit_6, mainl_vdigit_7, mainl_vdigit_8, mainl_vdigit_9
};
