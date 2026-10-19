# MAIN four-output preservation replay

This supplemental check compares two fresh default-build rounds with two fresh split-Marisa candidate rounds. It does not expand the original exact-owner scope, reconstruct the remaining carrier, or issue Factory acceptance. A preserved target mismatch remains a target mismatch and receives zero authored-byte credit.

The original aggregate replay must pass its unchanged gates for both runs. Use scripts/replay_th03_main_serial.py for serialized, bounded foreground execution and retained completion evidence under .analysis/th03-main-serial/runs/RUN_ID/. This verifier never launches a compiler, linker, emulator, analyzer or game.

## Inputs and invocation

Prepare a technical launch-plan JSON before running the pair. It contains:
- run_ids: [default_run_id, candidate_run_id]
- scheduled_not_before_utc
- supervisor_script_sha256
- schedule_adapter_sha256
- original_replay_sha256
- verifier_sha256
- layout_helper_sha256

The latter two pins identify scripts/verify_th03_main_preservation.py and scripts/lib/th03_preservation_layout.py. The supervisor and adapter pins identify the serial runner and schedule helper. The plan is technical scope, identity and freshness evidence; it is not an authorization assertion.

After both original receipts and completion sidecars exist:

    PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_th03_main_preservation.py \
      --default-receipt .analysis/th03-main-exact/DEFAULT/receipt.json \
      --candidate-receipt .analysis/th03-main-exact/CANDIDATE/receipt.json \
      --default-completion .analysis/th03-main-serial/runs/DEFAULT/completion-evidence.json \
      --candidate-completion .analysis/th03-main-serial/runs/CANDIDATE/completion-evidence.json \
      --launch-plan .analysis/PLAN.json --launch-plan-sha256 PLAN_SHA256 \
      --not-before PLAN_UTC_TIMESTAMP --report .analysis/NEW_PRESERVATION_REPORT.json

Use actual run IDs and plan values. The output parent must already exist under .analysis; existing reports are never overwritten. Missing private evidence fails closed.

## Preserved dimensions

All four outputs must agree on every load-image byte outside Marisa 0x142D0..0x14A76, the literal ordered relocation subsequence with multiplicity, overlays, entry and stack/allocation contracts. Relocation words crossing excluded or checked allocation boundaries are rejected. The check includes nonempty DATA/BSS contribution metadata, file-backed allocation bytes and relocations, zero allocation by both new producers, fixed new aliases and every preexisting DGROUP public. Virtual uninitialized BSS has no file bytes; its metadata and source allocation are checked instead.

The complete remainder source must remain identical. Its storage source region may differ only by the three declared alias/partition edits. Full original target raw/order comparisons for the remainder are reported independently of baseline preservation.

The verifier validates complete original aggregate receipts, fresh schedule/start evidence, frozen source guards, completion-pinned MAPs, receipt MAP rows, archived tool-attestation identities, compiler/environment agreement and the exact candidate-only input additions. It never sorts or normalizes target relocation sequences.

## Retention and reproducibility

Commit these scripts and portable tests, not private original executables, generated products, full source archives, toolchains or build trees. Retain the two complete private replay trees and their repository-inputs/reference archives, four MAIN images/MAPs/carrier sources, completion files, archived tool attestations, scheduling sidecars, before/after source inventories, canonical target, and technical plan. Those are required proof inputs and must not be replaced by a summary report.

Portable tests require only Python and repository code:

    python3 -m unittest discover -s tests -p 'test_main_preservation*.py'

This export intentionally changes script identities. Historical proof plans and receipts remain pinned to their original frozen scripts; replay those historical checks with the retained original implementation. Do not rewrite an old plan or report to make a new export appear to have been used earlier. Newly scheduled pairs should pin the exported implementation.

Current scope is explicitly the 53,122-byte default baseline and 55,080-byte split-Marisa candidate. Future owners need a separately reviewed scope update; they are not silently accepted.
