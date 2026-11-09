#pragma option -zCSHARED

#include "src/main/core/exit.hpp"
#include <dos.h>

// Preserve all four physical PC-98 VRAM page writes, including the
// repeated display-page 0 selection. TC4's <dos.h> outportb() intrinsic
// produces the original DX/AL/OUT sequence at each site, unlike a local
// page variable or an attempt to remove a supposedly redundant write.
enum {
    TH03_VRAM_DISPLAY_PAGE_PORT = 0xA6,
    TH03_VRAM_ACCESS_PAGE_PORT = 0xA4,
    TH03_VRAM_PAGE_FRONT = 1,
    TH03_VRAM_PAGE_BACK = 0,
};

// The Borland intrinsic uses a 16-bit port number and an 8-bit value;
// these actual TC4-compatible source guards allocate no DATA.
typedef char th03_exit_original_port_word[(sizeof(unsigned int) == 2) ? 1 : -1];
typedef char th03_exit_original_page_byte[(sizeof(unsigned char) == 1) ? 1 : -1];

void far __cdecl game_exit(void)
{
    pfend();

    outportb(TH03_VRAM_DISPLAY_PAGE_PORT, TH03_VRAM_PAGE_FRONT);
    graph_clear();

    outportb(TH03_VRAM_DISPLAY_PAGE_PORT, TH03_VRAM_PAGE_BACK);
    graph_clear();

    // This additional page-0 selection is a distinct original OUT,
    // even though the previous selection also chose page 0.
    outportb(TH03_VRAM_DISPLAY_PAGE_PORT, TH03_VRAM_PAGE_BACK);

    outportb(TH03_VRAM_ACCESS_PAGE_PORT, TH03_VRAM_PAGE_BACK);

    vsync_end();
    mem_unassign();
    text_clear();
    js_end();
    egc_start();
}
