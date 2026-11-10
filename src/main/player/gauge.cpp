#include "src/main/player/gauge.hpp"
#include "compat/rec98/th03/main/player/stuff.hpp"

// Original 16-bit unsigned gauge saturates at 0xFF0 (4080).
// The Hyper and full-gauge early returns share one native exit. Their
// natural short-circuit OR is TC4-original-exact (af851a), while
// combining the subsequent addition and saturation test is not.
typedef char gauge_native_word_width[(sizeof(gauge_t) == 2) ? 1 : -1];
typedef char gauge_native_byte_width[(sizeof(gauge_perbyte_t) == 1) ? 1 : -1];
typedef char gauge_native_max_value[(GAUGE_MAX == 0xFF0) ? 1 : -1];
void pascal near gauge_avail_add(pid_t pid, uint8_t charge)
{
	// The state stays in DGROUP: explicitly retaining its near pointer
	// preserves the original index and memory accesses under TC4.
	player_stuff_t near *p = &players[pid];
	// Refuse a charge while Hyper or an already-full gauge is active.
	if(p->hyper_active || (p->gauge_avail >= GAUGE_MAX)) {
		return;
	}
	// TC4's original compound memory addition is bytecode-sensitive:
	// explicit p->gauge_avail = p->gauge_avail + charge failed in
	// af851b. The post-add > GAUGE_MAX check (not >= MAX+1) is also
	// codegen-visible, even though mathematically equivalent (af851c).
	p->gauge_avail += charge;
	if(p->gauge_avail > GAUGE_MAX) {
		p->gauge_avail = GAUGE_MAX;
	}
}
