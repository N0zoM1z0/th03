# Original program resolver, incrementally revalidated as CRT source member 363

This increment does **not** assume that the older
[LoadProg notes](MAINL_LOADPROG_NATIVE_REVIEW.md) were correct. It checks the
tracked `src/mainl/crt/loadprog.asm` (and its source-bound
`src/mainl/crt/crt_errno.inc`) directly against original Japanese CL.LIB
member **891** and full linked MAINL output in independent fresh TASM/TLIB/
TLINK rounds.

The **complete 871-byte CODE** implements the far DBCS path-separator scan
(132 bytes), far executable-probe helper (137 bytes), and the near 602-byte
`__LoadProg` dispatcher exported at CODE+269. It contains all original path
lookup, `.COM`/`.EXE`/`.BAT`, COMSPEC, environment/command construction,
error return and buffer cleanup flow, including the original unguarded
80-byte and 128-byte buffers. It also preserves all **40 real initialized
DATA bytes** (PATH, suffixes, COMSPEC, /c) and the original empty BSS.
The original OMF program exposes 15 external references and 32 relocation
fields: full sites, widths, targets, **frames** and ordered FIXUPP fields
match both new source-produced objects exactly.

## Rechecked source discrepancy: original library versus standalone vendor

The alternate `.analysis/work/mainl/vendor/loadprog.obj` carries **two
non-identical BCC near-call frames** at CODE+633 and +754. At both sites it
uses original vendor TARGET frame5, whereas the actual pinned original
CL.LIB member 891 has CODE frame0. All code and initialized DATA, public /
external ABI and relocation site/target/addend fields are the same; the
whole original CL.LIB program is authoritative. The after337 native builder
now explicitly checks these two differences, rather than silently treating
one OMF program as the other. The original **complete OMF record program**
remains different from TASM's emitted metadata even though the full ordered
FIXUPP list and linked product match.

`scripts/build_th03_mainl_after337_work.py dos-loadprog-boss` consumes the
362-member source/receipt-bound `after336` parent, checks the complete
original library member in both inherited producer rounds, hashes and copies
the actual `crt_errno.inc`, and compiles only this changed member before
reconstructing its 893-slot CRT carrier and linking in two independent
native rounds. Both reproduce byte-for-byte the original **67,372-byte
Japanese MAINL EXE and complete MAP**, including all **677 ordered MZ
relocations**. There are now **363 original-equal source-backed members**,
**530 untouched contextual members**, and **118,895 source-compiled CRT CODE
bytes** (increase **871**, plus 40 initialized DATA bytes).

Raw OBJ/LIB/EXE/MAP vectors, source hashes, parent receipt references and
writer logs are retained under `.analysis/work/after337-*` and reviewed by
`scripts/review_th03_mainl_after337_work.py` and
`tests/test_mainl_after337_work.py`. This is working-source proof, not new
Factory-accepted or packed-product source ownership. No cold replay was run.
