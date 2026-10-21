// MAINL CDG effects. Native 16-bit TC4 arithmetic and inline assembler.
// The generated carrier supplies storage and library imports; no assets here.
#pragma option -zCMAINL_03_TEXT
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
extern mainl_cdg_slot_t cdg_slots[32];
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
 w = cdg_slots[slot].pixel_w;
 h = cdg_slots[slot].pixel_h;
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
extern "C" void near pascal cdg_put_dissolve_e_8(
 int center_x, int center_y, int slot, int strength)
{
 unsigned int p_offset;
 int w, h;
 w = cdg_slots[slot].pixel_w;
 h = cdg_slots[slot].pixel_h;
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
