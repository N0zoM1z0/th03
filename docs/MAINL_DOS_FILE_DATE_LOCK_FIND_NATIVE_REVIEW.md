# Five original Japanese DOS file/date/lock/drive/find CRT members

Five previously dirty, uncommitted **native 8086 source members** were
completed and independently revalidated from the
actual pinned Japanese Borland CL.LIB, rather than accepting aliases,
snippets, historical source guesses or post-assembly byte patches. Each
source file under `src/mainl/crt/<member>.asm` reproduces a complete
original DOS far-calling-convention routine pair:

| Original CL.LIB slot | Full CODE | Public entry points and native DOS behavior |
| --- | ---: | --- |
| `dossdate` (34) | 92 bytes | `__dos_setdate` +0, `__dos_settime` +44: INT 21h AH=2Bh/2Dh and original errno-19 path |
| `doslock` (31) | 78 bytes | `__dos_lock` +0, `__dos_unlock` +39: INT 21h AX=5C00h/5C01h and near `__DOSERROR` |
| `chdrive` (9) | 84 bytes | `__chdrive` +0, `__getdrive` +55: original far `__dos_setdrive` and `__dos_getdrive` calls |
| `dosfind` (27) | 104 bytes | `__dos_findfirst` +0, `__dos_findnext` +55: save/restore DOS DTA and exact findfirst/next error paths |
| `findfirs` (221) | 104 bytes | `_findfirst` +0, `_findnext` +55: C wrappers with original DTA and near `__IOERROR` |

This is **462 original CODE bytes**, ten complete public far entry points,
and **11 OMF import relocation fields**, across five original `_TEXT` segments
and genuine empty DATA/BSS segments. The full machine CODE, exported ABI,
import ordering, original DGROUP segment order, individual DOS carry paths,
and all original fixup sites/targets/addends have been independently checked.

## Recovering the actual original OMF order without hiding a frame difference

The original `dossdate`, `doslock` and `chdrive` OMF fixup lists were emitted
in descending instruction address order. The source emits actual 8086
function or instruction blocks with `ORG` at the original real offsets:
`dossdate`: CODE+44 before CODE+0, `doslock`: CODE+39 before CODE+0;
`chdrive`: CODE+55 then +26 then +0. These are not synthetic opcode arrays
or target-byte fillers. `dosfind` and `findfirs` already have their original
ascending FIXUPP order. **All five source objects now reproduce the exact
original fixup site order.**

Four objects (`dossdate`, `chdrive`, `dosfind`, `findfirs`) also reproduce
**all literal original FIXUPP frame fields**. Two near imported
`__DOSERROR` fixups in `doslock`, at CODE+29 and +68, remain intentionally
reported as different: original CL.LIB uses TARGET frame5 while TASM
emits CODE frame0. Both refer to the identical near target and link to the
identical original machine code. We tested plain and explicitly typed near-call declarations, segment
qualification, and unknown-CS assumptions; none produced the original TARGET-frame record without changing
or invalidating the code. The driver and reviewer therefore compare every
other field exactly and assert that these **two named, documented frame
values are the sole exception**. No blanket frame stripping, false literal
FIXUPP equality claim, or manual OMF/EXE rewrite is used. Full original
Borland member-record serialization also remains different from TASM.

`scripts/build_th03_mainl_after352_work.py dos-drive-find-lock-date`
inherits the full two-round **398-source** C++ `find1` carrier; it compiles
and links the original 893-slot CRT twice through TASM/TLIB/TLINK. Both
rounds reproduce the complete decoded Japanese MAINL **67,372-byte EXE
and MAP**, including **all 677 ordered original DOS MZ relocations**.
The verified carrier now contains **403 full source-backed CRT members**,
**490 untouched original contextual programs** and **129,234 original-equal
CODE bytes**, a gain of **462 bytes** from this five-member source batch.
Complete raw OBJ/LIB/EXE/MAP vectors, logs and source/parent/driver SHA
bindings are retained under `.analysis/work/after352-*`, reviewed by
`scripts/review_th03_mainl_after352_work.py` and
`tests/test_mainl_after352_work.py`.

No full cold replay, binary post-processing, new formally accepted Factory
extent, or packed-file ownership is claimed.
