#pragma option -zCSHARED

#include "src/main/formats/pi_load.hpp"

int far pascal pi_load(int slot, const char far *fn)
{
    graph_pi_free(&pi_headers[slot], pi_buffers[slot]);
    int ret = graph_pi_load_pack(fn, &pi_headers[slot], &pi_buffers[slot]);
    return ret;
}
