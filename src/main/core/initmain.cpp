#pragma option -zCSHARED -3

#include "src/main/core/initmain.hpp"

#define MEM_ASSIGN_PARAS (288000L >> 4)

int far pascal game_init_main(const unsigned char far *pf_fn)
{
    if(mem_assign_dos(MEM_ASSIGN_PARAS)) {
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
