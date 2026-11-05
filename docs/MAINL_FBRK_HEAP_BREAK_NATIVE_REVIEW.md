# Full original fbrk heap-break runtime, and a false vendor-OBJ equivalence corrected

The existing `src/mainl/crt/fbrk.asm` has been reattested and integrated into
the actual **source-bound Japanese CL.LIB carrier**: full original **352-byte
`_TEXT` CODE**, **2-byte initialized `_DATA`** (granule counter), zero BSS,
two near public entries `__brk` at CODE+142 and `__sbrk` at +209, and all 33
original relocation fields including literal FIXUPP ordering. The source
includes the full private `grow_break` near procedure, 1-KiB granule rounding,
DOS `_setblock`, original heap-top and break-level updates, near huge pointer
comparison/addition/shift helpers and the original failure behavior. This is
not a minimal stub or a fresh claim that a pre-existing source file was new.

## Provenance correction, not a relaxed original match

An unfinished untracked `after345` builder incorrectly insisted that
`.analysis/work/mainl/vendor/fbrk.obj` was an *identical original OMF program*
to the actual Japanese CL.LIB member **167**. The original member has
external symbols in this exact order: `_setblock`, `N_PCMP@`, `N_LXLSH@`,
`N_PADD@`, `__psp`, `__heapbase`, `__brklvl`, `__heaptop`, and uses group
`08ff03ff02` (`_DATA,_BSS`). The separate vendor OBJ has a different
EXTDEF index order and opposite DGROUP order `08ff02ff03`; moreover six
CODE sites **162,181,225,266,283,302** have target-framed near calls in the
vendor OBJ but CODE-framed calls in the *actual original library member*.

The builder now first checks the exact original logical CODE/DATA payloads,
publics, extern *names* (not falsely equal ordinal indices), and each
relocation site, target name, width and addend between these two actual
objects. It then requires all six specified frame differences and both
observed DGROUP orders rather than assuming interchangeability. The pinned
**CL.LIB member remains the authority** for the real native source-builder
checks. The direct independent native TASM compile of the unchanged tracked
`fbrk.asm` matches its full original CODE, all 33 **ordered** original FIXUPP
records (including their actual frames) and group. TASM COMENT metadata is
still different; complete literal original OMF record-program identity is
not claimed for `fbrk`.

`scripts/build_th03_mainl_after345_work.py heap-break-manager` inherits
the exact 378-source `after344` parent, verifies all source hashes and
both inherited OBJ/LIB/EXE/MAP vectors without cold replay, rebuilds
only this selected member from natural 8086 source, and produces **two
independent native TASM/TLIB/TLINK** original-equal Japanese decoded
**67,372-byte EXE and full MAP** outputs, including **677 ordered MZ
relocations**. All **893** CRT slots are retained: now **379** complete
source-backed producers, **514** unchanged original contextual members,
and **125,041 logical original CODE bytes** (+352). Raw round vectors,
source/parent binding receipts and phase logs are retained under
`.analysis/work/after345-*`, with direct original OMF assertions in
`tests/test_mainl_after345_work.py` and reviewer
`scripts/review_th03_mainl_after345_work.py`.

No full cold replay, patched native outputs, Factory accepted ownership
promotion or packed-file canonical unit credit follows from this work.
