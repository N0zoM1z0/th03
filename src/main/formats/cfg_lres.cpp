#include "src/main/formats/cfg_lres.hpp"
#include "compat/rec98/th03/formats/cfg_impl.hpp"

// Real original resident CFG filename symbol. The historical header may
// define CFG_FN as a macro, so the undef must precede this declaration.
// A natural file-scope extern has the same actual OMF symbol and call ABI
// as the original function-scope declaration (native af882a).
#undef CFG_FN
extern const char CFG_FN[];

resident_t __seg* near cfg_load_resident_ptr(void)
{
	// The original helper consumes this true stack-allocated scratch CFG.
	// Zero-initializing it emitted non-original CODE (af882d).
	cfg_t cfg;
	// Return the helper result directly: inserting a named near pointer
	// temporary changed TC4 registers/stack layout (af882c).
	return cfg_load_and_set_resident(cfg, CFG_FN);
}
