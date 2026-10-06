# MAINL direct-link CODE candidate intake

This review covers two remaining MAINL functions and eight producer bytes,
and binds all 33 directly linked ReC98 source providers to the cold trees. It does not accept their source, complete files,
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

Each image executes 493 bounded calls and all 16 new instruction positions.
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

## Replay and remaining work

```sh
python3 scripts/review_th03_mainl_linked_tail.py --output .analysis/NEW_MAINL_LINKED_TAIL.json
python3 scripts/review_th03_mainl_coverage.py --output .analysis/NEW_MAINL_COVERAGE.json
python3 -m unittest discover -s tests -p test_mainl_linked_tail_review.py
python3 scripts/ci.py
git diff --check
```

Complete the unowned PI boundary, source ownership and full Oracle gates;
review MAINL DATA/BSS/headers/dependencies and relevant CRT contracts separately.
Continue the remaining MAIN, OP, ZUN and shared frozen-file queue. Keep prior
receipts and coverage snapshots intact. No new compiler build or source
migration is credited by this diagnostic review.
