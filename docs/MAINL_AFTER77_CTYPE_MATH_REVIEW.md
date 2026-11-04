# Original Japanese MAINL CRT: numeric and ctype source recovery

After the 82-source far-string carrier, the selected **actual** Japanese CRT
member programs for four more source modules were reconstructed and verified:

| Original member slot | Source | Complete original CODE | Selected original ABI |
| ---: | --- | ---: | --- |
| 132 | `toupper.asm` | 48 | `_toupper`, original `__ctype` byte table |
| 194 | `atol.asm` | 138 | `_atol` (+0), `_atoi` (+117), original `__ctype` |
| 3 | `abs.asm` | 18 | `_abs` far, `int` result |
| 83 | `labs.asm` | 44 | `_labs` far, 32-bit `DX:AX` result |

For these four modules the literal original OMF FIXUPP order and frames are
identical to the source-built objects (two ctype fixups; zero for both math
members). The other five far-string sources are checked independently; only
member129 `strxfrm` has its two relocations in a different record order.

The reconstructed assembly preserves the **original unchecked behavior** and
native 16-bit arithmetic. `atol` is not a mere C-library stand-in: the single
member contains both `_atol` and `_atoi`, sign/whitespace handling, 16-bit
fast parsing and original 32-bit multiplication. `labs` uses the original
carry/borrow behavior when negating `DX:AX`. `toupper` uses the exact
Borland ctype table offset and case bit. All are symbolic 8086 TUs, without
target-code byte arrays or binary object patches.

Native TASM emits **48/48 + 138/138 + 18/18 + 44/44 CODE bytes exactly**,
with original public offsets, empty DATA/BSS, group layout and imports.
`toupper` and `atol` also reproduce their original literal ordered external
FIXUPP fields, including `__ctype` frame and addend; `abs` and `labs` have
no native fixups.

`scripts/build_th03_mainl_after77_work.py strings-ctype` and
`strings-ctype-math` extend the retained 77-member original Japanese native
carrier, including the five newly recovered string modules in the same source
build. Two independent TASM/TLIB/TLINK rounds in both modes reproduce the
**complete 67,372-byte original decoded Japanese MAINL EXE and original MAP**,
including all **677 ordered MZ relocations**. Working source CRT becomes
**86 original-position modules / 34,306 original-equal CODE bytes**; **807**
original vendor program records are unchanged. The earlier public `strxfrm`
member retains an original-versus-TASM FIXUPP **record order** difference;
it is not hidden by the complete linker success.

The source-bound reviewed raw OBJ/LIB/EXE/MAP pairs and real writer phase
logs are retained under `.analysis/work/after77-strings-ctype-math-*` and
`mainl-after77-*`, checked with `review_th03_mainl_after77_work.py` and
`tests.test_mainl_after77_work`. This is source-only native reconstruction,
not new formally accepted ledger credit; no full cold replay was performed.
