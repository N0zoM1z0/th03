# Full original Borland streambuf::dbp, real CODE and format DATA

The original Japanese CL.LIB member **704** (`stbdbp`) is fully recovered in
`src/mainl/crt/stbdbp.asm`. Its sole original far public is
`@streambuf@dbp$qv`. The entire **281-byte `_TEXTA` CODE** prints the
original streambuf allocation flags, base/ebuf pointers, put-area pointers
and get-area pointers. It formats into an 80-byte stack buffer using
`_sprintf`, obtains the length with `_strlen` and writes each line using
`_write`. All four repeated paths, the far ABI and original error handling
remain present. The source contains real 8086 instructions, not CODE bytes.

The original **126-byte initialized DATA segment** contains *four distinct*
zero-terminated debug format strings with exact offsets **0, 26, 50, 88**.
They are represented as plain ASCII string declarations with explicit LF
and NUL, not copied binary payloads. The original empty BSS, group order
`08ff02ff03`, all three far imports, the public symbol and all **16
relocations**, including group-framed string references, match the pinned
original OMF member. The original ordered FIXUPP records differ from TASM's
forward order and complete literal Borland OMF program identity is not
claimed, even though the entire CODE/DATA and relocation field set agrees.

`scripts/build_th03_mainl_after342_work.py streambuf-debug-printer` uses the
source-bound **375-member** parent chain and compiles this original member
with native TASM/TLIB/TLINK **twice**. Each retained round includes complete
OBJ/LIB/EXE/MAP and writer logs. Both independently reproduce the pinned
original Japanese decoded MAINL **67,372-byte EXE/MAP**, including 677
ordered DOS MZ relocations. The 893-slot original CRT carrier now contains
**376 complete source-backed members**, **517 untouched original contextual
members** and **121,643 logical original-equal CRT CODE bytes**, plus the
126 bytes of original DATA added here. The receipt chain is under
`.analysis/work/after342-*`; the scoped review and OMF tests are
`scripts/review_th03_mainl_after342_work.py` and
`tests/test_mainl_after342_work.py`.

No full cold replay, Factory formal acceptance or packed-file unit credit is
claimed from this working-only native source restoration.
