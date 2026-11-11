#include "src/main/formats/cfg_lres.hpp"
#include "compat/rec98/th03/formats/cfg_impl.hpp"

// Real original resident CFG filename symbol. The historical header may
// define CFG_FN as a macro, so the undef must precede this declaration.
// File-scope declaration retains original OMF EXTDEF order (af882a).
// Explicit `near` preserves the original two-byte DOS filename pointer
// rather than implying a far address inside the resident CFG callback.
#undef CFG_FN
extern const char near CFG_FN[];

resident_t __seg* near cfg_load_resident_ptr(void)
{
	// The original helper consumes this true stack-allocated scratch CFG.
	// Zero-initializing it emitted non-original CODE (af882d).
	cfg_t resident_cfg;
	// The address of the first filename byte is the same original near
	// pointer as array decay; the caller-owned scratch stays uninitialized.
	// Return the original resident segment pointer directly: naming a
	// result local changes TC4's register and stack layout.
	return cfg_load_and_set_resident(resident_cfg, &CFG_FN[0]);
}
