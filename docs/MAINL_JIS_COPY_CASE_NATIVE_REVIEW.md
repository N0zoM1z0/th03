# Japanese TH03: ten full multibyte copy, reverse and JIS case algorithms

Ten actually selected, distinct Borland CRT modules now have complete
human-readable symbolic 8086 source. `MBSREV`/`FMBSREV` each implement
**144 original CODE bytes** of multibyte string reverse; `MBSNCPY`/
`FMBSNCPY` each implement **133 bytes** of counted character-copy;
`MBSNBCPY`/`FMBSNBCP` each implement **137 bytes** of counted byte-copy;
`JSTRLWR`, `JSTRUPR`, `FJSTRLWR` and `FJSTRUPR` each implement **132 bytes**
of original Japanese near/far string case conversion. They cover original
CRT selected slots 628, 684, 621, 677, 615, 671, 647, 649, 692 and 694.

The source preserves the genuine 16-bit string and DBCS processing, direct
`DS`/`ES` pointer semantics, real register/branch behavior, near/far
calling conventions and original public offsets. All ten modules use the
actual original `_TEXT` CODE, empty `_DATA/_BSS` and `08ff02ff03` DGROUP.
Every member has exactly one `__mbctype` data-table reference, authored
with a named `DGROUP:__mbctype[bx+1]` expression rather than a hard-coded
address. No copied executable machine-CODE arrays, source padding or
post-assembled OBJ patches were used.

TASM 5.0 `/m /mx /kh32768 /t` independently reconstructs **all 1,356
original CODE bytes**, the selected public symbols, ordered EXTDEFs,
correct segment layout, and **all 10 literal original OMF FIXUPP fields
including original record order, original site, target, kind, addend,
width and frame method**. This stronger OMF observation refers to the
FIXUPP fields, not unrelated OMF records that were not compared bytewise.

`build_th03_mainl_after307_work.py jis-copy-case` extends the unchanged
source-bound **307-source Japanese CRT** and compiles the ten actual
selected CRT slots in **two independent normal TASM/TLIB/TLINK rounds**.
Both reproduce the **entire original 67,372-byte decoded Japanese MAINL
EXE and full MAP byte-for-byte**, preserving all **677 original ordered DOS
MZ relocations** and **576 untouched vendor CRT member programs**. The
working source CRT reaches **317 members / 104,320 original-equal CODE
bytes**. Formal accepted-ledger credit remains unchanged; no full cold
replay was performed.

Verify with `review_th03_mainl_after307_work.py jis-copy-case`,
`tests.test_mainl_after307_work`, and the retained source-hash-bound raw
OBJ/LIB/EXE/MAP vectors and actual tool writer logs under
`.analysis/work/after307-*` and `.analysis/work/mainl-after307-*`.
