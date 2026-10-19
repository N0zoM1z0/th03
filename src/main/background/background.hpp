#ifndef TH03_BACKGROUND_PROPOSAL_HPP
#define TH03_BACKGROUND_PROPOSAL_HPP
#include <stddef.h>
#include "compat/rec98/platform.h"
#include "src/main/math/vector_far.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"

// Existing root DGROUP storage only. No allocation/ownership transfer.
// This is an observed background view, not exclusive semantic ownership:
// another target routine clears DS:3E2E..3E3C, overlapping record70.y
// through record71.x low byte. Unrendered entries are not assumed unused.
struct background_particle_t {
    int x;
    int y;
    int vx;
    int vy;
    unsigned char speed;
    unsigned char unclassified_09;
    unsigned int sprite;
    int random_aux;
    unsigned char unclassified_14;
    unsigned char unclassified_15;
};
enum { BACKGROUND_CAPACITY = 80, BACKGROUND_PIXEL_COUNT = 24 };
extern background_particle_t background_particles[BACKGROUND_CAPACITY];
extern unsigned char background_angle;
extern unsigned long round_frame;
extern unsigned int round_or_result_frame;
typedef void (far *background_callback_t)(void);
extern background_callback_t background_render;

// REAL register ABI: DS:DI particle; pixel helper additionally requires ES=VRAM.
// No arguments live on the stack. Target machine contracts to verify:
// pixel preserves DX/SI/DI/BP and ES; AX/BX/CX are scratch.
// update preserves BX/CX/DX/SI/DI/BP and ES; AX ends as corrected y.
// Ordinary C++ lowering does NOT guarantee these extra preservation/results;
// both ordinary-local probes violated update DX/AX behavior. Its arithmetic
// now uses a complete symbolic register-interface block; native review remains
// required for compiler-owned entry/exit and call-site preservation behavior.
// The ordinary no-argument C declarations describe only linkage/call distance;
// callers must establish the documented register preconditions explicitly.
void near background_pixel_di(void);
void near background_update_di(void);
void far background_velocity_reset(void);
void far background_chain1_init(void);
void far background_chain1_accelerate(void);
void far background_chain1_periodic(void);
void far background_chain2_init(void);
void far background_chain2_accelerate(void);
void far background_chain2_periodic(void);

#define BG_FIELD(f, off, bytes) typedef char bg_field_##f[( \
    offsetof(background_particle_t, f) == off && \
    sizeof(((background_particle_t near *)0)->f) == bytes) ? 1 : -1]
BG_FIELD(x, 0, 2); BG_FIELD(y, 2, 2);
BG_FIELD(vx, 4, 2); BG_FIELD(vy, 6, 2);
BG_FIELD(speed, 8, 1); BG_FIELD(unclassified_09, 9, 1);
BG_FIELD(sprite, 10, 2); BG_FIELD(random_aux, 12, 2);
BG_FIELD(unclassified_14, 14, 1); BG_FIELD(unclassified_15, 15, 1);
#undef BG_FIELD
typedef char bg_size[(sizeof(background_particle_t) == 16) ? 1 : -1];
typedef char bg_widths[(sizeof(int) == 2 && sizeof(unsigned long) == 4 &&
    sizeof(background_callback_t) == 4 && sizeof(background_particle_t near *) == 2) ? 1 : -1];

// TC4 pseudo-register interface, used only where the original contract is DI.
// No ordinary C register allocation is assumed to choose DI for a variable.
#define BG_DI (reinterpret_cast<background_particle_t near *>(_DI))
#define BG_START(i) { _DI = (unsigned int)(background_particle_t near *)background_particles; i = 0; }
#define BG_NEXT(i) { _DI += sizeof(background_particle_t); i++; }
#define BG_GRAPHICS_BEGIN(rows, color) { \
    sprite16_put_size.w = 16; \
    sprite16_put_size.h = rows; \
    sprite16_clip.left = 0; \
    sprite16_clip.right = 639; \
    grcg_setcolor(GC_RMW, color); \
    _ES = 0xA800; \
}
#endif
