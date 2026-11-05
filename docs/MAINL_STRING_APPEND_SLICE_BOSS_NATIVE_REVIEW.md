# Entire original C++ `string::append(string &, unsigned, unsigned)`

The original Japanese Borland CL.LIB member **378** (`append1`) has been
reconstructed as native 8086 symbolic source at
`src/mainl/crt/append1.asm`, with **578 complete CODE bytes**, seven
original imports, and a far `@string@append$qmx6stringuiui` public. This is
not a wrapper: the original method's substring-bound logic, reference-counted
copy-on-write, full splice path, exception calls, and all cleanup paths are
present. The first `_TEXT` segment has **177 bytes**, including an actual
far unwind thunk, typed exception frame and two complete destructor helpers.
The second `_TEXTC` segment has **401 bytes**: the full 201-byte method and
three genuine RTTI records at +201 (`string::lengtherror`), +279 (`xalloc`),
and +345 (`xmsg`). Original DATA and BSS are empty.

Every original instruction/typed metadata byte, the one far public offset,
imports and segment/DGROUP ABI match the actual Japanese original OMF. The
source also reproduces **all 20 original FIXUPPs in their literal original
record order**, including 9 typed cleanup relocations in `_TEXT` and 11
method/RTTI relocations in `_TEXTC`, and their original target/frame/addend.
Real 8086 instructions and typed `dw`/`dd` source blocks are placed at
original offsets with `ORG`, without target-CODE byte arrays or patched
OBJ/EXE/MAP files. The full original Borland OMF *record serialization*
still differs in other metadata; full OBJ equality is not claimed.

`scripts/build_th03_mainl_after373_work.py string-append-slice-boss`
uses the **458-source** verified Japanese CRT parent and recompiles just
this original member before reconstituting all **893** CL.LIB slots and
running **two independent native TASM/TLIB/TLINK** rounds. Both regenerate
the original **67,372-byte decoded Japanese MAINL EXE and complete MAP**
byte-for-byte, including all **677 DOS MZ relocations in original order**.
The working-source carrier reaches **459 original-equal members**, **434
original contextual programs**, and **145,663 original-equal CODE bytes**
(+578). Native original/source OBJ/LIB/EXE/MAP, logs, source hashes and
parent receipt bindings remain under `.analysis/work/after373-*`; scoped
review and raw OMF/MZ regression are
`scripts/review_th03_mainl_after373_work.py` and
`tests/test_mainl_after373_work.py`.

This is scoped working-source evidence, not new Factory-accepted decoded
ownership or canonical packed-game unit credit; no full cold replay ran.
