#pragma option -zCSHARED -3

#include "src/main/core/initmain.hpp"

// DOS memory allocation is in 16-byte paragraphs. This constant is
// deliberately a compile-time value; no new DATA or BSS owner is added.
enum { MAIN_DOS_MEMORY_PARAGRAPHS = (288000L >> 4) };

int far pascal game_init_main(const unsigned char far *pf_fn)
{
    if(mem_assign_dos(MAIN_DOS_MEMORY_PARAGRAPHS)) {
        return 1;
    }
    vram_planes_set();
    vsync_start();
    egc_start();
    graph_400line();
    js_start();
    pfstart(pf_fn);
    return 0;
}
