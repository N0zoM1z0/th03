# OP keyboard scanner source checkpoint

## Bounded ownership

The maintained source is `src/op/hardware/input_sense.cpp`, reached by the original
`th03/input_s.cpp` and hardware forwarder through explicit compatibility headers.
Only `th03-op-decoded-input-sense`, decoded `0BEB:0304` through `0BEB:04A4`
inclusive, gains source presence: `size = compare_size = 417`, with no packed
`file_offset`. Its decoded linear interval is `[49588, 50005)`.
The historical trailing NOP at `0BEB:04A5` is unowned context in the 418-byte
carrier, not manufactured padding or an extra authored byte. The accounting
review finds no overlap or pre-existing OP scanner unit. All original OP rows
remain unchanged: source presence becomes 34/41 units and 12,436 scoped bytes
from 33/40 and 12,019; formal exact stays zero.

## Compiler and structural observations

One fresh compiler invocation and one context link completed. The source417
and carrier418 both match their decoded target slices, including their empty
ordered relocation lists. The scanner slice SHA-256 is
`ccc7d014eac993a1a96308951a30af17bb27175d7c73d27f36b1367337ebe728`.
The candidate EXE SHA-256 is
`9f2e2af591645963d802489b45f9355a1e9f9b4da4b49ab0767f5be069ec204d`.
The native OMF and MAP bind the source dependency chain and scanner public at
`0BEB:0304`; the complete 417-byte procedure has 115 decoded instructions.

The rest of this link is frozen reference context, NOT a rebuild or preservation
proof for the maintained 33-unit OP cohort. Those ledger entries retain only
their existing independent evidence. The whole 59,770-byte program still has
six byte differences; whole-file equality and whole ordered-relocation equality
are both false. Scoped raw equality must not erase those negatives. The retained diagnostic
baseline had 4,867 program-byte differences. Restoring the original source
carrier length from 417 to 418 shifts downstream byte-aligned contributions
by one byte and the later word-aligned tail by two; the observed result is six
differences, not 4,861 newly authored bytes or a maintained-cohort proof.

## Modeled runtime

The target and fresh candidate each pass 268 scenarios: 264 returning cases
and four bounded prefixes, 536 scenarios combined. Each covers 278 instruction
positions across the exercised model, with semantic equality. That coverage
number is not the scanner's 115-instruction procedure size. BIOS samples,
joystick and interrupts are modeled; no physical keyboard/device timing or
whole-game runtime has been demonstrated.

## Evidence and replay boundary

- Native completion: `.analysis/op-keyboard-native-output-v01/completion.json`.
- Structure: `.analysis/op-keyboard-native-output-v01/structural-verification.json`.
- Runtime: `.analysis/op-keyboard-native-output-v01/runtime-verification.json`.
- Source-bound checkpoint: `.analysis/op-keyboard-native-output-v01/source-proof.json`.
- Original accounting: `.analysis/op-keyboard-source-proposal-20261021/accounting-review.json`.
- Maintained replay entry point: `python3 scripts/replay_th03_op_keyboard.py`.

The historical diagnostic reports retain `source_acceptance=false`,
`target_boundary_reviewed=false`, and `exact_acceptance=false`; the completion
record's `runtime_pending=true` describes its earlier compile/link stage.
The subsequent runtime report records actual model completion. The separate
source-bound checkpoint review supports only the bounded source-present ledger
entry and must not rewrite the diagnostic history as formal acceptance.
There is no second cold build, full cold aggregate, maintained-cohort context
link, packing proof, whole OP source ownership or Factory/exact promotion.

The maintained config is a compact exact SHA-256/byte-length binding to the
ignored 3,818-file source-proof inventory. Offline replay checks actual compiler
and linker argv, emitted products, owned cleanup, headless resource bounds,
registry continuity and recomputed registry policy, original source forwarding
and OMF dependency lineage. It independently recomputes structural observations
and checks the later retained runtime traces without rerunning native tools or
the runtime model. Per-run inventories remain ignored evidence.

Cleanup retention is explicitly bound through `.analysis/op-keyboard-native-output-v01/source-retention.json`, whose inputs dictionary covers the complete ignored proof closure and the import-time inventory helper. This sidecar does not change the original native or source-proof records.
