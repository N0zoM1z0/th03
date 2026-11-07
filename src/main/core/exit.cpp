#pragma option -zCSHARED

#include "src/main/core/exit.hpp"

// PC-98 display and access VRAM page registers. Preserve individual OUTs,
// including the deliberate repeated page-0 selection before shutdown.
// Removing the repeated DX/AL writes changes original TC4 CODE (af876b),
// and routing the page through a local const also changed CODE (af876c).
// These are hardware-visible register effects, not a deduplicatable
// ordinary memory store or a generic C++ output-port helper.
enum {
    TH03_VRAM_DISPLAY_PAGE_PORT = 0xA6,
    TH03_VRAM_ACCESS_PAGE_PORT = 0xA4,
    TH03_VRAM_PAGE_FRONT = 1,
    TH03_VRAM_PAGE_BACK = 0,
};

// Original DOS large-memory model requires 16-bit DX and 8-bit AL.
// Use file-scope typedef guards accepted by the actual historical TC4.
typedef char th03_exit_original_port_word[(sizeof(unsigned int) == 2) ? 1 : -1];
typedef char th03_exit_original_page_byte[(sizeof(unsigned char) == 1) ? 1 : -1];

void far __cdecl game_exit(void)
{
    pfend();

    _DX = TH03_VRAM_DISPLAY_PAGE_PORT;
    _AL = TH03_VRAM_PAGE_FRONT;
    asm out dx, al;
    graph_clear();

    _DX = TH03_VRAM_DISPLAY_PAGE_PORT;
    _AL = TH03_VRAM_PAGE_BACK;
    asm out dx, al;
    graph_clear();

    // This extra page-0 display selection is a real separate original
    // OUT, not redundant implementation noise.
    _DX = TH03_VRAM_DISPLAY_PAGE_PORT;
    _AL = TH03_VRAM_PAGE_BACK;
    asm out dx, al;

    _DX = TH03_VRAM_ACCESS_PAGE_PORT;
    asm out dx, al;

    vsync_end();
    mem_unassign();
    text_clear();
    js_end();
    egc_start();
}
