#include "src/main/player/exatt.hpp"

// Preserve the original byte PID and signed 16-bit subpixel ABI without
// adding DATA or relying on a modern C++ file-scope static_assert.
typedef char exatt_subpixel_native_word[(sizeof(subpixel_t) == 2) ? 1 : -1];
typedef char exatt_pid_native_byte[(sizeof(pid_t) == 1) ? 1 : -1];

void pascal exatt_add(Subpixel center_x_, Subpixel center_y_, pid_t pid)
{
	// Both 16-bit local copies are real original compiler-visible state:
	// passing wrapper fields directly in both callbacks expands CODE
	// from 41 to 50 bytes (new independent original TC4 trial af858c).

	// The Subpixel wrapper stores one exact 16-bit subpixel word. Explicit
	// field loads preserve TC4's original two near-local copies and
	// both far-Pascal character callback argument widths.
	const subpixel_t center_x = center_x_.v;
	const subpixel_t center_y = center_y_.v;

	static_assert(PLAYER_COUNT == 2);
	// Preserve the original player-zero branch and callback order.
	// The first call can return directly; the player-one call then
	// occupies the remaining tail with the original far-Pascal ABI.
	// Reversing this decision changed CODE at unchanged size (af858d).
	if(!pid) {
		exatt_funcs[0].add(center_x, center_y, 0);
		return;
	}
	exatt_funcs[1].add(center_x, center_y, 1);
}
