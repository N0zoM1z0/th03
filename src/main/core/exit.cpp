#pragma option -zCSHARED

#include "src/main/core/exit.hpp"

// PC-98 display and access VRAM page registers. Preserve individual OUTs,
// including the deliberate repeated page-0 selection before shutdown.
enum {
    TH03_VRAM_DISPLAY_PAGE_PORT = 0xA6,
    TH03_VRAM_ACCESS_PAGE_PORT = 0xA4,
};

void far __cdecl game_exit(void)
{
    pfend();

    _DX = TH03_VRAM_DISPLAY_PAGE_PORT;
    _AL = 1;
    asm out dx, al;
    graph_clear();

    _DX = TH03_VRAM_DISPLAY_PAGE_PORT;
    _AL = 0;
    asm out dx, al;
    graph_clear();

    _DX = TH03_VRAM_DISPLAY_PAGE_PORT;
    _AL = 0;
    asm out dx, al;

    _DX = TH03_VRAM_ACCESS_PAGE_PORT;
    asm out dx, al;

    vsync_end();
    mem_unassign();
    text_clear();
    js_end();
    egc_start();
}
