#ifndef TH03_MAIN_ROUND_DEMO_TRANSITION_HPP
#define TH03_MAIN_ROUND_DEMO_TRANSITION_HPP

struct TransitionVertex { int x, y; };
typedef void (near *TransitionCallback)(void);
typedef char TransitionInt16[(sizeof(int) == 2) ? 1 : -1];
typedef char TransitionPoint4[(sizeof(TransitionVertex) == 4) ? 1 : -1];
typedef char TransitionNear2[(sizeof(TransitionCallback) == 2) ? 1 : -1];
extern "C" {
extern TransitionVertex playfield_transition_vertices[4];
extern unsigned char playfield_transition_frame, playfield_transition_midpoint;
extern unsigned int transition_hmask;
extern TransitionCallback stage_background_update;
int far pascal grc_setclip(int xl, int yt, int xr, int yb);
void far pascal grcg_setcolor(int mode, int color);
void far pascal grcg_off(void);
void far pascal grcg_triangle(int x1,int y1,int x2,int y2,int x3,int y3);
// The existing far renderer takes its pattern in BX, without stack arguments.
void far bomb_bg_fill(void);
void near stage_background_update_none(void);
void near stage_demo_finish(void);
void near stage_demo_uncover(void);
}
#pragma samecodeseg bomb_bg_fill

#endif
