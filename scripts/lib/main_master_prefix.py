"""Split unowned master.lib context at its real circle-helper boundary."""

FIRST = "include libs/master.lib/bfnt_entry_pat.asm"
NEXT = "include libs/master.lib/grcg_circle_x.asm"
EXPORTS = ('BFNT_ENTRY_PAT', 'BFNT_EXTEND_HEADER_SKIP', 'BFNT_HEADER_READ', 'BFNT_EXTEND_HEADER_ANALYSIS', 'BCLOSER', 'BFILL', 'BFNT_PALETTE_SET', 'BGETC', 'PALETTE_BLACK_OUT', 'BOPENR', 'BREAD', 'BSEEK', 'BSEEK_', 'cutline', 'DOS_KEYCLEAR', 'DOS_SETVECT', 'EGC_ON', 'EGC_OFF', 'EGC_END', 'EGC_START', 'FILE_FLUSH', 'FILE_CLOSE', 'FILE_READ', 'FILE_ROPEN', 'DOS_CLOSE', 'FONTFILE_CLOSE', 'DOS_ROPEN', 'FONTFILE_OPEN', 'GRCG_BOXFILL', 'GRCG_CIRCLE')

# ABI declarations follow the pinned reference's DATA/BSS files. These are
# extern views only; this generated context claims no authored-source credit.
HEADER = """.386
.model use16 large _TEXT
; Explicit forwarding of the candidate master.lib CODE prefix.
; This library context is unowned; no authored-source credit is claimed.
include ReC98.inc
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS

; Types follow the existing master.lib DATA/BSS declarations; no storage here.
extrn bbufsiz:word ; pf[data].asm
extrn BFNT_ID:byte ; bfnt_id[data].asm
extrn ClipXL:word ; clip[data].asm
extrn ClipXR:word ; clip[data].asm
extrn ClipXW:word ; clip[data].asm
extrn ClipYH:word ; clip[data].asm
extrn ClipYT:word ; clip[data].asm
extrn ClipYT_seg:word ; clip[data].asm
extrn EDGES:word ; edges[data].asm
extrn file_Buffer:dword ; fil[bss].asm
extrn file_BufferPos:dword ; fil[bss].asm
extrn file_BufferSize:word ; fil[data].asm
extrn file_BufPtr:word ; fil[bss].asm
extrn file_Eof:word ; fil[bss].asm
extrn file_ErrorStat:word ; fil[bss].asm
extrn file_Handle:word ; fil[data].asm
extrn file_InReadBuf:word ; fil[bss].asm
extrn file_sharingmode:word ; dos_ropen[data].asm
extrn gc_circl_cx_:word ; grcg_circle[bss].asm
extrn gc_circl_cy_:word ; grcg_circle[bss].asm
extrn graph_VramZoom:word ; grp[data].asm
extrn mem_AllocID:word ; mem[data].asm
extrn Palettes:byte ; pal[bss].asm
extrn PaletteTone:word ; pal[data].asm
extrn pferrno:word ; pf[data].asm

_TEXT segment word public 'CODE' use16
assume cs:_TEXT, ds:DGROUP
extrn GRCG_CIRCLE_X:far
extrn HMEM_ALLOCBYTE:far
extrn HMEM_FREE:far
extrn PALETTE_SHOW:far
extrn SMEM_RELEASE:far
extrn SMEM_WGET:far
extrn SUPER_ENTRY_PAT:far
extrn VSYNC_WAIT:far

"""


def interval(text):
    start, end = text.index(FIRST), text.index(NEXT)
    lines = text[start:end].strip().splitlines()
    if len(lines) != 24 or any(
        not line.startswith("include libs/master.lib/") or not line.endswith(".asm")
        for line in lines
    ):
        raise ValueError("master.lib source interval differs")
    return start, end


def source(raw):
    text = raw.decode("latin1").replace("\r\n", "\n")
    start, end = interval(text)
    return (HEADER + text[start:end] + "\n_TEXT ends\nend\n").encode("latin1")


def detach(text):
    start, end = interval(text)
    text = text[:start] + text[end:]
    marker = "assume cs:_TEXT"
    if text.count(marker) != 1:
        raise ValueError("master.lib CODE frame differs")
    declarations = "\n".join(
        "extrn " + name + (":near" if name == "cutline" else ":far") for name in EXPORTS
    )
    text = text.replace(marker, marker + "\n" + declarations, 1)
    marker = "include libs/master.lib/grcg_circle[bss].asm"
    if text.count(marker) != 1:
        raise ValueError("master.lib circle state differs")
    return text.replace(marker, "public gc_circl_cx_,gc_circl_cy_\n" + marker, 1)
