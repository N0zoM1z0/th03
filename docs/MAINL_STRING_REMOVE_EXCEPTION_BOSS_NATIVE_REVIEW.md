# Complete original Borland string::remove: 822 CODE, 30 DATA, 37 FIXUPPs

The pinned original Japanese CL.LIB **member 421** (`stremove`) has been
reconstructed as **real symbolic 8086 source** in
`src/mainl/crt/stremove.asm`. The member includes a complete
`@string@remove$quiui` far C++ implementation: position and length
validation, copy-on-write reference handling, `TStringRef::splice`, buffer
cloning, original exception/constructor/destructor paths and returns.
This is not merely an exported entry stub or a machine-code array.

The original `_TEXT` contains **284 CODE bytes**: five-byte unwind thunk,
compiler exception/catch metadata and all three real far cleanup helpers.
The `_TEXTC` contains **538 CODE bytes**, of which +0..279 are the actual
method and +280..537 are four complete typed RTTI descriptors for `xmsg`,
`string`, `xalloc` and `string::outofrange`. The original `_DATA` is a real
**30-byte initialized `String reference out of range` error message**;
`_BSS` is empty, original DGROUP is `0aff02ff03` and 12 original Borland
external imports and the real far public are preserved.

All **822 CODE bytes and 30 DATA bytes**, exact public/import/segment
interfaces, and **all 37 original OMF FIXUPPs** agree with the actual
pinned original member. This is **literal record-order equality**,
including 16 exception cleanup and 21 method/RTTI relocations with their
sites, widths, target methods, frames and addends. The source uses `ORG`
at original instruction/typed-data declaration boundaries to retain BCC's
descending FIXUPP chronology without padding or rewriting any native OBJ.
Full Borland OMF program-record serialization still differs in other
nonsemantic metadata and is not claimed identical.

`scripts/build_th03_mainl_after371_work.py string-remove-exception-boss`
revalidates the **451-source** original CRT parent, compiles only this
changed complete member and reconstructs the original **893-slot** library
and decoded Japanese MAINL program in **two independent serialized native
TASM/TLIB/TLINK rounds**, without full cold replay. Both reproduce the
original **67,372-byte EXE and complete MAP** byte-for-byte, including
all **677 ordered MZ relocations**. Verified working source now reaches
**452 original-equal full CRT members**, **441 contextual original vendor
members** and **143,949 source-compiled original-equal CODE bytes**, a gain
of **822**. All raw original and native OBJ/LIB/EXE/MAP pairs, logs, and
source/parent SHA receipts are retained under `.analysis/work/after371-*`,
with reviewer `scripts/review_th03_mainl_after371_work.py` and independent
raw OMF/MZ regression `tests/test_mainl_after371_work.py`.

This is working CRT source and linked-product verification, not a new
formal Factory accepted extent, canonical packed product or whole-game
ownership proof.
