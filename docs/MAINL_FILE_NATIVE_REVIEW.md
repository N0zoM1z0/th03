# MAINL file APIs and archive interrupt hook

The current root producer supplies the complete master.lib file API (786 bytes),
DOS helpers (80 bytes), PF INT21 hook (605 bytes), and two initialized file WORDs
(4 bytes). They add 1,475 library bytes and 16 procedures. The maintained state
includes preserve the original declarations and aliases. Twenty file BSS bytes
and 134 hook BSS bytes add no file-byte credit. Sharingmode remains outside this
new DATA owner.

## Actual producer and native evidence

`scripts/build_th03_mainl_file_work.py` substitutes only the three state includes
in the actual GAME=3 MAINL root. It assembles that root and links it in its
original position, reusing 35 unchanged project objects and the existing CRT
library. Two serialized TASM/TLINK rounds produced identical complete raw
OBJ/EXE/MAP vectors. Both complete EXEs equal the pinned Japanese decoded target;
both MAPs equal the retained MAP. Source/cold inputs and all 938 outputs remain
unchanged after restoring the root. No object or executable is patched.

The selected object's complete native payload and literal FIXUPP record order
equal the retained root. Complete public records and multiplicity also agree.
Native dependencies prove consumption of the maintained state includes and all
twelve API/hook source providers. CODE base 0000:0272, DATA 0E3F:0112 and BSS
0E3F:13F6 follow actual segment and group membership. All 140 native WORD fields
are resolved independently. The sole ordered MZ entry is 0000:295D, the hook's
DGROUP segment load. Near offsets, dispatch pointers and BSS references do not
become MZ segment relocations.

## Boundaries and storage

The file API at 0000:0786 contains eleven complete far Pascal bodies (783 bytes)
and three ordinary EVEN bytes. DOS_AXDX and DOS_FILESIZE at 0000:06AE contain
78 body bytes and two EVEN bytes. Public names, both MAP tables, complete
instruction decoding and RETF argument cleanup establish each boundary.

The hook at 0000:2850 contains PFSTART, PFEND and one interrupt handler. Internal
dispatch labels are entries within that ISR, not additional procedures. Its
549 instruction bytes and one EVEN byte are CODE. Five CS state bytes and
50 bytes of embedded dispatch/IOCTL storage are file-backed DATA. Twelve
dispatch records, their resolved destinations and the semantic IOCTL bit mask
are checked independently of the target.

The final dispatch key is deliberately `default dw ?, _Thru`. Its WORD at
0000:29AE has no LEDATA initializer. Both real TLINK rounds emit zero bytes in
this file-backed slot. The verifier obtains exactly these two bytes from the
independently linked output; every other byte requires native initializer
coverage. It never substitutes invented zeros for missing object bytes. The
source retains DW ?, and the actual CS BYTE write from AH establishes the
sentinel before dispatch. The DATA total includes these two linker-emitted
storage bytes; it does not assert that the source initializes them.

The separate DATA owner at 0E3F:0554 is `file_BufferSize dw 0` followed by
`file_Handle dw -1`, with both underscore/plain aliases. The BSS declarations
retain their original WORD/DWORD widths and ordering, the unchecked 128-byte
filename buffer, and the GAME>=3 entries WORD.

## Preserved behavior and acceptance limits

FILE_WRITE retains its distinct success values: buffered success is AX=1;
direct nonempty success is AX=FFFF and direct zero-length success is AX=0.
Buffered FILE_READ and direct DOS reads preserve their original error/EOF
handling. PFSTART retains unchecked reads, allocation and filename copying;
the zero-entry LOOP wraparound is unchanged. PFEND retains archive-dependent
freeing. PUSHA, interrupt-frame offsets, flags and IRET remain native behavior.

`scripts/lib/decoded_mainl_file_native.py` checks complete bytes, literal ordered
relocations, ownership, ABI, source transport and repeated native output. Small
negative controls test the unusual storage slot and relocation distinction.
This review makes no physical DOS, interrupt-vector or whole-product source
claim. Previous ancestor runtime observations remain historical support.

Current private inputs are `.analysis/work/mainl-file-build.json`,
`mainl-file-native.json`, both `file-roundN.obj/.exe/.map` vectors, and
`file-root.asm/.lnk`. Reuse the unchanged full cold pair; replay the selected
root producer only when these maintained sources or native inputs change.
