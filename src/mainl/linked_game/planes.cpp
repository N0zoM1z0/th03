// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#pragma option -zCSHARED

#include "planar.h"
#include "compat/rec98/th01/hardware/vplanset.h"

void vram_planes_set(void)
{
	VRAM_PLANE_B = reinterpret_cast<dots8_t __seg *>(SEG_PLANE_B);
	VRAM_PLANE_R = reinterpret_cast<dots8_t __seg *>(SEG_PLANE_R);
	VRAM_PLANE_G = reinterpret_cast<dots8_t __seg *>(SEG_PLANE_G);
	VRAM_PLANE_E = reinterpret_cast<dots8_t __seg *>(SEG_PLANE_E);
}
