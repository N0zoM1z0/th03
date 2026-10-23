"""Separate the unowned master.lib body from MAIN's retained assembly context."""

from lib.main_master_prefix import EXPORTS as PREFIX_EXPORTS, NEXT as FIRST

LAST = "include libs/master.lib/pfint21.asm"
NEXT = "include libs/master.lib/js_start.asm"

# These declarations view the existing root DATA/BSS, without allocating storage.
# Widths and aliases follow the pinned reference files named below.
STORAGE = (
    ("AtanTable8", "byte"),  # atan8[data].asm
    ("ClipXL", "word"),  # clip[data].asm
    ("ClipXW", "word"),  # clip[data].asm
    ("ClipXR", "word"),  # clip[data].asm
    ("ClipYT", "word"),  # clip[data].asm
    ("ClipYH", "word"),  # clip[data].asm
    ("ClipYB", "word"),  # clip[data].asm
    ("ClipYT_seg", "word"),  # clip[data].asm
    ("ClipYB_adr", "word"),  # clip[data].asm
    ("EDGES", "word"),  # edges[data].asm
    ("backup_mseg", "word"),  # gaiji_backup[data].asm
    ("bfnt_header2", "word"),  # gaiji_entry_bfnt[data].asm
    ("graph_VramSeg", "word"),  # grp[data].asm
    ("graph_VramWords", "word"),  # grp[data].asm
    ("graph_VramLines", "word"),  # grp[data].asm
    ("graph_VramWidth", "word"),  # grp[data].asm
    ("graph_VramZoom", "word"),  # grp[data].asm
    ("PaletteTone", "word"),  # pal[data].asm
    ("PaletteNote", "word"),  # pal[data].asm
    ("ResPalSeg", "word"),  # pal[data].asm
    ("random_seed", "dword"),  # rand[data].asm
    ("TextVramSeg", "word"),  # tx[data].asm
    ("TextShown", "word"),  # tx[data].asm
    ("vsync_Proc", "dword"),  # vs[data].asm
    ("vsync_Delay", "word"),  # vs[data].asm
    ("vsync_OldMask", "byte"),  # vs[data].asm
    ("BYTE_MASK", "byte"),  # wordmask[data].asm
    ("mem_TopSeg", "word"),  # mem[data].asm
    ("mem_MyOwn", "word"),  # mem[data].asm
    ("mem_AllocID", "word"),  # mem[data].asm
    ("mem_Reserve", "word"),  # mem[data].asm
    ("header", "bfnt_header"),  # super_entry_bfnt[data].asm
    ("super_buffer", "word"),  # superpa[data].asm
    ("super_patnum", "word"),  # superpa[data].asm
    ("super_charfree", "word"),  # superpa[data].asm
    ("ResPalID", "byte"),  # respal_exist[data].asm
    ("trapez_a", "word"),  # clip[bss].asm
    ("trapez_b", "word"),  # clip[bss].asm
    ("ylen", "word"),  # grcg_triangle[bss].asm
    ("Palettes", "byte"),  # pal[bss].asm
    ("vsync_Count1", "word"),  # vs[bss].asm
    ("vsync_Count2", "word"),  # vs[bss].asm
    ("vsync_OldVect", "dword"),  # vs[bss].asm
    ("vsync_delay_count", "word"),  # vsync[bss].asm
    ("mem_OutSeg", "word"),  # mem[bss].asm
    ("mem_TopHeap", "word"),  # mem[bss].asm
    ("mem_FirstHole", "word"),  # mem[bss].asm
    ("mem_EndMark", "word"),  # mem[bss].asm
    ("super_patdata", "word"),  # superpa[bss].asm
    ("super_patsize", "word"),  # superpa[bss].asm
    ("parfilename", "byte"),  # pfint21[bss].asm
    ("pfint21_pf", "word"),  # pfint21[bss].asm
    ("pfint21_handle", "word"),  # pfint21[bss].asm
    ("pfint21_entries", "word"),  # pfint21[bss].asm
)

# func defaults to FAR in the actual large model; explicit PROC/aliases stay NEAR.
EXPORTS = (
    ("GRCG_CIRCLE_X", "far"),
    ("GRC_SETCLIP", "far"),
    ("GRCG_FILL", "far"),
    ("GRCG_HLINE", "far"),
    ("GRCG_LINE", "far"),
    ("GRCG_SETCOLOR", "far"),
    ("GRCG_OFF", "far"),
    ("GRCG_SETTILE_1LINE", "far"),
    ("GRCG_TRIANGLE", "far"),
    ("GRCG_VLINE", "far"),
    ("GRCG_TRAPEZOID", "far"),
    ("GAIJI_BACKUP", "far"),
    ("GAIJI_RESTORE", "far"),
    ("GAIJI_ENTRY_BFNT", "far"),
    ("GAIJI_PUTCA", "far"),
    ("GAIJI_PUTSA", "far"),
    ("GAIJI_READ", "far"),
    ("GAIJI_READ_ALL", "far"),
    ("GAIJI_WRITE", "far"),
    ("GAIJI_WRITE_ALL", "far"),
    ("GRAPH_200LINE", "far"),
    ("GRAPH_400LINE", "far"),
    ("GRAPH_CLEAR", "far"),
    ("GRAPH_COPY_PAGE", "far"),
    ("GRAPH_EXTMODE", "far"),
    ("GRAPH_HIDE", "far"),
    ("GRAPH_PI_FREE", "far"),
    ("GRAPH_PI_LOAD_PACK", "far"),
    ("IATAN2", "far"),
    ("JS_END", "far"),
    ("PALETTE_SHOW", "far"),
    ("PFCLOSE", "far"),
    ("PFGETC", "far"),
    ("PFREAD", "far"),
    ("PFREWIND", "far"),
    ("PFSEEK", "far"),
    ("IRAND", "far"),
    ("SMEM_RELEASE", "far"),
    ("SMEM_WGET", "far"),
    ("TEXT_BOXFILLA", "far"),
    ("TEXT_CLEAR", "far"),
    ("TEXT_FILLCA", "far"),
    ("TEXT_PUTS", "far"),
    ("TEXT_PUTSA", "far"),
    ("VSYNC_START", "far"),
    ("VSYNC_END", "far"),
    ("VSYNC_WAIT", "far"),
    ("HMEM_LALLOCATE", "far"),
    ("MEM_ASSIGN_DOS", "far"),
    ("MEM_ASSIGN", "far"),
    ("MEM_ASSIGN_ALL", "far"),
    ("HMEM_ALLOCBYTE", "far"),
    ("HMEM_ALLOC", "far"),
    ("HMEM_FREE", "far"),
    ("MEM_UNASSIGN", "far"),
    ("SUPER_FREE", "far"),
    ("SUPER_ENTRY_PAT", "far"),
    ("SUPER_ENTRY_AT", "far"),
    ("SUPER_ENTRY_BFNT", "far"),
    ("SUPER_CANCEL_PAT", "far"),
    ("SUPER_PUT", "far"),
    ("RESPAL_EXIST", "far"),
    ("RESPAL_CREATE", "far"),
    ("RESPAL_GET_PALETTES", "far"),
    ("PFSTART", "far"),
    ("PFEND", "far"),
    ("make_linework", "near"),
    ("PFGETC1", "near"),
    ("PFGETX0", "near"),
    ("PFGETX1", "near"),
    ("VSYNC_LEAVE", "far"),
    ("SOUND_I", "near"),
    ("SOUND_O", "near"),
)

HEADER = """.386
.model use16 large _TEXT
; Forward existing library CODE; this context has no authored-source credit.
include ReC98.inc
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
IDLEN EQU 10 ; respal_exist[data].asm: sizeof ResPalID
"""


def interval(text):
    start = text.index(FIRST)
    end = text.index(LAST, start) + len(LAST)
    lines = text[start:end].splitlines()
    if len(lines) != 58 or any(
        not line.startswith("include libs/master.lib/") or not line.endswith(".asm")
        for line in lines
    ):
        raise ValueError("master.lib body interval differs")
    return start, end


def source(raw):
    text = raw.decode("latin1").replace("\r\n", "\n")
    start, end = interval(text)
    declarations = "\n".join("extrn " + n + ":" + k for n, k in STORAGE)
    imports = "\n".join(
        "extrn " + n + (":near" if n == "cutline" else ":far")
        for n in PREFIX_EXPORTS
    )
    return (
        HEADER + declarations + "\n_TEXT segment word public 'CODE' use16\n"
        + "assume cs:_TEXT, ds:DGROUP, es:nothing\n" + imports
        + "\nextrn draw_trapezoid:near\nextrn JS_START:far\nextrn PFOPEN:far\n"
        + "public SOUND_I,SOUND_O\n"  # Real near helpers called by js_start/sense.
        + text[start:end] + "\n_TEXT ends\nend\n"
    ).encode("latin1")


def detach(text):
    from lib.main_work_stage import once

    start, end = interval(text)
    # The odd-length body ends before JS_START. With separate word-aligned
    # objects TLINK supplies the gap; do not retain the scaffold's db 0.
    tail = once(text[end:], "\n\t\tdb 0\n" + NEXT, "\n" + NEXT)
    text = text[:start] + tail
    declarations = "\n".join("extrn " + n + ":" + k for n, k in EXPORTS)
    text = once(text, "assume cs:_TEXT", "assume cs:_TEXT\n" + declarations)
    # PUBLIC exposes genuine existing definitions; it emits no storage.
    return once(text, "\n\t.data\n", "\npublic " + ",".join(n for n, _ in STORAGE) + "\n\t.data\n")
