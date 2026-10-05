#pragma option -zCSHARED

#include "src/main/core/exit.hpp"

void far __cdecl game_exit(void)
{
    pfend();

    _DX = 0xA6;
    _AL = 1;
    asm out dx, al;
    graph_clear();

    _DX = 0xA6;
    _AL = 0;
    asm out dx, al;
    graph_clear();

    _DX = 0xA6;
    _AL = 0;
    asm out dx, al;

    _DX = 0xA4;
    asm out dx, al;

    vsync_end();
    mem_unassign();
    text_clear();
    js_end();
    egc_start();
}
