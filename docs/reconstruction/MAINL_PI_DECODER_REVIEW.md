# MAINL root PI decoder and release candidate review

This independently reviews decoded root `0000:0FEC..162B`:1600 bytes.
The previous PI note concerns five C++ wrappers in segment `0C7E` and models
the decoder interface. Its300 changed wrapper bytes do not cover this root
extent. Neither receipt grants maintained MAINL source or exact acceptance.

Receipt: `.analysis/sol-mainl-pi-decoder-review-20261006.json`, SHA-256
`b8df97fa69813085abf90a7d08fba4c0640614bf37b0c0449b64abda3192c584`; 817 guarded inputs.

```sh
DISPLAY= WAYLAND_DISPLAY= python3 scripts/review_th03_mainl_pi_decoder.py \
  --output .analysis/NEW_PI_DECODER_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_pi_decoder_review.py
```

## Boundaries and candidate lineage

| Root scope | Offset | Body bytes | Decoded instructions | Return |
| --- | ---: | ---: | ---: | --- |
| GRAPH_PI_FREE | FEC |76|33|RETF8|
| Shared loader error tail |1038|11|7|RETF12|
| GRAPH_PI_LOAD_PACK |1044|1211|537|RETF12|
| Private color decoder |1500|238|107|near RET|
| Private byte decoder |15EE|44|18|near RET|
| Private buffer refill |161A|18|9|near RET|

The1598 body bytes contain711 decoded instructions, including interior
producer NOPs. Outer EVEN bytes1043/14FF bring ownership to1600.
The shared error tail belongs to the loader, not a separate public callable
function. Loader ownership is `1038..162B`,1524 bytes; FREE owns76.
Prior native heap628, stack76 and DOS-open26 contribute730 context bytes
without duplicate unit credit. All2330 scoped CODE/producer bytes and10
sharing/heap DATA bytes match both fresh cold products, with matching
scoped ordered relocations. The loader scope has four sites,
0000:103C, 0000:1120, 0000:1179 and 0000:14EC; the previous prose
incorrectly called them empty. The immutable original receipts are retained. No stored-file offset is invented for decoded code.

The receipt pins22 consulted frozen providers at ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, both public MAP entries,
root TASM5 OMF identity and the prior complete MAIN cold receipt. Both root
objects have normalized SHA-256
`776680636e46c2e12ebe1e3d5b78a7af34ed2b271080e96c3c333b01bf91cefe`.
The152 archived repository inputs retain their original snapshot identities.
Cached ASM/INC comparisons normalize only LF/CRLF; previously maintained
MAIN forwarders and seven MAIN-only Tupfile substitutions are explicit lineage.
This is no new build and no whole ending image equality claim. The prior
340-byte ending difference classification remains outside this bounded root.
Selected stored packed MAINL was re-attested before target-dependent work;
no unpacked Ghidra observations are used.

## Native execution and independent models

The receipt records 985 terminal scenarios per image,
3399 terminal public calls /1184475 native entries across all three images,
and60 separate nonterminal semantic prefixes.

All three images execute real public far returns, private near calls and
native heap/stack/DOS-open bodies. PUSH CS plus near CALL implements the
actual far frame; the harness checks return addresses, CS, SP, cleanup,
BP/SI/DI/DS preservation and complete instruction boundaries. It rejects
bare private entries, indirect/unknown edges, operand/neighbor branches,
unknown interrupts/ports, segment aliases and stores whose full span leaves
its declared state/heap region. Callback exceptions stop Unicorn and are
raised outside its FFI. The tests use synthetic diagnostic opcodes only.

The scalar model independently parses synthetic PI fields, consumes bits
MSB-first, updates the sixteen move-to-front color rows and expands packed
pixels. Every rank and previous-color context is exercised. Position0 repeats
one byte for equal nibbles, otherwise alternates the last two bytes.
Positions1/2/3/4 reference one line/two lines/one pixel right/one pixel left,
including odd-width half-byte reconstruction and actual segment borrowing.
Repeated position selects literal color pairs with continuation bits and
resets previous position. Fixtures cover length-prefix/byte/word boundaries,
source/destination and far header/output wrap, zero height, mode128 palette
skip, comments/dummy/extension refill, comment-length wrap, all256 sharing
bytes, allocation failures, DOS Carry/AX replies and load/free/double-free.

DOS is an explicit service model, supplying ordered3D/3F/3E events and
synthetic file bytes, plus allocation replies for lazy heap assignment.
No actual filesystem/DOS/physical runtime claim follows. Each read must
request16384 bytes at offset0 of the native temporary segment. Short reads
retain pre-existing buffer bytes; failure injection explicitly controls
whether a failed service supplies bytes. File position advances by supplied
bytes, independently of returnedAX.

The comparison covers ordered header/extension/image/output-pointer/AllocID
stores, complete native-entry counts and DOS events, CF/AX where defined,
IF/DF, buffer/file state and all1MiB physical memory except64KiB stack.
Temporary control words and the color table are excluded from the ordered
store trace; their entire final memory is still compared. Stack memory is
excluded because real call frames differ from scalar execution. Cross-image
comparison omits full-memory hashes because unrelated executable/DGROUP
bytes differ; all scope traces and outcomes remain equal.

## Observed resource and geometry hazards

- Loader clears DF and retains IF. FREE retains caller DF and has no specified
  scalar AX/CF result. Mode bit7 skips palette, leaving previous48 header bytes.
- Open failure returnsFFFE/CF1. Invalid magic/aspect/plane returnsFFF3/CF1.
  Several failures after temporary allocation return without closing the
  handle or releasing the stack buffer. Image allocation failure returnsFFF8.
  No cleanup is fabricated in the scalar model.
- The machine-extension allocation return is stored even on failure. Failed
  allocation skips no extension bytes and continues with width/height parsing.
  Thus subsequent parsing depends on actual remaining input, not on the
  declared extension size. A zero-sized extension allocation also fails.
- Header comments store a16-bit count;65536 bytes wrap it to0. There is no
  delimiter/EOF termination based on DOS Carry orAX. The initial read and
  refill ignore both. Refill PUSHA/POPA retains callerAX; XOR SI clearsCarry.
- Image allocation uses `width * u16(height+2) / 2`. The output pointer skips
  the initial width packed bytes. Zero height still executes a decode block;
  odd geometries, wrapped height and overshoot are not sanitized.
- Copy positions1..4 ignore the length high word. Position0's LOOP/high-word
  Carry logic copies an extra65536-byte cycle when its low length word is0.
  Complete native vectors prove these diagnostic cases.
- Aligned REP chunks stop at the first pointer boundary. With width1,
  position3 has zero reference distance. After both pointers reach0, a
  positive remaining count repeatedly copies0 bytes and advances both
  segments by1000. Four native prefixes independently predict three such
  zero-progress iterations; no terminal return is assigned.
- FREE calls native HMEM_FREE for nonzero comment/machine/image segments.
  It clears comment and machine pointers/lengths even if the allocator
  rejects them, ignores image offset and leaves the image pointer unchanged.
  Connected second-free cases exercise the resulting retained argument.

## Prefixes, coverage and acceptance limits

Sixteen unterminated comment/dummy prefixes stop before a pending private
byte call after200 or16390 completed bytes, through all declared IF/DF
combinations. The scalar derives complete buffer/color-table/header/heap/DOS
state independently. One public frame remains open and no close/release is
reported. Four zero-copy prefixes stop before the fourth zero-sized chunk,
with independently predicted DS/ES/SI/DI/AX and unchanged pending frame.
These semantic stops are explicit harness boundaries, not target returns
or wall-clock timeout evidence.

All711 new instruction/producer positions are statically partitioned and
reviewed; 698 are executed by the combined terminal/prefix matrix.
The unvisited positions are `12CF,13E1,13E5,144F,1459,145A,145C,145F,1461,1465,1487,14B5,15DF`. The receipt retains their exact
list rather than asserting unobserved runtime coverage. Complete raw-byte
equality includes those positions and all outer alignment bytes.

Ten controls cover complete partitions/cleanup/shared error returns,
producer alignment, unknown edges/services/ports, real near/far frames,
private-entry rejection, full-span writes, stale completion, segment aliases,
open prefix frames and a color-table memory mutant outside the ordered trace.

Canonical targets remain Japanese YUMEZIKU, `candidate-local-attested`;
independent pristine-dump attestation is unknown. Full combined ending
callers, actual DOS lifetime/EOF semantics, V30/device behavior, startup/CRT,
root DATA/BSS, physical source ownership, link layout and DIET packaging
remain open. Observed target, compiler, model runtime and inference stay
separate. MAINL maintained source0/exact0 is unchanged.

The refreshed MAP/unit coverage receipt is `.analysis/sol-mainl-map-unit-coverage-after-pi-decoder-20261006.json`, SHA-256
`b10beb1dbff463df09beb4d8fa7d8e21d12af3182983b309ac6948739daefa0a`. It covers10222/10944 root bytes, with722
uncredited and zero overlapping ownership. Earlier coverage receipts remain
unchanged. CRT carriers and the remaining file/artifact queue stay open.

## Successful borrower and failed-refill supplement

Receipt: `.analysis/sol-mainl-pi-decoder-borrow-review-20261006.json`, SHA-256
`d723fa6225cfd1b9eaa6dbfa44a8e804332b83f73b6c2f6177c4cd646ed43935`; 820 guarded inputs. Replay:

```sh
python3 scripts/review_th03_mainl_pi_decoder_borrow.py \
  --output .analysis/NEW_PI_BORROW.json
python3 -m unittest discover -s tests -p test_mainl_pi_decoder_borrow_review.py
```

Supplement preserves original PI817-input receipt and adds21 successfully decoded public calls/99906 native entries across target and both cold images. Five copy positions after output wrap use enough heap space; AX0/CF0 and specific native borrower branches are mandatory. Two refillCF1/AX0 orFFFF models inject valid supplied bytes and still decode successfully. Combined706/711 instructions executed;unvisited[4815, 5199, 5255, 5301, 5599] are five unreachable interior EVEN NOPs. No new owned bytes/source/exact. Ordered output stores/DOS/native frames and entire1MiB outside64Kstack independently agree. Prior post-wrap fixtures retain their genuine allocation-error outcomes and grant no borrower credit.

The original coverage698/711 is preserved above. Some original fixtures
labelled post-wrap borrowing actually fail image allocation; their CF1/error
results remain legitimate resource-path observations. This supplement raises
heap capacity and requires success plus the exact borrower instruction.
Together the receipts execute706/711 positions. The remaining `12CF`,
`144F`, `1487`, `14B5` and `15DF` are EVEN NOPs after unconditional jumps
or returns, with no admitted incoming edge. They are included in raw-byte
and structural ownership, with no fabricated execution. No additional byte
credit is added. Full terminal totals become3420 calls /1284381
native entries, plus the original60 semantic prefixes. Two further controls
prevent crediting an allocation error as a successfully decoded branch.

Heap BSS at DGROUP1458..145F lies beyond the file program image; it is
compared through explicit runtime state and full memory, not a raw file
slice or a proved BSS linker-layout claim. Initialized DATA comparison
remains10 bytes. The immutable parent receipt keeps all original hashes.


## Maintained loader source checkpoint (2026-10-21)

The complete symbolic provider is localized in src/mainl/formats/pi_decode.asm:
the shared error tail, loader, private color/byte/refill procedures, all macros,
equates, conditional branches and original EVEN directives. The generated root
replaces only the loader provider include. GRAPH_PI_FREE's 76 bytes and the
730 contextual heap/stack/open bytes are excluded from this unit's ownership.
The 22 reviewed providers remain explicitly contextual; this is not a standalone
assembler unit or a claim that the entire root dependency tree is owned.

config/th03_mainl_pi_source.json pins the existing MRT01 carrier, original
provider, maintained source and composer. Full statement comparison preserves
quoted data, case, operands, branches and directive boundaries. Source tests
reject instruction, branch, body, padding and include-boundary changes, and
staging refuses an existing destination. Runtime quirks above are intentional.

This source checkpoint grants no progress yet. Fresh native include consumption,
scoped bytes/four ordered relocations, a second raw OBJ/EXE/MAP repeat and
current-image models remain required. MAINL exact acceptance remains zero;
whole cold aggregate, one decoded DATA-byte mismatch, relocation ordering and
packed canonical file mapping remain open.


## Fresh consumed-source proof (2026-10-21)

The pending-source checkpoint above is now followed by actual MPI01 and MPI02
root TASM plus TLINK runs, two invocations each. Both completed with owned
cleanup and lock release. MPI02 starts from the explicitly observed MPI01
input bytes and mtimes, excluding root OBJ, EXE and MAP. The raw root OBJ,
complete EXE and MAP repeat exactly. This is a fresh include-consumption
hybrid link, not a whole-program cold rebuild.

The maintained loader's 1,524 bytes equal the decoded target, SHA-256
901790670a82c4b2978ad7bb305f14e6d4b978d412054ea2efe6376aef9ea5ae.
All four scoped relocations match in order. Both full EXE and MAP equal the
previous MRT01 carrier. The earlier root OBJ differs only at two COMENT E9
records: root source mtime and the PI include path/mtime. Every other record
type and payload matches; no object or executable was rewritten or normalized.

Actual existing scalar/native models ran against target and fresh MPI01:
985 terminal scenarios, 20 semantic prefixes and 7 successful borrower/refill
scenarios per image, taking 244.45 seconds overall. The immutable full receipt
is .analysis/mainl-pi-fresh-models-20261021-v01.json, SHA-256
addec0e9c80ae53d99ef5dd66143fae862d779e2ce0748ef78cbf24951ec44bd.
The original Factory terminal response was lost at transport; a later read
verified the complete durable success receipt and all 210 input identities.
No second full model pass was performed. Each per-image independent model
still compares full 1 MiB except stack; cross-image comparison excludes only
the two existing whole-memory before/after hashes, because contextual
executable bytes differ. DOS remains modeled. The 711-instruction review
scope includes unowned FREE76, executes706, and retains five unreachable
EVEN NOPs without fabricated execution.

config/th03_mainl_pi_link.json binds source, consumed includes, native
manifests/commands/logs/cleanup, products, input mtimes and full model proof.
scripts/replay_th03_mainl_pi_link.py is a read-only fast replay: it executes
no compiler and reruns no expensive model. It verifies pinned full EXE
identity and retained observations, explicitly returning models_rerun=false.
No byte/function denominator changes: only the existing loader unit gains
1,524 source-present bytes. This supports MAINL 51/145 source units and17,196
source bytes, with exact acceptance still zero. The full decoded image still
has one DATA-byte difference and461 global relocation-order differences
(677 relocation sites with equal membership); packed canonical mapping,
whole cold aggregate and genuine runtime remain open.


The initial proof proposal over-pinned unrelated current Python presentation
scripts from the historical model inventory. The corrected live replay guard
uses the actual transitive imported model/composer/native-verifier dependencies.
The original full model receipt and native manifests remain immutable, including
their full historical input inventories. A regression permits a changed
progress renderer while rejecting changes to the actual PI model or native
receipts; this does not waive any consumed-source or model dependency check.
