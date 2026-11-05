# Original 32-bit long division/modulo: complete CODE, unresolved MAP aliases

`src/mainl/crt/h_ldiv.asm` is a full **174-byte original Japanese Borland
CRT h_ldiv member 67** implementation. It contains the entire 8086 signed
and unsigned 32-bit division/remainder algorithms, common 32-bit bitwise
long-division core, and 12 exact original PUBLIC near/far aliases at
`_TEXT+0,3,7,10,15,18,23,26`:
`N_LDIV@`, `F_LDIV@`/`LDIV@`, `N_LUDIV@`, `F_LUDIV@`/`LUDIV@`,
`N_LMOD@`, `F_LMOD@`/`LMOD@`, `N_LUMOD@`, `F_LUMOD@`/`LUMOD@`.

A new **independent runnable source audit**,
`scripts/audit_th03_mainl_h_ldiv_source.py`, compiles this exact native
source with TASM 5.0, checks the actual pinned Japanese CL.LIB member's
complete CODE payload and all original names and offsets, original
`_TEXT`/`_DATA` segment geometry, DGROUP and zero imports/relocations, and
binds the parent **408-member** source/receipt chain to the source hash.
It makes no claim that the source reproduces the entire original Borland
OMF program record metadata. `tests/test_mainl_h_ldiv_original_scope.py`
independently checks the CODE-only scope; the generated private audit report
is `.analysis/work/h_ldiv-original-source-scope.json`.

## The remaining real native issue (do not hide or count as complete)

The earlier direct Japanese TASM/TLIB/TLINK replacement test generated an
**exact original 67,372-byte MAINL EXE and ordered 677 DOS MZ relocation
table**, but the MAP differs in **two pairs of same-address public aliases**:
`LDIV@` versus `F_LDIV@` at `_TEXT+3`, and `F_LUMOD@` versus `LUMOD@`
at `_TEXT+26`. The original Borland CL.LIB and TASM 5 assembler emit
different PUBDEF record orders. Experiments exchanging label/public
statement order, `LABEL FAR`/`LABEL NEAR`, `EQU` variants and source
subdivision preserve the 174 CODE bytes but **do not** restore the two
original MAP tie orders. The historical raw diagnostic outputs remain at
`.analysis/work/huge-arithmetic-link-diagnostic.exe` and `.map`, and
`.analysis/work/mainl-after353-huge-arithmetic-build.json` retains the
failed former branch receipt (which was separated from the valid `rfind`
`after353` checkpoint, not overwritten or discarded).

**This member is NOT counted in the currently validated 408 original-equal
source-produced CRT members / 131,776 logical CODE bytes.** The complete
source and demonstrably correct original CODE are nevertheless committed,
so future work can solve the MAP/PUBDEF issue without repeating the actual
algorithm reconstruction. No target OBJ, linked EXE, MAP or MZ table was
patched or sorted to manufacture acceptance. Neither full cold replay nor
formal Factory decoded/packed-product source acceptance is claimed.
