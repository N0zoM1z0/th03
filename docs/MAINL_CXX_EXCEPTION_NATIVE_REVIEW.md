# Original Japanese C++ exception runtime: complete `xxv` with ordered DOS relocations

The genuinely selected Borland CRT member **156** (`xxv`) reconstructs
**nine original far public exception-runtime APIs** at their true offsets:
`terminate`, `set_terminate`, `__call_terminate`, `unexpected`,
`set_unexpected`, `__call_unexpected`, the near and far polymorphic
**destructor type-cast helpers** and `__ExceptInit`. Its complete original
layout is **649 `_TEXT` CODE bytes, 296 initialized `_DATA` bytes, and four
uninitialized `_BSS` bytes**, grouped as `08ff02ff03`. It exports **15
original DATA globals**, including `__CPPexceptionList`, handler pointers,
throw locations, two 128-byte original exception workspaces and the real
four-byte BSS destructor-count pointer. There are five ordered original
imports and **16 original OMF relocations**.

`src/mainl/crt/xxv.asm` implements all nine runtime algorithms as actual
symbolic 8086 instructions, preserving far stack callback ABI, original
catch cleanup, process termination, exception-register state, destructor
pointer arithmetic and unchecked historical behavior. CODE+76..117 is
original **non-executable 42-byte typed C++ exception frame metadata** with
two true far CODE pointers, not incorrectly disassembled instructions.
The original 296-byte initialized DATA is expressed with named public
fields and **two actual 128-byte zero-initialized exception buffers**;
each workspace byte is materialized just like the original selected OBJ.
No executable original machine-CODE byte array, invented padding, or
modified compiled OBJ/EXE was used.

## Why simple source/OBJ equality was insufficient

An initial natural TASM assembly reproduced **all 649 CODE and 296 DATA
bytes, all 24 CODE/DATA publics (9 CODE + 15 DATA), the BSS public,
every import, and all 16
native FIXUPP sites, targets, addends and frame methods**. But TLINK's
full Japanese EXE differed in **only four bytes**, all in the **ordered DOS
MZ relocation table**; the MAP and decoded program bytes were already
identical. The compiler's original relocation order included **CODE+127,
CODE+110, CODE+80**, followed independently by **DATA+14, DATA+10**.
TASM's source-order emission initially swapped two pairs of those entries.

The original typed CODE exception-frame metadata and initialized handler
pointers were therefore authored with **natural symbolic `ORG` position
selection**, arranging named real `dw`/`dd` fields in the original relevant
fixup order. This changes neither machine instructions nor data values:
`ORG` simply allows real CODE instructions and separately typed metadata
to be declared in the required positions, with the original handler pointer
at DATA+14 before DATA+10. A standalone TASM rebuild still reproduces
**all actual CODE/DATA materialized bytes**, all 24 original CODE/DATA
public offsets, the BSS public, and **16/16 fixups by site/target/frame**.
The complete BCC-vs-TASM literal FIXUPP *record sequence* still differs;
whole original OBJ byte serialization is **not** claimed. Crucially, the
**entire ordered product MZ relocation table now matches exactly**.

`build_th03_mainl_after306_work.py exception-boss` extends the actual
source-bound **306-source Japanese CRT** at original selected library slot
156. **Two independent normal TASM/TLIB/TLINK rounds** both reproduce the
**complete original 67,372-byte decoded Japanese MAINL EXE and MAP
byte-for-byte**, preserving **all 677 ordered DOS MZ relocations** and
**586 unchanged original vendor CRT member programs**. Working source
reaches **307 members / 102,964 original-equal CODE bytes**. This is
source-bound working evidence, not new formal accepted-ledger credit, and
no full historical cold replay was performed.

Reproduce and review with `review_th03_mainl_after306_work.py exception-boss`,
`tests.test_mainl_after306_work`, real native writer logs, hash-bound
receipts and two raw OBJ/LIB/EXE/MAP vectors under `.analysis/work/after306-*`.
