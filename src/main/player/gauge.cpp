#include "src/main/player/gauge.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"

// Original unsigned 16-bit gauge saturates at 0xFF0 (4080).
// Separate early returns are native-exact; combining the addition and
// overflow condition changed TC4 machine code (af699a).
void pascal near gauge_avail_add(pid_t pid, uint8_t charge)
{
	player_stuff_t near& p = players[pid];
	if(p.hyper_active) {
		return;
	}
	// Saturated gauge cannot be increased; this check remains before
	// the original additive update, not a post-add defensive rewrite.
	if(p.gauge_avail >= GAUGE_MAX) {
		return;
	}
	// TC4's original memory compound addition is codegen-sensitive:
	// p.gauge_avail = p.gauge_avail + charge differed in af753b.
	p.gauge_avail += charge;
	if(p.gauge_avail > GAUGE_MAX) {
		p.gauge_avail = GAUGE_MAX;
	}
}
