#pragma option -zCSHARED

#include "src/main/formats/pi_load.hpp"

int far pascal pi_load(int slot, const char far *fn)
{
    graph_pi_free(&pi_headers[slot], pi_buffers[slot]);
    // Keep the named 16-bit result: direct return changes original TC4 CODE.
    int load_result = graph_pi_load_pack(fn, &pi_headers[slot], &pi_buffers[slot]);
    return load_result;
}
