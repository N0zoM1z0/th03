# MAINL direct-link CODE candidate intake

This review connects all 33 directly linked ReC98 source paths to decoded
MAINL CODE diagnostics. It does not accept their source, complete files,
DATA/BSS, dependency closure or canonical packed storage. Frozen candidate
revision: `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`. Japanese target
provenance remains `candidate-local-attested`; pristine attestation is unknown.

## Remaining bounded functions and producers

Two complete functions and eight independent producer NOP bytes add 70
reviewed decoded bytes. The complete functions are:

| Frozen translation unit | Decoded entry | Bytes | Contract |
| --- | --- | ---: | --- |
| `th01/vplanset.cpp` | `0C7E:0002` | 41 | Far return; writes four complete VRAM far pointers |
| `th02/frmdely1.cpp` | `0C7E:0372` | 21 | Far Pascal return with two-byte cleanup; unsigned counter comparison |

The eight one-byte producers are `0049`, `0083`, `009F`, `0155`, `02A7`,
`0371`, `0669` and `0FA3`, relative to decoded CODE segment `0C7E`.
Their cold checksummed OMF emissions, normalized original object hashes and
complete SHARED CODE/MAP carrier sizes bind the selected producer offsets.
The functions' public MAP entries, complete instruction partitions, branch
bounds, ABI and raw bytes/ordered relocations agree in both cold products.

The target's `0C7E:0529` NOP remains **unowned**. At that coordinate both
cold products begin the PI palette function with PUSH BP. The existing PI
review explicitly distinguishes the original `052A` entry from cold `0529`,
and retains a 300-byte shifted PI difference region within the full 340-byte
ending image failure. A first attempt to include that NOP failed the cold
comparison; no producer source or equality was manufactured to close it.

`vram_planes_set()` writes `A800:0000`, `B000:0000`, `B800:0000` and
`E000:0000` as four DWORDs at DGROUP `1C60..1C6F`. This 16-byte BSS fixture
is distinct from initialized file data or full layout acceptance.

`frame_delay(int)` clears the native counter and uses unsigned JB. Negative
arguments consequently wait as large unsigned counts. Its new independent
unit does not reuse byte credit from the earlier sound review's native context.

Tail receipt: `.analysis/sol-mainl-linked-tail-review-20261006.json`, SHA-256
`0a7d3bc422baa9cab175ff55f5b4e73d70382c58ccfb9f785bb823a661f67b4b`; 1018 guarded inputs.

Each image executes 493 bounded calls and all 16 new instruction positions:
129 calls return and 364 retain waiting prefixes, with 78,169 native IRQ
entries. Across three images these total 1,479 calls, 387 returns, 1,092
prefixes and 234,507 native IRQ entries.
The matrix checks IF/DF, zero and extreme arguments, counter wrap, accumulator
carry, multiple schedules, bounded waiting prefixes and a complete return
after 65,535 delivered IRQs. An independent scalar model predicts the exact
ordered stores, counter changes and PIC acknowledgments; all physical memory
outside the 64 KiB stack is compared. Native far frames and saved registers
are checked at entry and return.

The previously reviewed 58-byte VSYNC handler is context only. The harness
constructs a real six-byte IP/CS/FLAGS interrupt frame and executes the native
no-callback IRQ handler and IRET. It checks registers, flags, SP and the resumed
logical poll address in the nonzero shared CODE segment. Host polling and IF
gating schedule interrupts explicitly. Physical asynchronous eligibility,
PIC timing, callbacks and combined game execution remain open.

## Frozen file-level candidate index

All 33 directly linked frozen translation units now have candidate index rows.
Their 36 nonzero CODE carriers total 27,753 bytes: 27,752 independently covered,
zero overlap and one unowned PI neighbor byte. Thirty-two file rows have
complete CODE interval coverage; `th03/pi_put.cpp` retains the one-byte gap.
Five file rows fail raw equality (`th03_mainl.asm`, `th03/cutscene.cpp`,
`th03/pi_put.cpp`, `th03/pi_put_i.cpp`, `th03/regist.cpp`); three fail original
ordered relocations (`th03_mainl.asm`, `th03/pi_put.cpp`, `th03/pi_put_i.cpp`). These failures remain explicit.

Index receipt: `.analysis/sol-mainl-candidate-index-review-20261006.json`, SHA-256
`f69b026ff98967cfa01d57be6e1226397e9a84643c73e3efe87ca3221125fd2e`; 1053 guarded inputs and 177 selected evidence rows.
Coverage receipt: `.analysis/sol-mainl-map-unit-coverage-after-linked-tail-20261006.json`, SHA-256
`645511e72881b4de5b8e898849d84acaaa218a26a8b051a6755057f8d3f6980a`. Across all 108 nonzero MAINL CODE carriers, the 58,339-byte total
has 28,380 independently covered bytes, 29,959 gap bytes and zero overlap.
The root `_TEXT` remains complete at 10,944 bytes. Remaining carrier gaps
are separate from this file intake and from unproved runtime contracts.


The separate `config/rec98_th03_candidate_reviews.csv` retains the artifact,
frozen path/hash, CODE-only scope, independent unit/evidence references,
carrier coverage and raw/ordered relocation results for each direct source.
The accepted MAIN review ledger remains separate. Ten C++ forwarding wrappers
and one `hfliplut.asm` copy in the cold trees are declared maintained MAIN
providers, bound to the original archived cold inputs. MAIN acceptance does
not transfer to MAINL. Other frozen providers agree byte-for-byte; ASM/INC
comparisons alone permit CRLF/LF normalization.

Every candidate row has source and exact acceptance false. A covered CODE
interval does not imply whole-file review, equality or complete Oracle
acceptance. The checker rejects other artifacts, membership/hash changes,
accepted states, invalid coverage accounting, overlapping units, unreviewed
or authored-source unit references, and missing or wrong-Oracle evidence. Failed evidence must be retained explicitly,
and each unit must have a passing diagnostic bundle.
Private replay also checks each selected evidence output hash and preserves
raw failures. The selected evidence rows are snapshotted independently of
unrelated later journal additions.

## Replay and remaining work

```sh
python3 scripts/review_th03_mainl_linked_tail.py --output .analysis/NEW_MAINL_LINKED_TAIL.json
python3 scripts/review_rec98_th03_mainl_intake.py --check
python3 scripts/review_rec98_th03_mainl_intake.py --output .analysis/NEW_MAINL_CANDIDATE_INDEX.json
python3 scripts/review_th03_mainl_coverage.py --output .analysis/NEW_MAINL_COVERAGE.json
python3 -m unittest discover -s tests -p test_mainl_linked_tail_review.py
python3 -m unittest discover -s tests -p test_mainl_candidate_intake.py
python3 scripts/ci.py
git diff --check
```

Complete the unowned PI boundary, source ownership and full Oracle gates;
review MAINL DATA/BSS/headers/dependencies and relevant CRT contracts separately.
Continue the remaining MAIN, OP, ZUN and shared frozen-file queue. Keep prior
receipts and coverage snapshots intact. No new compiler build or source
migration is credited by this diagnostic review.

Full repository CI passes 426 tests and all available private headless gates.
Log: `.analysis/sol-mainl-linked-code-full-ci.log`, SHA-256
`617cbfe1e85d44c61df0d0ab0887fa4ce0db1544a42bfeb3458d7fa3d1822e8d`. MAIN acceptance remains 38 owners /43 CODE extents /101
functions /11,628 owned bytes. MAINL maintained-source/exact owners remain zero.
