#pragma option -zCSHARED -3

#include "src/main/core/initmain.hpp"

// DOS allocates memory in 16-byte paragraphs. Compute the original
// 288,000-byte requirement as a compile-time paragraph count, without
// allocating an additional data object.
enum {
    MAIN_DOS_PARAGRAPH_BYTES = 16,
    MAIN_DOS_MEMORY_PARAGRAPHS = (288000L / MAIN_DOS_PARAGRAPH_BYTES),
};

int far pascal game_init_main(const unsigned char far *pf_fn)
{
    if(mem_assign_dos(MAIN_DOS_MEMORY_PARAGRAPHS) != 0) {
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
