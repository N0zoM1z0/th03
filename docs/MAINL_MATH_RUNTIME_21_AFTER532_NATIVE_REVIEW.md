# Five arithmetic helpers and sixteen runtime storage owners — after532

Twenty-one original Japanese CL.LIB members now have complete maintained
source programs in the incremental CRT carrier. CODE, initialized DATA and
uninitialized BSS are accounted separately:

| Slot / member | CODE bytes | DATA bytes | BSS bytes | Literal fields |
| --- | ---: | ---: | ---: | ---: |
| 69 / `h_lrsh` | 32 | 0 | 0 | 0 |
| 70 / `h_lursh` | 33 | 0 | 0 | 0 |
| 74 / `h_psbh` | 32 | 0 | 0 | 2 |
| 75 / `h_psbp` | 40 | 0 | 0 | 0 |
| 76 / `h_spush` | 39 | 0 | 0 | 0 |
| 45 / `files` | 0 | 400 | 0 | 5 |
| 46 / `files2` | 0 | 42 | 0 | 0 |
| 47 / `fmode` | 0 | 4 | 0 | 0 |
| 48 / `fpstklen` | 0 | 2 | 0 | 0 |
| 77 / `heaplen` | 0 | 2 | 0 | 0 |
| 117 / `sigdata` | 0 | 0 | 4 | 0 |
| 122 / `stklen` | 0 | 2 | 0 | 0 |
| 165 / `dtrcount` | 0 | 0 | 4 | 0 |
| 319 / `sysnerr` | 0 | 2 | 0 | 0 |
| 550 / `coniotyp` | 0 | 2 | 0 | 0 |
| 571 / `wclrnorm` | 0 | 2 | 0 | 0 |
| 572 / `wedgectl` | 0 | 2 | 0 | 0 |
| 573 / `wgarbage` | 0 | 2 | 0 | 0 |
| 576 / `wkanji` | 0 | 2 | 0 | 0 |
| 577 / `wnewline` | 0 | 2 | 0 | 0 |
| 578 / `wscroll` | 0 | 2 | 0 | 0 |

Total: **176 executable CODE bytes, 468 initialized DATA bytes, 8 BSS bytes
and seven literal ordered relocation fields**. The sixteen storage owners
receive no CODE credit. Every original payload, public offset, segment
name/order/size, alignment/combination attribute, import and GROUP record is
checked. `h_psbh` retains its original single CODE segment and absence of a
DATA segment or DGROUP.

## Arithmetic and stack ABI

The signed and unsigned right-shift helpers retain DX:AX operands, CL counts,
BX scratch and their original high-word paths. Their near entries convert the
return address to a FAR return using pop/push CS, while the FAR aliases share
the original body. No new count masking or input-domain restrictions were
introduced.

`h_psbh` preserves separate near/FAR returns and SI saving. Its two immediate
`__AHSHIFT` references remain symbolic references to the original absolute
linker symbol; the source does not replace them with a guessed constant or
memory load. `h_psbp` retains segment:offset subtraction, DI preservation and
original signed DX:AX result construction. `h_spush` retains distinct near/
FAR entry setup, SS destination, DS source, return-address handling, saved
registers, WORD copy plus odd-byte copy, and original CLD behavior.

All five helpers use the already pinned **JWasm v2.12pre** compatible emitter
under an [explicit five-member profile](../config/th03_mainl_math_jwasm.toml).
Their PUBLIC declarations follow the original CL.LIB chronology. Every ordered
name/offset/type payload matches the original PUBDEF entries, even where the
native emitter groups entries into one record. This preserves same-address
MAP aliases without sorting a MAP or rewriting an object. The original
assembler is not identified; source revision, version, binary/profile hashes
and attestation-driver hash are bound in the native receipt.

## Typed stdio initialization

[files.asm](../src/mainl/crt/files.asm) owns twenty real 20-byte FILE records.
The local record macro declares WORD level/flags, byte descriptor/hold, WORD
buffer size, two FAR buffer pointers, WORD temporary number and near token.
The five standard streams retain their original flags, handles and symbolic
self tokens. The fifteen unused entries are initialized FILE records, not BSS
or filler. Original relocation chronology is descending token sites
**98, 78, 58, 38, 18**, with original offsets **80, 60, 40, 20, 0**.

[files2.asm](../src/mainl/crt/files2.asm) owns `__nfile=20` and all twenty WORD
descriptor states. The five initial states remain 6001h, 6002h, 6002h, A004h
and A002h; the remaining fifteen are initialized zero states. Native iterated
zero initializers are materialized for complete byte and coverage comparison.
Both existing [FILE declarations](../src/mainl/crt/stdio_layout.inc) and
[temporary-field declarations](../src/mainl/crt/stdio_tmp.inc) remain unchanged
and hash-bound. The unused `__setupio` import is preserved.

## Scalar and BSS ownership

The scalar sources preserve text-mode defaults and inverse umask, original
floating-stack length 204, stack length 4096, zero heap-length default,
48-error count, zero console-type detection state and six enabled window
options. `coniotyp` retains its original `___conio_type_init` import. Signal
pointer and destructor count each remain four bytes of **uninitialized BSS**.
All names, WORD/DWORD widths, offsets and original storage classes are checked;
there is no new runtime initialization or defensive behavior.

## Exact field and native evidence

**All twenty-one members have literal ordered FIXUPP equality**, including the
two `__AHSHIFT` fields and all five FILE token fields. There are **zero new
frame exceptions** and no logical field normalization in this stage. Raw
Borland OBJ program-record identity is still not claimed; record boundaries,
headers and producer metadata are separate from payload/relocation equality.

The [producer](../scripts/build_th03_mainl_after532_work.py) validates the
unchanged after531 carrier, including twenty-five TUs, all three include
hashes and its seven explicitly retained stdio frame differences. Original
compiler CL.LIB hashes remain distinct from the earlier source carrier.
Only the twenty-one affected programs are assembled: five through the
attested compatible emitter and sixteen through TASM 5.0. Native writers stay
headless, serialized, on one CPU at nice10.

Two native TLIB/TLINK rounds reproduce the complete **67,372-byte Japanese
MAINL EXE, retained original MAP and all 677 ordered MZ relocations**. Both
entire OBJ/LIB/EXE/MAP vectors agree between rounds. All 856 earlier
incremental source members, 16 context members and original 893-member order
are preserved. The [independent reviewer](../scripts/review_th03_mainl_after532_work.py)
checks complete native vectors/logs, source/include/recipe/tool hashes, full
initialized/uninitialized storage, every literal ordered field, five ordered
PUBLIC payloads and all 197 source-linked iostream members at slots 696–892.
All evidence and candidate branches remain retained. No full CI, cold replay,
new runtime model or redundant test matrix was run.

Incremental working-source CRT: **877/893 members, 209,016 original-equal
CODE-segment bytes**. Earlier cold-source owners remain separately tracked;
the remaining context list is not a list of missing source functions. Formal
Factory canonical packed-file acceptance stays **0/250**; whole-game completion
is unknown. Japanese targets remain `candidate-local-attested`.

Receipt: `.analysis/work/mainl-after532-math-runtime-storage-twenty-one-build.json`

SHA-256: `6c58f141f33277f5903521492056cb45a1473f6fe1445eb73740a3a0bf2f5307`.
