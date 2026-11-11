#pragma codeseg HITCIRC_TEXT main_01
#include "src/main/round/demo_transition.hpp"
#define v playfield_transition_vertices
// Keep signed loop-bound/frame constants separate from the high-bit
// unsigned GRCG masks. TC4 promotes signed i to unsigned if the 320
// bound is put in the same enum as 0xAAAA/0xFFFF (negative af1367m).
// The two triangles-per-side passes use a 320-pixel playfield offset.
enum demo_transition_offset_t {
 DEMO_TRANSITION_SECOND_PLAYFIELD_OFFSET = 320,
 DEMO_TRANSITION_HALF_PHASE_FRAMES = 16,
};
// Alternate the two hardware checkerboard masks, then restore all bits.
enum demo_transition_mask_t {
 DEMO_TRANSITION_MASK_FIRST = 0x5555,
 DEMO_TRANSITION_MASK_SECOND = 0xAAAA,
 DEMO_TRANSITION_MASK_RESET = 0xFFFF,
};
extern "C" void near stage_background_update_none(void) {}
extern "C" void near stage_demo_finish(void)
{
 if(playfield_transition_frame == 0) {
  v[0].x=303; v[0].y=382; v[1].x=16; v[1].y=382;
  v[2].x=16; v[2].y=16; v[3].x=303; v[3].y=16;
 }
 grc_setclip(8,0,623,191);
 v[0].x-=18; v[1].y-=23; v[2].x+=18; v[3].y+=23;
 grcg_setcolor(0xC0,2);
 transition_hmask=DEMO_TRANSITION_MASK_FIRST;
 int i = 0;
 while(i <= DEMO_TRANSITION_SECOND_PLAYFIELD_OFFSET) {
  grcg_triangle(i+303,8,i+303,191,v[0].x+i,v[0].y/2);
  grcg_triangle(i+16,8,i+16,191,v[2].x+i,v[2].y/2);
  i += DEMO_TRANSITION_SECOND_PLAYFIELD_OFFSET;
 }
 transition_hmask=DEMO_TRANSITION_MASK_SECOND;
 i = 0;
 while(i <= DEMO_TRANSITION_SECOND_PLAYFIELD_OFFSET) {
  grcg_triangle(i+16,191,i+303,191,v[1].x+i,v[1].y/2);
  grcg_triangle(i+16,8,i+303,8,v[3].x+i,v[3].y/2);
  i += DEMO_TRANSITION_SECOND_PLAYFIELD_OFFSET;
 }
 playfield_transition_frame++;
 if(playfield_transition_frame >= DEMO_TRANSITION_HALF_PHASE_FRAMES) {
  asm { mov bx,0x3932; }
  bomb_bg_fill();
  asm { mov bx,0x395A; }
  bomb_bg_fill();
  playfield_transition_midpoint=1;
  playfield_transition_frame=0;
  stage_background_update=stage_demo_uncover;
 }
 transition_hmask=DEMO_TRANSITION_MASK_RESET;
 grcg_off();
 grc_setclip(0,0,639,199);
}
extern "C" void near stage_demo_uncover(void)
{
 if(playfield_transition_frame==0) {
  v[0].x=303; v[0].y=16; v[1].x=303; v[1].y=382;
  v[2].x=16; v[2].y=382; v[3].x=16; v[3].y=16;
 }
 grc_setclip(16,0,623,191);
 v[0].y+=23; v[1].x-=18; v[2].y-=23; v[3].x+=18;
 grcg_setcolor(0xC0,2);
 int i = 0;
 while(i <= DEMO_TRANSITION_SECOND_PLAYFIELD_OFFSET) {
  grcg_triangle(i+16,191,i+303,191,v[0].x+i,v[0].y/2);
  grcg_triangle(i+16,8,i+16,191,v[1].x+i,v[1].y/2);
  grcg_triangle(i+16,8,i+303,8,v[2].x+i,v[2].y/2);
  grcg_triangle(i+303,8,i+303,191,v[3].x+i,v[3].y/2);
  i += DEMO_TRANSITION_SECOND_PLAYFIELD_OFFSET;
 }
 playfield_transition_frame++;
 if(playfield_transition_frame >= DEMO_TRANSITION_HALF_PHASE_FRAMES) {
  playfield_transition_frame=0;
  stage_background_update=stage_background_update_none;
 }
 grcg_off();
 grc_setclip(0,0,639,199);
}
