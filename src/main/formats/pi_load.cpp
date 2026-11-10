#pragma option -zCSHARED

#include "src/main/formats/pi_load.hpp"

int far pascal pi_load(int slot, const char far *fn)
{
    // The original far-Pascal loader preserves its 16-bit local result.
    // The header and pointer-slot addresses are calculated at each call:
    // caching the header in a pointer local changes the TC4 stack frame.
    int load_result;
    graph_pi_free(pi_headers + slot, pi_buffers[slot]);
    load_result = graph_pi_load_pack(fn, pi_headers + slot, pi_buffers + slot);
    return load_result;
}
