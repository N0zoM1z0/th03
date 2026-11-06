# Complete locale, multibyte, DDVT, allocation and string members — after530

Twenty original Japanese CL.LIB members now have complete maintained source
programs in the incremental CRT carrier:

| Slot / member | CODE bytes | DATA bytes | Ordered fields |
| --- | ---: | ---: | ---: |
| 188 / `_setcoll` | 106 | 2 | 9 |
| 190 / `_setxfrm` | 101 | 2 | 9 |
| 187 / `_setbll` | 46 | 0 | 2 |
| 189 / `_setudef` | 29 | 0 | 1 |
| 283 / `setlocal` | 66 | 4 | 3 |
| 580 / `MBBTYPE` | 103 | 0 | 4 |
| 653 / `FMBBTYPE` | 103 | 0 | 4 |
| 652 / `NTHCTYPE` | 91 | 0 | 2 |
| 695 / `FNTHCTYP` | 91 | 0 | 2 |
| 595 / `MBISPRN` | 83 | 0 | 4 |
| 53 / `ddvt` | 83 | 0 | 3 |
| 54 / `fddvt` | 84 | 0 | 3 |
| 92 / `newf` | 85 | 0 | 4 |
| 169 / `fcorelft` | 80 | 0 | 5 |
| 445 / `fstrdup` | 81 | 0 | 3 |
| 455 / `fstrrchr` | 77 | 0 | 1 |
| 262 / `memicmp` | 71 | 0 | 2 |
| 437 / `fmemicmp` | 71 | 0 | 2 |
| 1 / `_stpcpy` | 61 | 0 | 2 |
| 123 / `stpcpy` | 61 | 0 | 2 |

Total: **1,573 CODE-segment bytes, 8 initialized DATA bytes and 67 ordered
logical relocation fields**. CODE contains **1,557 executable instruction
bytes and 16 bytes of inline FAR dispatch-pointer metadata**. These members
add no BSS or INITDATA. All original segments, packing/alignment, public
identities/offsets, import order and GROUP records remain checked. No earlier
cold-source owner is duplicated or added to this stage's member count.

## Locale ownership and far callbacks

The [locale field declarations](../src/mainl/crt/locale_fields.inc) preserve
original offsets: locale name +160h, collator +1A0h, transformer +1A4h and
user buffer +993h. All pointer slots remain four bytes. `_setcoll` and
`_setxfrm` preserve explicit callbacks; a null argument selects their original
C/default or locale-specific delegate. Function segments and offsets have
separate symbolic relocations. `_setbll` preserves library lookup and its
DX:AX result; `_setudef` writes the original far buffer slot.

`setlocal` retains the original C-only request behavior and pointer returns,
including returning the accepted caller pointer rather than replacing it
with a canonical string. Four distinct typed `C` strings occupy the original
eight DATA bytes across three owners. There are no new locale features,
pointer defenses or changed ownership policies.

## Multibyte state and bounded shared source

`MBBTYPE`/`FMBBTYPE` preserve single/lead/trail/illegal states and original
unsigned-byte table indexing through `__ctype` and `__mbctype`. The two
`NTHCTYPE` owners retain stateful scanning, signed index comparisons,
zero-terminator behavior and CBW sign extension of the byte result.
`MBISPRN` keeps the original lead/trail checks for double-byte characters and
single-byte printable classifications.

Each original member remains a separate TU with its own public/imports and
native extent. The paired bodies use the bounded
[byte classifier](../src/mainl/crt/mb_byte_type.inl) and
[indexed classifier](../src/mainl/crt/mb_nth_type.inl); the
[case comparison](../src/mainl/crt/memicmp_body.inl) and
[copy-end body](../src/mainl/crt/stpcpy_body.inl) likewise expand into separate
original owners. All four bounded bodies and the locale declarations are
hash-bound native inputs, with short include filenames.

## Dynamic dispatch, allocation and strings

`ddvt` and `fddvt` own distinct **word-aligned**
`DDVT_TEXT`/`FDDVT_TEXT` segments. Each begins
with **two typed FAR pointer slots**, one null and one symbolic `_abort`
pointer. They are metadata, not decoded instructions. Their two FAR entry
points select the fallback slot and return a FAR address of a dispatch slot.
The bodies retain descending word-key scans with STD/REPNE SCASW, base-table
traversal, original entry arithmetic and CLD before return. One version uses
a DS-relative table chain; the other loads ES:BX from FAR table links.

`newf` preserves zero-size normalization to one byte, the original 32-bit
allocation size and far new-handler retry loop. Existing null-result behavior
is unchanged. `fcorelft` keeps huge-pointer subtraction, original paragraph
overhead handling and low-word alignment. `fstrdup` and `fstrrchr` retain their
original 16-bit lengths and far pointer arithmetic, including the terminator
in the reverse search. Both case comparators zero-extend source bytes before
calling their original uppercase delegates and return the WORD subtraction.
The two stpcpy owners copy the original WORD strlen+1 count and return the
terminator offset with the original segment. No overflow repairs or extra
failure handling were added.

## One disclosed near-call frame difference

Nineteen members have **literal ordered FIXUPP equality**. In `fcorelft`, the
near `N_PSBP@` field at CODE offset **34** uses original
`(frame_method=5, frame=null)` TARGET versus TASM's
`(frame_method=0, frame=1)` CODE. Segment, site, location type/width, relative
flag, external target, addend and ordered position agree. Both raw transcripts
are retained per round and independently enumerated by the reviewer.

The logical comparison recognizes only that pinned target/site and guarded
frame pair. It changes no object bytes. Original Borland OBJ program-record
identity and complete literal FIXUPP equality are **not** claimed.

## Scoped native evidence

The [producer](../scripts/build_th03_mainl_after530_work.py) validates the
unchanged after529 source carrier, including fourteen TU hashes, initialized
coverage/uninitialized extents and twelve raw console-frame differences.
Original member profiles come directly from the pinned compiler CL.LIB,
whose SHA-256 is bound through the retained cold receipt and this stage's
receipt. Earlier native sources, includes and both complete output rounds
remain retained. Only the twenty affected TUs are assembled.

Two headless native TASM 5.0 / TLIB / TLINK rounds reproduce the complete
**67,372-byte Japanese MAINL EXE, retained original MAP and all 677 ordered
MZ relocations**. Both entire OBJ/LIB/EXE/MAP vectors agree between rounds.
All 811 inherited incremental source members, 62 retained context members
and the original 893-member order are preserved. The
[independent reviewer](../scripts/review_th03_mainl_after530_work.py) checks
actual source/include/recipe/parent hashes, actual writer logs, complete
initialized/uninitialized storage, ordered fields and both native vectors.
The initial byte-aligned DDVT draft failed the strict SEGDEF check before
linking; no progress was credited to it. Its complete source/include/recipe
snapshot and SHA inventory remain at
`.analysis/work/probe/locale-multibyte-word-segment-correction/`; the original
`TH03ML/probe/after530` scratch and writer logs are retained. The corrected
stage uses `TH03ML/probe/af530b` scratch and **af530b-** raw output/log paths,
explicitly bound in its receipt.
All outputs, logs and scratch remain protected pending a new storage audit.
No full CI, cold replay or new runtime/test matrix was used.

Incremental working-source CRT: **831/893 members, 207,321 original-equal
CODE-segment bytes**. Counts enumerate explicit incremental member receipts;
earlier cold-source owners remain separately tracked. Formal Factory canonical
packed-file acceptance remains **0/250**; whole-game completion is unknown.
Pinned Japanese targets remain `candidate-local-attested`.

Receipt: `.analysis/work/mainl-after530-locale-multibyte-dispatch-twenty-build.json`

SHA-256: `97416af0d48e07559a469928bc2fff5c39c0e909fe087d72132e5096410d7733`.
