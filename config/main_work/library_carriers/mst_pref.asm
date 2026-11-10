.386
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

include libs/master.lib/bfnt_entry_pat.asm
include libs/master.lib/bfnt_extend_header_skip.asm
include libs/master.lib/bfnt_header_read.asm
include libs/master.lib/bfnt_header_analysis.asm
include libs/master.lib/bcloser.asm
include libs/master.lib/bfill.asm
include libs/master.lib/bfnt_palette_set.asm
include libs/master.lib/bgetc.asm
include libs/master.lib/palette_black_out.asm
include libs/master.lib/bopenr.asm
include libs/master.lib/bread.asm
include libs/master.lib/bseek.asm
include libs/master.lib/bseek_.asm
include libs/master.lib/cutline.asm
include libs/master.lib/dos_keyclear.asm
include libs/master.lib/dos_setvect.asm
include libs/master.lib/egc.asm
include libs/master.lib/file_close.asm
include libs/master.lib/file_read.asm
include libs/master.lib/file_ropen.asm
include libs/master.lib/dos_close.asm
include libs/master.lib/dos_ropen.asm
include libs/master.lib/grcg_boxfill.asm
include libs/master.lib/grcg_circle.asm

_TEXT ends
end
