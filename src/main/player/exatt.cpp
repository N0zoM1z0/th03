#include "src/main/player/exatt.hpp"

void pascal exatt_add(Subpixel center_x_, Subpixel center_y_, pid_t pid)
{
	// Both Subpixel-to-16-bit local copies are native-visible: calling
	// the character function pointers directly with the parameter
	// objects emitted different CODE (negative control af699e).

	// The Subpixel wrapper stores one exact 16-bit subpixel word. Explicit
	// field loads preserve TC4's original two near-local copies and
	// both far-Pascal character callback argument widths.
	subpixel_t center_x = center_x_.v;
	subpixel_t center_y = center_y_.v;

	static_assert(PLAYER_COUNT == 2);
	// The original zero-player branch compiles naturally as !pid;
	// the distinct function pointer and 16-bit Pascal ABI remain.
	if(!pid) {
		exatt_funcs[0].add(center_x, center_y, 0);
	} else {
		exatt_funcs[1].add(center_x, center_y, 1);
	}
}
