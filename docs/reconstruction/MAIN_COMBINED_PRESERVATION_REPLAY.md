# Combined MAIN preservation replay

This read-only verifier does not execute native toolchains, install runtime supervisors, modify historical receipts, or grant exactness/Factory acceptance. It independently checks four outputs: two fresh default rounds and two fresh full Marisa+Reimu+Mima candidate rounds. All prior scripts and the reviewed Reimu-only proposal remain immutable.

The candidate is pinned to config/th03_main_mima_gameplay_candidate.toml (855730e3d9943ef8afa4117c3b5a4ebe0c22ae12de56049f847e69c6182c270d). Final source closure is the planner's proposal.json complete_combined_source_inputs (27 files). Expected full scope: 78 extents, 371 functions, 59,624 owned bytes; default stays 74/334/53,122. Initializer is excluded.

The only default-to-combined payload and ordered-relocation exclusions are [0x142D0,0x158F5) and [0x17043,0x17384). The intervening gap remains protected. Every two-byte relocation crossing any of the four boundaries fails. Literal segment:offset tuples retain order and representation. The known 0x9F39/0x9F3E startup swap remains a hard failure; a natural carve resolving it must be observed, never assumed.

Every pinned old/new extent, function, producer range and manifest MAP contribution is recomputed independently against actual target/image/MAP data. Forged receipt booleans cannot bypass those checks. Mima charge carries 9 and bomb 13 target MZ entries; Marisa 30 and Reimu 23 remain separate exact checks. Six semantic producers must have zero DATA/BSS contributions. All preexisting DATA/BSS rows (including zero-sized ones), file-backed allocated bytes, DGROUP publics and aliases, overlay and allocation/stack header contract remain protected. Candidate-only zero allocation rows are removed solely for baseline inventory comparison; their presence and zero size are independently required.

Source closure includes frozen source inventories, input guards, exact whole carrier transformation by declared edits, unchanged shared inputs and bounded additions. Freshness, original receipt/control/behavior gates, supervisor start/order/completion guards, tool attestation, reference archive, all four EXE/MAP identity pins and post-read guards remain required.

An unresolved launch plan deliberately fails closed. No readiness is inferred from synthetic tests or a retained link. Before execution the owner must resolve native result review, authorized source activation, complete frozen default/candidate inventories and exact runtime/scheduling pins, then authorize fresh runs. Do not overwrite historical launch plans or receipts.

Portable tests: PYTHONDONTWRITEBYTECODE=1 python3 tests/test_main_combined_preservation.py

CLI: python3 scripts/verify_th03_main_combined_preservation.py --default-receipt PATH --candidate-receipt PATH --default-completion PATH --candidate-completion PATH --launch-plan NEW_REVIEWED_PLAN --launch-plan-sha256 SHA256 --not-before UTC_TIMESTAMP --report NEW_IGNORED_REPORT_PATH

All test payloads are synthetic in-memory structures, never executable fixtures or acceptance artifacts.

## Diagnostic scope clarification (v02)

The report field target_hitbox_tail_exact and target_comparison_scope refer only to payload [0x158F5,0x159FF), the retained hitbox tail. They do not claim exactness of the whole unowned remainder or whole image. The former v01 field target_remainder_exact had this same narrow range. This version changes only diagnostic naming/scope and documentation; every preservation gate and both exclusion intervals remain unchanged. The v01 proposal remains immutable.

## Installed entrypoints

The CLI imports scripts/lib/th03_combined_preservation_layout.py and binds both files in its input guards. It retains the immutable scripts/lib/th03_preservation_layout.py helper and scripts/lib/pc98.py parser. A reviewed fresh launch plan must bind these actual tracked paths and SHA-256 values after the source/control checkpoint, together with complete default/candidate frozen inventories. The portable 34-test suite uses committed config manifests and a synthetic unresolved plan; it does not require ignored launch templates or invoke native tools.

## Physical MAP producer regression

The first combined cold pair passed the original native Oracle, but its supplemental verifier failed on a previously accepted split owner: an explicit MAP part must use its declared physical producer wrapper, not the logical owner name. A second diagnostic found that the existing ordering producer is ex_ord.asm, as declared in the pinned manifest, rather than ex_ord.cpp. Both metadata-resolution defects are covered by positive and negative regressions, including all four retained MAPs. No byte, relocation-order, ownership or preservation gate was relaxed.

The failed cold-plan-v01/four-output-preservation.json and original native receipts remain immutable. Diagnostic checks on those outputs do not backfill historical success. The corrected helper requires a new pinned launch plan and fresh default/candidate pair before claiming the complete supplemental preservation result.
