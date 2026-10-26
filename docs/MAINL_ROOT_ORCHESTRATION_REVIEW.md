# MAINL root orchestration and continue: current source ownership

2026-10-26, baseline06e7f3a. This verifies already implemented C++ source; it is
not a new implementation or whole-product reconstruction claim. The existing
complete source-only two-cold graph is unchanged. No native rebuild, new runtime
harness, object rewrite, padding or default ancestor replay is introduced.

## Real producers and partition

rootdata.obj is compiled from src/mainl/root/complete_data.cpp as GAME3/L. Its
actual includes supply cfg_resident.cpp and win.cpp before the root bodies.
The older root.asm/prefix.cpp candidates are not substituted for this producer.
TC86 Borland C++4.02 emits ROOTPRE_TEXT2458, DATA112 and BSS186. The object SHA is
0074716832a17ec51bc1ca4fcee7c0a516437181c83b83783bd55e1eb66b24e0.

contmenu.obj comes from src/mainl/root/continue.cpp with precisely the declared
CONTINUE_TEXT to CUTSCENE_TEXT composer replacement. It emits417 CODE, no private
DATA/BSS. The maintained text and complete transformed staged input are checked,
not treated as an arbitrary source-equality exception.

| CS offset | Entry | Instruction bytes | ABI |
|---|---|---:|---|
|095F:0003|cfg_load_resident_ptr|49|near noargs, segment in AX|
|095F:0034|win_load|282|near noargs|
|095F:014E|win_text_put|56|near noargs|
|095F:0186|cdg_free_all|23|near noargs|
|095F:019D|mainl_win_animate|250|near noargs|
|095F:0297|mainl_story_dispatch|133|near noargs, integer AX|
|095F:031C|mainl_stage_load|288|near noargs|
|095F:043C|mainl_stage_intro|627|near noargs|
|095F:06C1|mainl_shot_pair|111|near Pascal, RET6|
|095F:0730|mainl_shot_load|93|near Pascal, RET2|
|095F:078D|main|528|far cdecl, RETF0|
|095F:099D|mainl_continue_menu|417|near noargs, integer AX|

Twelve complete procedures own2857 instruction bytes/944 instructions. The
18-byte switch at095F:06AF..06C1 is checked separately: nine WORD destinations,
all instruction boundaries in stage_intro, plus its own CODE-relative dispatch
field. It is not counted as instructions. No gaps are hidden by byte masking.

All313 literal native fields are independently resolved in recorded order:
rootdata278 and continue35. rootdata has111 external far CODE calls,92 external
DGROUP offsets,eight self-relative near externals,29 local DATA/BSS offsets,
ten local CODE fields and28 DATA far pointers. Continue has20 far calls and15
DGROUP offsets. Both complete CODE producers and root DATA112 match target and
candidate. All131 ordered CODE relocations and28 ordered context DATA relocations
match literally. Complete record inventory, native groups/alignment, all CODE/
DATA/BSS publics and all133 literal external declarations bind to both MAP tables.

Root DATA is allocated0E3F:00A2..0112 and BSS133C..13F6. Those pointers, win_text,
playchar and flag storage remain required uncredited context. Unrelated callees,
resources and vendor code receive no new ownership. The existing current cold
audit binds all938 repeated outputs, full source graph and consumed SDK headers.

## Preserved semantics and ABI

CFG reads eight bytes into a local struct, ignores file-operation results,
sets resident offset0 and returns its segment in AX. It does not promise a valid
loaded resident or synthesize an error branch.

Win loading keeps BYTE winner atBP-1 and unsigned message index atBP-2. Explicit
zero extension before indexing is retained. Three60-byte reads receive separate
NUL terminators in the183-byte external text array. win_text_put draws atx80,
y272/288/304. Failed reads and unchecked player/message indices are not sanitized.

Story dispatch retains its signed16 promotion of optional BYTE player ID minus1,
unchecked stage/opponent indexing and original special-stage outcomes. Stage
loading mutates filenames in place. Shot loading copies the12-byte template to
its local buffer; the far pointer crosses into the RET6 helper that mutates its
extension before loading the second image. No allocator/ownership is invented.

Main is far cdecl. The high-score-menu failed execl at080C cleans12 bytes and
falls through0814 into the following code; later launch/final-exit execl at093E
returns viaRETF0947. CFG failure returns viaRETF099C. Success of exec and physical
I/O/timing are not claimed. The current calls at233E and2382 are mainl_reg_music
and mainl_ending respectively; old runtime-model labels ending/staff are historical
names only, not current symbol attribution. Existing decoder is reused only for
complete boundaries, direct-edge and switch closure, not its runtime harness.

Continue retains the source's unsigned remaining-credit BYTE, selection/input
ordering and both terminal AX outcomes. score_last is cleared before the zero-credit
return; OK/SHOT precedes CANCEL, and the later story-stage decrement/lives reset
also occurs after declining in the loop. External state changes and polling are
not replaced with host-side behavior or strengthened preconditions.

## Current acceptance and verification

Previous84 owner observations are preserved by their exact digest before adding
these twelve. Current totals become96 extents/101 procedures/15525 CODE+224 DATA.
The live tracked namespace becomes192; historical145 eligibility and mocked150
numerators stay fixed. Existing tests receive necessary counter/fixture updates
only. Shared status changes require OP/ZUN publication refresh without native
or source changes to either product.

Reports are preserved under .analysis/work/mainl-root-orchestration-preserved.
The new review requires --current-cold and writes atomically after success. Whole
product source ownership, Factory registry acceptance and whole-game denominator
remain open. Final focused/fullCI terminal results are reported separately; this
note will not be changed after final gates.
