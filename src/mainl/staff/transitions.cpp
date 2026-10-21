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
