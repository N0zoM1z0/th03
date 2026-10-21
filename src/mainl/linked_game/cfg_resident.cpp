// Maintained TH03 MAINL linked-game provider.
// Historical source statements, declarations, inline assembly and compiler pragmas
// are retained. The composer uses the actual cached first-use GAME/BINARY slot.
// Contextual headers retain the original real-mode ABI; no MAIN acceptance is inherited.

#include "compat/rec98/th03/formats/cfg_impl.hpp"

resident_t __seg* near cfg_load_resident_ptr(void)
{
	#undef CFG_FN
	extern const char CFG_FN[];
	cfg_t cfg;
	return cfg_load_and_set_resident(cfg, CFG_FN);
}
