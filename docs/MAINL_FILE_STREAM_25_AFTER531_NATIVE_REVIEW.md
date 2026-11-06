# Complete file, stream-buffer and conversion-fallback members — after531

Twenty-five original Japanese CL.LIB members now have complete maintained
source programs in the incremental CRT carrier:

| Slot / member | CODE bytes | DATA bytes | BSS bytes | Ordered fields |
| --- | ---: | ---: | ---: | ---: |
| 24 / `dosdfree` | 60 | 0 | 0 | 1 |
| 32 / `dosopen` | 58 | 0 | 0 | 1 |
| 106 / `rmtmp` | 81 | 0 | 0 | 3 |
| 112 / `setbuf` | 49 | 0 | 0 | 1 |
| 118 / `sopen` | 63 | 0 | 0 | 2 |
| 119 / `srchpath` | 68 | 5 | 80 | 3 |
| 152 / `xclose` | 42 | 0 | 0 | 2 |
| 159 / `brk` | 40 | 0 | 0 | 2 |
| 182 / `_access` | 59 | 0 | 0 | 2 |
| 185 / `_fsopen` | 57 | 0 | 0 | 2 |
| 200 / `chmod` | 77 | 0 | 0 | 2 |
| 204 / `close` | 44 | 0 | 0 | 4 |
| 205 / `closea` | 51 | 0 | 0 | 2 |
| 218 / `fdopen` | 67 | 0 | 0 | 2 |
| 230 / `freopen` | 64 | 0 | 0 | 2 |
| 281 / `srchenv` | 71 | 1 | 0 | 3 |
| 322 / `tmpfile` | 75 | 4 | 2 | 5 |
| 334 / `xfclose` | 66 | 0 | 0 | 3 |
| 705 / `fsattch` | 82 | 0 | 0 | 3 |
| 718 / `fsclose` | 66 | 0 | 0 | 3 |
| 739 / `iostasn1` | 41 | 0 | 0 | 1 |
| 853 / `stbalc` | 77 | 0 | 0 | 1 |
| 870 / `stbstb1` | 79 | 0 | 0 | 2 |
| 872 / `stbtalc` | 51 | 0 | 0 | 6 |
| 341 / `cvtfak` | 31 | 57 | 0 | 8 |

Total: **1,519 executable CODE bytes, 67 initialized DATA bytes, 82 BSS bytes
and 66 ordered logical relocation fields**. There is no inline CODE metadata
or INITDATA in these members. All segment names/order, original sizes,
alignment/combination attributes, public identities/offsets, import order and
GROUP records are checked. Original iostream slots **696–892 (197 members)
now all source-link** in the incremental library.

## DOS, stdio and temporary-file ownership

`dosdfree` preserves INT 21h/36h, original error 19 and all four disk-statistic
WORD writes. `dosopen` retains access-mode translation, sharing flags, DS save/
restore and near error translation. `brk`/`sbrk` keep their far external APIs,
near internal helpers, original sign extension and caller cleanup. `_access`
and `chmod` retain DOS readonly-bit handling and original errno behavior.
`close` preserves descriptor-state clearing before the low-level close result;
`closea` retains the push-CS/near-call sequence into its local FAR entry.

`sopen` keeps the original optional creation-mode argument and flag merge.
`_fsopen`, `fdopen` and `freopen` retain near GETFP/OPENFP delegation, original
Pascal cleanup and existing validation. Descriptor storage stays byte-sized;
`freopen` preserves the original FILE token comparison. `setbuf` retains its
512-byte size and original null-buffer mode selection. No new range checks,
sharing behavior or defensive product changes were introduced.

The new [temporary-file field declaration](../src/mainl/crt/stdio_tmp.inc)
includes the unchanged [FILE layout](../src/mainl/crt/stdio_layout.inc) and
defines its original **WORD temporary number at +16**. `rmtmp` begins after
the five standard streams and counts successful temporary-stream closes.
`xfclose` scans original FILE flags. Both advance by the original 20-byte
FILE width. `tmpfile` owns its two-byte uninitialized `__tmpnum`, calls the
original name generator and opens `w+b`, storing that number only on the
original successful path. Existing [errno declarations](../src/mainl/crt/crt_errno.inc)
are reused without edits; all three include hashes are bound to the stage.

`srchpath` owns the original **80-byte BSS** result buffer and typed `PATH`
string. `srchenv` owns the empty-string fallback for a missing environment
value. Original far returns, unchecked buffer behavior and helper arguments
are preserved. BSS is checked as uninitialized storage, not emitted zeros.

## Stream buffer completion

`fsattch` and `fsclose` preserve their original ios state transitions and
filebuf delegation, including the distinction between clear and setstate.
`iostasn1` keeps the original ios buffer lookup and assignment return.
`stbalc` allocates 1024 bytes, installs the original owned buffer fields and
retains low-word end-pointer arithmetic. `stbstb1` preserves both delegated
buffer ranges, caller-provided offsets and cleanup. `stbtalc` retains its
signed high-word guard, preincremented 32-bit global bit number, long shift
helper and original exhaustion result.

These were the six remaining context entries in the original contiguous
iostream block. The independent reviewer checks actual native library source
membership for **every slot 696–892**, alongside complete inherited programs.
This is a CRT source-link milestone, not whole-game source acceptance.

## Typed floating-format fallback vectors

`cvtfak` retains four original segments: CODE, `_DATA`, `_CVTSEG` and `_SCNSEG`.
The three DATA segments own **49 diagnostic bytes and four near pointer
words (8 bytes)**. Typed strings preserve the original five-byte prefix writes
and 39-byte suffix write to DOS handle 2. The conversion vector selects the
printf entry; three scanning vector words select the scanf entry. All four
are symbolic CODE offsets with original ordered relocations. The diagnostic
ends with the original near abort tail jump. These are actual fallback
semantics, not substitutes for the already retained floating conversion code.

## Seven disclosed near-call frame differences

Twenty members have **literal ordered FIXUPP equality**. Five members have
seven original `(frame_method=5, frame=null)` TARGET versus native
`(frame_method=0, frame=1)` CODE differences:

| Member | Ordered field site / external target |
| --- | --- |
| `_fsopen` | 49 / `__OPENFP`, 9 / `__GETFP` |
| `close` | 19 / `__IOERROR` |
| `fdopen` | 59 / `__OPENFP`, 15 / `__GETFP` |
| `freopen` | 58 / `__OPENFP` |
| `tmpfile` | 18 / `__TMPNAM` |

Every other attribute and ordered position agrees. Original CODE-framed near
calls in `dosopen`, `brk`, `closea` and `cvtfak` already match literally.
The guarded logical comparison recognizes only the seven pinned target/site
pairs and changes no object bytes. Both raw field transcripts remain recorded
per native round and independently enumerated. Original Borland OBJ identity
and full literal FIXUPP equality are **not** claimed.

## Scoped native evidence

The [producer](../scripts/build_th03_mainl_after531_work.py) revalidates the
unchanged after530 carrier, including twenty TU hashes, all five include
hashes and the original raw arithmetic-frame difference. Pinned compiler
CL.LIB programs and its SHA-256 remain distinct from the inherited 28-source
carrier. Both complete parent rounds and the earlier source DAG are retained.
Only the twenty-five affected members are assembled.

Two headless TASM 5.0 / TLIB / TLINK rounds reproduce the complete original
**67,372-byte Japanese MAINL EXE, retained MAP and all 677 ordered MZ
relocations**. Both full OBJ/LIB/EXE/MAP vectors agree between rounds; all
831 earlier incremental source members, 37 context members and the original
893-member order are preserved. The
[independent reviewer](../scripts/review_th03_mainl_after531_work.py) verifies
source/include/recipe/parent hashes, writer logs, complete storage coverage,
ordered fields, the entire iostream block and both full native vectors.
All artifacts, candidate branches and logs remain retained. No full CI,
cold replay or new runtime/test matrix was used.

Incremental working-source CRT: **856/893 members, 208,840 original-equal
CODE-segment bytes**. Earlier cold-source owners remain separately tracked.
Formal Factory canonical packed-file acceptance stays **0/250**; whole-game
completion is unknown. Japanese targets remain `candidate-local-attested`.

Receipt: `.analysis/work/mainl-after531-file-stream-fallback-twenty-five-build.json`

SHA-256: `5bf827de0862526924dc01689f3204e6405b2eea6fb28b85495935661fb617d0`.
