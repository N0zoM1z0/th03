#pragma option -zCSHARED

#include "compat/rec98/planar.h"
#include "src/main/hardware/vram_planes.hpp"

void vram_planes_set(void)
{
	VRAM_PLANE_B = (dots8_t __seg *)SEG_PLANE_B;
	VRAM_PLANE_R = (dots8_t __seg *)SEG_PLANE_R;
	VRAM_PLANE_G = (dots8_t __seg *)SEG_PLANE_G;
	VRAM_PLANE_E = (dots8_t __seg *)SEG_PLANE_E;
}
